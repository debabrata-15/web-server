import socket

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8080

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((SERVER_HOST, SERVER_PORT))

server_socket.listen(5)

print("Listening on port ",SERVER_PORT)
while True:    
    client_socket, client_address = server_socket.accept()
    request = client_socket.recv(1024).decode()
    print(request)
    headers = request.split('\n')
    first_header_components = headers[0].split()

    http_method = first_header_components[0]
    path = first_header_components[1]

    ROUTES = {
        '/' : 'index.html',
        '/book' : 'book.json'
    }
    
    if http_method == 'GET':
        filename = ROUTES.get(path)
        if filename:
            try :
                with open(filename, 'r') as fin:
                    content = fin.read()
                response = 'HTTP/1.1 200 OK\r\n\r\n' + content
            except FileNotFoundError:
                response = 'HTTP/1.1 404 Not Found\r\n\r\n404 File Not Found'
        else:
            response = 'HTTP/1.1 404 Not Found\r\n\r\n404 Page Not Found'
    else:
        response = 'HTTP/1.1 405 Method Not Allowed\n\nAllow: GET'
    client_socket.sendall(response.encode())
    client_socket.close()
