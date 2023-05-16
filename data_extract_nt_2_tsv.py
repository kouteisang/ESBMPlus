# @Author : Cheng Huang
# @Time   : 14:36 2022/9/5
# @File   : data_extract.py


import os
import re
from os import path

from rdflib import Graph


def parser(f):
    triples = list()
    for i, triple in enumerate(f):
        # extract subject
        sub = triple.strip().replace("<", "").split(">")[0]
        sub = sub[sub.rfind("/") + 1:]
        # extract content from "content"
        if "\"" in sub:
            pattern = re.compile('"(.*)"')
            try:
                sub_new = pattern.findall(sub)[0]
            except IndexError:
                # like "United States/Australian victory"
                sub = sub.replace("\"", "").strip()
                sub_new = sub
        # extract content from ":content"
        elif ":" in sub:
            pattern = re.compile(':(.*)')
            sub_new = pattern.findall(sub)[0]
        else:
            sub_new = sub
        sub_new = sub_new.replace(" ", "")

        # extract object
        obj = triple.strip().replace("<", "").split(">")[2]
        # fix extract content form "content\"
        if obj.rfind("/") + 1 == len(obj):
            obj = obj[:-1]
        obj = obj[obj.rfind("/") + 1:]
        # extract content from "content"
        if "\"" in obj:
            pattern = re.compile('"(.*)"')
            try:
                obj_new = pattern.findall(obj)[0]
            except IndexError:
                # like "United States/Australian victory"
                obj = obj.replace("\"", "").strip()
                obj_new = obj
        # extract content from ":content"
        elif ":" in obj:
            pattern = re.compile(':(.*)')
            obj_new = pattern.findall(obj)[0]
        else:
            obj_new = obj
        obj_new = obj_new.replace(" ", "")
        if obj_new == "":
            obj_new = "UNK"

        # extract predicate
        pred = triple.strip().replace("<", "").split(">")[1]
        pred = pred[pred.rfind("/") + 1:]
        if "#" in pred:
            pattern = re.compile('#(.*)')
            pred_new = pattern.findall(pred)[0]
        elif ":" in pred:
            pattern = re.compile(':(.*)')
            pred_new = pattern.findall(pred)[0]
        else:
            pred_new = pred
        pred_new = pred_new.replace(" ", "")
        if not (sub_new == "" or pred_new == "" or obj_new == ""):
            triple_tuple = (
            i, sub, pred, obj, sub_new.replace(" ", ""), pred_new.replace(" ", ""), obj_new.replace(" ", ""))
            triples.append(triple_tuple)
        else:
            print(triple)
    return triples

def prepare_data(db_path, num):
    with open(path.join(db_path,
        "{}".format(num),
        "{}_desc.nt".format(num)),
        encoding="utf8") as f:
        triples = parser(f)
    return triples

if __name__ == '__main__':

    # dbpedia_data [1-100, 141-165]
    # lmdb_data [101-140, 166-175]

    # root = os.path.abspath(os.path.dirname(os.getcwd()))
    # dbpedia_path = os.path.join(root, "data", "dbpedia_data")
    # lmdb_path = os.path.join(root, "data", "lmdb_data")
    #
    # # dbpedia_list index
    # dbpedia_list = [i for i in range(1, 101)]
    # dbpedia_list += [i for i in range(141, 166)]
    #
    # # lmdb_list index
    # lmdb_list = [i for i in range(101, 141)]
    # lmdb_list += [i for i in range(166, 176)]
    #
    # dbpedia_all_path = os.path.join(os.getcwd(), "dbpedia","dbpedia_all.txt")
    # lmdb_all_path = os.path.join(os.getcwd(), "lmdb", "lmdb_all.txt")
    #
    # db_write = open(dbpedia_all_path, "w")
    # lm_write = open(lmdb_all_path, "w")
    #
    # for i in dbpedia_list:
    #     triples = prepare_data(dbpedia_path, i)
    #     file_path = os.path.join(os.getcwd(), "dbpedia", "{}_desc.nt".format(i))
    #     file = open(file_path, "w")
    #     for _, _, _, _, head, pred, tail in triples:
    #         db_write.write(head+"\t"+pred+"\t"+tail+"\n")
    #         file.write(head + "\t" + pred + "\t" + tail + "\n")
    #     file.close()
    #
    # db_write.close()
    #
    # for i in lmdb_list:
    #     triples = prepare_data(lmdb_path, i)
    #     file_path = os.path.join(os.getcwd(), "lmdb", "{}_desc.nt".format(i))
    #     file = open(file_path, "w")
    #     for _, _, _, _, head, pred, tail in triples:
    #         lm_write.write(head+"\t"+pred+"\t"+tail+"\n")
    #         file.write(head + "\t" + pred + "\t" + tail + "\n")
    #     file.close()
    #
    # lm_write.close()

    root = os.path.abspath(os.path.dirname(os.getcwd()))
    # nt file to be read
    complete_path = os.path.join(root, "complete_data", "dbpedia", "complete_dbpedia.nt")
    # store in this csv file
    writefile = open("/Users/huangcheng/Documents/ESBasedonSimilarity/complete_data/dbpedia/complete_extract_dbpedia.tsv", 'w')
    cnt = 0
    remover = set()
    with open(complete_path, encoding="utf-8") as f:
        triples = parser(f)
        for _, _, _, _, head, pred, tail in triples:
            t = head+"\t"+pred+"\t"+tail
            if t in remover:
                print(head, pred, tail)
                cnt = cnt + 1
                continue
            remover.add(t)
            writefile.write(t+"\n")
        print(cnt)
    # cnt = 0
    # g = Graph()
    # g.parse(complete_path)
    # write_tsv = open(os.path.join(root, "complete_data", "dbpedia", "complete_dbpedia.tsv"), 'w')
    # remover = set()
    # for stmt in g:
    #     cnt = cnt + 1
    #     head = str(stmt[0])
    #     rel = str(stmt[1])
    #     tail = re.sub("\s+", "", str(stmt[2]))
    #
    #     if "\"" in head:
    #         head = head.replace("\"","")
    #     if "\'" in head:
    #         head = head.replace("\'","")
    #
    #     if "\"" in rel:
    #         rel = rel.replace("\"","")
    #     if  "\'" in rel:
    #         rel = rel.replace("\'","")
    #
    #     if "\"" in tail:
    #         tail = tail.replace("\"","")
    #     if  "\'" in tail:
    #         tail = tail.replace("\'","")
    #     if tail == "":
    #         tail = "UNK"
    #
    #     t = head + "\t" + rel + "\t" + tail
    #     if t in remover:
    #         continue
    #     else:
    #         remover.add(t)
    #         write_tsv.write(t+"\n")
    #
    # write_tsv.close()

