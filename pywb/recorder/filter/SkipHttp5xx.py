'''
Created on Aug 1, 2024

@author: lisias
'''

from requests import Request, Response

class SkipDefaultFilter(object):
    def skip_request(self, path:str, req:Request):
        return False

    def skip_response(self, path:str, req:Request, resp:Response, params):
        return  5 == (resp.status_code/100)
