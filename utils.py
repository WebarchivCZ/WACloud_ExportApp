from flask import json


def content_type_json(func):
    def wrapper():
        res = func()
        res.content_type = 'application/json'
        return res
    return wrapper


def exception_handler(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response
