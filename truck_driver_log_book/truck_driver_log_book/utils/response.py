from rest_framework.response import Response


def success_response(detail:str=None, data:dict=None, status=200, append_json:dict={}):
    """generic success response"""

    return json_response(detail=detail, data=data, status=status, append_json=append_json)

def bad_request_response(detail:str=None, data:dict=None, append_json:dict={}):
    return json_response(detail=detail, data=data, status=400, append_json=append_json)

def json_response(detail:str=None, data:dict=None, status:int=200, append_json:dict={}):
    """return json http response"""

    json = { 'detail': detail, 'data': data}
    json.update(append_json)

    return Response(json, status)
