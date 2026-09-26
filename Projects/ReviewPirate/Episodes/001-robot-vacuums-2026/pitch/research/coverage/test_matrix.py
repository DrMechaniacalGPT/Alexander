import csv
import copy
import unittest
from pathlib import Path
from build_matrix import transform, validate, EXPECTED_PAIRS

class EvidenceSemantics(unittest.TestCase):
    def setUp(self):
        with (Path(__file__).parent/'coverage_audit.csv').open() as file:
            self.audit = list(csv.DictReader(file))
        self.rows = transform(self.audit)

    def change(self, coverage=None, source=None, product=None, **fields):
        rows = copy.deepcopy(self.rows)
        row = next(r for r in rows if (coverage is None or r['coverage']==coverage) and (source is None or r['source']==source) and (product is None or r['product']==product))
        row.update(fields)
        return rows

    def test_full_expected_cartesian_product(self):
        self.assertEqual({(r['source'],r['product']) for r in self.rows},EXPECTED_PAIRS)
        self.assertTrue(validate(self.rows))

    def test_empty_matrix_rejected(self):
        with self.assertRaisesRegex(ValueError,'64-pair'):validate([])

    def test_truncated_matrix_rejected(self):
        with self.assertRaisesRegex(ValueError,'64-pair'):validate(self.rows[:-1])

    def test_duplicate_rejected(self):
        with self.assertRaisesRegex(ValueError,'Duplicate'):validate(self.rows+[self.rows[0]])

    def test_unknown_source_rejected(self):
        rows=copy.deepcopy(self.rows);rows[0]['source']='Invented Publisher'
        with self.assertRaisesRegex(ValueError,'unknown source'):validate(rows)

    def test_unknown_product_rejected(self):
        rows=copy.deepcopy(self.rows);rows[0]['product']='Invented Robot'
        with self.assertRaisesRegex(ValueError,'unknown product'):validate(rows)

    def test_invalid_access_rejected(self):
        with self.assertRaisesRegex(ValueError,'invalid access'):validate(self.change(access_level='fabricated'))

    def test_invalid_page_type_rejected(self):
        with self.assertRaisesRegex(ValueError,'invalid page'):validate(self.change(page_type='anything'))

    def test_invalid_testing_evidence_rejected(self):
        with self.assertRaisesRegex(ValueError,'invalid testing evidence'):validate(self.change(testing_evidence='trust_me'))

    def test_empty_variant_rejected(self):
        with self.assertRaisesRegex(ValueError,'missing or identical'):validate(self.change(coverage='related_variant',tested_product=''))

    def test_invented_variant_rejected(self):
        with self.assertRaisesRegex(ValueError,'invalid tested product'):validate(self.change(coverage='related_variant',tested_product='Eufy E99'))

    def test_known_but_unrelated_variant_rejected(self):
        with self.assertRaisesRegex(ValueError,'unaudited variant'):validate(self.change(coverage='related_variant',tested_product='Roborock Saros 10R'))

    def test_unknown_never_means_not_tested(self):
        rows=copy.deepcopy(self.rows);next(r for r in rows if r['coverage']=='unknown')['coverage']='explicit_not_tested'
        with self.assertRaisesRegex(ValueError,'unsupported coverage'):validate(rows)

    def test_x60_pro_cannot_be_counted_as_max_test(self):
        rows=copy.deepcopy(self.rows)
        row=next(r for r in rows if r['source']=='TechRadar' and r['product']=='Dreame X60 Max Ultra Complete')
        row['coverage']='substantive'
        with self.assertRaisesRegex(ValueError,'exact-model'):validate(rows)

    def test_e28_does_not_silently_become_tested_e25(self):
        row=next(r for r in self.rows if r['source']=='RTINGS' and r['product']=='Eufy Omni E25')
        self.assertEqual(row['tested_product'],'Eufy Omni E28')
        self.assertEqual(row['coverage'],'related_variant')

    def test_current_guide_is_not_full_review(self):
        row=next(r for r in self.rows if r['source']=='Vacuum Wars' and r['product']=='MOVA V70 Ultra Complete')
        self.assertEqual(row['coverage'],'guide')
        self.assertEqual(row['testing_evidence'],'guide_asserts_testing_no_product_test_detail')
        rows=copy.deepcopy(self.rows)
        next(r for r in rows if r['source']=='Vacuum Wars' and r['product']=='MOVA V70 Ultra Complete')['coverage']='substantive'
        with self.assertRaisesRegex(ValueError,'not directly tested'):validate(rows)

    def test_two_products_share_one_comparison(self):
        pair=[r for r in self.rows if r['source']=='The Hook Up' and r['article_cohort']=='2026 seven-product comparison']
        self.assertEqual(len(pair),2)
        self.assertEqual(len({r['independent_test_id'] for r in pair}),1)

    def test_bad_date_rejected(self):
        with self.assertRaisesRegex(ValueError,'invalid observation date'):validate(self.change(observed_at='2026-99-99'))

    def test_missing_locator_rejected(self):
        with self.assertRaisesRegex(ValueError,'missing claim locator'):validate(self.change(claim_locator='  '))

    def test_non_url_rejected(self):
        with self.assertRaisesRegex(ValueError,'invalid evidence URL'):validate(self.change(evidence_url='not a URL'))

    def test_coverage_cannot_claim_winner(self):
        with self.assertRaisesRegex(ValueError,'verdict direction'):validate(self.change(direction='winner'))

    def test_missing_field_rejected(self):
        rows=copy.deepcopy(self.rows);del rows[0]['page_type']
        with self.assertRaisesRegex(ValueError,'fields differ'):validate(rows)

    def test_transform_rejects_unsupported_status(self):
        rows=copy.deepcopy(self.audit);rows[0]['status']='made_up'
        with self.assertRaisesRegex(ValueError,'unsupported audit status'):transform(rows)

    def test_transform_missing_field_has_useful_error(self):
        rows=copy.deepcopy(self.audit);del rows[0]['verification']
        with self.assertRaisesRegex(ValueError,'missing audit field verification'):transform(rows)

if __name__=='__main__':unittest.main()
