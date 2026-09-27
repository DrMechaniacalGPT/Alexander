"""One local request per turn; raw responses and usage are retained by the runner."""
import copy
import json
import time
import urllib.request
from urllib.parse import urlparse

SCHEMA = {'type': 'object', 'properties': {
    'say': {'type': 'string', 'maxLength': 480}, 'private_note': {'type': 'string', 'maxLength': 180},
    'evidence': {'type': 'array', 'items': {'type': 'string'}, 'maxItems': 8},
    'conclusion': {'type': 'string', 'maxLength': 600}, 'action': {'type': 'string'}},
    'required': ['say', 'private_note', 'evidence', 'conclusion', 'action'], 'additionalProperties': False}

def action_schema(view, strict_output=False):
    schema = copy.deepcopy(SCHEMA)
    schema['properties']['action']['enum'] = view.get('legal_actions', ['none'])
    known = [e['id'] for e in view.get('observations', [])]
    if known:
        schema['properties']['evidence']['items']['enum'] = known
    else:
        schema['properties']['evidence']['maxItems'] = 0
    if strict_output:
        if view.get('final_assessment'):
            schema['properties']['say']['enum'] = ['']
            schema['properties']['action']['enum'] = ['none']
            schema['properties']['conclusion']['minLength'] = 1
        else:
            schema['properties']['conclusion']['enum'] = ['']
    return schema

class Ollama:
    def __init__(self, model='qwen3.5:9b', endpoint='http://127.0.0.1:11434', context=4096, tokens=256, seed=1, thinking=False, strict_output=False, assessment_thinking=None, assessment_tokens=None, assessment_model=None):
        url = urlparse(endpoint)
        if url.scheme != 'http' or url.hostname not in ('127.0.0.1', 'localhost', '::1') or url.username:
            raise ValueError('Only local unauthenticated HTTP Ollama endpoints are supported')
        self.endpoint, self.model = endpoint.rstrip('/'), model
        self.context, self.tokens, self.seed = context, tokens, seed
        self.thinking, self.strict_output = thinking, strict_output
        self.assessment_thinking, self.assessment_tokens = assessment_thinking, assessment_tokens
        self.assessment_model = assessment_model
        if assessment_tokens is not None and assessment_tokens <= 0:
            raise ValueError("Assessment token budget must be positive")

    def payload(self, messages):
        view = json.loads(messages[-1]['content'])
        schema = action_schema(view, self.strict_output)
        final = view.get('final_assessment', False)
        tokens = self.assessment_tokens if final and self.assessment_tokens is not None else self.tokens
        thinking = self.assessment_thinking if final and self.assessment_thinking is not None else self.thinking
        # Conservative byte-based estimate, including structured-output schema and
        # extra chat-template headroom. Actual tokenizer counts are logged afterward.
        upper_bound = sum(len(m['content'].encode()) for m in messages) + len(json.dumps(schema).encode()) + 512
        if upper_bound + tokens > self.context:
            raise ValueError(f'Conservative context bound {upper_bound}+{tokens} exceeds {self.context}; explicitly choose a larger context')
        return {'model': self.assessment_model if final and self.assessment_model else self.model, 'messages': messages, 'stream': False,
                'think': thinking, 'format': schema, 'keep_alive': '2m',
                'options': {'temperature': 0.7, 'seed': self.seed, 'num_ctx': self.context,
                            'num_predict': tokens}}

    def complete(self, payload, timeout=120):
        request = urllib.request.Request(self.endpoint+'/api/chat', data=json.dumps(payload).encode(),
                                         headers={'Content-Type': 'application/json'})
        start = time.monotonic()
        with urllib.request.urlopen(request, timeout=timeout) as response:
            result = json.load(response)
        if result.get('done_reason') == 'length':
            # Keep the full raw response; runner decides it is a failed turn.
            result['truncated'] = True
        return {'response': result, 'wall_seconds': round(time.monotonic()-start, 3)}

class Stub:
    def __init__(self, replies, strict_output=False):
        self.replies = replies
        self.strict_output = strict_output

    def payload(self, messages):
        result = {'messages': messages}
        if self.strict_output:
            result['format'] = action_schema(json.loads(messages[-1]['content']), True)
        return result

    def complete(self, payload, timeout=120):
        view = json.loads(payload['messages'][-1]['content'])
        action = self.replies.get(view['self'], {'say': 'I have no information to add.',
               'private_note': '', 'evidence': [], 'conclusion': 'Unknown.', 'action': 'none'})
        if self.strict_output:
            # Render the deterministic fixture's fields for this phase; not model-output repair.
            action = copy.deepcopy(action)
            if view.get('final_assessment'):
                action['say'], action['action'] = '', 'none'
            else:
                action['conclusion'] = ''
        return {'response': {'message': {'content': json.dumps(action)}, 'done_reason': 'stop',
                             'prompt_eval_count': 0, 'eval_count': 0}, 'wall_seconds': 0}
