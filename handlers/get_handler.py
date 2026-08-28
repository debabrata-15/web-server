from routes import ROUTES

def get_handler(path):
    filename = ROUTES.get(path)
    if filename:
        try:
            with open(filename, "r") as fin:
                content = fin.read()
            return "HTTP/1.1 200 OK\r\n\r\n" + content
        except FileNotFoundError:
            return "HTTP/1.1 404 Not Found\r\n\r\n404 File Not Found"
    else:
        return "HTTP/1.1 404 Not Found\r\n\r\n404 Page Not Found"