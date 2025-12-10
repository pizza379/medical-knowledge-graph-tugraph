#!/usr/bin/env python3

# coding: utf-8

import pandas as pd

df = pd.read_csv('./disease3.csv', encoding='utf-8')


node_name_list = ["Alias", "Part", "Age", "Infection", "Insurance","Department","Checklist","Symptom","Complication","Treatment","Drug","Period","Rate","Money"]
edge_name_list = ["HAS_ALIAS", "IS_OF_PART", "IS_OF_AGE", "IS_INFECTIOUS", "In_Insurance","IS_OF_Department","HAS_Checklist","HAS_SYMPTOM","HAS_Complication","HAS_Treatment","HAS_Drug","Cure_Period","Cure_Rate","NEED_Money"]
node_filenames = []
for k in range(0,13):
    node_filenames.append(node_name_list[k]+".csv")

edge_filenames = []
for k in range(0,13):
    edge_filenames.append(edge_name_list[k]+".csv")

for i in range(0,28):
    cell_value = df.iloc[i, 0]
    #node_1 = Node("Disease", name = cell_value)
    #graph.create(node_1)
    log = open("Disease.csv",mode="a",encoding="utf-8")
    print(df.iloc[i, 0], file = log)

    for k in range(1,14):
        cell_value = str(df.iloc[i, k])
        new_value=cell_value.split()
        for j in range(len(new_value)):
            #node_2 = Node(node_name_list[k-1], name = new_value[j])
            #graph.merge(node_2,node_name_list[k-1],'name')
            log1 = open(node_filenames[k-1],mode="a",encoding="utf-8")
            print(new_value[j], file = log1)

            #node_1_call_node_2 = Relationship(node_1,edge_name_list[k-1],node_2)
            #graph.merge(node_1_call_node_2)
            log2 = open(edge_filenames[k-1],mode="a",encoding="utf-8")
            print(df.iloc[i, 0],new_value[j], file = log2)






