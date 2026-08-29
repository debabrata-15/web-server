import os
import mimetypes

STATIC_DIR = "static"

def get_handler(path):

    if path =="/":
        path = "/index.html"
    
    filename = os.path.join(STATIC_DIR,path.lstrip("/"))
    filename = os.path.normpath(filename)
    if not filename.startswith(STATIC_DIR):
        return "HTTP/1.1 403 Forbidden\r\n\r\n403 Forbidden"

    if not os.path.isfile(filename):
        return "HTTP/1.1 404 Not Found\r\n\r\n404 File Not Found"

    content_type, _ = mimetypes.guess_type(filename)
    content_type = content_type or "application/octet-stream"
    
    with open(filename, "rb") as fin:
        content = fin.read()

    headers = (
        "HTTP/1.1 200 OK\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(content)}\r\n"
        "\r\n"
    )
    return headers.encode() + content