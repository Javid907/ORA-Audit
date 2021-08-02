import glob
import os

def exact_equal_string(first, second):
    if first.lower() == second.lower():
        return "success"
    else:
        return "failed"


def approx_equal_string(first, second):
    if first.lower() in second.lower():
        return "success"
    else:
        return "failed"


def head_equal_string(first, second):
    my_str1 = str(second)
    my_str2 = str(first)
    if my_str1.startswith(my_str2):
        return "success"
    else:
        return "failed"


def latest_first_file(working_directory):
    list_of_files = glob.glob(working_directory + "report*")
    paths = sorted(list_of_files, key=os.path.getmtime)
    return paths[-1]


def latest_second_file(working_directory):
    list_of_files = glob.glob(working_directory + "report*")
    paths = sorted(list_of_files, key=os.path.getmtime)
    return paths[-2]


def diff_file(old_report, new_report, difference_file):
    with open(old_report, 'r') as t1, open(new_report, 'r') as t2:
        file_one = t1.readlines()
        file_two = t2.readlines()
    with open(difference_file, 'w') as outFile:
        for line in file_two:
            if line not in file_one:
                outFile.write(line.rstrip() + ",TABLE_ADDED\n")
        for line in file_one:
            if line not in file_two:
                outFile.write(line.rstrip() + ",TABLE_REMOVED\n")