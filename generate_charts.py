import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
import json
import math
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

def format_pct(val):
    return f'{val*100:.1f}%' if val is not None else 'N/A'

def format_wan(val):
    return f'{val:.0f}万'

# ============= Sheet1 & Sheet2: KA及智屏渠道业绩分析 =============
def draw_sheet1_charts(data, title_prefix, output_prefix):
    categories = ['KA合计', '智屏-TCL', '空调-TCL', '冰洗-TCL', 'CIOT-TCL']
    channels = ['合计', '全国连锁', '区域连锁']

    filtered = [d for d in data if d['品类'] in categories and d['渠道'] in channels]

    labels = [f"{d['品类']}-{d['渠道']}" for d in filtered]
    actual = [d['收入_实际'] for d in filtered]
    bp = [d['收入_BP'] for d in filtered]
    achieve = [d['收入_BP达成率'] for d in filtered]
    yoy = [d['收入_同比'] for d in filtered]

    fig, ax1 = plt.subplots(figsize=(30, 12))
    x = np.arange(len(labels))
    width = 0.35

    bars1 = ax1.bar(x - width/2, actual, width, label='实际', color=COLOR_BLUE, alpha=0.9)
    bars2 = ax1.bar(x + width/2, bp, width, label='BP', color=COLOR_LIGHT_BLUE, alpha=0.9)
    ax1.set_xlabel('品类-渠道', fontsize=16, fontweight='bold')
    ax1.set_ylabel('收入（万元）', fontsize=16, color=COLOR_BLUE, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=COLOR_BLUE, labelsize=14)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=45, ha='right', fontsize=12)

    for bar in bars1:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 50, f'{h:.0f}',
                 ha='center', va='bottom', fontsize=10, fontweight='bold')

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

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ref_line = plt.Line2D([0], [0], color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    handles = lines1 + lines2 + [ref_line]
    labels_all = labels1 + labels2 + ['100%基准线']
    ax1.legend(handles, labels_all, loc='upper right', fontsize=12, framealpha=0.95)
    ax1.grid(axis='y', color=COLOR_GRAY, linestyle='--', alpha=0.5)

    plt.title(f'{title_prefix} - 收入与BP达成分析', fontsize=20, fontweight='bold', pad=20)
    plt.tight_layout()
    save_chart(fig, f'{output_prefix}_收入BP达成.png')

    # Chart 2: 销量与ASP
    vol_actual = [d['销量_实际'] for d in filtered]
    vol_bp = [d['销量_BP达成率'] for d in filtered]

    fig, ax1 = plt.subplots(figsize=(30, 12))
    bars1 = ax1.bar(x - width/2, vol_actual, width, label='销量实际', color=COLOR_BLUE, alpha=0.9)
    ax1.set_xlabel('品类-渠道', fontsize=16, fontweight='bold')
    ax1.set_ylabel('销量（万台）', fontsize=16, color=COLOR_BLUE, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=COLOR_BLUE, labelsize=14)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=45, ha='right', fontsize=12)

    for bar in bars1:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 0.02, f'{h:.1f}',
                 ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax2 = ax1.twinx()
    ax2.plot(x, vol_bp, 'o-', color=COLOR_ORANGE, linewidth=2.5, markersize=10, label='BP达成率', zorder=5)
    ax2.axhline(y=1, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    ax2.set_ylabel('BP达成率', fontsize=16, color=COLOR_ORANGE, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=COLOR_ORANGE, labelsize=14)
    ax2.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=0))

    for i, v in enumerate(vol_bp):
        offset = 0.03 if v >= 0 else -0.03
        ax2.text(i, v + offset, f'{v*100:.0f}%', ha='center', va='bottom', fontsize=10, color=COLOR_ORANGE, fontweight='bold')

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ref_line = plt.Line2D([0], [0], color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    handles = lines1 + lines2 + [ref_line]
    labels_all = labels1 + labels2 + ['100%基准线']
    ax1.legend(handles, labels_all, loc='upper right', fontsize=12, framealpha=0.95)
    ax1.grid(axis='y', color=COLOR_GRAY, linestyle='--', alpha=0.5)

    plt.title(f'{title_prefix} - 销量与BP达成分析', fontsize=20, fontweight='bold', pad=20)
    plt.tight_layout()
    save_chart(fig, f'{output_prefix}_销量BP达成.png')

    # Chart 3: 毛利率与净利
    profit_actual = [d['端到端净利_实际'] for d in filtered]
    profit_bp = [d['端到端净利_BP达成率'] for d in filtered]
    margin_actual = [d['端到端毛利率_实际'] for d in filtered]
    margin_bp = [d['端到端毛利率_BP达成率'] for d in filtered]

    fig, ax1 = plt.subplots(figsize=(30, 12))
    bars1 = ax1.bar(x - width/2, margin_actual, width, label='毛利率实际', color=COLOR_BLUE, alpha=0.9)
    ax1.set_xlabel('品类-渠道', fontsize=16, fontweight='bold')
    ax1.set_ylabel('毛利率', fontsize=16, color=COLOR_BLUE, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=COLOR_BLUE, labelsize=14)
    ax1.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=1))
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=45, ha='right', fontsize=12)

    for bar in bars1:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 0.005, f'{h*100:.1f}%',
                 ha='center', va='bottom', fontsize=10, fontweight='bold')

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

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    zero_line = plt.Line2D([0], [0], color='green', linestyle='--', linewidth=1.5, alpha=0.7)
    handles = lines1 + lines2 + [zero_line]
    labels_all = labels1 + labels2 + ['0%基准线']
    ax1.legend(handles, labels_all, loc='upper right', fontsize=12, framealpha=0.95)
    ax1.grid(axis='y', color=COLOR_GRAY, linestyle='--', alpha=0.5)

    plt.title(f'{title_prefix} - 毛利率与净利BP达成分析', fontsize=20, fontweight='bold', pad=20)
    plt.tight_layout()
    save_chart(fig, f'{output_prefix}_毛利率净利.png')

