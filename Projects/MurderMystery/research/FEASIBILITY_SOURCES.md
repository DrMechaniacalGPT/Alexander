# Feasibility evidence and access record

September 26, 2026. Bounded engineering/decision review, not a systematic literature review. The user's follow-up requested a concrete feasibility sketch, then specifically asked about calling installed local Ollama models. Previous market evidence remains in [sources.csv](sources.csv), [reviews](experience/reviews.md) and [comparison](market/comparison.md). This pass does not expand the buyer-review sample.

| ID | Primary source actually opened | What it supports / limits |
|---|---|---|
| F01 | [OpenAI conversation state](https://developers.openai.com/api/docs/guides/conversation-state) | Explicit history and managed-state options; context must be controlled by our application. No guarantee of psychological independence. |
| F02 | [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs) | Structured response schemas; valid structure can still contain mistakes. |
| F03 | [OpenAI API pricing](https://developers.openai.com/api/docs/pricing) | Dated Standard short-context rates for the illustrative calculations; account access not established. |
| F04 | [Park et al., Generative Agents, 2023](https://arxiv.org/abs/2304.03442) | Abstract inspected: memory/planning architecture and 25-agent social environment; believability is not dinner-party predictive validity. |
| F05 | [Zhou et al., SOTOPIA](https://arxiv.org/abs/2310.11667) | Abstract inspected: social scenarios and human comparisons; the paper's tested models are not our installed models. |
| F06 | [Wang et al., SOTOPIA-π](https://arxiv.org/abs/2403.08715) | Abstract inspected: model evaluators overestimated specialized agents in reported experiments; motivates caution, not a universal impossibility result. |
| F07 | [SOTOPIA repository](https://github.com/sotopia-lab/sotopia) | README inspected: existing framework, local JSON/Redis options. No installation, code audit, dependency/license audit or integration benchmark. |
| F08 | [OpenAI prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching) | Separate cache-write/read/uncached accounting; the scenarios must not assume cache hits. Markdown endpoint failed; HTML page read successfully. |
| F09 | [ChatGPT/Codex pricing](https://learn.chatgpt.com/docs/pricing) | Product usage and API-key pricing distinction. The owner's Pro upgrade does not demonstrate a configured endpoint for our Python program. |
| F10 | [AI mystery project decision log](https://github.com/DilanRG/ai-murder-mystery-v2/blob/master/docs/decision_log.md) | An adjacent public project surfaced; opened page did not provide enough usable implementation text for capability claims. Lead only; not validation or proof of competition at our exact scope. |
| F11 | [Ollama chat API](https://docs.ollama.com/api/chat) | Local chat endpoint, supplied message history, streaming/thinking controls and response timing fields. Our actual probe uses the installed server rather than assuming docs establish connectivity. |

## Local observations

- `python3 --version`: Python 3.12.3 on Linux; a small arithmetic program also ran successfully.
- Python import lookup: OpenAI SDK absent from this interpreter. Checked only presence of `OPENAI_API_KEY`, which was false; no secret values printed and no credential stores searched.
- `ollama list`: gemma4:e4b-it-qat (6.1 GB), qwen3.5:9b (6.6 GB), qwen3:8b (5.2 GB). These displayed installed sizes are not measured memory requirements.
- Loopback access was initially denied by the shell sandbox. An approved escalation permitted listing. This is an execution-permission requirement, not an Ollama fault.
- `ollama ps` before inference showed no loaded models.
- A subsequent user request authorized a tiny local-inference probe. [Code](feasibility/local_probe.py) and [raw results](feasibility/local_probe_results.json) preserve its actual prompts, settings, outputs and timings. The synthetic marker is not real private data. All three expected-output checks passed. Cold wall time was 13.036 s (12.584 s reported loading); warm calls were 0.140 and 0.385 s. The three calls test a known marker, a separate conversation without it, then explicit delivery. They do not test strategic play, long-context reliability or isolation against arbitrary attacks.

## Search record

Queries included:

- `site.developers.openai.com API conversation state responses isolated conversations`
- `site.developers.openai.com API pricing batch cached input`
- `generative agents interactive simulacra human behavior 25 agents memory reflection planning arxiv`
- `SOTOPIA interactive evaluation social intelligence language agents human evaluation arxiv`
- `language models simulating humans social science limitations validation population diversity arxiv`
- `ChatGPT subscription API separately billed` (official domains)
- `"murder mystery" "simulation" "AI" game design` (arXiv/GitHub)
- `"Sotopia" "github" environment agent license`
- `"AI" "murder mystery party" "YouTube"`
- `Ollama API chat localhost 11434 think false stream false` (no results; official endpoint documentation opened directly)

Selected original papers/docs for technical claims; excluded creator self-promotion and search snippets from market-validation claims. Video query did not establish an audience-to-purchase funnel. No comprehensive novelty search or current-model social benchmark was conducted. This pass cannot estimate virality, host demand or human enjoyment.
