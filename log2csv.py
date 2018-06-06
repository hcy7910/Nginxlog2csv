# -*- coding: UTF-8 -*-

import csv
import optparse
import re
import datetime

l2c_ = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})" \
      r"\s\-\s\-\s\[" \
      r"(.*)" \
      r"\s\+\d{4}\]\s\"" \
      r"([A-Z]{3,10}\s)" \
      r"(.*)" \
      r"(\s\w{4}\/\d\.\d)(\"\s.*\s\")" \
      r"(cdhq\.\w{3}\.\w{3}\.\w{2})"


# 逐行正则匹配函数
def line_to_dict(line):
    if re.match(l2c_, line):
        dt = re.match(l2c_, line)
        dat = {"ip": dt.group(1), 'time': dt.group(2), 'request': dt.group(3), 'url': dt.group(4),
               'from': dt.group(7)}
        param = ['qid', 'uid']
        # 匹配 qid, uid
        for p in param:
            if p in dt.group(4):
                dt1 = dt.group(4).split('?')
                dt2 = dt1[1].split("&")
                for i in range(len(dt2)):
                    pv = dt2[i].split('=')
                    if p == pv[0]:
                        print('dt2')
                        print(dt2)
                        dat[p] = pv[1]
                        break
            else:
                dat[p] = ''
        return dat
    else:
        # return {'ip': '', 'time': '', 'request': '', 'url': '', 'from': ''}
        pass


# 写入 CSV 文件
def dict_write_to_csv(dict, line_num):
    # 在第一行前面加入表头
    if line_num == 1:
        csv.DictWriter(csv_file_output_fd, dict.keys()).writeheader()
    if dict:
        csv.DictWriter(csv_file_output_fd, dict.keys()).writerow(dict)


if __name__ == '__main__':
    start = datetime.datetime.now()
    print(start)
    csv_file_path = 'log0603.csv'
    nginx_log_path = '20180603-access.log'
    with open(csv_file_path, 'w') as csv_file_output_fd:  # 打开 CSV 文件
        with open(nginx_log_path, 'r') as nginx_log_file_fd:  # 打开日志文件
            line_num = 1
            for line in nginx_log_file_fd:
                dict = line_to_dict(line)  # 调用逐行正则匹配函数
                print(dict)
                dict_write_to_csv(dict, line_num)  # 调用写入csv文件函数
                line_num += 1  # 行号加 1
    end = datetime.datetime.now()
    print(end-start)