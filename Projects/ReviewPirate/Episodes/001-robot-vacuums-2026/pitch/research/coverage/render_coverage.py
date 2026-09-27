"""Render an accessible, offline coverage appendix from the validated core CSV."""
from pathlib import Path
import csv
import html
from urllib.parse import urlparse
from build_matrix import validate

ROOT = Path(__file__).resolve().parent
SOURCE_ORDER = ['RTINGS', 'Vacuum Wars', 'The Hook Up', 'TechRadar', "Tom's Guide", 'Expert Reviews', 'WIRED', 'Good Housekeeping']
PRODUCT_ORDER = ['Roborock Saros 10R', 'Roborock Qrevo Curv 2 Flow', 'Roborock Qrevo Curv', 'Roborock S8 MaxV Ultra', 'MOVA V70 Ultra Complete', 'Dreame X60 Max Ultra Complete', 'Eufy Omni E25', 'Shark PowerDetect UV Reveal']
LABELS = {'substantive': ('●', 'Review / test'), 'guide': ('▤', 'Guide'), 'related_variant': ('◇', 'Related variant'), 'mentioned': ('·', 'Mention'), 'test_reference': ('↗', 'Test reference'), 'unknown': ('?', 'Unknown')}

def esc(value):
    return html.escape(str(value), quote=True)

def safe_link(url, label):
    parsed=urlparse(url)
    if parsed.scheme not in {'https','http'} or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Unsafe evidence URL')
    return f'<a href="{esc(url)}" rel="noreferrer">{esc(label)}</a>'

