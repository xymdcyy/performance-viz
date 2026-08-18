import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

with open(r"d:\代码\业绩分析可视化_26年2月\sheet8_output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

df = df[df['大区'] != '总计'].copy()

df = df.dropna(subset=['战区'])

region_order = ['东北', '华北', '华东', '华南', '西北', '西南']
df['大区排序'] = pd.Categorical(df['大区'], categories=region_order, ordered=True)
df = df.sort_values(['大区排序', '战区']).reset_index(drop=True)

fig, ax1 = plt.subplots(figsize=(16, 8))

x = np.arange(len(df))
width = 0.35

bars1 = ax1.bar(x - width/2, df['零售'], width, label='零售', color='#4472C4')
bars2 = ax1.bar(x + width/2, df['库存'], width, label='库存', color='#ED7D31')

ax1.set_xlabel('战区', fontsize=12)
ax1.set_ylabel('数量', fontsize=12, color='#4472C4')
ax1.tick_params(axis='y', labelcolor='#4472C4')
ax1.set_ylim(0, df[['零售', '库存']].max().max() * 1.15)

ax2 = ax1.twinx()
line = ax2.plot(x, df['存销比'], 'o-', color='#70AD47', linewidth=2, markersize=6, label='存销比')
ax2.set_ylabel('存销比', fontsize=12, color='#70AD47')
ax2.tick_params(axis='y', labelcolor='#70AD47')
ax2.set_ylim(0, df['存销比'].max() * 1.2)

ax1.set_xticks(x)
ax1.set_xticklabels(df['战区'], rotation=45, ha='right', fontsize=10)

region_boundaries = []
current_region = df['大区'].iloc[0]
start_idx = 0
for i, region in enumerate(df['大区']):
    if region != current_region:
        region_boundaries.append((current_region, start_idx, i - 1))
        current_region = region
        start_idx = i
region_boundaries.append((current_region, start_idx, len(df) - 1))

for region, start, end in region_boundaries:
    mid = (start + end) / 2
    ax1.annotate(region, xy=(mid, ax1.get_ylim()[1] * 0.98), 
                 ha='center', va='top', fontsize=11, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgray', alpha=0.5))
    if end < len(df) - 1:
        ax1.axvline(x=end + 0.5, color='gray', linestyle='--', alpha=0.5, linewidth=1)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=10)

plt.title('26年2月KA及智屏渠道业绩分析', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()

output_path = r"d:\代码\业绩分析可视化_26年2月\chart_sheet8.png"
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"Chart saved: {output_path}")

plt.close()
