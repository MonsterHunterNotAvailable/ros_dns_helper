import os
import queue
import subprocess
import threading
import time

from GDB import *


def dns_lookup(domain, dns_server):
    # 设置使用的 DNS 服务器
    cmd = '''nslookup %s %s''' % (domain, dns_server)
    try:
        result = subprocess.check_output(cmd, shell=True, text=True)
        if (result.__contains__("No answer")):
            return False
        return True
    except:
        return False


db = GDB("home_db")
db.connectDB("192.168.50.12", "root", "abcd1234", 3306)


def process_data_from_queue(queue, dns_addr, db):
    while True:
        data = queue.get()  # 从队列中获取数据
        if data is None:
            break  # 如果队列中没有数据了，线程退出
        # 在这里进行数据处理，例如打印数据
        # print("Processing data:", data)
        if dns_lookup(data, dns_addr):
            print("域名 " + str(data) + " 查询成功")
            sql = "update domains set is_ok = -1 where name='%s'" % (data)
            db.execute(sql)
        else:
            # print("域名 " + str(data) + " 查询失败")
            sql = "update domains set is_ok = is_ok + 1 where name='%s'" % (data)
            db.execute(sql)
        queue.task_done()  # 表示已经处理完一个任务
        time.sleep(0.1)

data_queue = queue.Queue()
result_set = db.queryList("select * from domains where is_ok >0 and is_ok <= 5 ")
for one_result in result_set:
    data_queue.put(one_result["name"])

# 创建10个线程
dns_address = [
    '119.29.29.29',
    '114.114.114.114',
    '101.226.4.6',
    '123.125.81.6',
    '223.5.5.5',
    '4.2.2.1',
    '61.132.163.68',
    '61.128.192.68',
    '180.76.76.76',
    '208.67.222.222'
]
threads = []
for i in range(10):
    tmpDb = GDB("home_db")
    tmpDb.connectDB("192.168.50.12", "root", "abcd1234", 3306)
    thread = threading.Thread(target=process_data_from_queue, args=(data_queue, dns_address[i],tmpDb))
    threads.append(thread)

# 启动线程
for thread in threads:
    thread.start()

# 等待所有线程完成
for thread in threads:
    thread.join()

# 此时所有线程已经处理完队列中的数据
print("All data processed.")
