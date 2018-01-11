# coding=utf-8

import os
import sys
import re
from prepare import add_file


def segment_CRF(file, crf_model, sep="  "):
    print("##Start to handle {0}.".format(file))
    temp_file = [file+".temp0", file+".temp1"]
    result_file = file+".result"
    if os.path.exists(temp_file[0]):
        os.remove(temp_file[0])
    def save(content, target_file, mode="a"):
        with open(target_file, mode=mode, encoding="utf8", errors="ignore") as f:
            f.write(content)

    with open(file, encoding="utf8", mode="r", errors="ignore") as f:
        buffer = ""
        for line in f:
            line = line.strip()
            buffer += ("\n".join(line)+"\n"+"\n")
            if len(buffer) > (1 << 20):
                save(buffer, temp_file[0])
                buffer = ""
        save(buffer, temp_file[0])
    cmd = '"CRF++-0.58\crf_test.exe" {0} -m {1} -o {2}'.format(temp_file[0], crf_model, temp_file[1])
    print(cmd)
    os.system(cmd)
    with open(temp_file[1], encoding="utf8", mode="r", errors="ignore", newline="\r\n") as f:   # For linux, newline="\n"
        buffer = ""
        for line in f:
            if len(buffer) > (1 << 20):
                save(buffer, result_file)
                buffer = ""
            line = line.strip()
            if not line:
                buffer += "\n"
                continue
            character, tag = line.split("\t")
            #print(character, tag)
            if tag == "S" or tag == "E":
                buffer += (character+sep)
            elif tag == "M" or tag == "B":
                buffer += character
            else:
                raise ValueError("Invalid tag found!")
        save(buffer, result_file)
    for file in temp_file:
        os.remove(file)
    print("##Success.")

if __name__ == '__main__':
    testing_files = list()
    while True:
        path = input("Please add testing files: (Enter 0 to stop)\n")
        if path == "0":
            break
        elif os.path.exists(path):
            add_file(path, testing_files)
        else:
            print("Can't find the file or folder!")
    if not testing_files:
        print("No testing file provided.")
        exit()
    crf_model = input("Please input the CRF model:") or "CRF_Model/crf_model_pku"
    for file in testing_files:
        try:
            segment_CRF(file, crf_model)
        except Exception as e:
            print("Seems something wrong while segmenting {0}.".format(file))
            print("Detailed infomation:", e, sep="\n")
            break
    print("Done!")
