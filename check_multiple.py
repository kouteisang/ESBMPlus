# @Author : Cheng Huang
# @Time   : 14:16 2022/12/12
# @File   : check_multiple.py


myset = set()

with open("/Users/huangcheng/Documents/esbm_data_generate/data/origin_dbpedia_data/images_en.ttl", "r") as f:
    for line in f:
        if line not in myset:
            myset.add(line)
        else:
            print(line)