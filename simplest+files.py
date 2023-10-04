import socket

HOST, PORT = '', 8080

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print("Serving HTTP on port {PORT} ...".format(PORT=PORT))

while True:
    client_connection, client_address = listen_socket.accept()
    request_data = client_connection.recv(1024).decode("utf-8")
    print(request_data)

    # Open and read the HTML file
    with open('htmldocs/index.html', 'r') as infile:
        content = infile.read()

    # Construct the HTTP response with the "Content-Type" header
    http_response = (
        "HTTP/1.1 200 OK\n"
        "Content-Type: text/html\n"  # Header to demonstrate this is served as html so the browser can render it correctly
        "\n"  # Empty line to separate headers from content
        + content
    ).encode()

    client_connection.sendall(http_response)
    client_connection.close()

listen_socket.close()
