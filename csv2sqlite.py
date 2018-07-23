# -*- coding: utf-8 -*-
import pandas as pd
import sqlite3 as lite
import optparse
import sys


def csv2pds(csv_file_path):
    dt = pd.read_csv(csv_file_path)
    return dt


def df2sql(data, db_name, table_name, mode='append'):
    con = lite.connect(db_name)
    data.to_sql(name=table_name, con=con, if_exists=mode)
    print("{}, {}, {}".format(db_name, table_name, mode))
    con.close()


def options_gen():
    option = optparse.OptionParser()
    option.add_option('-i', '--input', dest='csv_file_path', help='assign input csv file path')
    option.add_option('-d', '--database', dest='database_file_path', help='assign output database file path')
    option.add_option('-t', '--table', dest='table_name', help='assign output table name')
    option.add_option('-m', '--mode', dest='mode', help='if table exists, append or replace, default append')
    return option.parse_args()


if __name__ == '__main__':
    # 没有输入参数时自动打印帮助
    if not len(sys.argv) == 1:
        pass
    else:
        sys.argv.append('-h')
    (options, value) = options_gen()  # 生成选项
    df = csv2pds(options.csv_file_path)
    if options.mode:
        df2sql(df, options.database_file_path, options.table_name, options.mode)
    else:
        df2sql(df, options.database_file_path, options.table_name)