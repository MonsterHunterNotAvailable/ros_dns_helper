import base64
import json
import os
import re
import urllib.request

current_path = os.path.dirname(os.path.abspath(__file__))
current_path += "/"
##读取配置文件
conf_file = current_path + "conf.json"
conf_json = {}
with open(conf_file, "r", encoding="utf-8") as f:
    conf_json = json.load(f)

# 定义记录文件路径
RECORDS_FILE = current_path + "/custom_domain.txt"
DNS_SERVER = conf_json["dns_server"]
RSC_FILE = conf_json["out_put_file_dir"] + "/gfw.domain.rsc"
NF_LIST = []
with open(current_path + "netflix_domains.json", "r", encoding="utf-8") as f:
    tmp = json.load(f)
    NF_LIST = tmp["netflix"]

GFW_URL = "https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt"
GFW_CONTENT = urllib.request.urlopen(GFW_URL).read()

GFW_DEC_CONTENT = base64.b64decode(GFW_CONTENT).decode("utf-8")

GFW_LINES = []
lines = GFW_DEC_CONTENT.split("\n")
for line in lines:
    line = re.sub(r'^\|\|?', '', line)
    line = re.sub(r'https?:\/\/', '', line)
    line = re.sub(r'^\.', '', line)
    line = re.sub(r'\*.*', '', line)
    line = re.sub(r'\/.*', '', line)
    line = re.sub(r'%.*', '', line)
    if not re.match(r'^$|^!|^\@|^\[|\.$|^[^\.]*$|^[0-9\.]*$', line):
        GFW_LINES.append(line)

GFW_LINES = sorted(set(GFW_LINES))

def generate_rsc_file(dns_server, domain_list, file_path, nf_list, user_add_domains):
    with open(file_path, "w", encoding="utf-8") as rsc_file:
        # rsc_file.write(":global dnsserver \"%s\"\n" % dns_server)
        rsc_file.write(":global dnsserver \n")
        rsc_file.write("/ip dns static remove [find type=FWD]\n")
        rsc_file.write("/ip dns static\n")
        for domain in domain_list:
            if domain not in nf_list:
                rsc_file.write(
                    ":do { add forward-to=$dnsserver type=FWD address-list=gfw_list match-subdomain=yes name=%s } on-error={}\n" % (
                        domain))
        for domain in nf_list:
            rsc_file.write(
                ":do { add forward-to=$dnsserver type=FWD address-list=nf_list match-subdomain=yes name=%s } on-error={}\n" % (
                    domain))
        for domain in user_add_domains:
            rsc_file.write(
                ":do { add forward-to=$dnsserver type=FWD address-list=gfw_list match-subdomain=yes name=%s } on-error={}\n" % (
                    domain))
        print(file_path + " generated")


user_add_domains = []

with open(RECORDS_FILE, "r") as file:
    lines = file.readlines()

for line in lines:
    _domain = line.split(" ")[0].lstrip()
    _type = line.split(" ")[1].lstrip()
    if (_type.__contains__("netflix")):
        NF_LIST.append(_domain)
    if (_type.__contains__("vpn")):
        user_add_domains.append(_domain)

print("netflix doman")
print(NF_LIST)
print("user add vpn domain")
print(user_add_domains)

generate_rsc_file(DNS_SERVER, GFW_LINES, RSC_FILE, NF_LIST, user_add_domains)

with open(current_path + "user_msg.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
for ln in lines:
    print(ln)