# ============= Sheet3: 费用项目分析 =============
def draw_sheet3_charts(data, title_prefix, output_prefix):
    fee_items = [d for d in data if d['类型'] == '金额']
    rate_items = [d for d in data if d['类型'] == '费率']

    channels = ['合计', '智屏_连锁渠道', '智屏_区域连锁', '空调_连锁渠道', '空调_区域连锁',
                '冰洗_连锁渠道', '冰洗_区域连锁', 'CIOT_连锁渠道', 'CIOT_区域连锁']
    channel_labels = ['汇总', '智屏-连锁', '智屏-区域连锁', '空调-连锁', '空调-区域连锁',
                      '冰洗-连锁', '冰洗-区域连锁', 'CIOT-连锁', 'CIOT-区域连锁']

    fixed_fees = []
    variable_fees = []
    for ch in channels:
        fixed_key = f'{ch}_实际'
        var_key = f'{ch}_实际'
        for item in fee_items:
            if item['费用项目'] == '固定性费用':
                fixed_fees.append(item.get(fixed_key, 0))
            elif item['费用项目'] == '变动性费用':
                variable_fees.append(item.get(var_key, 0))

    fig, ax = plt.subplots(figsize=(30, 12))
    x = np.arange(len(channel_labels))
    width = 0.6

    bars1 = ax.bar(x, fixed_fees, width, label='固定费用', color=COLOR_BLUE, alpha=0.9)
    bars2 = ax.bar(x, variable_fees, width, bottom=fixed_fees, label='变动费用', color=COLOR_LIGHT_BLUE, alpha=0.9)

    total_fees = [f + v for f, v in zip(fixed_fees, variable_fees)]
    for i, (bar, total) in enumerate(zip(bars1, total_fees)):
        ax.text(bar.get_x() + bar.get_width()/2, total + 30, f'{total:.0f}',
               ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_xlabel('渠道', fontsize=16, fontweight='bold')
    ax.set_ylabel('费用金额（万元）', fontsize=16, color=COLOR_BLUE, fontweight='bold')
    ax.tick_params(axis='y', labelcolor=COLOR_BLUE, labelsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(channel_labels, rotation=45, ha='right', fontsize=12)
    ax.legend(loc='upper right', fontsize=12, framealpha=0.95)
    ax.grid(axis='y', color=COLOR_GRAY, linestyle='--', alpha=0.5)

    plt.title(f'{title_prefix} - 费用构成分析', fontsize=20, fontweight='bold', pad=20)
    plt.tight_layout()
    save_chart(fig, f'{output_prefix}_费用构成.png')

    # Chart 2: 费用率对比
    fee_rate_item = [d for d in rate_items if d['费用项目'] == '汇总费用费率'][0]
    x_labels = []
    actual_rates = []
    bp_rates = []
    yoy_rates = []

    for ch in channels:
        x_labels.append(ch.replace('_', '\n'))
        actual_rates.append(fee_rate_item.get(f'{ch}_实际', 0))
        bp_rates.append(fee_rate_item.get(f'{ch}_BP比', 0))
        yoy_rates.append(fee_rate_item.get(f'{ch}_同比', 0))

    fig, ax1 = plt.subplots(figsize=(30, 12))
    x = np.arange(len(x_labels))

    bars = ax1.bar(x, actual_rates, 0.5, label='费用率实际', color=COLOR_BLUE, alpha=0.9)
    ax1.set_xlabel('渠道', fontsize=16, fontweight='bold')
    ax1.set_ylabel('费用率', fontsize=16, color=COLOR_BLUE, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=COLOR_BLUE, labelsize=14)
    ax1.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=1))
    ax1.set_xticks(x)
    ax1.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=11)

    for bar in bars:
        h = bar.get_height()
        offset = 0.003 if h >= 0 else -0.003
        ax1.text(bar.get_x() + bar.get_width()/2, h + offset, f'{h*100:.2f}%',
                ha='center', va='bottom' if h >= 0 else 'top', fontsize=10, fontweight='bold')

    ax2 = ax1.twinx()
    ax2.plot(x, bp_rates, 'o-', color=COLOR_ORANGE, linewidth=2.5, markersize=10, label='BP比变化', zorder=5)
    ax2.plot(x, yoy_rates, 's--', color=COLOR_GREEN, linewidth=2.5, markersize=10, label='同比变化', zorder=5)
    ax2.axhline(y=0, color='green', linestyle='--', linewidth=1.5, alpha=0.7)
    ax2.set_ylabel('变化率（差值）', fontsize=16, color=COLOR_ORANGE, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=COLOR_ORANGE, labelsize=14)
    ax2.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=2))

    for i, (v1, v2) in enumerate(zip(bp_rates, yoy_rates)):
        offset = 0.005 if v1 >= 0 else -0.005
        ax2.text(i, v1 + offset, f'{v1*100:.2f}%', ha='center', va='bottom', fontsize=9, color=COLOR_ORANGE, fontweight='bold')
        offset = 0.005 if v2 >= 0 else -0.005
        ax2.text(i, v2 + offset, f'{v2*100:.2f}%', ha='center', va='bottom', fontsize=9, color=COLOR_GREEN)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    zero_line = plt.Line2D([0], [0], color='green', linestyle='--', linewidth=1.5, alpha=0.7)
    handles = lines1 + lines2 + [zero_line]
    labels_all = labels1 + labels2 + ['0%基准线']
    ax1.legend(handles, labels_all, loc='upper right', fontsize=12, framealpha=0.95)
    ax1.grid(axis='y', color=COLOR_GRAY, linestyle='--', alpha=0.5)

    plt.title(f'{title_prefix} - 费用率对比分析', fontsize=20, fontweight='bold', pad=20)
    plt.tight_layout()
    save_chart(fig, f'{output_prefix}_费用率对比.png')

