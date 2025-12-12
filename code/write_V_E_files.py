#!/usr/bin/env python3
# coding: utf-8
import pandas as pd

# 读取医疗数据集
df = pd.read_csv('./disease3.csv', encoding='utf-8')

# 节点类型列表（13种关联节点）
node_name_list = ["Alias", "Part", "Age", "Infection", "Insurance","Department","Checklist","Symptom","Complication","Treatment","Drug","Period","Rate","Money"]
# 边类型列表（13种关联关系）
edge_name_list = ["HAS_ALIAS", "IS_OF_PART", "IS_OF_AGE", "IS_INFECTIOUS", "In_Insurance","IS_OF_Department","HAS_Checklist","HAS_SYMPTOM","HAS_Complication","HAS_Treatment","HAS_Drug","Cure_Period","Cure_Rate","NEED_Money"]

# 生成节点文件名称（如 Alias.csv、Part.csv）
node_filenames = [node_name_list[k]+".csv" for k in range(0,13)]
# 生成边文件名称（如 HAS_ALIAS.csv、IS_OF_PART.csv）
edge_filenames = [edge_name_list[k]+".csv" for k in range(0,13)]

# 遍历 disease3.csv 中每一行（每个疾病）
for i in range(0, len(df)):
    # 写入疾病节点（Disease.csv）
    disease_name = df.iloc[i, 0]
    with open("Disease.csv", mode="a", encoding="utf-8") as f:
        f.write(f"{disease_name}\n")
    
    # 遍历每个关联维度（从第1列到第13列）
    for k in range(1,14):
        cell_value = str(df.iloc[i, k]).strip()
        # 跳过空值（如部分疾病无别名）
        if cell_value == "nan" or cell_value == "":
            continue
        # 按空格拆分多值（如一个疾病有多个症状）
        related_values = cell_value.split()
        for val in related_values:
            # 写入关联节点（如 Alias.csv 写入具体别名）
            with open(node_filenames[k-1], mode="a", encoding="utf-8") as f_node:
                f_node.write(f"{val}\n")
            # 写入边（如 HAS_ALIAS.csv 写入 疾病名-别名 的关联）
            with open(edge_filenames[k-1], mode="a", encoding="utf-8") as f_edge:
                f_edge.write(f"{disease_name},{val}\n")

print("节点和边CSV文件生成完成！")