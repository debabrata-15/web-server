import json
from routes import ROUTES


def put_handler(path, body):
    filename = ROUTES.get(path)
    if not filename:
        return "HTTP/1.1 404 Not Found\r\n\r\n404 File Not Found"

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return "HTTP/1.1 400 Bad Request\r\n\r\nInvalid JSON"

    try:
        with open(filename, "r+") as file:
            json_file = json.load(file)
            for key, value in data.items():
                json_file[key] = value
            file.seek(0)
            json.dump(json_file, file)
            file.truncate()
    except FileNotFoundError:
        return "HTTP/1.1 404 Not Found\r\n\r\n404 File Not Found"

    response_body = json.dumps({"status": "ok", "data": json_file})
    return (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: application/json\r\n"
        f"Content-Length: {len(response_body)}\r\n"
        "\r\n" + response_body
    )
