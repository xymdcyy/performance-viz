import json
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

with open(r'd:\代码\业绩分析可视化_26年2月\charts\sheet7.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

flat_data = data['flat']
keys = list(flat_data[0].keys())

STOCK_KEY = '客\xa0\xa0\xa0\xa0\xa0\xa0户\xa0\xa0\xa0\xa0\xa0\xa0\xa0存\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0销'
STAGN_KEY = '客\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0户\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0滞\xa0\xa0\xa0\xa0\xa0\xa0\xa0销'

def find_key(prefix):
    for k in keys:
        if k.startswith(prefix):
            return k
    return None

stock_key = find_key(STOCK_KEY)
stagn_key = find_key(STAGN_KEY)
print(f'stock_key: {repr(stock_key)}')
print(f'stagn_key: {repr(stagn_key)}')

regions = {}
for row in flat_data:
    region = row.get('大区')
    if region and region != '合计' and '小计' not in str(row.get('战区', '')):
        if region not in regions:
            regions[region] = {'库存': 0, '销售': 0, '存销比': []}

        if stock_key:
            kucun = row.get(f'{stock_key}') or 0
            xiaoshou = row.get(f'{stock_key.replace(".库存", ".销售")}') or 0
            cunxiao = row.get(f'{stock_key.replace(".库存", ".存销")}')
            regions[region]['库存'] += kucun
            regions[region]['销售'] += xiaoshou
            if cunxiao:
                regions[region]['存销比'].append(cunxiao)

print('Regions data:', {k: {kk: vv for kk, vv in v.items() if kk != '存销比'} for k, v in regions.items()})

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('客户存销滞销分析 - 区域汇总', fontsize=14, fontweight='bold')

region_names = list(regions.keys())
inventory = [regions[r]['库存'] for r in region_names]
sales = [regions[r]['销售'] for r in region_names]

x = range(len(region_names))
width = 0.35

axes[0].bar([i - width/2 for i in x], inventory, width, label='库存', color='steelblue')
axes[0].bar([i + width/2 for i in x], sales, width, label='销售', color='coral')
axes[0].set_xlabel('区域')
axes[0].set_ylabel('数量')
axes[0].set_title('各区域库存与销售对比')
axes[0].set_xticks(x)
axes[0].set_xticklabels(region_names, rotation=45, ha='right')
axes[0].legend()
axes[0].grid(axis='y', alpha=0.3)

avg_ratios = []
for r in region_names:
    ratios = regions[r]['存销比']
    avg_ratios.append(sum(ratios) / len(ratios) if ratios else 0)

axes[1].bar(region_names, avg_ratios, color='green', alpha=0.7)
axes[1].set_xlabel('区域')
axes[1].set_ylabel('存销比')
axes[1].set_title('各区域平均存销比')
axes[1].axhline(y=1, color='red', linestyle='--', label='健康线(1.0)')
axes[1].legend()
axes[1].grid(axis='y', alpha=0.3)
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.savefig(r'd:\代码\业绩分析可视化_26年2月\charts\sheet7_区域汇总.png', dpi=150, bbox_inches='tight')
plt.close()

customers = ['苏宁', '五星']
customer_data = {c: {'库存': 0, '销售': 0} for c in customers}
stagnation_data = {c: {'台数': 0, '金额': 0} for c in customers}

def get_stock_key(customer, field):
    return stock_key.replace('.合计', f'.{customer}').replace('库存', field) if stock_key else None

def get_stagn_key(customer, key_type, field):
    if not stagn_key:
        return None
    return stagn_key.replace('.苏宁', f'.{customer}').replace('60+库存', key_type).replace('台数', field)

for row in flat_data:
    if '小计' in str(row.get('战区', '')) or row.get('大区') == '合计':
        continue
    if stock_key:
        for c in customers:
            k = get_stock_key(c, '库存')
            s = get_stock_key(c, '销售')
            customer_data[c]['库存'] += row.get(k) or 0
            customer_data[c]['销售'] += row.get(s) or 0
    if stagn_key:
        for c in customers:
            key_type = '60+库存' if c == '苏宁' else '90+库存'
            t = get_stagn_key(c, key_type, '台数')
            j = get_stagn_key(c, key_type, '金额')
            stagnation_data[c]['台数'] += row.get(t) or 0
            stagnation_data[c]['金额'] += row.get(j) or 0

print('Customer data:', customer_data)
print('Stagnation data:', stagnation_data)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('客户存销滞销分析 - 客户对比', fontsize=14, fontweight='bold')

cx = range(len(customers))
axes[0].bar([i - width/2 for i in cx], [customer_data[c]['库存'] for c in customers], width, label='库存', color='steelblue')
axes[0].bar([i + width/2 for i in cx], [customer_data[c]['销售'] for c in customers], width, label='销售', color='coral')
axes[0].set_xlabel('客户')
axes[0].set_ylabel('数量')
axes[0].set_title('客户库存与销售对比')
axes[0].set_xticks(cx)
axes[0].set_xticklabels(customers)
axes[0].legend()
axes[0].grid(axis='y', alpha=0.3)

axes[1].bar([i - width/2 for i in cx], [stagnation_data[c]['台数'] for c in customers], width, label='滞销台数', color='purple')
axes[1].bar([i + width/2 for i in cx], [stagnation_data[c]['金额'] for c in customers], width, label='滞销金额', color='orange')
axes[1].set_xlabel('客户')
axes[1].set_ylabel('数量')
axes[1].set_title('客户滞销库存对比')
axes[1].set_xticks(cx)
axes[1].set_xticklabels(customers)
axes[1].legend()
axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(r'd:\代码\业绩分析可视化_26年2月\charts\sheet7_客户对比.png', dpi=150, bbox_inches='tight')
plt.close()

print('可视化完成！')
