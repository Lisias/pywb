'''
Created on Aug 1, 2024

@author: lisias
'''
import logging
from requests import Request, Response

class SkipFilter(object):
    def skip_request(self, path:str, req_headers):
        return False

    def skip_response(self, path:str, req:Request, resp:Response, params):
        r = 4 == (resp.status_code//100)
        if r:
            logging.debug("Skiping response for {:s}".format(resp.url))
        return r
