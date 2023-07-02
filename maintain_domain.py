import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import base64

# 定义用户验证信息
VALID_USERNAME = 'gfw'
VALID_PASSWORD = '1234567'

# 定义记录文件路径
RECORDS_FILE = 'custom_domain.txt'


# HTTP请求处理类
class MyHTTPRequestHandler(BaseHTTPRequestHandler):

    # 处理GET请求
    def do_GET(self):
        # 检查路径是否为根路径"/"
        if self.path == '/':
            # 检查用户身份验证
            if not self.authenticate_user():
                self.send_authenticate_response()
                return

            # 读取记录文件内容
            records = self.read_records()

            # 构建HTML响应内容
            response_content = '<html><body>'
            response_content += '<h1>自定义记录列表</h1>'
            response_content += '<ul>'
            for record in records:
                response_content += '<li>' + record + ' <a href="/delete?record=' + record + '">删除</a></li>'
            response_content += '</ul>'
            response_content += '<h1>添加自定义域名记录</h1>'
            response_content += '<form method="POST" action="/add">'
            response_content += '<input type="text" name="record">'
            response_content += '<input type="submit" value="添加奈飞" formaction="/add?param=netflix">'
            response_content += '<input type="submit" value="添加翻墙" formaction="/add?param=vpn">'
            response_content += '</form>'
            response_content += '<h1>点击生成rsc</h1>'
            response_content += '<a href="/execute">生成</a>'
            response_content += '</body></html>'
            response_content += '</body></html>'

            # 发送响应
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(response_content.encode())

        # 处理删除请求
        elif self.path.startswith('/delete?'):
            # 检查用户身份验证
            if not self.authenticate_user():
                self.send_authenticate_response()
                return

            # 解析请求参数
            query_string = self.path.split('?', 1)[1]
            query_params = parse_qs(query_string)
            record = query_params.get('record', [''])[0]

            # 删除记录
            if record:
                self.delete_record(record)

            # 重定向回首页
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()

        elif self.path == '/execute':
            # 检查用户身份验证
            if not self.authenticate_user():
                self.send_authenticate_response()
                return

            # 执行本地程序并捕获输出结果
            output = self.execute_local_program()

            # 构建 HTML 响应内容
            response_content = '<html><body>'
            response_content += '<h1>执行本地程序</h1>'
            response_content += '<pre>' + output + '</pre>'
            response_content += '</body></html>'

            # 发送响应
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(response_content.encode())

        # 处理未知请求
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    # 处理POST请求
    def do_POST(self):
        # 检查路径是否为添加记录
        if self.path.startswith('/add'):
            # 检查用户身份验证
            if not self.authenticate_user():
                self.send_authenticate_response()
                return

            # 读取POST请求数据
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode()
            record = parse_qs(post_data).get('record', [''])[0]
            param = self.path.split("=")[1]
            record += " "
            record += param

            # 添加记录
            if record:
                self.add_record(record)

            # 重定向回首页
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()

    # 用户身份验证
    def authenticate_user(self):
        auth_header = self.headers.get('Authorization')
        if auth_header:
            auth_type, auth_data = auth_header.split(' ', 1)
            if auth_type == 'Basic':
                username, password = base64.b64decode(auth_data.strip()).decode().split(':', 1)
                return username == VALID_USERNAME and password == VALID_PASSWORD
        return False

    # 发送身份验证响应
    def send_authenticate_response(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Authentication required"')
        self.end_headers()
        self.wfile.write(b'Authentication required')

    # 读取记录文件内容
    def read_records(self):
        try:
            with open(RECORDS_FILE, 'r') as file:
                records = file.read().splitlines()
        except IOError:
            records = []
        return records

    # 写入记录到文件
    def write_records(self, records):
        with open(RECORDS_FILE, 'w') as file:
            for record in records:
                file.write(record + '\n')

    # 添加记录
    def add_record(self, record):
        record = record.lstrip()
        records = self.read_records()
        if record not in records:
            records.append(record)
            self.write_records(records)

    # 删除记录
    def delete_record(self, record):
        records = self.read_records()
        if record in records:
            records.remove(record)
            self.write_records(records)

    def execute_local_program(self):
        try:
            output = subprocess.check_output(['python3', 'update.gfw.list2.py'], stderr=subprocess.STDOUT)
            return output.decode()
        except subprocess.CalledProcessError as e:
            return f"执行程序时出错：{e.output.decode()}"


# 启动HTTP服务器
def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHTTPRequestHandler)
    httpd.serve_forever()


# 运行服务器
if __name__ == '__main__':
    run_server()
