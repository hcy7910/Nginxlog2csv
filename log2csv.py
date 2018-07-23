# -*- coding: UTF-8 -*-

import csv
import optparse
import re
import datetime
import sys

l2c_ = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})" \
      r"\s\-\s\-\s\[" \
      r"(.*)" \
      r"\s\+\d{4}\]\s\"" \
      r"([A-Z]{3,10}\s)" \
      r"(.*)" \
      r"(\s\w{4}\/\d\.\d)(\"\s.*\s\")" \
      r"(cdhq\.\w{3}\.\w{3}\.\w{2})"

# 选项生成
def options_gen():
    option = optparse.OptionParser()
    option.add_option('-i', '--input', dest='nginx_log_path', help='assign input nginx log file path')
    option.add_option('-o', '--output', dest='csv_file_path', help='assign output csv file path')
    return option.parse_args()


# 逐行正则匹配
def line_to_dict(line):
    if re.match(l2c_, line):
        dt = re.match(l2c_, line)
        tm = dt.group(2)
        tm2 = datetime.datetime.strptime(tm, '%d/%b/%Y:%H:%M:%S')# '%d/%b/%Y:%H:%M:%S %z'
        dat = {"ip": dt.group(1), 'time': tm2, 'request': dt.group(3), 'url': dt.group(4),
               'from': dt.group(7)}
        param = ['qid', 'uid']
        # 匹配 qid, uid
        for p in param:
            ps = 'p' + '='
            if ps in dt.group(4):
                dt1 = dt.group(4).split('?')
                dt2 = dt1[1].split("&")
                for i in range(len(dt2)):
                    pv = dt2[i].split('=')
                    for j in range(len(pv)):
                        if p == pv[j]:
                            print('dt2')
                            print(pv[j])
                            dat[p] = pv[j+1]
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
    print('任务启动时刻              :', start)
    nginx_log_path = '/home/hcy7/sharedata/waf-log-doc/20180616-access.log'
    csv_file_path = '/home/hcy7/sharedata/waf-log-doc/log20180616.csv'
    with open(csv_file_path, 'w') as csv_file_output_fd:  # 打开 CSV 文件
        print('写入文件目录              :', csv_file_path)
        print('读取文件目录              :', nginx_log_path)
        with open(nginx_log_path, 'r') as nginx_log_file_fd:  # 打开日志文件
            line_num = 1  # 初始化行号
            for line in nginx_log_file_fd:
                dict = line_to_dict(line)  # 调用逐行正则匹配函数
                print(dict)
                if dict:
                    dict_write_to_csv(dict, line_num)  # 调用写入 CSV 文件函数
                    line_num += 1  # 行号加 1
    end = datetime.datetime.now()
    print("任务结束时刻              :", end)
    print("任务运行时长              :", end - start)