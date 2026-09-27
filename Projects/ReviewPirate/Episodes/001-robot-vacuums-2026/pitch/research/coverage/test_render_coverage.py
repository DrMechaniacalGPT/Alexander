import csv
import copy
import unittest
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from render_coverage import render

class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True)
        self.tags=[];self.records=[];self.links=[];self.text=[];self.ids=set();self.headers=[]
        self.feed(text)
    def handle_starttag(self,tag,attrs):
        self.tags.append(tag);attrs=dict(attrs)
        if 'data-record' in attrs:self.records.append(attrs['data-record']);self.headers.extend(attrs.get('headers','').split())
        if tag=='a':self.links.append(attrs.get('href'))
        if 'id' in attrs:self.ids.add(attrs['id'])
    def handle_data(self,text):self.text.append(text)

class CoveragePage(unittest.TestCase):
    def setUp(self):
        with (Path(__file__).parent/'source_product_matrix_v2.csv').open() as file:self.rows=list(csv.DictReader(file))
    def test_exact_64_displayed_records_with_headers(self):
        page=Page(render(self.rows))
        self.assertEqual(len(page.records),64)
        self.assertEqual(len(set(page.records)),64)
        self.assertEqual(page.tags.count('details'),64)
        self.assertEqual(page.tags.count('summary'),64)
        self.assertTrue(set(page.headers)<=page.ids)
    def test_every_located_evidence_link_preserved(self):
        page=Page(render(self.rows))
        actual=Counter(url for url in page.links if url.startswith('https://') or url.startswith('http://'))
        expected=Counter(r['evidence_url'] for r in self.rows if r['evidence_url'])
        self.assertEqual(actual,expected)
    def test_untrusted_note_is_text_not_html(self):
        rows=copy.deepcopy(self.rows)
        payload='<script>alert("x")</script><img src=x onerror=alert(1)> & "quoted"'
        rows[0]['note']=payload
        output=render(rows);page=Page(output)
        self.assertNotIn('script',page.tags)
        self.assertNotIn('img',page.tags)
        self.assertIn(payload,''.join(page.text))
        self.assertIn('&lt;script&gt;',output)
    def test_url_attribute_escaped_and_roundtrips(self):
        rows=copy.deepcopy(self.rows)
        url='https://example.com/evidence?q="hello"&x=1'
        rows[0]['evidence_url']=url
        output=render(rows)
        self.assertIn(url,Page(output).links)
        self.assertIn('&quot;hello&quot;&amp;x=1',output)
    def test_unsafe_link_rejected(self):
        rows=copy.deepcopy(self.rows);rows[0]['evidence_url']='javascript:alert(1)'
        with self.assertRaisesRegex(ValueError,'invalid evidence URL'):render(rows)
    def test_unknown_warning_and_no_scripts(self):
        page=Page(render(self.rows))
        self.assertIn('Unknown does not mean untested.',''.join(page.text))
        self.assertNotIn('script',page.tags)
    def test_incomplete_table_rejected(self):
        with self.assertRaisesRegex(ValueError,'64-pair'):render(self.rows[:-1])

if __name__=='__main__':unittest.main()
