import csv
import cx_Oracle
import pandas as pd
import difflib
import time
import glob
import os

# openfile = open("../config/key.csv")
# read_csv = csv.reader(openfile, delimiter=',')
# next(read_csv)
# list_csv_content = list(read_csv)
# for i, row in enumerate(list_csv_content):
#     print(row[1])

# def query(db_name, db_ip, db_port, username, password):
#     cx_Oracle.init_oracle_client(lib_dir="../config/win64_lib_19")
#     dsn = cx_Oracle.makedsn(host=db_ip, port=db_port, service_name=db_name)
#     con = cx_Oracle.connect(user=username, password=password, dsn=dsn)
#     cursor_table = con.cursor()
#
#     for row in cursor_table.execute("SELECT SERIAL_NUM_1 FROM DWHPRD.DWH_DIM_IMSI_SERIAL_DUET WHERE ROWNUM = 1"):
#         return row
#
#
# a = query()
# print(a)
# for i in a:
#     b = str(i)
#     if b.startswith("8999"):
#         print("yes")
#     else:
#         print("no")

# openfile = open("../config/test.csv")
# read_csv = csv.reader(openfile, delimiter=',')
# next(read_csv)
# list_csv_content = list(read_csv)
# for i, row in enumerate(list_csv_content):
#     line = row[0], row[1], row[2], row[3]
#     print(row[0], row[1], row[2], row[3])

# file_name = "../config/test.csv"
# file_name_output = "../config/test_test.csv"
#
# df = pd.read_csv(file_name)
# df.drop_duplicates(subset=None, inplace=True)
# df.to_csv(file_name_output, index=False)



# except Exception as my_error:
#     with open(error_log, 'a') as outF:
#         outF.write("Error while getting first row" + ", " + "OWNER: " + o_name + ", " + "TABLE_NAME: " \
#                     + t_name + ", " + str(my_error) + "\n")
# except Exception as my_error:
#     with open(error_log, 'a') as outF:
#         outF.write("Error while getting field name" + ", " + "OWNER: " + o_name + ", " + "TABLE_NAME: "\
#                     + t_name + ", " + str(my_error) + "\n")

                # cursor_first_row = con.cursor()
                # try:
                #     cursor_first_row.execute("SELECT * FROM " + o_name + "." + t_name + " WHERE ROWNUM = 1")
                #     for first_row in cursor_first_row:
                #         for first_row_data in first_row:
                #             openfile = open(key_list)
                #             read_csv = csv.reader(openfile, delimiter=',')
                #             next(read_csv)
                #             list_csv_content = list(read_csv)
                #             for i, row in enumerate(list_csv_content):
                #                 if row[1] == "only":
                #                     my_compare = compare.exact_equal_string(row[0], first_row_data)
                #                     if my_compare == "success":
                #                         add_to_report(db_name, o_name, t_name, row[0])
                #                 else:
                #                     my_compare = compare.approx_equal_string(row[0], first_row_data)
                #                     if my_compare == "success":
                #                         add_to_report(db_name, o_name, t_name, row[0])
                # except:
                #     pass
                # cursor_field_name = con.cursor()
                # try:
                #     cursor_field_name.execute("SELECT column_name FROM all_tab_columns where table_name='" + t_name + "'")
                #     for field_name in cursor_field_name:
                #         for field_name_data in field_name:
                #             openfile = open(key_list)
                #             read_csv = csv.reader(openfile, delimiter=',')
                #             next(read_csv)
                #             list_csv_content = list(read_csv)
                #             for i, row in enumerate(list_csv_content):
                #                 if row[1] == "only":
                #                     my_compare = compare.exact_equal_string(row[0], field_name_data)
                #                     if my_compare == "success":
                #                         add_to_report(db_name, o_name, t_name, field_name_data, row[0])
                #                 else:
                #                     my_compare = compare.approx_equal_string(row[0], field_name_data)
                #                     if my_compare == "success":
                #                         add_to_report(db_name, o_name, t_name, field_name_data, row[0])
                # except:
                #     pass
time_str = time.strftime("%Y%m%d-%H%M%S")

my_directory = "../report/"
file3 = my_directory + "difference_" + time_str + ".csv"


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
                outFile.write(line)
        for line in file_one:
            if line not in file_two:
                outFile.write(line)

new_file = latest_first_file(my_directory)
old_file = latest_second_file(my_directory)
diff_file(old_file, new_file, file3)



