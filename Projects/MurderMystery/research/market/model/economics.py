"""Illustrative US Etsy digital-kit economics; standard library only.
Run from any directory. Refunds reduce gross receipts; conservatively no fee credits.
Cash assumes unpaid founder support/development. Economic profit values both.
"""
import json
import math
from pathlib import Path
ROOT = Path(__file__).resolve().parent

def calculate(case, params):
    n, price = case['orders'], case['price']
    if n < 0 or price < 0 or not 0 <= case['refund_rate'] <= 1:
        raise ValueError('Invalid orders, price or refund rate')
    fees = (price * params['transaction_rate']
            + price * (1 + params['buyer_tax_rate']) * params['processing_rate']
            + params['listing_and_processing_fixed']
            + price * params['offsite_attributed_fraction'] * params['offsite_rate'])
    support = case['support_minutes'] / 60 * params['support_hourly_value']
    cash_unit = price * (1 - case['refund_rate']) - fees - params['delivery_per_order'] - case['cac']
    contribution = cash_unit - support
    full_fixed = params['fixed_cash'] + params['development_hours'] * params['development_hourly_value']
    return dict(gross=n*price, fees_per_order=fees, cash_unit=cash_unit,
                contribution=contribution, cash_surplus=n*cash_unit-params['fixed_cash'],
                economic_profit=n*contribution-full_fixed,
                cash_break_even=break_even(params['fixed_cash'], cash_unit),
                economic_break_even=break_even(full_fixed, contribution))

def break_even(fixed, unit):
    return math.ceil(fixed / unit) if unit > 0 else None

def render(params):
    lines = ['# Generated economics results', '',
             'Run `python3 economics.py` beside this file. Inputs are assumptions, not forecasts.', '',
             '| Case | Orders | Gross | Contribution/order after support | Cash surplus | Profit after valued labor | Cash / full break-even orders |',
             '|---|---:|---:|---:|---:|---:|---:|']
    for c in params['cases']:
        r = calculate(c, params)
        lines.append(f"| {c['name']} | {c['orders']} | ${r['gross']:,.2f} | ${r['contribution']:.3f} | ${r['cash_surplus']:,.2f} | ${r['economic_profit']:,.2f} | {r['cash_break_even']} / {r['economic_break_even']} |")
    b = params['cases'][1]
    lines += ['', '## Price and acquisition sensitivity', '', 'Contribution per order after support; other base inputs unchanged.', '', '| Price / CAC | $0 | $5 | $10 | $20 | $30 | $40 |', '|---|---:|---:|---:|---:|---:|---:|']
    for price in [39,49,59]:
        values=[calculate({**b,'price':price,'cac':cac},params)['contribution'] for cac in [0,5,10,20,30,40]]
        lines.append(f'| ${price} | '+' | '.join(f'${v:.2f}' for v in values)+' |')
    lines += ['', '## One-variable stress cases', '', '| Change from base | Contribution/order | Full break-even |', '|---|---:|---:|']
    changes=[('Support 3 minutes',{'support_minutes':3},{}),('Support 15 minutes',{'support_minutes':15},{}),('Support 30 minutes',{'support_minutes':30},{}),('All orders carry 15% offsite fee',{}, {'offsite_attributed_fraction':1}),('Buyer sales-tax rate 8%',{}, {'buyer_tax_rate':.08}),('Development 60 hours',{}, {'development_hours':60}),('Development 240 hours',{}, {'development_hours':240})]
    for label, c, p in changes:
        r=calculate({**b,**c},{**params,**p})
        lines.append(f"| {label} | ${r['contribution']:.3f} | {r['economic_break_even']} |")
    r=calculate(b,params)
    fixed=params['fixed_cash']+params['development_hours']*params['development_hourly_value']
    lines += ['', '## Capital and traffic requirements', '']
    for target in [10000,100000]:
        lines.append(f"- ${target:,} beyond fixed costs needs {break_even(params['fixed_cash']+target,r['cash_unit']):,} orders on an unpaid-founder cash basis or {break_even(fixed+target,r['contribution']):,} with labor valued (base unit assumptions).")
    lines += ['- 300 purchases at hypothetical 1%, 2%, or 3% visit-to-purchase conversion require 30,000, 15,000, or 10,000 qualified visits respectively.', '- $10 acquisition cost at hypothetical 2% paid conversion permits only $0.20 per click before other marketing costs.', '- Zero sales loses $1,500 cash plus $4,200 valued development time if the full assumed budget is spent.', '', 'No stock, currency, tax, demand, conversion or advertising forecast is being made.']
    return '\n'.join(lines)+'\n'

if __name__ == '__main__':
    params=json.loads((ROOT/'inputs.json').read_text())
    (ROOT/'results.md').write_text(render(params))
