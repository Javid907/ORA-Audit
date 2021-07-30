import csv
import cx_Oracle
from . import config
from . import compare

key_list = config.get_config("key_list")
exclude_key_list = config.get_config("exclude_key_list")
exclude_status = config.get_config("exclude_status")
error_log = config.get_config("error_log")
report_file = config.get_config("report_file")


def get_db_count(file_name):
    file = open(file_name)
    reader = csv.reader(file)
    lines = len(list(reader))
    return lines


def get_db_name(number, file_name):
    openfile = open(file_name)
    read_csv = csv.reader(openfile, delimiter=',')
    list_csv_content = list(read_csv)
    for i, row in enumerate(list_csv_content):
        if i == number:
            return row[0]
            break


def get_db_ip(number, file_name):
    openfile = open(file_name)
    read_csv = csv.reader(openfile, delimiter=',')
    list_csv_content = list(read_csv)
    for i, row in enumerate(list_csv_content):
        if i == number:
            return row[1]
            break


def get_db_port(number, file_name):
    openfile = open(file_name)
    read_csv = csv.reader(openfile, delimiter=',')
    list_csv_content = list(read_csv)
    for i, row in enumerate(list_csv_content):
        if i == number:
            return row[2]
            break


def get_db_connection_type(number, file_name):
    openfile = open(file_name)
    read_csv = csv.reader(openfile, delimiter=',')
    list_csv_content = list(read_csv)
    for i, row in enumerate(list_csv_content):
        if i == number:
            return row[3]
            break


def add_to_report(db_name, o_name, t_name, field):
    my_csv_file = open(report_file, "a")
    my_csv_file.write(db_name + "," + o_name + "," + t_name + "," + field + "\n")
    my_csv_file.close()


def get_exclude(o_name, c_name):
    exclude_open_key_file = open(exclude_key_list)
    exclude_read_key_csv = csv.reader(exclude_open_key_file, delimiter=',')
    next(exclude_read_key_csv)
    exclude_list_csv_key = list(exclude_read_key_csv)
    for exclude_i, exclude_row in enumerate(exclude_list_csv_key):
        if exclude_row[1] == "owner_exclude":
            exclude_my_compare = compare.approx_equal_string(exclude_row[0], o_name)
            if exclude_my_compare == "success":
                return "success"
        elif exclude_row[1] == "field_exclude":
            exclude_my_compare = compare.approx_equal_string(exclude_row[0], c_name)
            if exclude_my_compare == "success":
                return "success"


def get_sensitive_table(db_name, db_ip, db_port, username, password, type):
    try:
        if "svc" == type:
            dsn = cx_Oracle.makedsn(host=db_ip, port=db_port, service_name=db_name)
        else:
            dsn = cx_Oracle.makedsn(host=db_ip, port=db_port, sid=db_name)
        con = cx_Oracle.connect(user=username, password=password, dsn=dsn)
        cursor_table = con.cursor()
        try:
            cursor_table.execute("SELECT a.OWNER,a.table_name,a.column_name FROM all_tab_columns \
                                a,all_all_tables b where a.OWNER=b.owner and \
                                a.TABLE_NAME=b.table_name and b.num_rows!=0")
            for o_name, t_name, c_name in cursor_table:

                if exclude_status:
                    exclude_compare = get_exclude(o_name, c_name)
                    if exclude_compare == "success":
                        continue

                open_key_file = open(key_list)
                read_key_csv = csv.reader(open_key_file, delimiter=',')
                next(read_key_csv)
                list_csv_key = list(read_key_csv)
                for i, row in enumerate(list_csv_key):
                    if row[1] == "only":
                        my_compare = compare.exact_equal_string(row[0], c_name)
                        if my_compare == "success":
                            add_to_report(db_name, o_name, t_name, c_name)
                    elif row[1] == "begin":
                        cursor_first_row = con.cursor()
                        try:
                            for first_row in cursor_first_row.execute("SELECT " + c_name + " FROM " + \
                                                                      o_name + "." + \
                                                                      t_name + " WHERE ROWNUM = 1"):
                                my_compare = compare.head_equal_string(row[0], first_row[0])
                                if my_compare == "success":
                                    add_to_report(db_name, o_name, t_name, c_name)
                        except:
                            pass
                    else:
                        my_compare = compare.approx_equal_string(row[0], c_name)
                        if my_compare == "success":
                            add_to_report(db_name, o_name, t_name, c_name)
        except Exception as my_error:
            with open(error_log, 'a') as outF:
                outF.write("Error while getting table list" + ", " + "DB_NAME: " + db_name + ", " + \
                           str(my_error) + "\n")
    except Exception as my_error:
        with open(error_log, 'a') as outF:
            outF.write("Cannot connect to" + ", " + "DB_NAME: " + db_name + ", " + str(my_error) + "\n")