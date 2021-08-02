import os
import time
import socket
import pandas as pd
import cx_Oracle
from module import config
from module import db
from module import compare

ora_user = config.get_config("ora_user")
ora_user_pass = config.get_config("ora_user_pass")
ora_db_list_file = config.get_config("ora_db_list_file")
report_file = config.get_config("report_file")
oracle_lib_dir = config.get_config("oracle_lib_dir")
cx_Oracle.init_oracle_client(lib_dir=oracle_lib_dir)
ora_list_file_count = db.get_db_count(ora_db_list_file)
time_str = time.strftime("%Y%m%d-%H%M%S")
function_folder = config.get_config("function_folder")
difference_file = function_folder + "difference_" + time_str + ".csv"

log_server_ip_address = config.get_config("log_server_ip_address")
log_server_port = config.get_config("log_server_port")

def syslog(message):
    data = "{log_message}".format(log_message=message)
    UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPSock.sendto(data.encode(), (log_server_ip_address, log_server_port))
    UDPSock.close()

def ora_audit():
    csv_file = open(report_file, "a")
    csv_file.write("DB_NAME,OWNER,TABLE_NAME,FIELD_NAME\n")
    csv_file.close()
    for i in range(1, ora_list_file_count):
        ora_db_name = db.get_db_name(i, ora_db_list_file)
        ora_db_ip = db.get_db_ip(i, ora_db_list_file)
        ora_db_port = db.get_db_port(i, ora_db_list_file)
        get_db_connection_type = db.get_db_connection_type(i, ora_db_list_file)
        db.get_sensitive_table(ora_db_name, ora_db_ip, ora_db_port, ora_user, ora_user_pass, get_db_connection_type)

    new_report_file = report_file.split('.csv')[0] + "_" + time_str + ".csv"
    try:
        try:
            df = pd.read_csv(report_file)
            df.drop_duplicates(subset=None, inplace=True)
            df.to_csv(new_report_file, index=False)
        except:
            print("Does not exist duplicate in this report")
        os.remove(report_file)
    except:
        print("Did not find report")

    try:
        new_file = compare.latest_first_file(function_folder)
        old_file = compare.latest_second_file(function_folder)
        compare.diff_file(old_file, new_file, difference_file)
    except:
        pass

    if os.stat(difference_file).st_size != 0:
        with open(difference_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                my_log = line
                syslog(my_log)

print("ORA-Audit is Running")
ora_audit()
