import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.gridspec import GridSpec
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

with open(r'D:\代码\业绩分析可视化_26年2月\json\sheet1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

records = data['data']

def get_value(record, key):
    return record.get(key, 0) or 0

fig = plt.figure(figsize=(16, 12))
fig.patch.set_facecolor('#f8f9fa')
gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.3)

ax_kpi = fig.add_subplot(gs[0, :])
ax_stack = fig.add_subplot(gs[1, 0])
ax_bar = fig.add_subplot(gs[1, 1])

ax_kpi.set_facecolor('#f8f9fa')
ax_stack.set_facecolor('white')
ax_bar.set_facecolor('white')

ax_kpi.set_xlim(0, 10)
ax_kpi.set_ylim(0, 1)
ax_kpi.axis('off')

kpi_data = []
for r in records:
    if r['渠道'] == '合计' and r['品类'] != 'KA合计':
        kpi_data.append(r)

total_income = get_value(records[0], '收入_实际')
ka_total = records[0]
tcl_smart = next(r for r in records if r['品类'] == '智屏-TCL' and r['渠道'] == '合计')
tcl_ac = next(r for r in records if r['品类'] == '空调-TCL' and r['渠道'] == '合计')
tcl_cool = next(r for r in records if r['品类'] == '冰洗-TCL' and r['渠道'] == '合计')
tcl_ciot = next(r for r in records if r['品类'] == 'CIOT-TCL' and r['渠道'] == '合计')

kpis = [
    ('总收入', f'{total_income/10000:.2f}亿', '#2E86AB'),
    ('收入达成', f'{ka_total["收入_BP达成率"]*100:.0f}%', '#28A745' if ka_total["收入_BP达成率"] >= 1 else '#DC3545'),
    ('毛利', f'{ka_total["端到端毛利率_实际"]*100:.1f}%', '#17A2B8'),
    ('净利', f'{ka_total["端到端净利_实际"]:.0f}万', '#DC3545' if ka_total["端到端净利_实际"] < 0 else '#28A745'),
    ('同比', f'+{ka_total["收入_同比"]*100:.0f}%', '#28A745'),
]

for i, (label, value, color) in enumerate(kpis):
    x = 0.5 + i * 1.9
    ax_kpi.add_patch(mpatches.FancyBboxPatch((x-0.7, 0.25), 1.5, 0.5, boxstyle="round,pad=0.02", 
                       facecolor=color, edgecolor='none', alpha=0.15))
    ax_kpi.text(x+0.05, 0.65, label, ha='center', va='center', fontsize=11, color='#495057', fontweight='bold')
    ax_kpi.text(x+0.05, 0.42, value, ha='center', va='center', fontsize=16, color=color, fontweight='bold')

ax_kpi.set_title('KA及智屏渠道业绩分析（26年2月）', fontsize=18, fontweight='bold', color='#212529', pad=15)

categories = ['智屏-TCL', '空调-TCL', '冰洗-TCL', 'CIOT-TCL']
national = []
regional = []
for cat in categories:
    nat = next((r for r in records if r['品类'] == cat and r['渠道'] == '全国连锁'), None)
    reg = next((r for r in records if r['品类'] == cat and r['渠道'] == '区域连锁'), None)
    national.append(get_value(nat, '收入_实际') if nat else 0)
    regional.append(get_value(reg, '收入_实际') if reg else 0)

x = np.arange(len(categories))
width = 0.5
bars1 = ax_stack.bar(x, national, width, label='全国连锁', color='#2E86AB', alpha=0.9)
bars2 = ax_stack.bar(x, regional, width, bottom=national, label='区域连锁', color='#A23B72', alpha=0.9)

ax_stack.set_ylabel('收入（万）', fontsize=11)
ax_stack.set_title('品类收入结构（渠道拆分）', fontsize=14, fontweight='bold', pad=10)
ax_stack.set_xticks(x)
ax_stack.set_xticklabels([c.replace('-TCL', '') for c in categories], fontsize=11)
ax_stack.legend(loc='upper right', framealpha=0.9)
ax_stack.spines['top'].set_visible(False)
ax_stack.spines['right'].set_visible(False)

