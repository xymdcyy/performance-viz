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
    '汇总': '#2E75B6',
    '智屏': '#5B9BD5',
    '空调': '#ED7D31',
    '冰洗': '#A9D18E',
    'CIOT': '#FFC000'
}

def save_chart(fig, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f'Saved: {path}')
    plt.close(fig)

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def draw_sheet3_charts(data, title_prefix, output_prefix):
    categories = ['汇总', '智屏', '空调', '冰洗', 'CIOT']
    category_data = {cat: {'固定费用': 0, '变动费用': 0, '费率': 0, 'BP比': 0, '同比': 0} for cat in categories}

    for d in data:
        item_type = d.get('费用项目', '')
        for cat in categories:
            if cat == '汇总':
                fixed_key = f'合计_实际'
                var_key = f'合计_实际'
                rate_key = f'合计_实际'
                bp_key = f'合计_BP比'
                yoy_key = f'合计_同比'
            else:
                fixed_key = f'{cat}_连锁渠道_实际'
                var_key = f'{cat}_区域连锁_实际'
                rate_key = f'{cat}_连锁渠道_实际'
                bp_key = f'{cat}_连锁渠道_BP比'
                yoy_key = f'{cat}_连锁渠道_同比'

            if item_type == '固定性费用':
                category_data[cat]['固定费用'] += d.get(fixed_key, 0)
            elif item_type == '变动性费用':
                category_data[cat]['变动费用'] += d.get(var_key, 0)
            elif item_type == '汇总费用费率':
                category_data[cat]['费率'] = d.get(rate_key, 0)
                category_data[cat]['BP比'] = d.get(bp_key, 0)
                category_data[cat]['同比'] = d.get(yoy_key, 0)

    cat_labels = categories
    fixed_fees = [category_data[cat]['固定费用'] for cat in categories]
    variable_fees = [category_data[cat]['变动费用'] for cat in categories]
    total_fees = [f + v for f, v in zip(fixed_fees, variable_fees)]

    fig, ax = plt.subplots(figsize=(20, 10))
    x = np.arange(len(cat_labels))
    width = 0.5

    colors_fixed = [CATEGORY_COLORS[cat] for cat in categories]
    colors_var = ['#8FAADC', '#A2C4E8', '#F4A460', '#C5E0B4', '#FFE699']

    bars1 = ax.bar(x, fixed_fees, width, label='固定费用', color=colors_fixed, alpha=0.9, edgecolor='black', linewidth=0.5)
    bars2 = ax.bar(x, variable_fees, width, bottom=fixed_fees, label='变动费用', color=colors_var, alpha=0.9, edgecolor='black', linewidth=0.5)

    for i, (fixed, variable, total) in enumerate(zip(fixed_fees, variable_fees, total_fees)):
        ax.text(i, fixed/2, f'{fixed:.0f}', ha='center', va='center', fontsize=11, fontweight='bold', color='white')
        ax.text(i, fixed + variable/2, f'{variable:.0f}', ha='center', va='center', fontsize=11, fontweight='bold', color='white')
        ax.text(i, total + 80, f'{total:.0f}', ha='center', va='bottom', fontsize=12, fontweight='bold')

    ax.set_xlabel('品类', fontsize=16, fontweight='bold')
    ax.set_ylabel('费用金额（万元）', fontsize=16, color=COLOR_BLUE, fontweight='bold')
    ax.tick_params(axis='y', labelcolor=COLOR_BLUE, labelsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(cat_labels, fontsize=14)
    ax.legend(loc='upper right', fontsize=12, framealpha=0.95)
    ax.grid(axis='y', color=COLOR_GRAY, linestyle='--', alpha=0.5)
    plt.title(f'{title_prefix} - 费用构成分析', fontsize=20, fontweight='bold', pad=20)
    plt.tight_layout()
    save_chart(fig, f'{output_prefix}_费用构成.png')

    rates = [category_data[cat]['费率'] for cat in categories]
    bp_rates = [category_data[cat]['BP比'] for cat in categories]
    yoy_rates = [category_data[cat]['同比'] for cat in categories]

    fig, ax1 = plt.subplots(figsize=(20, 10))
    x = np.arange(len(cat_labels))

    colors_bar = [CATEGORY_COLORS[cat] for cat in categories]
    bars = ax1.bar(x, rates, 0.5, label='费用率实际', color=colors_bar, alpha=0.9, edgecolor='black', linewidth=0.5)
    ax1.set_xlabel('品类', fontsize=16, fontweight='bold')
    ax1.set_ylabel('费用率', fontsize=16, color=COLOR_BLUE, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=COLOR_BLUE, labelsize=14)
    ax1.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=1))
    ax1.set_xticks(x)
    ax1.set_xticklabels(cat_labels, fontsize=14)

    for bar, rate in zip(bars, rates):
        ax1.text(bar.get_x() + bar.get_width()/2, rate + 0.005, f'{rate*100:.1f}%',
                ha='center', va='bottom', fontsize=11, fontweight='bold')

    legend_patches = [plt.Rectangle((0,0),1,1, color=CATEGORY_COLORS[cat], alpha=0.9) for cat in categories]
    ax1.legend(legend_patches, cat_labels, loc='upper right', fontsize=11, framealpha=0.95, ncol=5)

    ax2 = ax1.twinx()
    ax2.plot(x, bp_rates, 'o-', color=COLOR_ORANGE, linewidth=2.5, markersize=10, label='BP比变化', zorder=5)
    ax2.plot(x, yoy_rates, 's--', color=COLOR_GREEN, linewidth=2.5, markersize=10, label='同比变化', zorder=5)
    ax2.axhline(y=0, color='green', linestyle='--', linewidth=1.5, alpha=0.7)
    ax2.set_ylabel('变化率（差值）', fontsize=16, color=COLOR_ORANGE, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=COLOR_ORANGE, labelsize=14)
    ax2.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=2))

    for i, (v1, v2) in enumerate(zip(bp_rates, yoy_rates)):
        offset = 0.005 if v1 >= 0 else -0.005
        ax2.text(i, v1 + offset, f'{v1*100:.1f}%', ha='center', va='bottom', fontsize=10, color=COLOR_ORANGE, fontweight='bold')
        offset = 0.005 if v2 >= 0 else -0.005
        ax2.text(i, v2 + offset, f'{v2*100:.1f}%', ha='center', va='bottom', fontsize=10, color=COLOR_GREEN)

    ax2_lines = ax2.get_legend_handles_labels()
    ref_line = plt.Line2D([0], [0], color='green', linestyle='--', linewidth=1.5, alpha=0.7)
    handles2 = ax2_lines[0] + [ref_line]
    labels2 = ax2_lines[1] + ['0%基准线']
    ax2.legend(handles2, labels2, loc='upper left', fontsize=11, framealpha=0.95)

    ax1.grid(axis='y', color=COLOR_GRAY, linestyle='--', alpha=0.5)
    plt.title(f'{title_prefix} - 费用率对比分析', fontsize=20, fontweight='bold', pad=20)
    plt.tight_layout()
    save_chart(fig, f'{output_prefix}_费用率对比.png')

if __name__ == '__main__':
    base_path = r'd:\代码\业绩分析可视化_26年2月\json'
    print("Processing Sheet3...")
    data3 = load_json(os.path.join(base_path, 'sheet3.json'))
    draw_sheet3_charts(data3['data'], data3['title'], 'sheet3')
    print("Sheet3 charts generated successfully!")
