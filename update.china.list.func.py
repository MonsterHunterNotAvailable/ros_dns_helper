import base64
import json
import os
import re
import urllib.request

current_path = os.path.dirname(os.path.abspath(__file__))
current_path += "/"
##读取配置文件
conf_file = current_path + "conf_china.json"
conf_json = {}
with open(conf_file, "r", encoding="utf-8") as f:
    conf_json = json.load(f)

# 定义记录文件路径
RECORDS_FILE = current_path + "/custom_china_domain.txt"
DNS_SERVER = conf_json["dns_server"]
RSC_FILE = conf_json["out_put_file_dir"] + "/china.domain.rsc"
NF_LIST = []
with open(current_path + "china_user_add_domains.json", "r", encoding="utf-8") as f:
    tmp = json.load(f)
    NF_LIST = tmp["user_add"]

GFW_URL = "https://raw.githubusercontent.com/felixonmars/dnsmasq-china-list/master/accelerated-domains.china.conf"

GFW_CONTENT = urllib.request.urlopen(GFW_URL).read()

GFW_DEC_CONTENT = GFW_CONTENT.decode()

GFW_LINES = []
lines = GFW_DEC_CONTENT.split("\n")
for line in lines:
    try:
        line = line.split("/")[1]
        GFW_LINES.append(line)
    except:
        pass
GFW_LINES = sorted(set(GFW_LINES))


def generate_rsc_file(dns_server, domain_list, file_path, user_add_domains):
    with open(file_path, "w", encoding="utf-8") as rsc_file:
        rsc_file.write(":global dnsserver \"%s\"\n" % dns_server)
        # rsc_file.write(":global dnsserver \n")
        rsc_file.write("/ip dns static remove [find type=FWD]\n")
        rsc_file.write("/ip dns static\n")
        for domain in domain_list:
            rsc_file.write(
                ":do { add forward-to=$dnsserver type=FWD address-list=china_list match-subdomain=yes name=%s } on-error={}\n" % (
                    domain))
        for domain in user_add_domains:
            rsc_file.write(
                ":do { add forward-to=$dnsserver type=FWD address-list=china_list match-subdomain=yes name=%s } on-error={}\n" % (
                    domain))
        rsc_file.write("/ip dns cache flush\n")
        print(file_path + " generated")


generate_rsc_file(DNS_SERVER, GFW_LINES, RSC_FILE, NF_LIST)