# ============= Sheet4: 产品线费用分解 =============
def draw_sheet4_charts(data, title_prefix, output_prefix):
    product_lines = ['合计', '智屏', '空调', '白电']
    periods = ['当期', '同期']

    fig, axes = plt.subplots(1, 3, figsize=(30, 10))

    for idx, channel in enumerate(['汇总', '连锁', '区域连锁']):
        ax = axes[idx]
        period_data = {p: [] for p in periods}

        for pl in product_lines:
            for period in periods:
                key = f"{pl}_{channel}_{period}"
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

    # Chart 2: 费用结构
    fig, axes = plt.subplots(1, 3, figsize=(30, 10))
    fee_items = ['折扣', '价格保护', '联合促销与推广', '临时激励', '销售返利']
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

    # Chart 3: 同期比变化
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

# ============= Sheet5: H1月度预测 =============
def draw_sheet5_charts(data, title_prefix, output_prefix):
    categories = ['合计', '智屏', '空调', '冰洗', 'CIOT']
    months = ['1-2月', '3月', '4月', '5月', '6月', 'H1累计']

    income_data = {}
    margin_data = {}
    profit_data = {}

    for cat in categories:
        income_data[cat] = []
        margin_data[cat] = []
        profit_data[cat] = []

        for d in data:
            if d['品类'] == cat:
                if d['类型'] == '收入':
                    for m in ['1-2月_实际', '3月_预测', '4月_预测', '5月_预测', '6月_预测', 'H1累计']:
                        income_data[cat].append(d.get(m, 0))
                elif d['类型'] == '毛利率':
                    for m in ['1-2月_实际', '3月_预测', '4月_预测', '5月_预测', '6月_预测', 'H1累计']:
                        margin_data[cat].append(d.get(m, 0))
                elif d['类型'] == '利润':
                    for m in ['1-2月_实际', '3月_预测', '4月_预测', '5月_预测', '6月_预测', 'H1累计']:
                        profit_data[cat].append(d.get(m, 0))

    # Chart 1: 收入预测
    fig, ax = plt.subplots(figsize=(20, 10))
    x = np.arange(len(months))
    colors = [COLOR_BLUE, COLOR_ORANGE, COLOR_GREEN, '#9E480E', '#7B7B7B']

    for i, cat in enumerate(categories):
        ax.plot(x, income_data[cat], 'o-', color=colors[i], linewidth=2.5, markersize=10, label=cat, zorder=5)

    ax.set_xlabel('月份', fontsize=16, fontweight='bold')
    ax.set_ylabel('收入（万元）', fontsize=16)
    ax.set_xticks(x)
    ax.set_xticklabels(months, fontsize=14)
    ax.legend(loc='upper left', fontsize=12)
    ax.grid(color=COLOR_GRAY, linestyle='--', alpha=0.5)

    plt.title(f'{title_prefix} - 收入预测趋势', fontsize=20, fontweight='bold', pad=20)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, f'{output_prefix}_收入预测.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Saved: {output_prefix}_收入预测.png")

    # Chart 2: 毛利率趋势
    fig, ax = plt.subplots(figsize=(20, 10))

    for i, cat in enumerate(categories):
        ax.plot(x, margin_data[cat], 'o-', color=colors[i], linewidth=2.5, markersize=10, label=cat, zorder=5)

    ax.set_xlabel('月份', fontsize=16, fontweight='bold')
    ax.set_ylabel('毛利率', fontsize=16)
    ax.tick_params(axis='y', labelsize=14)
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=1))
    ax.set_xticks(x)
    ax.set_xticklabels(months, fontsize=14)
    ax.legend(loc='upper left', fontsize=12)
    ax.grid(color=COLOR_GRAY, linestyle='--', alpha=0.5)

    plt.title(f'{title_prefix} - 毛利率预测趋势', fontsize=20, fontweight='bold', pad=20)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, f'{output_prefix}_毛利率预测.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Saved: {output_prefix}_毛利率预测.png")

    # Chart 3: 利润走势
    fig, ax = plt.subplots(figsize=(20, 10))

    for i, cat in enumerate(categories):
        ax.plot(x, profit_data[cat], 'o-', color=colors[i], linewidth=2.5, markersize=10, label=cat, zorder=5)

    ax.axhline(y=0, color='red', linestyle='--', linewidth=2, alpha=0.7)
    ax.set_xlabel('月份', fontsize=16, fontweight='bold')
    ax.set_ylabel('利润（万元）', fontsize=16)
    ax.set_xticks(x)
    ax.set_xticklabels(months, fontsize=14)
    ax.legend(loc='upper left', fontsize=12)
    ax.grid(color=COLOR_GRAY, linestyle='--', alpha=0.5)

    plt.title(f'{title_prefix} - 利润预测走势', fontsize=20, fontweight='bold', pad=20)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, f'{output_prefix}_利润预测.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Saved: {output_prefix}_利润预测.png")

