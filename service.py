#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime

class MyHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # カスタムフォーマット: 現在日時 - クライアントIP - ログメッセージ
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f"{now} - {self.client_address[0]} - {format % args}\n"
        sys.stderr.write(message)

if __name__ == '__main__':
    server_address = ('', 8001)
    httpd = HTTPServer(server_address, MyHandler)
    print(f"Serving HTTP on port {server_address[1]}...")
    httpd.serve_forever()
