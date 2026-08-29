import socket
from handlers import get_handler,post_handler,put_handler,delete_handler

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8080
ROUTES = {"/": "index.html", "/book": "book.json"}

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
server_socket.settimeout(1.0)

print(f"Listening on http://localhost:{SERVER_PORT}")
try:
    while True:
        try:
            client_socket, client_address = server_socket.accept()
        except:
            continue

        request = client_socket.recv(1024).decode()
        print(request)
        header_part, _, body = request.partition("\r\n\r\n")
        header_lines = header_part.split("\r\n")
        http_method, path, *_ = header_lines[0].split()

        headers = {}
        for line in header_lines[1:]:
            if ": " in line:
                key, value = line.split(": ", 1)
                headers[key.lower()] = value
        print(headers)
        if http_method in ("POST","PUT"):
            content_length = int(headers.get("content-length", 0))
            while len(body.encode()) < content_length:
                body += client_socket.recv(1024).decode()

        if http_method == "GET":
            response = get_handler(path)
        elif http_method == "POST":
            response = post_handler(path ,body)
        elif http_method == "PUT":
            response = put_handler(path,body)
        elif http_method == "DELETE":
            response = delete_handler(path)
        else:
            response = "HTTP/1.1 405 Method Not Allowed\n\nAllow: GET,PUT,DELETE,POST"

        if isinstance(response,str):
            client_socket.sendall(response.encode())
        else:
            client_socket.sendall(response)
        client_socket.close()
except KeyboardInterrupt:
    print('Shutting down server...')
finally:
    server_socket.close()