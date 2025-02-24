import http.server
import ssl

server_address = ('', 9000)
handler = http.server.CGIHTTPRequestHandler
handler.cgi_directories = ['/cgi-bin']

httpd = http.server.HTTPServer(server_address, handler)

# SSLContextを作成
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

# ソケットをSSLでラップする
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print("HTTPSサーバーが起動しました: https://localhost:9000")
httpd.serve_forever()
