import socket

HOST, PORT = '', 8080

http_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
http_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
http_server.bind((HOST, PORT))
http_server.listen(1)

print("Serving HTTP on port {PORT} ...".format(PORT=PORT))

while True:
    client_connection, client_address = http_server.accept()
    request_data = client_connection.recv(1024)
    print(request_data.decode("utf-8"))

    http_response = b"""\
HTTP/1.1 200 OK

Hello Napier!
"""
    client_connection.sendall(http_response)
    client_connection.close