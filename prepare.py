# coding=utf-8

import os
import re


def add_file(filepath, file_list, open_folder=False):
    if os.path.isfile(filepath):
        if filepath in file_list:
            print("##{0} already exists".format(filepath))
        else:
            file_list.append(filepath)
            print("##Add {0} to file list.".format(filepath))
    elif os.path.isdir(filepath):
        if open_folder == False:
            option = input("Seems that it's a folder, so add all the files inside?(y/n)\n")
            if option.lower() == "y":
                add_file(filepath, file_list, open_folder=True)
            else:
                print("Okay, we ignore this folder.")
        else:
            for path in os.listdir(filepath):
                add_file(os.path.join(filepath, path), file_list, open_folder=True)


def tag_and_save(raw_file, result_file):

    def save(content):
        try:
            with open(result_file, encoding="utf-8", mode="a", errors="ignore") as ff:
                ff.write(content)
        except:
            print("Failed to wirte the result into the file {0}!".format(result_file))
            return False
        else:
            return True
    try:
        print("##Start to process {0}.".format(raw_file))
        with open(raw_file, encoding="utf-8", mode="r", errors="ignore") as f:
            buffer = ""
            for line in f:
                line = line.strip()
                if len(buffer) > (1 << 20):
                    save(buffer)
                    buffer = ""
                words = re.split(r"[\s]{2,}", line)
                for word in words:
                    if len(word) == 1:
                        buffer += "{0}\t{1}\n".format(word, "S")
                    elif len(word) >= 2:
                        tags = "B"+"M"*(len(word)-2)+"E"
                        buffer += "".join("{0}\t{1}\n".format(*t) for t in zip(word, tags))
        if buffer:
            save(buffer)
    except:
        print("Failed to open the file {0}!".format(raw_file))
        return False
    return True


if __name__ == "__main__":
    training_files = list()
    while True:
        path = input("Please add training files: (Enter 0 to stop)\n")
        if path == "0":
            break
        elif os.path.exists(path):
            add_file(path, training_files)
        else:
            print("Can't find the file or folder!")
    if not training_files:
        print("No training file provided.")
        exit()
    result_file = input("Please input the file to save the result:")
    for file in training_files:
        if not tag_and_save(file, result_file):
            option = input("Seems something wrong...Continue?(y/n)")
            if not option or option.lower()[0] != "y":
                exit()
    print("Done!")
