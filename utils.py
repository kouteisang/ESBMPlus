# @Author : Cheng Huang
# @Time   : 18:29 2022/10/27
# @File   : utils.py
import os
import pandas as pd
from rdflib import Graph

def get_entity_list(type):
    """
    This function returns the entity list in the esbm dataset according to type
    """
    path = os.path.join(os.getcwd(), 'data', "elist.txt")
    euri = pd.read_csv(path, on_bad_lines='skip', sep='\t')['euri']
    if type == "dbpedia":
        entity_list = [str(entity) for entity in euri[:125]]
    elif type == "lmdb":
        entity_list = [str(entity) for entity in euri[125:]]
    return entity_list

def check_number():
    """
    This function returns the number of entity description for each entity in the ESBM dataset
    """
    path = os.path.join(os.getcwd(), "data", "origin_dbpedia_data")
    lists = os.listdir(path)
    esbm_length = []
    esbm_entity_list = get_entity_list("dbpedia")
    for target in esbm_entity_list:
        cnt = 0
        print(target)
        for filename in lists:
            with open(os.path.join(path, filename)) as f:
                for line in f:
                    if target in line:
                        cnt = cnt + 1
        esbm_length.append(cnt)
        print(cnt)
    print("esbm entity length = ", esbm_length)

def gerente_not_in_entity_list(type="dbpedia"):
    """
    This function scan all the ESBM file according to the type("dbpedia" or "lmdb")
    and return all the class/entity that not in the esbm entity list
    """
    project_path = os.path.join(os.getcwd())
    print(project_path)
    entity_not_list= []
    entity_list = get_entity_list(type)
    if type == "dbpedia":
        index = [i for i in range(1, 101)]
        index += [i for i in range(141, 166)]
        path = os.path.join(project_path, "data", "dbpedia_data")
    elif type == 'lmdb':
        index = [i for i in range(101, 141)]
        index += [i for i in range(166, 176)]
        path = os.path.join(project_path, "data", "lmdb_data")

    for i in index:
        filepath = os.path.join(path, str(i), "{}_desc.nt".format(i))
        g = Graph()
        g.parse(filepath)
        for stmt in g:
            if str(stmt[0]) not in entity_list and "owl#Thing" not in str(stmt[0]):
                entity_not_list.append(str(stmt[0]))
            if str(stmt[2]) not in entity_list and "owl#Thing" not in str(stmt[2]):
                entity_not_list.append(str(stmt[2]))

        final_entity_list = []
        for item in entity_not_list:
            if "http" in item:
                final_entity_list.append(item)

    return list(set(final_entity_list))

def generate_first_neighbour_tail(type):
    """
        This is the situation when the entity is head.
        entity->(entity/class/literal)this part is what we want to find
    """
    project_path = os.path.join(os.getcwd())
    print(project_path)
    tail= []
    entity_list = get_entity_list(type)
    if type == "dbpedia":
        index = [i for i in range(1, 101)]
        index += [i for i in range(141, 166)]
        path = os.path.join(project_path, "data", "dbpedia_data")
    elif type == "lmdb":
        index = [i for i in range(101, 141)]
        index += [i for i in range(166, 176)]
        path = os.path.join(project_path, "data", "lmdb_data")
    for i in index:
        filepath = os.path.join(path, str(i), "{}_desc.nt".format(i))
        g = Graph()
        g.parse(filepath)
        for stmt in g:
            if str(stmt[0]) in entity_list and str(stmt[2]) not in entity_list:
                tail.append(str(stmt[2]))

    tail = list(set(tail))
    return tail

def generate_first_neighbour_head(type):
    """
        This is the situation when the entity is tail.
        (entity/class/literal)this part is what we want to find->entity
    """
    project_path = os.path.join(os.getcwd())
    print(project_path)
    head = []
    entity_list = get_entity_list(type)
    if type == "dbpedia":
        index = [i for i in range(1, 101)]
        index += [i for i in range(141, 166)]
        path = os.path.join(project_path, "data", "dbpedia_data")
    elif type == "lmdb":
        index = [i for i in range(101, 141)]
        index += [i for i in range(166, 176)]
        path = os.path.join(project_path, "data", "lmdb_data")

    for i in index:
        filepath = os.path.join(path, str(i), "{}_desc.nt".format(i))
        g = Graph()
        g.parse(filepath)
        for stmt in g:
            if str(stmt[2]) in entity_list and str(stmt[0]) not in entity_list:
                head.append(str(stmt[0]))

    head = list(set(head))
    return head

