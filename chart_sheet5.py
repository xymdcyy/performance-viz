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
    '合计': '#2E75B6',
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

def draw_sheet5_charts(data, title_prefix, output_prefix):
    categories = ['合计', '智屏', '空调', '冰洗']
    months = ['1-2月', '3月', '4月', '5月', '6月', 'H1']
    month_keys = ['1-2月_实际', '3月_预测', '4月_预测', '5月_预测', '6月_预测', 'H1累计']

    data_dict = {}
    for cat in categories:
        data_dict[cat] = {'收入': [], '毛利率': [], '利润': []}
        for d in data:
            if d['品类'] == cat:
                if d['类型'] == '收入':
                    for m in month_keys:
                        data_dict[cat]['收入'].append(d.get(m, 0))
                elif d['类型'] == '毛利率':
                    for m in month_keys:
                        data_dict[cat]['毛利率'].append(d.get(m, 0))
                elif d['类型'] == '利润':
                    for m in month_keys:
                        data_dict[cat]['利润'].append(d.get(m, 0))

    fig, axes = plt.subplots(2, 2, figsize=(24, 16))
    axes = axes.flatten()

    for idx, cat in enumerate(categories):
        ax = axes[idx]
        x = np.arange(len(months))
        width = 0.3

        income = data_dict[cat]['收入']
        margin = data_dict[cat]['毛利率']
        profit = data_dict[cat]['利润']

        bars1 = ax.bar(x - width, income, width, label='收入', color=COLOR_BLUE, alpha=0.9)
        bars2 = ax.bar(x, profit, width, label='利润', color=COLOR_GREEN, alpha=0.9)

        ax2 = ax.twinx()
        ax2.plot(x, margin, 'o-', color=COLOR_ORANGE, linewidth=2.5, markersize=10, label='毛利率', zorder=5)

        for bar in bars1:
            h = bar.get_height()
            if h > 0:
                ax.text(bar.get_x() + bar.get_width()/2, h + 50, f'{h/1000:.1f}k',
                       ha='center', va='bottom', fontsize=8, fontweight='bold')

        for bar in bars2:
            h = bar.get_height()
            if h != 0:
                offset = 50 if h >= 0 else -50
                ax.text(bar.get_x() + bar.get_width()/2, h + offset, f'{h:.0f}',
                       ha='center', va='bottom' if h >= 0 else 'top', fontsize=7, fontweight='bold', color=COLOR_GREEN)

        for i, m in enumerate(margin):
            if m is not None and m != 0:
                offset = 0.005 if m > 0 else -0.005
                ax2.text(i, m + offset, f'{m*100:.1f}%', ha='center', va='bottom', fontsize=9, color=COLOR_ORANGE, fontweight='bold')

        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

        ax.set_xlabel('月份', fontsize=12, fontweight='bold')
        ax.set_ylabel('金额（万元）', fontsize=12, color=COLOR_BLUE, fontweight='bold')
        ax2.set_ylabel('毛利率', fontsize=12, color=COLOR_ORANGE, fontweight='bold')
        ax.tick_params(axis='y', labelcolor=COLOR_BLUE, labelsize=10)
        ax2.tick_params(axis='y', labelcolor=COLOR_ORANGE, labelsize=10)
        ax2.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=1))

        ax.set_xticks(x)
        ax.set_xticklabels(months, fontsize=11)

        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)

        ax.grid(axis='y', color=COLOR_GRAY, linestyle='--', alpha=0.5)
        ax.set_title(f'{cat}', fontsize=14, fontweight='bold', color=CATEGORY_COLORS.get(cat, COLOR_BLUE))

    plt.suptitle(f'{title_prefix} - H1月度预测', fontsize=18, fontweight='bold', y=1.02)
    plt.tight_layout()
    save_chart(fig, f'{output_prefix}_H1月度预测.png')

if __name__ == '__main__':
    base_path = r'd:\代码\业绩分析可视化_26年2月\json'
    print("Processing Sheet5...")
    data5 = load_json(os.path.join(base_path, 'sheet5.json'))
    draw_sheet5_charts(data5['data'], data5['title'], 'sheet5')
    print("Sheet5 charts generated successfully!")