# ============= Sheet6: 应收账款逾期分析 =============
def draw_sheet6_charts(data, title_prefix, output_prefix):
    filtered = [d for d in data if d['大区'] and d['战区'] and d['渠道'] != '']

    sorted_data = sorted(filtered, key=lambda x: x.get('合计_超期应收', 0), reverse=True)

    labels = [f"{d['大区']}-{d['战区']}-{d['渠道']}" for d in sorted_data if d.get('合计_超期应收', 0) > 0]
    overdue = [d.get('合计_超期应收', 0) for d in sorted_data if d.get('合计_超期应收', 0) > 0]
    rates = [d.get('合计_逾期率', 0) for d in sorted_data if d.get('合计_超期应收', 0) > 0]

    if labels:
        fig, ax = plt.subplots(figsize=(20, 12))
        y = np.arange(len(labels))

        max_rate = max(rates) if rates else 1
        colors = []
        for r in rates:
            if r < 0.01:
                colors.append(COLOR_GREEN)
            elif r < 0.05:
                colors.append(COLOR_ORANGE)
            else:
                colors.append(COLOR_RED)

        bars = ax.barh(y, overdue, color=colors, alpha=0.9)

        for i, (bar, rate) in enumerate(zip(bars, rates)):
            w = bar.get_width()
            ax.text(w + 1, bar.get_y() + bar.get_height()/2, f'{w:.0f}万 ({rate*100:.1f}%)',
                   ha='left', va='center', fontsize=10, fontweight='bold')

        ax.set_yticks(y)
        ax.set_yticklabels(labels, fontsize=11)
        ax.set_xlabel('逾期金额（万元）', fontsize=16, fontweight='bold')
        ax.set_title(f'{title_prefix} - 逾期金额排名', fontsize=20, fontweight='bold', pad=20)
        ax.grid(axis='x', color=COLOR_GRAY, linestyle='--', alpha=0.5)

        plt.tight_layout()
        fig.savefig(os.path.join(OUTPUT_DIR, f'{output_prefix}_逾期金额排名.png'), dpi=150, bbox_inches='tight', facecolor='white')
        plt.close(fig)
        print(f"Saved: {output_prefix}_逾期金额排名.png")
    else:
        print(f"Warning: No overdue data for {output_prefix}")

    # Chart 2: 逾期率对比
    all_sorted = sorted(filtered, key=lambda x: x.get('合计_逾期率', 0), reverse=True)
    labels2 = [f"{d['大区']}-{d['战区']}" for d in all_sorted]
    rates2 = [d.get('合计_逾期率', 0) for d in all_sorted]
    amounts2 = [d.get('合计_超期应收', 0) for d in all_sorted]

    fig, ax1 = plt.subplots(figsize=(24, 10))
    x = np.arange(len(labels2))
    width = 0.5

    bars = ax1.bar(x, rates2, width, label='逾期率', color=COLOR_BLUE, alpha=0.9)
    ax1.set_xlabel('战区', fontsize=16, fontweight='bold')
    ax1.set_ylabel('逾期率', fontsize=16, color=COLOR_BLUE, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=COLOR_BLUE, labelsize=14)
    ax1.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=1))
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels2, rotation=60, ha='right', fontsize=10)

    for bar in bars:
        h = bar.get_height()
        if h > 0:
            offset = 0.005 if h >= 0 else -0.005
            ax1.text(bar.get_x() + bar.get_width()/2, h + offset, f'{h*100:.2f}%',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax2 = ax1.twinx()
    ax2.plot(x, amounts2, 'o-', color=COLOR_ORANGE, linewidth=2, markersize=8, label='超期应收', zorder=5)
    ax2.set_ylabel('超期应收金额（万元）', fontsize=16, color=COLOR_ORANGE, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=COLOR_ORANGE, labelsize=14)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    handles = lines1 + lines2
    labels_all = labels1 + labels2
    ax1.legend(handles, labels_all, loc='upper right', fontsize=11)
    ax1.grid(axis='y', color=COLOR_GRAY, linestyle='--', alpha=0.5)

    plt.title(f'{title_prefix} - 各战区逾期率对比', fontsize=20, fontweight='bold', pad=20)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, f'{output_prefix}_逾期率对比.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Saved: {output_prefix}_逾期率对比.png")

# ============= Sheet7: 客户存销和滞销分析 =============
def draw_sheet7_charts(data, title_prefix, output_prefix):
    regions = list(set([d['大区'] for d in data]))
    sorted_regions = sorted(regions)

    suning_ratio = []
    wuxing_ratio = []
    labels = []

    for d in data:
        region = d.get('大区', '')
        zhanqu = d.get('战区', '')
        labels.append(f"{region}-{zhanqu}")
        suning_ratio.append(d.get('存销比_苏宁', 0) or 0)
        wuxing_ratio.append(d.get('存销比_五星', 0) or 0)

    fig, ax = plt.subplots(figsize=(24, 12))
    x = np.arange(len(labels))
    width = 0.35

    bars1 = ax.bar(x - width/2, suning_ratio, width, label='苏宁存销比', color=COLOR_BLUE, alpha=0.9)
    bars2 = ax.bar(x + width/2, wuxing_ratio, width, label='五星存销比', color=COLOR_ORANGE, alpha=0.9)

    for bar in bars1:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.02, f'{h:.1f}',
                   ha='center', va='bottom', fontsize=8, fontweight='bold')
    for bar in bars2:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.02, f'{h:.1f}',
                   ha='center', va='bottom', fontsize=8, fontweight='bold')

    ax.set_xlabel('战区', fontsize=16, fontweight='bold')
    ax.set_ylabel('存销比', fontsize=16)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=60, ha='right', fontsize=9)
    ax.legend(loc='upper right', fontsize=12)
    ax.grid(axis='y', color=COLOR_GRAY, linestyle='--', alpha=0.5)

    plt.title(f'{title_prefix} - 存销比对比', fontsize=20, fontweight='bold', pad=20)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, f'{output_prefix}_存销比对比.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Saved: {output_prefix}_存销比对比.png")

    # Chart 2: 滞销占比
    suning_stale = []
    wuxing_stale = []
    labels2 = []

    for d in data:
        labels2.append(f"{d.get('大区','')}-{d.get('战区','')}")
        suning_stale.append(d.get('滞销_苏宁_滞销占比_金额', 0) or 0)
        wuxing_stale.append(d.get('滞销_五星_滞销占比_金额', 0) or 0)

    fig, ax = plt.subplots(figsize=(24, 12))
    x = np.arange(len(labels2))

    bars1 = ax.bar(x - width/2, suning_stale, width, label='苏宁60+滞销占比', color=COLOR_BLUE, alpha=0.9)
    bars2 = ax.bar(x + width/2, wuxing_stale, width, label='五星90+滞销占比', color=COLOR_ORANGE, alpha=0.9)

    for bar in bars1:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.005, f'{h*100:.1f}%',
                   ha='center', va='bottom', fontsize=8, fontweight='bold')
    for bar in bars2:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.005, f'{h*100:.1f}%',
                   ha='center', va='bottom', fontsize=8, fontweight='bold')

    ax.set_xlabel('战区', fontsize=16, fontweight='bold')
    ax.set_ylabel('滞销占比', fontsize=16)
    ax.tick_params(axis='y', labelsize=14)
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=0))
    ax.set_xticks(x)
    ax.set_xticklabels(labels2, rotation=60, ha='right', fontsize=9)
    ax.legend(loc='upper right', fontsize=12)
    ax.grid(axis='y', color=COLOR_GRAY, linestyle='--', alpha=0.5)

    plt.title(f'{title_prefix} - 滞销占比对比', fontsize=20, fontweight='bold', pad=20)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, f'{output_prefix}_滞销占比对比.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Saved: {output_prefix}_滞销占比对比.png")

