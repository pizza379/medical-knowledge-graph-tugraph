#!/usr/bin/env python3

# coding: utf-8

import pandas as pd

file=open('example.json', 'w')
file.write('Hello, world!\n')
file.write('[')

df = pd.read_csv('./disease3.csv', encoding='utf-8')

node_name_list = ["Alias", "Part", "Age", "Infection", "Insurance","Department","Checklist","Symptom","Complication","Treatment","Drug","Period","Rate","Money"]
edge_name_list = ["HAS_ALIAS", "IS_OF_PART", "IS_OF_AGE", "IS_INFECTIOUS", "In_Insurance","IS_OF_Department","HAS_Checklist","HAS_SYMPTOM","HAS_Complication","HAS_Treatment","HAS_Drug","Cure_Period","Cure_Rate","NEED_Money"]

file.write('{"label":"Disease","type":"VERTEX","properties":\n')
file.write('[{"name":"name","type":"STRING","optional":false,"unique":true,"index":true}],"primary":"name"},\n')

for k in range(1,14):
    aa='{"label":"'+node_name_list[k-1]+'","type":"VERTEX","properties":\n'
    file.write(aa)
    file.write('[{"name":"name","type":"STRING","optional":false,"unique":true,"index":true}],"primary":"name"},\n')

    bb='{"label":"'+edge_name_list[k-1]+'","type":"EDGE","properties":[],"constraints":[["Disease","'+node_name_list[k-1]+'"]]},\n'
    file.write(bb)

file.write(']\n')



