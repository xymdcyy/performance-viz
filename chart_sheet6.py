import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
import json
import os
from matplotlib.ticker import FuncFormatter

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

REGION_COLORS = {
    '华北': '#2E75B6',
    '华东': '#5B9BD5',
    '华南': '#ED7D31',
    '西北': '#A9D18E',
    '西南': '#FFC000',
    '东北': '#9E480E',
    '总部': '#7B7B7B'
}

COLOR_ZHIPING = '#4472C4'
COLOR_KONGDIAO = '#ED7D31'
COLOR_BAIDIAN = '#70AD47'
COLOR_CIOT = '#FFC000'

def save_chart(fig, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f'Saved: {path}')
    plt.close(fig)

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def draw_sheet6_charts(data, title_prefix, output_prefix):
    filtered = [d for d in data if d['大区'] and d['战区'] and d['渠道']]

    sorted_data = sorted(filtered, key=lambda x: (x.get('大区', ''), x.get('战区', ''), x.get('渠道', '')))

    labels = [f"{d['大区']}-{d['战区']}-{d['渠道']}" for d in sorted_data]
    regions = [d.get('大区', '') for d in sorted_data]
    total_recv = [d.get('合计_应收', 0) for d in sorted_data]
    overdue_recv = [d.get('合计_超期应收', 0) for d in sorted_data]
    normal_recv = [t - o for t, o in zip(total_recv, overdue_recv)]

    fig, ax1 = plt.subplots(figsize=(28, 12))
    x = np.arange(len(labels))
    width = 0.5

    bars_normal = []
    bars_overdue = []
    bar_colors = []

    for i, (region, nr, ov) in enumerate(zip(regions, normal_recv, overdue_recv)):
        color = REGION_COLORS.get(region, COLOR_BLUE)
        bar_colors.append(color)

        if nr > 0:
            bar_n = ax1.bar(i, nr, width, color=color, alpha=0.9)
            bars_normal.append(bar_n)
        if ov > 0:
            bar_o = ax1.bar(i, ov, width, bottom=nr, color=COLOR_RED, alpha=0.9)
            bars_overdue.append(bar_o)

    def fmt_val(x, pos):
        if x >= 1000:
            return f'{x/1000:.0f}k'
        elif x >= 1:
            return f'{x:.0f}'
        elif x > 0:
            return f'{x:.1f}'
        return '0'

    ax1.yaxis.set_major_formatter(FuncFormatter(fmt_val))

    for i, (nr, ov) in enumerate(zip(normal_recv, overdue_recv)):
        total = nr + ov
        if total > 0:
            if total >= 1000:
                ax1.text(i, total * 1.1, f'{total/1000:.1f}k', ha='center', va='bottom', fontsize=7, fontweight='bold')
            else:
                ax1.text(i, total * 1.1, f'{total:.0f}', ha='center', va='bottom', fontsize=7, fontweight='bold')

    region_patches = [plt.Rectangle((0,0),1,1, color=REGION_COLORS.get(r, COLOR_BLUE), alpha=0.9) for r in REGION_COLORS.keys()]
    ax1.legend(region_patches, REGION_COLORS.keys(), loc='upper right', fontsize=9, ncol=4, title='大区')

    ax1.set_xlabel('大区-战区-渠道', fontsize=14, fontweight='bold')
    ax1.set_ylabel('应收金额（万元）', fontsize=14, color=COLOR_BLUE, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=COLOR_BLUE, labelsize=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=60, ha='right', fontsize=7)
    ax1.grid(axis='y', color=COLOR_GRAY, linestyle='--', alpha=0.5)
    ax1.set_yscale('log')
    ax1.set_ylim(bottom=0.5)
    plt.title(f'{title_prefix} - 应收账款分布', fontsize=18, fontweight='bold', pad=20)
    plt.tight_layout()
    save_chart(fig, f'{output_prefix}_应收分布.png')

    overdue_data = [d for d in sorted_data if d.get('合计_超期应收', 0) > 0]

    if overdue_data:
        labels2 = [f"{d['大区']}-{d['战区']}-{d['渠道']}" for d in overdue_data]
        zhiping = [d.get('逾期金额_智屏', 0) for d in overdue_data]
        kongdiao = [d.get('逾期金额_空调', 0) for d in overdue_data]
        baidian = [d.get('逾期金额_白电', 0) for d in overdue_data]
        ciot = [d.get('逾期金额_CIOT', 0) for d in overdue_data]

        fig, ax2 = plt.subplots(figsize=(20, 10))
        x2 = np.arange(len(labels2))
        width2 = 0.5

        bars_zp = ax2.bar(x2, zhiping, width2, label='智屏', color=COLOR_ZHIPING, alpha=0.9)
        bars_kd = ax2.bar(x2, kongdiao, width2, bottom=zhiping, label='空调', color=COLOR_KONGDIAO, alpha=0.9)
        bottom_kd = [z + k for z, k in zip(zhiping, kongdiao)]
        bars_bd = ax2.bar(x2, baidian, width2, bottom=bottom_kd, label='白电', color=COLOR_BAIDIAN, alpha=0.9)
        bottom_bd = [z + k + b for z, k, b in zip(zhiping, kongdiao, baidian)]
        bars_ciot = ax2.bar(x2, ciot, width2, bottom=bottom_bd, label='CIOT', color=COLOR_CIOT, alpha=0.9)

        for i, (zp, kd, bd, ct) in enumerate(zip(zhiping, kongdiao, baidian, ciot)):
            total = zp + kd + bd + ct
            if total > 0:
                ax2.text(i, total + 2, f'{total:.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

        ax2.set_xlabel('大区-战区-渠道', fontsize=14, fontweight='bold')
        ax2.set_ylabel('逾期金额（万元）', fontsize=14, color=COLOR_BLUE, fontweight='bold')
        ax2.tick_params(axis='y', labelcolor=COLOR_BLUE, labelsize=12)
        ax2.set_xticks(x2)
        ax2.set_xticklabels(labels2, rotation=45, ha='right', fontsize=9)
        ax2.legend(loc='upper right', fontsize=10)
        ax2.grid(axis='y', color=COLOR_GRAY, linestyle='--', alpha=0.5)
        plt.title(f'{title_prefix} - 逾期金额产品线分布', fontsize=18, fontweight='bold', pad=20)
        plt.tight_layout()
        save_chart(fig, f'{output_prefix}_逾期产品线分布.png')
    else:
        print("Warning: No overdue data")

if __name__ == '__main__':
    base_path = r'd:\代码\业绩分析可视化_26年2月\json'
    print("Processing Sheet6...")
    data6 = load_json(os.path.join(base_path, 'sheet6.json'))
    draw_sheet6_charts(data6['data'], data6['title'], 'sheet6')
    print("Sheet6 charts generated successfully!")
