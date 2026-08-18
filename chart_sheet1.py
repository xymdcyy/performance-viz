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

CATEGORY_COLORS = {
    'KA合计': '#2E75B6',
    '智屏-TCL': '#5B9BD5',
    '空调-TCL': '#ED7D31',
    '冰洗-TCL': '#A9D18E',
    'CIOT-TCL': '#FFC000'
}

CHANNEL_COLORS = {
    '合计': '#4472C4',
    '全国连锁': '#5B9BD5',
    '区域连锁': '#8FAADC'
}

def save_chart(fig, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f'Saved: {path}')
    plt.close(fig)

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def draw_sheet1_charts(data, title_prefix, output_prefix):
    categories = ['KA合计', '智屏-TCL', '空调-TCL', '冰洗-TCL', 'CIOT-TCL']
    channels = ['合计', '全国连锁', '区域连锁']
    filtered = [d for d in data if d['品类'] in categories and d['渠道'] in channels]

    labels = [f"{d['品类']}-{d['渠道']}" for d in filtered]
    cat_types = [d['品类'] for d in filtered]
    actual = [d['收入_实际'] for d in filtered]
    bp = [d['收入_BP'] for d in filtered]
    achieve = [d['收入_BP达成率'] for d in filtered]
    yoy = [d['收入_同比'] for d in filtered]

    fig, ax1 = plt.subplots(figsize=(30, 12))
    x = np.arange(len(labels))
    width = 0.35

    for i, (label, cat, act) in enumerate(zip(labels, cat_types, actual)):
        color = CATEGORY_COLORS.get(cat, COLOR_BLUE)
        ax1.bar(x[i] - width/2, act, width, color=color, alpha=0.9)

    ax1.bar(x + width/2, bp, width, label='BP', color=COLOR_LIGHT_BLUE, alpha=0.9)
    ax1.set_xlabel('品类-渠道', fontsize=16, fontweight='bold')
    ax1.set_ylabel('收入（万元）', fontsize=16, color=COLOR_BLUE, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=COLOR_BLUE, labelsize=14)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=45, ha='right', fontsize=12)

    for i, act in enumerate(actual):
        ax1.text(i - width/2, act + 50, f'{act:.0f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax2 = ax1.twinx()
    ax2.plot(x, achieve, 'o-', color=COLOR_ORANGE, linewidth=2.5, markersize=10, label='BP达成率', zorder=5)
    ax2.plot(x, yoy, 's--', color=COLOR_GREEN, linewidth=2.5, markersize=10, label='同比', zorder=5)
    ax2.axhline(y=1, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    ax2.set_ylabel('比率', fontsize=16, color=COLOR_ORANGE, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=COLOR_ORANGE, labelsize=14)
    ax2.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=0))

    for i, (v1, v2) in enumerate(zip(achieve, yoy)):
        offset = 0.03 if v1 >= 0 else -0.03
        ax2.text(i, v1 + offset, f'{v1*100:.0f}%', ha='center', va='bottom', fontsize=10, color=COLOR_ORANGE, fontweight='bold')
        offset = 0.03 if v2 >= 0 else -0.03
        ax2.text(i, v2 + offset, f'{v2*100:.0f}%', ha='center', va='bottom', fontsize=9, color=COLOR_GREEN)

    legend_patches = [plt.Rectangle((0,0),1,1, color=CATEGORY_COLORS[cat], alpha=0.9) for cat in categories]
    legend_labels = [f'{cat}（实际）' for cat in categories]
    bp_patch = plt.Rectangle((0,0),1,1, color=COLOR_LIGHT_BLUE, alpha=0.9, label='BP')
    ax1.legend(legend_patches + [bp_patch], legend_labels + ['BP'], loc='upper right', fontsize=11, framealpha=0.95, ncol=2)

    ax2_lines = ax2.get_legend_handles_labels()
    ref_line = plt.Line2D([0], [0], color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    handles2 = ax2_lines[0] + [ref_line]
    labels2 = ax2_lines[1] + ['100%基准线']
    ax2.legend(handles2, labels2, loc='upper left', fontsize=11, framealpha=0.95)

    ax1.grid(axis='y', color=COLOR_GRAY, linestyle='--', alpha=0.5)
    plt.title(f'{title_prefix} - 收入与BP达成分析', fontsize=20, fontweight='bold', pad=20)
    plt.tight_layout()
    save_chart(fig, f'{output_prefix}_收入BP达成.png')

    vol_actual = [d['销量_实际'] for d in filtered]
    vol_bp = [d['销量_BP达成率'] for d in filtered]

    fig, ax1 = plt.subplots(figsize=(30, 12))

    for i, (cat, vol) in enumerate(zip(cat_types, vol_actual)):
        color = CATEGORY_COLORS.get(cat, COLOR_BLUE)
        ax1.bar(x[i] - width/2, vol, width, color=color, alpha=0.9)

    ax1.set_xlabel('品类-渠道', fontsize=16, fontweight='bold')
    ax1.set_ylabel('销量（万台）', fontsize=16, color=COLOR_BLUE, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=COLOR_BLUE, labelsize=14)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=45, ha='right', fontsize=12)

    for i, vol in enumerate(vol_actual):
        ax1.text(i - width/2, vol + 0.02, f'{vol:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax2 = ax1.twinx()
    ax2.plot(x, vol_bp, 'o-', color=COLOR_ORANGE, linewidth=2.5, markersize=10, label='BP达成率', zorder=5)
    ax2.axhline(y=1, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    ax2.set_ylabel('BP达成率', fontsize=16, color=COLOR_ORANGE, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=COLOR_ORANGE, labelsize=14)
    ax2.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=0))

    for i, v in enumerate(vol_bp):
        offset = 0.03 if v >= 0 else -0.03
        ax2.text(i, v + offset, f'{v*100:.0f}%', ha='center', va='bottom', fontsize=10, color=COLOR_ORANGE, fontweight='bold')

    legend_patches = [plt.Rectangle((0,0),1,1, color=CATEGORY_COLORS[cat], alpha=0.9) for cat in categories]
    legend_labels = [f'{cat}' for cat in categories]
    ax1.legend(legend_patches, legend_labels, loc='upper right', fontsize=11, framealpha=0.95, ncol=2)

    ax2_lines = ax2.get_legend_handles_labels()
    ref_line = plt.Line2D([0], [0], color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    handles2 = ax2_lines[0] + [ref_line]
    labels2 = ax2_lines[1] + ['100%基准线']
    ax2.legend(handles2, labels2, loc='upper left', fontsize=11, framealpha=0.95)

    ax1.grid(axis='y', color=COLOR_GRAY, linestyle='--', alpha=0.5)
    plt.title(f'{title_prefix} - 销量与BP达成分析', fontsize=20, fontweight='bold', pad=20)
    plt.tight_layout()
    save_chart(fig, f'{output_prefix}_销量BP达成.png')

    profit_actual = [d['端到端净利_实际'] for d in filtered]
    profit_bp = [d['端到端净利_BP达成率'] for d in filtered]
    margin_actual = [d['端到端毛利率_实际'] for d in filtered]
    margin_bp = [d['端到端毛利率_BP达成率'] for d in filtered]

    fig, ax1 = plt.subplots(figsize=(30, 12))

    for i, (cat, margin) in enumerate(zip(cat_types, margin_actual)):
        color = CATEGORY_COLORS.get(cat, COLOR_BLUE)
        ax1.bar(x[i] - width/2, margin, width, color=color, alpha=0.9)

    ax1.set_xlabel('品类-渠道', fontsize=16, fontweight='bold')
    ax1.set_ylabel('毛利率', fontsize=16, color=COLOR_BLUE, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=COLOR_BLUE, labelsize=14)
    ax1.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=1))
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=45, ha='right', fontsize=12)

    for i, margin in enumerate(margin_actual):
        ax1.text(i - width/2, margin + 0.005, f'{margin*100:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax2 = ax1.twinx()
    ax2.plot(x, margin_bp, 'o-', color=COLOR_ORANGE, linewidth=2.5, markersize=10, label='毛利率BP达成', zorder=5)
    ax2.plot(x, profit_bp, 's--', color=COLOR_GREEN, linewidth=2.5, markersize=10, label='净利BP达成', zorder=5)
    ax2.axhline(y=0, color='green', linestyle='--', linewidth=1.5, alpha=0.7)
    ax2.set_ylabel('BP达成率差值（个百分点）', fontsize=14, color=COLOR_ORANGE, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=COLOR_ORANGE, labelsize=14)

    for i, (v1, v2) in enumerate(zip(margin_bp, profit_bp)):
        offset = 0.3 if v1 >= 0 else -0.3
        ax2.text(i, v1 + offset, f'{v1:.1f}', ha='center', va='bottom', fontsize=9, color=COLOR_ORANGE, fontweight='bold')
        offset = 0.3 if v2 >= 0 else -0.3
        ax2.text(i, v2 + offset, f'{v2:.1f}', ha='center', va='bottom', fontsize=9, color=COLOR_GREEN)

    legend_patches = [plt.Rectangle((0,0),1,1, color=CATEGORY_COLORS[cat], alpha=0.9) for cat in categories]
    legend_labels = [f'{cat}' for cat in categories]
    ax1.legend(legend_patches, legend_labels, loc='upper right', fontsize=11, framealpha=0.95, ncol=2)

    ax2_lines = ax2.get_legend_handles_labels()
    zero_line = plt.Line2D([0], [0], color='green', linestyle='--', linewidth=1.5, alpha=0.7)
    handles2 = ax2_lines[0] + [zero_line]
    labels2 = ax2_lines[1] + ['0%基准线']
    ax2.legend(handles2, labels2, loc='upper left', fontsize=11, framealpha=0.95)

    ax1.grid(axis='y', color=COLOR_GRAY, linestyle='--', alpha=0.5)
    plt.title(f'{title_prefix} - 毛利率与净利BP达成分析', fontsize=20, fontweight='bold', pad=20)
    plt.tight_layout()
    save_chart(fig, f'{output_prefix}_毛利率净利.png')

if __name__ == '__main__':
    base_path = r'd:\代码\业绩分析可视化_26年2月\json'
    print("Processing Sheet1...")
    data1 = load_json(os.path.join(base_path, 'sheet1.json'))
    draw_sheet1_charts(data1['data'], data1['title'], 'sheet1')
    print("Sheet1 charts generated successfully!")
