"""Build the fixed eight-source/eight-product coverage matrix, never infer scores."""
from pathlib import Path
from datetime import date
from urllib.parse import urlparse
import csv

ROOT = Path(__file__).resolve().parent
SOURCES = frozenset(['RTINGS', 'Vacuum Wars', 'The Hook Up', 'TechRadar', "Tom's Guide", 'Expert Reviews', 'WIRED', 'Good Housekeeping'])
PRODUCTS = frozenset(['Roborock Saros 10R', 'Roborock Qrevo Curv 2 Flow', 'Roborock Qrevo Curv', 'Roborock S8 MaxV Ultra', 'MOVA V70 Ultra Complete', 'Dreame X60 Max Ultra Complete', 'Eufy Omni E25', 'Shark PowerDetect UV Reveal'])
EXPECTED_PAIRS = frozenset((source, product) for source in SOURCES for product in PRODUCTS)
# Audited relations, not an assumption that different names are equivalent.
VARIANT_RELATIONS = frozenset([
    ('RTINGS', 'Eufy Omni E25', 'Eufy Omni E28'),
    ('TechRadar', 'Dreame X60 Max Ultra Complete', 'Dreame X60 Pro Ultra Complete'),
])
TESTED_PRODUCTS = PRODUCTS | frozenset(x[2] for x in VARIANT_RELATIONS)
MAP = {
    'substantive_review': 'substantive', 'substantive_test_table': 'substantive',
    'guide_coverage': 'guide', 'related_variant': 'related_variant',
    'mention': 'mentioned', 'test_reference': 'test_reference',
    'unknown_after_search': 'unknown',
}
FIELDS = ['source', 'product', 'coverage', 'direction', 'evidence_url', 'observed_at', 'access_level', 'model_match', 'tested_product', 'page_type', 'claim_locator', 'testing_evidence', 'methodology_version', 'coverage_scope', 'article_cohort', 'independent_test_id', 'noncoverage_scope', 'note']
ACCESS = frozenset(['bounded_search', 'direct_page', 'indexed_article_text', 'indexed_review_text', 'indexed_guide_text', 'access_blocked'])
PAGE_TYPES = frozenset(['comparison', 'feature_or_related_review', 'review', 'review_or_comparison', 'roundup', 'test_table', 'unknown'])
TESTING_EVIDENCE = frozenset(['firsthand_review_text', 'guide_asserts_testing_no_product_test_detail', 'not_established', 'published_firsthand_test_summary', 'published_test_table', 'related_model_test_only', 'retrospective_testing_assertion'])

def require(condition, message):
    if not condition:
        raise ValueError(message)

def transform(rows):
    result = []
    for index, row in enumerate(rows):
        try:
            require(row.get('status') in MAP, f'Row {index}: unsupported audit status {row.get("status")!r}')
            result.append(dict(source=row['source'], product=row['product'], coverage=MAP[row['status']], direction='not_assessed', evidence_url=row['evidence_url'], observed_at=row['observed'], access_level=row['verification'], model_match=row['model_match'], tested_product=row['tested_product'], page_type=row['page_type'], claim_locator=row['claim_locator'], testing_evidence=row['testing_evidence'], methodology_version=row['methodology_version'], coverage_scope=row['coverage_scope'], article_cohort=row['article_cohort'], independent_test_id=row['independent_test_id'], noncoverage_scope=row['noncoverage_scope'], note=row['note']))
        except KeyError as error:
            raise ValueError(f'Row {index}: missing audit field {error.args[0]}') from error
    return result

