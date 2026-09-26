import json
import unittest
from pathlib import Path
from economics import calculate, break_even

class EconomicsTests(unittest.TestCase):
    def setUp(self):
        self.p=json.loads((Path(__file__).parent/'inputs.json').read_text())
        self.b=self.p['cases'][1]
    def test_hand_calculated_base(self):
        r=calculate(self.b,self.p)
        self.assertAlmostEqual(r['fees_per_order'],5.105)
        self.assertAlmostEqual(r['contribution'],29.175)
        self.assertAlmostEqual(r['cash_surplus'],8152.5)
        self.assertAlmostEqual(r['economic_profit'],3052.5)
        self.assertEqual(r['economic_break_even'],196)
        self.assertLess(calculate({**self.b,'orders':195},self.p)['economic_profit'],0)
        self.assertGreaterEqual(calculate({**self.b,'orders':196},self.p)['economic_profit'],0)
    def test_zero_sales_and_negative_margin(self):
        r=calculate({**self.b,'orders':0},self.p)
        self.assertEqual(r['cash_surplus'],-1500)
        self.assertEqual(r['economic_profit'],-5700)
        self.assertIsNone(calculate({**self.b,'cac':100},self.p)['economic_break_even'])
        self.assertIsNone(break_even(100,0))
    def test_sensitivity_and_tax_base(self):
        base=calculate(self.b,self.p)['contribution']
        self.assertAlmostEqual(base-calculate({**self.b,'cac':20},self.p)['contribution'],10)
        self.assertAlmostEqual(base-calculate(self.b,{**self.p,'buyer_tax_rate':.08})['contribution'],49*.08*.03)
        self.assertAlmostEqual(base-calculate(self.b,{**self.p,'offsite_attributed_fraction':1})['contribution'],49*.15)
        self.assertLess(calculate({**self.b,'refund_rate':1},self.p)['contribution'],0)

if __name__=='__main__': unittest.main()
