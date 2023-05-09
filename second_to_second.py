# @Author : Cheng Huang
# @Time   : 15:14 2022/10/28
# @File   : second_to_second.py
import os
from utils import get_all_second_neighbour


def get_secondnb_to_secondnb(type="dbpedia"):
    second_nb = get_all_second_neighbour(type)
    project_path = os.path.join(os.getcwd())
    file_path = os.path.join(project_path,
                             "data",
                             "origin_{}_data".format(type))
    write_path = os.path.join(project_path,
                              "generate_data",
                              "second_to_second",
                              type)

    file_name_lists = ["linkedmdb-latest-dump.nt"]

    for item in file_name_lists:
        write_file = open(os.path.join(write_path,"second_to_second_{}".format(item)), 'w')
        with open(os.path.join(file_path, item), 'r') as f:
            for line in f:
                if "owl#Thing" in line:
                    continue
                head, rel, tail = line.split(" ", 2)
                head = head.replace("<","").replace(">","")
                tail = tail.replace("<", "").replace("> .\n", "")
                if head in second_nb and tail in second_nb:
                    print(line)
                    write_file.write(line)
        write_file.close()
