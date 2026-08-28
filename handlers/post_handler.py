import json
from routes import ROUTES


def post_handler(path, body):
    filename = ROUTES.get(path)
    if not filename:
        return "HTTP/1.1 404 Not Found\r\n\r\n404 Page Not Found"

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return "HTTP/1.1 400 Bad Request\r\n\r\nInvalid JSON"

    with open(filename, "w") as fout:
        json.dump(data, fout)

    response_body = json.dumps({"status": "ok", "data": data})
    return (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: application/json\r\n"
        f"Content-Length: {len(response_body)}\r\n"
        "\r\n" + response_body
    )