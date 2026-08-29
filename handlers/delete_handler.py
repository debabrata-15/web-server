import os
import json

STATIC_DIR = "static"

def delete_handler(path):

    filename = os.path.join(STATIC_DIR, path.lstrip("/"))
    filename = os.path.normpath(filename)

    if not filename.startswith(STATIC_DIR):
        return "HTTP/1.1 403 Forbidden\r\n\r\n403 Forbidden"

    if not os.path.isfile(filename):

        response_body = json.dumps({"status": "error", "message": "resource not found"})
        return (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: application/json\r\n"
            f"Content-Length: {len(response_body)}\r\n"
            "\r\n" + response_body
        )

    os.remove(filename)
    response_body = json.dumps({"status": "ok", "message": f"{path} deleted"})
    return (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: application/json\r\n"
        f"Content-Length: {len(response_body)}\r\n"
        "\r\n" + response_body
    )
