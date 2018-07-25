import os
from swift.common.swob import Request, Response
from swift.common.utils import split_path
from hashlib import md5
import cStringIO


class Cache:
    '''
    Class to interact with the cache
    '''

    def __init__(self, cache_dir):
        self.cache_dir = cache_dir

    def route_cache_request(self, req):
        if req.method == 'PUT':
            resp = self.write_to_cache(req)
        elif req.method == 'GET':
            resp = self.read_from_cache(req)
        return resp

    def write_to_cache(self, req):
        version, account, container, obj = split_path(req.path, 1, 4, True)
        if account and container and obj:
            '''
            Can only cache objects lol
            '''
            print(version, account, container, obj)
            '''
            Now check whether account and container directory exists in the cache_dir else create them
            '''
            self.create_or_check_dirs(account, container)
            write_path = self.cache_dir + '/' + account + '/' + container + '/' + obj
            resp = self.write_obj_to_cache(req, write_path)
            return resp

    def create_or_check_dirs(self, account, container):
        account_dir = self.cache_dir + '/' + account
        if not os.path.exists(account_dir):
            os.makedirs(account_dir)
        container_dir = account_dir + '/' + container
        if not os.path.exists(container_dir):
            os.makedirs(container_dir)

    def build_get_response(self, req, data):
        resp = Response(request=req)
        resp.accept_ranges = 'bytes'
        resp.body = data
        resp.status = 200
        return resp

    def get_data_from_cache(self, req, read_path):
        with open(read_path, 'r') as fp:
            data = fp.read()
            print("1038912098210{}".format(data))
            return self.build_get_response(req, data)

    def read_from_cache(self, req):
        version, account, container, obj = split_path(req.path, 1, 4, True)
        if account and container and obj:
            read_path = self.cache_dir + '/' + account + '/' + container + '/' + obj
            if os.path.exists(read_path):
                resp = self.get_data_from_cache(req, read_path)
                return resp
            else:
                return None
        else:
            return None

    def write_obj_to_cache(self, req, write_path):

        def reader():
            body = req.environ['wsgi.input'].read()
            req.environ['wsgi.input'] = cStringIO.StringIO(body)
            return body
        '''
        If object exists check if the object is updated
        '''
        if os.path.exists(write_path):
            with open(write_path, 'w+') as fp:
                curr_data = fp.read()
                new_data = reader()
                if md5().update(curr_data) == md5().update(new_data):
                    print("10792319871029)(@#!^)(&^)(#&!)^($&^)@(&$^)@&#^)@&#^")
                    return self.build_get_response(req, 'Object is already present')
                else:
                    fp.write(new_data)
                    return None
        else:
            with open(write_path, 'w+') as fp:
                new_data = reader()
                fp.write(new_data)
                return None
