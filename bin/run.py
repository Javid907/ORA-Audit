import os
import time
import pandas as pd
import cx_Oracle
from module import config
from module import db

ora_user = config.get_config("ora_user")
ora_user_pass = config.get_config("ora_user_pass")
ora_db_list_file = config.get_config("ora_db_list_file")
report_file = config.get_config("report_file")
oracle_lib_dir = config.get_config("oracle_lib_dir")
cx_Oracle.init_oracle_client(lib_dir=oracle_lib_dir)
ora_list_file_count = db.get_db_count(ora_db_list_file)
time_str = time.strftime("%Y%m%d-%H%M%S")


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



print("ORA-Audit is Running")
ora_audit()
