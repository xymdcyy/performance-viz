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

def draw_sheet9_charts(data, title_prefix, output_prefix):
    labels = [d.get('分部名称', '') for d in data]
    inventory = [d.get('库存金额', 0) for d in data]
    stale = [d.get('滞销库存', 0) for d in data]
    rates = [d.get('逾期率', 0) for d in data]

    normal = [inv - st for inv, st in zip(inventory, stale)]

    fig, ax1 = plt.subplots(figsize=(24, 10))
    x = np.arange(len(labels))
    width = 0.6

    bars1 = ax1.bar(x, normal, width, label='正常库存', color=COLOR_BLUE, alpha=0.9)
    bars2 = ax1.bar(x, stale, width, bottom=normal, label='滞销库存', color=COLOR_RED, alpha=0.9)

    for i, inv in enumerate(inventory):
        ax1.text(i, inv + 3, f'{inv:.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax1.set_xlabel('分部', fontsize=14, fontweight='bold')
    ax1.set_ylabel('库存金额（万元）', fontsize=14, color=COLOR_BLUE, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=COLOR_BLUE, labelsize=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=60, ha='right', fontsize=9)
    ax1.legend(loc='upper left', fontsize=11)
    ax1.grid(axis='y', color=COLOR_GRAY, linestyle='--', alpha=0.5)

    ax2 = ax1.twinx()
    ax2.plot(x, rates, 'o-', color=COLOR_ORANGE, linewidth=2.5, markersize=8, label='逾期率', zorder=5)
    ax2.set_ylabel('逾期率', fontsize=14, color=COLOR_ORANGE, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=COLOR_ORANGE, labelsize=12)
    ax2.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=0))

    for i, rate in enumerate(rates):
        ax2.text(i, rate + 0.02, f'{rate*100:.0f}%', ha='center', va='bottom', fontsize=8, color=COLOR_ORANGE, fontweight='bold')

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=11, framealpha=0.95)

    plt.title(f'{title_prefix} - 库存金额与逾期率分析', fontsize=18, fontweight='bold', pad=20)
    plt.tight_layout()
    save_chart(fig, f'{output_prefix}_库存逾期分析.png')

if __name__ == '__main__':
    base_path = r'd:\代码\业绩分析可视化_26年2月\json'
    print("Processing Sheet9...")
    data9 = load_json(os.path.join(base_path, 'sheet9.json'))
    draw_sheet9_charts(data9['data'], data9['title'], 'sheet9')
    print("Sheet9 charts generated successfully!")
