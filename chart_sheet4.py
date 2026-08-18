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

def draw_sheet4_charts(data, title_prefix, output_prefix):
    product_lines = ['合计', '智屏', '空调', '白电']
    periods = ['当期', '同期']

    fig, axes = plt.subplots(1, 3, figsize=(30, 10))

    for idx, channel in enumerate(['汇总', '连锁', '区域连锁']):
        ax = axes[idx]
        period_data = {p: [] for p in periods}

        for pl in product_lines:
            for period in periods:
                for d in data:
                    if d['产品线'] == pl and d['渠道'] == channel and d['项目'] == period:
                        period_data[period].append(d.get('毛收入', 0))
                        break

        x = np.arange(len(product_lines))
        width = 0.35

        ax.bar(x - width/2, period_data['当期'], width, label='当期', color=COLOR_BLUE, alpha=0.9)
        ax.bar(x + width/2, period_data['同期'], width, label='同期', color=COLOR_ORANGE, alpha=0.9)

        ax.set_xlabel('产品线', fontsize=14, fontweight='bold')
        ax.set_ylabel('毛收入（万元）', fontsize=14)
        ax.set_title(f'{channel}渠道', fontsize=16, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(product_lines, fontsize=12)
        ax.legend(loc='upper right', fontsize=11)
        ax.grid(axis='y', color=COLOR_GRAY, linestyle='--', alpha=0.5)

    plt.suptitle(f'{title_prefix} - 当期vs同期收入对比', fontsize=20, fontweight='bold', y=1.02)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, f'{output_prefix}_当期同期对比.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Saved: {output_prefix}_当期同期对比.png")

    fig, axes = plt.subplots(1, 3, figsize=(30, 10))
    fee_keys = ['折扣', '价格保护', '联合促销与推广', '临时激励', '销售返利']

    for idx, channel in enumerate(['汇总', '连锁', '区域连锁']):
        ax = axes[idx]
        fee_data = {item: [] for item in fee_keys}

        for pl in product_lines:
            for d in data:
                if d['产品线'] == pl and d['渠道'] == channel and d['项目'] == '当期':
                    for item in fee_keys:
                        fee_data[item].append(d.get(item, 0))
                    break

        x = np.arange(len(product_lines))
        bottom = np.zeros(len(product_lines))
        colors = [COLOR_BLUE, COLOR_LIGHT_BLUE, COLOR_ORANGE, '#FFD966', '#A9D08E']

        for i, (item, color) in enumerate(zip(fee_keys, colors)):
            ax.bar(x, fee_data[item], 0.6, bottom=bottom, label=item, color=color, alpha=0.9)
            bottom += np.array(fee_data[item])

        ax.set_xlabel('产品线', fontsize=14, fontweight='bold')
        ax.set_ylabel('费用金额（万元）', fontsize=14)
        ax.set_title(f'{channel}渠道', fontsize=16, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(product_lines, fontsize=12)
        ax.legend(loc='upper right', fontsize=9)
        ax.grid(axis='y', color=COLOR_GRAY, linestyle='--', alpha=0.5)

    plt.suptitle(f'{title_prefix} - 费用结构分析', fontsize=20, fontweight='bold', y=1.02)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, f'{output_prefix}_费用结构.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Saved: {output_prefix}_费用结构.png")

    fig, ax = plt.subplots(figsize=(20, 10))
    yoy_changes = []

    for pl in product_lines:
        for d in data:
            if d['产品线'] == pl and d['渠道'] == '汇总' and d['项目'] == '同期比':
                yoy_changes.append(d.get('毛收入', 0))
                break

    x = np.arange(len(product_lines))
    colors = [COLOR_GREEN if v >= 0 else COLOR_RED for v in yoy_changes]

    bars = ax.bar(x, yoy_changes, 0.5, color=colors, alpha=0.9)

    for bar in bars:
        h = bar.get_height()
        offset = 0.1 if h >= 0 else -0.1
        ax.text(bar.get_x() + bar.get_width()/2, h + offset, f'{h:.0f}',
               ha='center', va='bottom' if h >= 0 else 'top', fontsize=12, fontweight='bold')

    ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax.set_xlabel('产品线', fontsize=16, fontweight='bold')
    ax.set_ylabel('同期比变化（万元）', fontsize=16)
    ax.set_xticks(x)
    ax.set_xticklabels(product_lines, fontsize=14)
    ax.grid(axis='y', color=COLOR_GRAY, linestyle='--', alpha=0.5)
    plt.title(f'{title_prefix} - 同期比变化分析', fontsize=20, fontweight='bold', pad=20)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, f'{output_prefix}_同期比变化.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Saved: {output_prefix}_同期比变化.png")

if __name__ == '__main__':
    base_path = r'd:\代码\业绩分析可视化_26年2月\json'
    print("Processing Sheet4...")
    data4 = load_json(os.path.join(base_path, 'sheet4.json'))
    draw_sheet4_charts(data4['data'], data4['title'], 'sheet4')
    print("Sheet4 charts generated successfully!")