def get_all_second_neighbour(type = "dbpedia"):
    """
    This function returns all second neighbour
    There are four different situation:
    1. entity -> first -> second
    2. entity -> first <- second
    3. second -> first -> entity
    4. second <- first -> entity
    """
    project_path = os.path.join(os.getcwd())
    file_path = os.path.join(project_path,
                             "generate_data",
                             "second_neighbour",
                             type)

    second_neighbour = []
    # in this situation, this second neighbourhood is tail
    f_d_s = os.path.join(file_path, "first_direct_second")
    file_below = os.listdir(f_d_s)
    for item in file_below:
        if "persondata_en" in item or \
            "mappingbased_literals" in item or \
            "labels_en" in item or \
            "geo_coordinates_mappingbased_en" in item:
            continue
        below_path = os.path.join(f_d_s, str(item))
        g = Graph()
        g.parse(below_path)
        for stmt in g:
            if "http" in str(stmt[2]):
                second_neighbour.append(str(stmt[2]))

    # in this situation, this second neighbouhoodr is head
    # f_i_s = os.path.join(file_path, "first_inverse_second")
    # file_below = os.listdir(f_i_s)
    # for item in file_below:
    #     if "persondata_en" in item or \
    #         "mappingbased_literals" in item or \
    #         "labels_en" in item or \
    #         "geo_coordinates_mappingbased_en" in item:
    #         continue
    #     below_path = os.path.join(f_i_s, str(item))
    #     g = Graph()
    #     g.parse(below_path)
    #     for stmt in g:
    #         if "http" in str(stmt[0]):
    #             second_neighbour.append(str(stmt[0]))


    # in this situation, this second neighbouhoodr is head
    s_d_f = os.path.join(file_path, "second_direct_first")
    file_below = os.listdir(s_d_f)
    for item in file_below:
        if "persondata_en" in item or \
            "mappingbased_literals" in item or \
            "labels_en" in item or \
            "geo_coordinates_mappingbased_en" in item:
            continue
        below_path = os.path.join(s_d_f, str(item))
        g = Graph()
        g.parse(below_path)
        for stmt in g:
            if "http" in str(stmt[0]):
                second_neighbour.append(str(stmt[0]))


    # in this situation, this second neighbourhood is tail
    # s_i_f = os.path.join(file_path, "second_inverse_first")
    # file_below = os.listdir(s_i_f)
    # for item in file_below:
    #     if "persondata_en" in item or \
    #         "mappingbased_literals" in item or \
    #         "labels_en" in item or \
    #         "geo_coordinates_mappingbased_en" in item:
    #         continue
    #     below_path = os.path.join(s_i_f, str(item))
    #     g = Graph()
    #     g.parse(below_path)
    #     for stmt in g:
    #         if "http" in str(stmt[2]):
    #             second_neighbour.append(str(stmt[2]))


    return list(set(second_neighbour))

def remove_repeat_by_file(file_path):
    """
    For each file, they contains some repeat items, we try to remove them
    """
    repeat = set()
    project_path = os.path.join(os.getcwd())
    path = os.path.join(project_path, "clean_generate_data", "second_to_second", "dbpedia", "second_to_second_yago_types.ttl")
    newfile = open(path, 'w')
    with open(file_path, 'r') as f:
        for line in f:
            if line in repeat:
                continue
            else:
                newfile.write(line)
                repeat.add(line)
    newfile.close()

def merge_dbpedia():
    """
    This function merges the ESBM dbpedia file into one big file
    """
    index = [i for i in range(1, 101)]
    index += [i for i in range(141, 166)]
    project_path = os.path.join(os.getcwd())

    all_dbpedia = open(os.path.join(project_path, "data", "all_dbpedia.ttl"), 'w')

    for i in index:
        path = os.path.join(project_path, "data", "dbpedia_data", str(i), "{}_desc.nt".format(str(i)))
        with open(path, 'r') as f:
            for line in f:
                all_dbpedia.write(line)
                print(line)

    all_dbpedia.close()

def create_whole_dbpedia():
    """
    This function merges orgional dbpedia files,
                        first to first neighbour,
                        second to second neighbour into one big file
    """
    project_path = os.path.join(os.getcwd())
    path = os.path.join(project_path, "temp", "dbpedia")
    files = os.listdir(path)

    complete_dbpedia = open(os.path.join(project_path,"temp","complete_dbpedia.txt"), 'w')
    repeat_remover = set()

    for file in files:
        with open(os.path.join(path, file), 'r') as f:
            for line in f:
                if line in repeat_remover:
                    print(line)
                    continue
                else:
                    repeat_remover.add(line)
                    complete_dbpedia.write(line)

    complete_dbpedia.close()

def merge_lmdb():
    """
    This function merges the ESBM lmdb file into one big file
    """
    index = [i for i in range(101, 141)]
    index += [i for i in range(166, 176)]
    project_path = os.path.join(os.getcwd())

    all_lmdb = open(os.path.join(project_path, "data", "all_lmdb.ttl"), 'w')

    for i in index:
        path = os.path.join(project_path, "data", "lmdb_data", str(i), "{}_desc.nt".format(str(i)))
        with open(path, 'r') as f:
            for line in f:
                all_lmdb.write(line)
                print(line)

    all_lmdb.close()

def create_whole_lmdb():
    """
    This function merges orgional lmdb files,
                        first to first neighbour,
                        second to second neighbour into one big file
    """
    project_path = os.path.join(os.getcwd())
    path = os.path.join(project_path, "temp", "lmdb")
    files = os.listdir(path)

    complete_lmdb = open(os.path.join(project_path,"temp","complete_lmdb.txt"), 'w')
    repeat_remover = set()

    for file in files:
        with open(os.path.join(path, file), 'r') as f:
            for line in f:
                if line in repeat_remover:
                    continue
                else:
                    repeat_remover.add(line)
                    complete_lmdb.write(line)
                    print(line)

    complete_lmdb.close()
