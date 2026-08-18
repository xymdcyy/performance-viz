import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
import json
import os

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

OUTPUT_DIR = r'd:\代码\业绩分析可视化_26年2月\charts'
os.makedirs(OUTPUT_DIR, exist_ok=True)

COLOR_BLUE = '#4472C4'
COLOR_ORANGE = '#C55A11'
COLOR_GREEN = '#70AD47'
COLOR_RED = '#FF0000'
COLOR_LIGHT_BLUE = '#8FAADC'
COLOR_GRAY = '#CCCCCC'

def save_chart(fig, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f'Saved: {path}')
    plt.close(fig)

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def draw_sheet7_charts(data, title_prefix, output_prefix):
    labels = [f"{d.get('大区','')}-{d.get('战区','')}" for d in data]
    ratio_suning = [d.get('存销比_苏宁', 0) or 0 for d in data]
    ratio_wuxing = [d.get('存销比_五星', 0) or 0 for d in data]
    stale_suning = [d.get('滞销_苏宁_滞销占比_金额', 0) or 0 for d in data]
    stale_wuxing = [d.get('滞销_五星_滞销占比_金额', 0) or 0 for d in data]

    fig, ax1 = plt.subplots(figsize=(28, 12))
    x = np.arange(len(labels))
    width = 0.25

    bars1 = ax1.bar(x - width/2, ratio_suning, width, label='苏宁存销比', color=COLOR_BLUE, alpha=0.9)
    bars2 = ax1.bar(x + width/2, ratio_wuxing, width, label='五星存销比', color=COLOR_ORANGE, alpha=0.9)

    for bar in bars1:
        h = bar.get_height()
        if h > 0:
            ax1.text(bar.get_x() + bar.get_width()/2, h + 0.03, f'{h:.1f}',
                    ha='center', va='bottom', fontsize=8, fontweight='bold')
    for bar in bars2:
        h = bar.get_height()
        if h > 0:
            ax1.text(bar.get_x() + bar.get_width()/2, h + 0.03, f'{h:.1f}',
                    ha='center', va='bottom', fontsize=8, fontweight='bold')

    ax1.set_xlabel('战区', fontsize=14, fontweight='bold')
    ax1.set_ylabel('存销比', fontsize=14, color=COLOR_BLUE, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=COLOR_BLUE, labelsize=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=60, ha='right', fontsize=9)
    ax1.legend(loc='upper left', fontsize=11)
    ax1.grid(axis='y', color=COLOR_GRAY, linestyle='--', alpha=0.5)

    ax2 = ax1.twinx()
    ax2.plot(x, stale_suning, 'o--', color=COLOR_BLUE, linewidth=2, markersize=6, label='苏宁滞销占比', zorder=5)
    ax2.plot(x, stale_wuxing, 's--', color=COLOR_ORANGE, linewidth=2, markersize=6, label='五星滞销占比', zorder=5)
    ax2.set_ylabel('滞销占比', fontsize=14, color=COLOR_ORANGE, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=COLOR_ORANGE, labelsize=12)
    ax2.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=0))

    for i, (s, w) in enumerate(zip(stale_suning, stale_wuxing)):
        if s > 0:
            ax2.text(i, s + 0.02, f'{s*100:.0f}%', ha='center', va='bottom', fontsize=7, color=COLOR_BLUE)
        if w > 0:
            ax2.text(i, w + 0.02, f'{w*100:.0f}%', ha='center', va='bottom', fontsize=7, color=COLOR_ORANGE)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=10, framealpha=0.95, ncol=2)

    plt.title(f'{title_prefix} - 存销比与滞销占比分析', fontsize=18, fontweight='bold', pad=20)
    plt.tight_layout()
    save_chart(fig, f'{output_prefix}_存销滞销分析.png')

if __name__ == '__main__':
    base_path = r'd:\代码\业绩分析可视化_26年2月\json'
    print("Processing Sheet7...")
    data7 = load_json(os.path.join(base_path, 'sheet7.json'))
    draw_sheet7_charts(data7['data'], data7['title'], 'sheet7')
    print("Sheet7 charts generated successfully!")
