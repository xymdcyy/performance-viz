import json
import pandas as pd

with open(r"d:\代码\业绩分析可视化_26年2月\sheet8_output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

print("=== 数据结构分析 ===\n")

print(f"数据行数: {len(df)}")
print(f"字段数: {len(df.columns)}")

print("\n=== 字段列表 ===")
for col in df.columns:
    dtype = df[col].dtype
    non_null = df[col].notna().sum()
    sample = df[col].dropna().head(3).tolist()
    print(f"  - {col} ({dtype}): {non_null} 非空, 示例: {sample}")

print("\n=== 字段类型分类 ===")
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
string_cols = df.select_dtypes(include=['object']).columns.tolist()

print(f"数值型字段: {numeric_cols}")
print(f"分类型字段: {string_cols}")

print("\n=== 数据预览 ===")
print(df.head(10).to_string())

print("\n=== 大区分布 ===")
print(df['大区'].value_counts())
