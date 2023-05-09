# @Author : Cheng Huang
# @Time   : 18:29 2022/10/27
# @File   : first_to_first.py
import os

from utils import get_entity_list, gerente_not_in_entity_list


def get_firstnb_to_firstnb(type="dbpedia"):
    entity_not_list = gerente_not_in_entity_list(type)
    project_path = os.path.join(os.getcwd())
    if type == "dbpedia":
        path = os.path.join(project_path, "data", "origin_dbpedia_data")
    elif type == "lmdb":
        path = os.path.join(project_path, "data", "origin_lmdb_data")
    lists = os.listdir(path) # this is the generated file list
    for file in lists:
        if file == "geo_coordinates_mappingbased_en.ttl" or \
            file == "labels_en.ttl" or \
            file == "mappingbased_literals_en.ttl" or \
            file == "persondata_en.ttl" :
            continue
        gd_path = os.path.join(project_path,"generate_data", "first_to_first", type)
        firstnb_pair = open(os.path.join(gd_path, "first_to_first_{}".format(file)), 'w')
        with open(os.path.join(path, file), 'r') as f:
            for line in f:
                if "# started" in line or "# completed" in line:
                    continue
                head, rel, tail = line.split(" ", 2)
                head = head.replace("<", "").replace(">", "")
                tail = tail.replace("<", "").replace("> .\n", "")
                if head in entity_not_list and tail in entity_not_list:
                    firstnb_pair.write(line)
                    print(line)
            firstnb_pair.close()