# ============= Sheet8: 零售vs库存对比 =============
def draw_sheet8_charts(data, title_prefix, output_prefix):
    labels = [f"{d.get('大区','')}-{d.get('战区','')}" for d in data]
    retail = [d.get('零售', 0) for d in data]
    inventory = [d.get('库存', 0) for d in data]
    ratios = [d.get('存销比', 0) for d in data]

    # Chart 1: 散点图
    fig, ax = plt.subplots(figsize=(16, 12))

    scatter = ax.scatter(retail, inventory, s=[r*100 for r in ratios], alpha=0.6, c=COLOR_BLUE, edgecolors='black')

    for i, label in enumerate(labels):
        if retail[i] > 0 or inventory[i] > 0:
            ax.annotate(label, (retail[i], inventory[i]), fontsize=9, ha='left', va='bottom')

    ax.plot([0, max(retail)], [0, max(retail)], 'g--', linewidth=1.5, alpha=0.5, label='1:1线')
    ax.set_xlabel('零售', fontsize=16, fontweight='bold')
    ax.set_ylabel('库存', fontsize=16, fontweight='bold')
    ax.grid(color=COLOR_GRAY, linestyle='--', alpha=0.5)
    ax.legend(fontsize=12)

    plt.title(f'{title_prefix} - 零售vs库存散点图', fontsize=20, fontweight='bold', pad=20)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, f'{output_prefix}_零售库存散点.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Saved: {output_prefix}_零售库存散点.png")

    # Chart 2: 存销比排名
    sorted_data = sorted(zip(labels, ratios), key=lambda x: x[1], reverse=True)
    sorted_labels = [x[0] for x in sorted_data]
    sorted_ratios = [x[1] for x in sorted_data]

    fig, ax = plt.subplots(figsize=(16, 12))
    y = np.arange(len(sorted_labels))

    colors = [COLOR_RED if r > 1.5 else COLOR_ORANGE if r > 1 else COLOR_GREEN for r in sorted_ratios]

    bars = ax.barh(y, sorted_ratios, color=colors, alpha=0.9)

    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.05, bar.get_y() + bar.get_height()/2, f'{w:.1f}',
               ha='left', va='center', fontsize=11, fontweight='bold')

    ax.set_yticks(y)
    ax.set_yticklabels(sorted_labels, fontsize=11)
    ax.set_xlabel('存销比', fontsize=16, fontweight='bold')
    ax.axvline(x=1, color='green', linestyle='--', linewidth=2, alpha=0.7)
    ax.grid(axis='x', color=COLOR_GRAY, linestyle='--', alpha=0.5)

    plt.title(f'{title_prefix} - 存销比排名', fontsize=20, fontweight='bold', pad=20)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, f'{output_prefix}_存销比排名.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Saved: {output_prefix}_存销比排名.png")

