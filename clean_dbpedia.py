# @Author : Cheng Huang
# @Time   : 20:13 2022/11/3
# @File   : clean_dbpedia.py
import os

from rdflib import Graph

from utils import get_entity_list


def remove_owlthing():
    """
    When I generate the second neighbour, sadly, I forget to remove the "owl#Thing" so name I need to remove them
    :return:
    """
    remover = set()
    project_path = os.path.join(os.getcwd())
    path = os.path.join(project_path, "temp", "complete_dbpedia.txt")
    newfile = open(os.path.join(project_path, "temp", "new_complete_dbpedia.nt"), 'w')
    db_list = get_entity_list("dbpedia")
    with open(path, 'r') as f:
        for line in f:
            g = Graph()
            g.parse(data=line, format="nt")
            for stmt in g:
                head = str(stmt[0])
                rel = str(stmt[1])
                tail = str(stmt[2])
                if (head not in db_list) and ("owl#Thing" in tail):
                    continue
                if line in remover:
                    continue
                remover.add(line)
                newfile.write(line)
    newfile.close()





remove_owlthing()