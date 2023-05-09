# @Author : Cheng Huang
# @Time   : 20:54 2022/10/27
# @File   : second_neighbour.py
import os

from utils import generate_first_neighbour_tail, generate_first_neighbour_head, get_entity_list


def generate_first_direct_second(type="dbpedia"):
    """
        THe first neighbourhood is only from ESBM
        entity->first neighbour->second neighbourhood
    """
    project_path = os.path.join(os.getcwd())
    if type == "dbpedia":
        path = os.path.join(project_path, "data", "origin_dbpedia_data")
    elif type == "lmdb":
        path = os.path.join(project_path, "data", "origin_lmdb_data")
    lists = os.listdir(path) # this is the generated file list
    tail = generate_first_neighbour_tail(type)
    new_tail = []
    for item in tail:
        if "http" in item:
            new_tail.append(item)

    for file in lists:
        res_file = open(os.path.join(project_path,
                          "generate_data",
                          "second_neighbour",
                          type,
                          "first_direct_second",
                          "second_neighbour_{}".format(file)), 'w')
        with open(os.path.join(path, file), 'r') as f:
            for line in f:
                head, rel, tail = line.split(" ", 2)
                head = head.replace("<", "").replace(">", "")
                if head in new_tail:
                    print(line)
                    res_file.write(line)
            res_file.close()

def generate_first_inverse_second(type="dbpedia"):
    """
        entity->first neighbour<-second neighbourhood
    """
    entity_list = get_entity_list("dbpedia")
    project_path = os.path.join(os.getcwd())
    path = os.path.join(project_path, "data", "origin_dbpedia_data")
    # lists = os.listdir(path) # this is the generated file list
    tail = generate_first_neighbour_tail(type)
    new_tail = tail
    print(new_tail)
    lists = ["article_categories_en.ttl"]
    for file in lists:
        res_file = open(os.path.join(project_path,
                          "generate_data",
                          "second_neighbour",
                          "dbpedia",
                          "first_inverse_second",
                          "second_neighbour_{}".format(file)), 'w')
        print("file", file)
        if "persondata_en" in file or \
                "mappingbased_literals" in file or \
                "labels_en" in file or \
                "geo_coordinates_mappingbased_en" in file:
            continue
            # with open(os.path.join(path, file), 'r') as f:
            #     for line in f:
            #         head, rel, tail = line.split(" ", 2)
            #         if tail.startswith("<http"):
            #             t_tail = tail.replace("<","").replace(">","")
            #         else:
            #             start_pos = tail.find("\"")
            #             end_pos = tail.rfind("\"")
            #             t_tail = tail[start_pos+1:end_pos]
            #             print(t_tail)
            #         if t_tail in new_tail:
            #             print(line)
            #             res_file.write(line)
            #     res_file.close()


        else:
            with open(os.path.join(path, file), 'r') as f:
                for line in f:
                    head, rel, tail = line.split(" ", 2)
                    t_head = head.replace("<","").replace(">","")
                    t_tail = tail.replace("<", "").replace("> .\n", "")
                    if t_tail in new_tail and t_head not in entity_list and "owl#Thing" not in t_tail:
                        print(line)
                        res_file.write(line)
                res_file.close()

def generate_second_direct_first(type="dbpedia"):
    """
        second neighbour->first neighbour->entity
    """
    project_path = os.path.join(os.getcwd())
    if type == "dbpedia":
        path = os.path.join(project_path, "data", "origin_dbpedia_data")
    elif type == "lmdb":
        path = os.path.join(project_path, "data", "origin_lmdb_data")
    lists = os.listdir(path) # this is the generated file list
    head = generate_first_neighbour_head(type)
    new_head = []
    for item in head:
        if "http" in item:
            new_head.append(item)

    for file in lists:
        res_file = open(os.path.join(project_path,
                          "generate_data",
                          "second_neighbour",
                          type,
                          "second_direct_first",
                          "second_neighbour_{}".format(file)), 'w')
        if "persondata_en" in file or \
                "mappingbased_literals" in file or \
                "labels_en" in file or \
                "geo_coordinates_mappingbased_en" in file:
            continue
        with open(os.path.join(path, file), 'r') as f:
            for line in f:
                head, rel, tail = line.split(" ", 2)
                tail = tail.replace("<", "").replace("> .\n", "")
                if tail in new_head:
                    print(line)
                    res_file.write(line)
            res_file.close()

def generate_second_inverse_first(type="dbpedia"):
    """
        second neighbour<-first neighbour->entity
    """
    project_path = os.path.join(os.getcwd())
    path = os.path.join(project_path, "data", "origin_dbpedia_data")
    lists = os.listdir(path) # this is the generated file list
    head = generate_first_neighbour_head(type)
    new_head = []
    for item in head:
        if "http" in item:
            new_head.append(item)

    for file in lists:
        res_file = open(os.path.join(project_path,
                          "generate_data",
                          "second_neighbour",
                          "dbpedia",
                          "second_inverse_first",
                          "second_neighbour_{}".format(file)), 'w')
        with open(os.path.join(path, file), 'r') as f:
            for line in f:
                head, rel, tail = line.split(" ", 2)
                head = head.replace("<", "").replace(">", "")
                if head in new_head:
                    print(line)
                    res_file.write(line)
            res_file.close()