# ============= Sheet9: 库存金额分布 =============
def draw_sheet9_charts(data, title_prefix, output_prefix):
    labels = [f"{d.get('大区','')}-{d.get('战区','')}" for d in data]
    inventory = [d.get('库存金额', 0) for d in data]
    stale = [d.get('滞销库存', 0) for d in data]
    rates = [d.get('逾期率', 0) for d in data]

    # Chart 1: 库存构成
    fig, ax = plt.subplots(figsize=(20, 10))
    x = np.arange(len(labels))
    width = 0.6

    bars1 = ax.bar(x, inventory, width, label='库存金额', color=COLOR_BLUE, alpha=0.9)
    bars2 = ax.bar(x, stale, width, bottom=inventory, label='滞销库存', color=COLOR_RED, alpha=0.9)

    for i, (inv, st, rate) in enumerate(zip(inventory, stale, rates)):
        total = inv + st
        ax.text(i, total + 1, f'{total:.0f}万', ha='center', va='bottom', fontsize=10, fontweight='bold')
        if rate > 0:
            ax.text(i, inv/2, f'{rate*100:.0f}%', ha='center', va='center', fontsize=10, fontweight='bold', color='white')

    ax.set_xlabel('战区', fontsize=16, fontweight='bold')
    ax.set_ylabel('库存金额（万元）', fontsize=16)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=60, ha='right', fontsize=10)
    ax.legend(loc='upper right', fontsize=12)
    ax.grid(axis='y', color=COLOR_GRAY, linestyle='--', alpha=0.5)

    plt.title(f'{title_prefix} - 库存金额分布', fontsize=20, fontweight='bold', pad=20)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, f'{output_prefix}_库存金额分布.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Saved: {output_prefix}_库存金额分布.png")

    # Chart 2: 逾期率排名
    sorted_data = sorted(zip(labels, rates), key=lambda x: x[1], reverse=True)[:15]
    sorted_labels = [x[0] for x in sorted_data]
    sorted_rates = [x[1] for x in sorted_data]

    fig, ax = plt.subplots(figsize=(16, 10))
    y = np.arange(len(sorted_labels))

    colors = [COLOR_RED if r > 0.5 else COLOR_ORANGE if r > 0.2 else COLOR_GREEN for r in sorted_rates]

    bars = ax.barh(y, sorted_rates, color=colors, alpha=0.9)

    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.01, bar.get_y() + bar.get_height()/2, f'{w*100:.1f}%',
               ha='left', va='center', fontsize=11, fontweight='bold')

    ax.set_yticks(y)
    ax.set_yticklabels(sorted_labels, fontsize=11)
    ax.set_xlabel('逾期率', fontsize=16, fontweight='bold')
    ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=0))
    ax.grid(axis='x', color=COLOR_GRAY, linestyle='--', alpha=0.5)

    plt.title(f'{title_prefix} - 逾期率TOP15排名', fontsize=20, fontweight='bold', pad=20)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, f'{output_prefix}_逾期率排名.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Saved: {output_prefix}_逾期率排名.png")

