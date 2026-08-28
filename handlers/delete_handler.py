import os
import json
from routes import ROUTES


def delete_handler(path):
    filename = ROUTES.get(path)
    if not filename:
        return "HTTP/1.1 404 Not Found\r\n\r\n404 File Not Found"

    try:
        os.remove(filename)
        response_body = json.dumps({"status": "ok", "message": f"{path} deleted"})
        return (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: application/json\r\n"
            f"Content-Length: {len(response_body)}\r\n"
            "\r\n" + response_body
        )
    except FileNotFoundError:
        response_body = json.dumps({"status": "ok", "message": f"{path} not found"})
        return (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: application/json\r\n"
            f"Content-Length: {len(response_body)}\r\n"
            "\r\n" + response_body
        )