for i, cat in enumerate(categories):
    total = national[i] + regional[i]
    ax_stack.text(i, total + 100, f'{total:.0f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

ax_bar.set_title('品类达成率对比', fontsize=14, fontweight='bold', pad=10)

metrics = ['收入达成率', '销量达成率', '净利达成率', '毛利率达成率']
x = np.arange(len(categories))
width = 0.18
colors = ['#2E86AB', '#F18F01', '#C73E1D', '#3A7D44']

for j, (metric, color) in enumerate(zip(metrics, colors)):
    values = []
    for cat in categories:
        record = next((r for r in records if r['品类'] == cat and r['渠道'] == '合计'), None)
        if record:
            if '收入' in metric:
                values.append(get_value(record, '收入_BP达成率') * 100)
            elif '销量' in metric:
                values.append(get_value(record, '销量_BP达成率') * 100)
            elif '净利' in metric:
                values.append(max(-200, min(200, get_value(record, '端到端净利_BP达成率'))))
            elif '毛利' in metric:
                values.append(max(-50, min(50, get_value(record, '端到端毛利率_BP达成率'))))
        else:
            values.append(0)
    ax_bar.bar(x + (j - 1.5) * width, values, width, label=metric, color=color, alpha=0.85)

ax_bar.axhline(y=100, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='100%基准')
ax_bar.set_ylabel('达成率 (%)', fontsize=11)
ax_bar.set_xticks(x)
ax_bar.set_xticklabels([c.replace('-TCL', '') for c in categories], fontsize=11)
ax_bar.legend(loc='upper right', ncol=2, fontsize=9, framealpha=0.9)
ax_bar.spines['top'].set_visible(False)
ax_bar.spines['right'].set_visible(False)

fig.savefig(r'D:\代码\业绩分析可视化_26年2月\charts\sales_dashboard.png', 
            dpi=150, bbox_inches='tight', facecolor='#f8f9fa', edgecolor='none')
plt.close()

fig2 = plt.figure(figsize=(16, 10))
fig2.patch.set_facecolor('#f8f9fa')

ax_heatmap = fig2.add_subplot(111)
ax_heatmap.set_facecolor('#f8f9fa')

heat_data = []
labels = []
for r in records:
    if r['渠道'] != '合计':
        labels.append(f"{r['品类'].replace('-TCL', '')}\n{r['渠道']}")
        heat_data.append([
            get_value(r, '收入_BP达成率') * 100,
            get_value(r, '销量_BP达成率') * 100,
            get_value(r, 'ASP_BP达成'),
            get_value(r, '端到端净利_BP达成率'),
            get_value(r, '端到端毛利率_BP达成率') * 10
        ])

heat_array = np.array(heat_data)

vmin, vmax = -50, 200
cmap = 'RdYlGn'

im = ax_heatmap.imshow(heat_array, cmap=cmap, aspect='auto', vmin=vmin, vmax=vmax)

ax_heatmap.set_xticks(range(5))
ax_heatmap.set_xticklabels(['收入\n达成率%', '销量\n达成率%', 'ASP\n差异', '净利\n达成率', '毛利率\n达成率'], 
                            fontsize=11, ha='center')
ax_heatmap.set_yticks(range(len(labels)))
ax_heatmap.set_yticklabels(labels, fontsize=10)

ax_heatmap.set_title('品类×渠道 指标达成热力图', fontsize=16, fontweight='bold', pad=20)

for i in range(len(labels)):
    for j in range(5):
        val = heat_array[i, j]
        color = 'white' if abs(val - 100) > 60 else 'black'
        text_color = 'white'
        if j == 2:
            ax_heatmap.text(j, i, f'{val:.0f}', ha='center', va='center', fontsize=9, color=text_color, fontweight='bold')
        elif j in [0, 1]:
            ax_heatmap.text(j, i, f'{val:.0f}%', ha='center', va='center', fontsize=9, color=text_color, fontweight='bold')
        elif j == 3:
            ax_heatmap.text(j, i, f'{val:.0f}%', ha='center', va='center', fontsize=9, color=text_color, fontweight='bold')
        else:
            ax_heatmap.text(j, i, f'{val:.1f}%', ha='center', va='center', fontsize=9, color=text_color, fontweight='bold')

cbar = plt.colorbar(im, ax=ax_heatmap, shrink=0.6, aspect=30)
cbar.set_label('指标值 (绿=优/红=劣)', fontsize=11)

ax_heatmap.axvline(x=0.5, color='gray', linewidth=2, linestyle='-')
ax_heatmap.axvline(x=1.5, color='gray', linewidth=2, linestyle='-')
ax_heatmap.axvline(x=2.5, color='gray', linewidth=2, linestyle='-')
ax_heatmap.axvline(x=3.5, color='gray', linewidth=2, linestyle='-')

for i in range(len(labels)):
    if i % 3 == 0 and i > 0:
        ax_heatmap.axhline(y=i-0.5, color='gray', linewidth=1.5, linestyle='--')

fig2.savefig(r'D:\代码\业绩分析可视化_26年2月\charts\heatmap.png', 
             dpi=150, bbox_inches='tight', facecolor='#f8f9fa', edgecolor='none')
plt.close()

print('图表已保存:')
print('  - D:\\代码\\业绩分析可视化_26年2月\\charts\\sales_dashboard.png')
print('  - D:\\代码\\业绩分析可视化_26年2月\\charts\\heatmap.png')
