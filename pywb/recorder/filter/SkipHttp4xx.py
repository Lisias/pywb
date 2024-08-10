'''
Created on Aug 1, 2024

@author: lisias
'''

from requests import Request, Response

class SkipFilter(object):
    def skip_request(self, path:str, req_headers):
        return False

    def skip_response(self, path:str, req:Request, resp:Response, params):
        r = 4 == (resp.status_code//100)
        return r
