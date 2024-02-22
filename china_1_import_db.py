import os
import subprocess

from GDB import *

current_path = os.path.dirname(os.path.abspath(__file__))
current_path += "/"

def dns_lookup(domain, dns_server):
    # 设置使用的 DNS 服务器
    cmd = '''nslookup %s %s''' % (domain, dns_server)
    try:
        result = subprocess.check_output(cmd, shell=True, text=True)
        resul = result.strip()
        if (result.__contains__("No answer")):
            return False
        return True
    except subprocess.CalledProcessError as e:
        return f"执行程序时出错：{e.output.decode()}"
        return False


db = GDB("home_db")
db.connectDB("192.168.50.12", "root", "abcd1234",3306)

with open(current_path + "accelerated-domains.china.conf", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        line = line.split("/")[1]
        try:
            sql = "insert into domains values('%s',0)" % (line)
            db.execute(sql)
        except:
            pass