# ============= Main Execution =============
if __name__ == '__main__':
    base_path = r'd:\代码\业绩分析可视化_26年2月\json'

    # Sheet1
    print("Processing Sheet1...")
    data1 = load_json(os.path.join(base_path, 'sheet1.json'))
    draw_sheet1_charts(data1['data'], data1['title'], 'sheet1')

    # Sheet2
    print("Processing Sheet2...")
    data2 = load_json(os.path.join(base_path, 'sheet2.json'))
    draw_sheet1_charts(data2['data'], data2['title'], 'sheet2')

    # Sheet3
    print("Processing Sheet3...")
    data3 = load_json(os.path.join(base_path, 'sheet3.json'))
    draw_sheet3_charts(data3['data'], data3['title'], 'sheet3')

    # Sheet4
    print("Processing Sheet4...")
    data4 = load_json(os.path.join(base_path, 'sheet4.json'))
    draw_sheet4_charts(data4['data'], data4['title'], 'sheet4')

    # Sheet5
    print("Processing Sheet5...")
    data5 = load_json(os.path.join(base_path, 'sheet5.json'))
    draw_sheet5_charts(data5['data'], data5['title'], 'sheet5')

    # Sheet6
    print("Processing Sheet6...")
    data6 = load_json(os.path.join(base_path, 'sheet6.json'))
    draw_sheet6_charts(data6['data'], data6['title'], 'sheet6')

    # Sheet7
    print("Processing Sheet7...")
    data7 = load_json(os.path.join(base_path, 'sheet7.json'))
    draw_sheet7_charts(data7['data'], data7['title'], 'sheet7')

    # Sheet8
    print("Processing Sheet8...")
    data8 = load_json(os.path.join(base_path, 'sheet8.json'))
    draw_sheet8_charts(data8['data'], data8['title'], 'sheet8')

    # Sheet9
    print("Processing Sheet9...")
    data9 = load_json(os.path.join(base_path, 'sheet9.json'))
    draw_sheet9_charts(data9['data'], data9['title'], 'sheet9')

    print("\n" + "="*50)
    print("All charts generated successfully!")
    print(f"Output directory: {OUTPUT_DIR}")
    print("="*50)