def render(rows):
    validate(rows)
    keyed={(r['source'],r['product']):r for r in rows}
    legend=''.join(f'<li><span aria-hidden="true">{esc(symbol)}</span> <strong>{esc(label)}</strong></li>' for symbol,label in LABELS.values())
    headers=''.join(f'<th scope="col" id="product-{i}">{esc(product)}</th>' for i,product in enumerate(PRODUCT_ORDER))
    body=[]
    for si,source in enumerate(SOURCE_ORDER):
        cells=[]
        for pi,product in enumerate(PRODUCT_ORDER):
            row=keyed[source,product]
            symbol,label=LABELS[row['coverage']]
            evidence=safe_link(row['evidence_url'],'Open source evidence') if row['evidence_url'] else '<span>No exact-model evidence established in this search.</span>'
            facts=[('Observed',row['observed_at']),('Access',row['access_level'].replace('_',' ')),('Page type',row['page_type'].replace('_',' ')),('Test evidence',row['testing_evidence'].replace('_',' ')),('Target model',product),('Tested model',row['tested_product'] or 'Not established'),('Claim locator',row['claim_locator'] or 'No located claim'),('Test method version',row['methodology_version'].replace('_',' ')),('Coverage scope',row['coverage_scope'].replace('_',' ')),('Comparison cohort',row['article_cohort'] or 'Not recorded'),('Shared test ID',row['independent_test_id'] or 'Unresolved; do not count as independent')]
            detail=''.join(f'<dt>{esc(name)}</dt><dd>{esc(value)}</dd>' for name,value in facts)
            cells.append(f'<td data-record="{si}-{pi}" headers="source-{si} product-{pi}"><details><summary><span aria-hidden="true">{esc(symbol)}</span> {esc(label)}<span class="sr-only"> — {esc(source)}, {esc(product)}</span></summary><div class="entry"><p>{evidence}</p><p>{esc(row["note"])}</p><dl>{detail}</dl></div></details></td>')
        body.append(f'<tr><th scope="row" id="source-{si}">{esc(source)}</th>{"".join(cells)}</tr>')
    template='''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Located review coverage — robot vacuums</title>
<style>
:root{color-scheme:light;font:16px/1.5 system-ui,sans-serif;color:#172a32;background:#f5f6f3}*{box-sizing:border-box}body{margin:0;min-width:0;overflow-wrap:anywhere}main{width:100%;min-width:0;max-width:1500px;margin:auto;padding:2rem 1rem 4rem}h1{font-size:clamp(1.7rem,3vw,2.6rem);line-height:1.15;margin:.3rem 0 1rem}h2{font-size:1.25rem}.intro{max-width:850px}.tag{font-size:.85rem;text-transform:uppercase;letter-spacing:.06em;font-weight:700}.notice{background:#fff;border-left:4px solid #245c67;padding:1rem;max-width:1000px}.legend{list-style:none;padding:0;display:flex;flex-wrap:wrap;gap:.6rem 1.6rem}.legend span{display:inline-block;width:1.3em;text-align:center}.table-scroll{position:relative;width:100%;max-width:100%;min-width:0;overflow:auto;border:1px solid #aeb9bb;border-radius:.4rem;background:white;margin-top:1rem}.table-scroll:focus-visible,a:focus-visible,summary:focus-visible{outline:3px solid #9b4400;outline-offset:3px}table{border-collapse:separate;border-spacing:0;width:100%;min-width:1180px;table-layout:fixed}caption{overflow-wrap:anywhere;text-align:left;padding:1rem;font-weight:600;background:#e8efed}th,td{text-align:left;vertical-align:top;padding:.85rem .65rem;border-right:1px solid #d7dfe0;border-bottom:1px solid #d7dfe0;overflow-wrap:anywhere}thead th{background:#edf2ef;font-size:.85rem}thead th:first-child{width:130px}tbody th{background:#edf2ef;font-size:.9rem}summary{position:relative;cursor:pointer;font-size:.87rem;min-height:3rem;font-weight:650}summary span[aria-hidden]{display:inline-block;min-width:1em}details[open]{min-width:135px}.entry{font-size:.82rem}.entry p{margin:.65rem 0}.entry dl{margin-top:1rem}.entry dt{font-weight:700;margin-top:.65rem}.entry dd{margin-left:0}a{color:#154c85;text-decoration-thickness:.1em;text-underline-offset:.15em}.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}.limits{max-width:950px;margin-top:2rem}.limits li{margin-bottom:.6rem}@media(max-width:700px){main{padding-top:1.2rem}.legend{font-size:.85rem}.table-scroll{max-height:75vh}thead th{position:sticky;top:0;z-index:1}tbody th{position:sticky;left:0;z-index:1}thead th:first-child{z-index:2;left:0}}
@media print{main{padding:0}.table-scroll{overflow:visible;max-height:none}table{font-size:9pt;min-width:0}summary{font-size:8pt}.entry{font-size:7pt}thead th,tbody th{position:static}}
</style></head><body><main><header><p class="tag">Research appendix · observed September 26, 2026</p><h1>What review coverage we located</h1><p class="intro">Eight publishers, eight robot vacuums. This table records the kind of coverage found, not which product wins. Open any cell for its evidence, tested model and limitations.</p></header>
<p class="notice"><strong>Unknown does not mean untested.</strong> It means this bounded search did not establish relevant exact-model coverage. A related variant is not a direct test of the target product. All verdict directions remain unassessed.</p>
<ul class="legend" aria-label="Coverage categories">LEGEND</ul><p id="table-help">On a small screen, scroll the table horizontally. Each cell opens with a click, Enter or Space. Labels accompany every symbol; color carries no evidence meaning.</p>
<div class="table-scroll" role="region" aria-label="Coverage matrix" aria-describedby="table-help" tabindex="0"><table><caption>64 source–product records. Publisher archive coverage includes historical reviews; it is not a shared current test cohort.</caption><thead><tr><th scope="col">Publisher / target product</th>HEADERS</tr></thead><tbody>BODY</tbody></table></div>
<section class="limits"><h2>How to read this evidence</h2><ul><li><strong>Review / test:</strong> an exact-model review, comparison or published test table was located. This does not certify every claim or show long-term reliability.</li><li><strong>Guide:</strong> a roundup or ranking entry. Some contain firsthand test summaries; others supply a ranking without a complete product test. Read the cell.</li><li><strong>Related variant:</strong> the reviewed unit differs from the target. Do not transfer its verdict automatically.</li><li><strong>Mention / test reference:</strong> contextual reporting or a retrospective assertion of testing. Neither is a full exact-model test report.</li><li>Multiple products in one comparison share a test family. Unresolved test IDs are not independent tests. No score averaging or source voting is performed.</li><li>This is the fixed eight-source core appendix. Supplementary creators and owner reports in the broader project ledger remain separate. Publication dates, test dates, firmware, prices and current availability need claim-specific checks.</li></ul><p>Built from <a href="source_product_matrix_v2.csv">the validated core CSV</a>. <a href="MATRIX_SCHEMA.md">Schema and validation notes</a> describe its scope.</p></section></main></body></html>'''
    return template.replace('LEGEND',legend).replace('HEADERS',headers).replace('BODY',''.join(body))

if __name__=='__main__':
    with (ROOT/'source_product_matrix_v2.csv').open() as file:
        rows=list(csv.DictReader(file))
    output=ROOT/'coverage.html'
    output.write_text(render(rows),encoding='utf-8')
    print(f'Wrote {output} with {len(rows)} records')
