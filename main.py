import socket
import json

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8080

ROUTES = {"/": "index.html", "/book": "book.json"}

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((SERVER_HOST, SERVER_PORT))

server_socket.listen(5)

print("Listening on port ", SERVER_PORT)
while True:
    client_socket, client_address = server_socket.accept()
    request = client_socket.recv(1024).decode()
    print(request)
    header_part, _, body = request.partition("\r\n\r\n")
    header_lines = header_part.split("\r\n")
    http_method, path, *_ = header_lines[0].split()

    headers = {}
    for line in header_lines[1:]:
        if ": " in line :
            key, value = line.split(": ",1)
            headers[key.lower()] = value

    if http_method == "POST":
        content_length = int(headers.get("content-length", 0))
        while len(body.encode()) < content_length:
            body += client_socket.recv(1024).decode()

        filename = ROUTES.get(path)
        if filename:
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                response = "HTTP/1.1 400 Bad Request\r\n\r\nInvalid JSON"
                client_socket.sendall(response.encode())
                client_socket.close()
                continue

            with open(filename, "w") as fout:
                json.dump(data,fout)

            response_body = json.dumps({"status": "ok",
                                        "data": data})
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: application/json\r\n"
                f"Content-Length: {len(response_body)}\r\n"
                "\r\n" + response_body
            )
    elif http_method == "GET":
        filename = ROUTES.get(path)
        if filename:
            try:
                with open(filename, "r") as fin:
                    content = fin.read()
                response = "HTTP/1.1 200 OK\r\n\r\n" + content
            except FileNotFoundError:
                response = "HTTP/1.1 404 Not Found\r\n\r\n404 File Not Found"
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n404 Page Not Found"
    else:
        response = "HTTP/1.1 405 Method Not Allowed\n\nAllow: GET"
    client_socket.sendall(response.encode())
    client_socket.close()