def validate(rows):
    """Validate this fixed core matrix. Not a validator for partial/expanded ledgers."""
    pairs = []
    for index, row in enumerate(rows):
        prefix = f'Row {index}'
        require(isinstance(row, dict), f'{prefix}: expected a row mapping')
        require(set(row) == set(FIELDS), f'{prefix}: matrix fields differ from schema')
        require(all(isinstance(value, str) for value in row.values()), f'{prefix}: all field values must be strings')
        require(row['source'] in SOURCES, f'{prefix}: unknown source')
        require(row['product'] in PRODUCTS, f'{prefix}: unknown product')
        pairs.append((row['source'], row['product']))
        coverage = row['coverage']
        require(coverage in MAP.values(), f'{prefix}: unsupported coverage state')
        require(row['direction'] == 'not_assessed', f'{prefix}: coverage does not establish verdict direction')
        require(row['access_level'] in ACCESS, f'{prefix}: invalid access level')
        require(row['page_type'] in PAGE_TYPES, f'{prefix}: invalid page type')
        require(row['model_match'] in {'exact', 'related_variant', 'unknown'}, f'{prefix}: invalid model match')
        require(row['testing_evidence'] in TESTING_EVIDENCE, f'{prefix}: invalid testing evidence')
        require(row['methodology_version'] in {'not_recorded', 'v1.0', 'v1.1'}, f'{prefix}: unsupported methodology version')
        require(row['coverage_scope'] == 'publisher_archive', f'{prefix}: unsupported coverage scope')
        require(not row['noncoverage_scope'], f'{prefix}: explicit non-coverage is not supported by this audit')
        require(bool(row['note'].strip()), f'{prefix}: missing evidence limitation/note')
        try:
            require(date.fromisoformat(row['observed_at']).isoformat() == row['observed_at'], f'{prefix}: noncanonical observation date')
        except ValueError as error:
            raise ValueError(f'{prefix}: invalid observation date') from error
        tested = row['tested_product']
        require(not tested or tested in TESTED_PRODUCTS, f'{prefix}: invalid tested product')
        if coverage == 'unknown':
            require(row['model_match'] == 'unknown' and not tested, f'{prefix}: unknown cannot imply a tested model')
            require(row['page_type'] == 'unknown' and row['testing_evidence'] == 'not_established', f'{prefix}: unknown cannot imply test evidence')
            require(row['access_level'] in {'bounded_search', 'access_blocked'}, f'{prefix}: unknown access level inconsistent')
        else:
            parsed = urlparse(row['evidence_url'])
            require(parsed.scheme in {'http', 'https'} and bool(parsed.hostname) and not parsed.username and not parsed.password, f'{prefix}: invalid evidence URL')
            require(bool(row['claim_locator'].strip()), f'{prefix}: missing claim locator')
            require(row['access_level'] != 'bounded_search', f'{prefix}: located coverage requires page or indexed access')
        if coverage == 'related_variant':
            require(bool(tested) and tested != row['product'], f'{prefix}: missing or identical tested variant')
            require((row['source'], row['product'], tested) in VARIANT_RELATIONS, f'{prefix}: unaudited variant relationship')
            require(row['model_match'] == 'related_variant' and row['testing_evidence'] == 'related_model_test_only', f'{prefix}: variant evidence inconsistent')
            require(row['page_type'] in {'review', 'feature_or_related_review'}, f'{prefix}: variant page inconsistent')
        elif coverage != 'unknown':
            require(row['model_match'] == 'exact', f'{prefix}: exact-model coverage required')
        if coverage == 'substantive':
            require(tested == row['product'], f'{prefix}: target was not directly tested')
            expected_evidence = 'published_test_table' if row['page_type'] == 'test_table' else 'firsthand_review_text'
            require(row['page_type'] in {'review', 'review_or_comparison', 'comparison', 'test_table'}, f'{prefix}: substantive page inconsistent')
            require(row['testing_evidence'] == expected_evidence, f'{prefix}: substantive test evidence inconsistent')
        if coverage == 'guide':
            require(row['page_type'] == 'roundup', f'{prefix}: guide must remain a roundup')
            require(row['testing_evidence'] in {'guide_asserts_testing_no_product_test_detail', 'published_firsthand_test_summary'}, f'{prefix}: invalid guide evidence')
            require(tested == (row['product'] if row['testing_evidence'] == 'published_firsthand_test_summary' else ''), f'{prefix}: guide tested product inconsistent')
        if coverage in {'mentioned', 'test_reference'}:
            expected = 'not_established' if coverage == 'mentioned' else 'retrospective_testing_assertion'
            require(not tested and row['testing_evidence'] == expected, f'{prefix}: mention/reference cannot become direct test')
            require(row['page_type'] == 'feature_or_related_review', f'{prefix}: mention/reference page inconsistent')
        if row['independent_test_id']:
            require(bool(row['article_cohort']) and row['page_type'] == 'comparison', f'{prefix}: test identity requires a comparison cohort')
    require(len(pairs) == len(set(pairs)), 'Duplicate source/product key')
    require(set(pairs) == EXPECTED_PAIRS, f'Expected full 64-pair core matrix; missing {len(EXPECTED_PAIRS-set(pairs))}, extra {len(set(pairs)-EXPECTED_PAIRS)}')
    return True

if __name__ == '__main__':
    with (ROOT / 'coverage_audit.csv').open() as file:
        rows = transform(list(csv.DictReader(file)))
    validate(rows)
    with (ROOT / 'source_product_matrix_v2.csv').open('w', newline='') as file:
        writer = csv.DictWriter(file, FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f'Wrote {len(rows)} uniquely keyed matrix rows')
