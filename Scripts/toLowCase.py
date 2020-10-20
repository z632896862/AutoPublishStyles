#!/usr/bin/python
# -*- coding: UTF-8 -*-
if __name__ == "__main__":
    source_path = "/data/projects/pythonProjects/sldsources/"  
    targe_path = "/data/projects/pythonProjects/slds/"
    files = os.listdir(source_path)
    for singerfile in files:
        file = open(targe_path + singerfile, 'w', encoding='UTF-8')
        with open(source_path + singerfile, 'r', encoding='UTF-8') as f:

            for line in f.readlines():
                newline = line
                continue
                if line.__contains__("TEXT_"):
                    newline = line.replace("TEXT_", "text_")
                if line.__contains__("UNAME"):
                    newline = line.replace("UNAME", "uname")
                if line.__contains__("Class"):
                    newline = line.replace("Class", "class")
                if line.__contains__("Label"):
                    newline = line.replace("Label", "label")
                if line.__contains__("微软雅黑"):
                    newline = line.replace("微软雅黑", "Microsoft YaHei")
                if line.__contains__("STName"):
                    newline = line.replace("STName", "stname")
                else:
                    if line.__contains__("NAME"):
                        newline = line.replace("NAME", "name")
                file.write(newline)

        print(singerfile + " finished!!")