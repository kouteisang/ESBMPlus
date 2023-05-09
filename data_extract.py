# @Author : Cheng Huang
# @Time   : 19:01 2022/11/1
# @File   : data_extract.py
import os
import re

from rdflib import Graph

project_path = os.path.join(os.getcwd())
path = os.path.join(project_path, "data", "dbpedia_data")
index = [i for i in range(1, 101)]
index += [i for i in range(141, 166)]

rel_remover = set()
entity_remover = set()
cntrel = 0
cntentity = 0

# for i in index:
with open(os.path.join(project_path, "complete_data", "complete_dbpedia2.tsv"), 'r') as f:
    # origion = open(os.path.join(project_path, "dbpedia_origion", "{}_desc.nt".format(i)),'w')
    for line in f:
        print(line)
        # g = Graph()
        # g.parse(data=line, format="nt")
        # for stmt in g:
        head, rel, tail = line.split("\t")
        tail = tail.replace("\n","")

        if "\"" in head:
            head = head.replace("\"", "")
        if "\'" in head:
            head = head.replace("\'", "")

        if "\"" in rel:
            rel = rel.replace("\"", "")
        if "\'" in rel:
            rel = rel.replace("\'", "")

        if "\"" in tail:
            tail = tail.replace("\"", "")
        if "\'" in tail:
            tail = tail.replace("\'", "")
        if tail == "":
            tail = "UNK"

        if head not in entity_remover:
            entity_remover.add(head)
            cntentity = cntentity + 1

        if tail not in entity_remover:
            entity_remover.add(tail)
            cntentity = cntentity + 1

        if rel not in rel_remover:
            rel_remover.add(rel)
            cntrel = cntrel + 1

            # origion.write(head+"\t"+rel+"\t"+tail+"\n")
    # origion.close()

print("cnt entity", cntentity)
print("cnt rel", cntrel)
