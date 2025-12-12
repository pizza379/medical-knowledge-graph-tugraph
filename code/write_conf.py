#!/usr/bin/env python3
# coding: utf-8
import pandas as pd

# 打开配置文件写入
with open('example.json', 'w', encoding='utf-8') as file:
    file.write('Hello, world!\n')
    file.write('[\n')  # 配置文件以数组开头
    
    # 1. 定义 Disease 节点（核心节点）
    file.write('{"label":"Disease","type":"VERTEX","properties":\n')
    file.write('[{"name":"name","type":"STRING","optional":false,"unique":true,"index":true}],"primary":"name"},\n')
    
    # 2. 定义13种关联节点和对应的边
    node_name_list = ["Alias", "Part", "Age", "Infection", "Insurance","Department","Checklist","Symptom","Complication","Treatment","Drug","Period","Rate","Money"]
    edge_name_list = ["HAS_ALIAS", "IS_OF_PART", "IS_OF_AGE", "IS_INFECTIOUS", "In_Insurance","IS_OF_Department","HAS_Checklist","HAS_SYMPTOM","HAS_Complication","HAS_Treatment","HAS_Drug","Cure_Period","Cure_Rate","NEED_Money"]
    
    for k in range(1,14):
        # 定义关联节点（如 Alias、Part）
        node_label = node_name_list[k-1]
        file.write(f'{{"label":"{node_label}","type":"VERTEX","properties":}}\n')
        file.write('[{"name":"name","type":"STRING","optional":false,"unique":true,"index":true}],"primary":"name"},\n')
        
        # 定义边（如 Disease -> HAS_ALIAS -> Alias）
        edge_label = edge_name_list[k-1]
        file.write(f'{{"label":"{edge_label}","type":"EDGE","properties":[],"constraints":[["Disease","{node_label}"]]}},\n')
    
    # 移除最后一个逗号（JSON语法要求），此处简化处理（手动删除或代码优化均可）
    file.write(']\n')

print("TuGraph配置文件 example.json 生成完成！")