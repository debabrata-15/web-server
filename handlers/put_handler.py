import json
import os

STATIC_DIR = "static"

def put_handler(path, body):

    filename = os.path.join(STATIC_DIR,path.lstrip("/"))
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

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return "HTTP/1.1 400 Bad Request\r\n\r\nInvalid JSON"

    with open(filename, "r+") as file:
        try:
            json_file = json.load(file)
        except json.JSONDecodeError:
             response_body = json.dumps({"status": "error", "message":"Stored filed is not JSON or is corrupted"})
        for key, value in data.items():
            json_file[key] = value
        file.seek(0)
        json.dump(json_file, file)
        file.truncate()
   
    response_body = json.dumps({"status": "ok", "data": f"{json_file}"})
    return (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: application/json\r\n"
        f"Content-Length: {len(response_body)}\r\n"
        "\r\n" + response_body
    )
