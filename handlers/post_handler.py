import json
import os

STATIC_DIR = "static"


def post_handler(path, body):

    filename = os.path.join(STATIC_DIR,path.lstrip("/"))
    filename = os.path.normpath(filename)

    if not filename.startswith(STATIC_DIR):
        return "HTTP/1.1 403 Forbidden\r\n\r\nForbidden"
    
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        response_body = json.dumps({"status": "error", "message": "Invalid JSON"})
        return (
            "HTTP/1.1 400 Bad Request\r\n"
            "Content-Type: application/json\r\n"
            f"Content-Length: {len(response_body)}\r\n"
            "\r\n" + response_body
        )

    with open(filename, "w") as fout:
        json.dump(data, fout)

    response_body = json.dumps({"status": "ok", "data": f"{data}"})
    return (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: application/json\r\n"
        f"Content-Length: {len(response_body)}\r\n"
        "\r\n" + response_body
    )