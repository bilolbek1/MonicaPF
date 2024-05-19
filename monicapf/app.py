from webob import Request
from parse import parse
import inspect
import requests
import wsgiadapter
from jinja2 import Environment, FileSystemLoader
import os
from whitenoise import WhiteNoise
from .middleware import Middleware
from .response import Response



class Monica:
    def __init__(self):
        self.routes = dict()
        
        self.whitenoise = WhiteNoise(self.wsgi_app, root='static', prefix='/static')

        self.middleware = Middleware(self)

        self.exemption_hanlder = None

    def __call__(self, environ, start_response):
        path_info = environ["PATH_INFO"]

        if path_info.startswith('/static'):
            return self.whitenoise(environ, start_response)

        return self.middleware(environ, start_response)
    
    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        
        return response(environ, start_response)
    
    def handle_request(self, request):
        response = Response()

        handler_data, kwargs = self.find_handler(request)
        
        if handler_data is not None:
            handler = handler_data['handler']
            allowed_methods = handler_data['allowed_methods']

            if inspect.isclass(handler):
                handler = getattr(handler() , request.method.lower(), None)
                if handler is None:
                    return self.method_not_allowed(response)
            else:
                if request.method.lower() not in allowed_methods:
                    return self.method_not_allowed(response)
            
            try:
                handler(request, response, **kwargs)
            except Exception as e:
                if self.exemption_hanlder is not None:
                    self.exemption_hanlder(request, response, e)
                else:
                    raise e


        else:
            self.default_response(response)

        return response        
    
    def method_not_allowed(self, response):
        response.status_code = 405
        response.text = 'Method not Allowed'
        return response
           
    
    def find_handler(self, request):
        for path, handler_data in self.routes.items():
            parsed_result = parse(path, request.path)

            if parsed_result is not None:
                return handler_data, parsed_result.named
                
        return None, None

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not found"
        
    def add_route(self, path, handler, allowed_methods=None):
        assert path not in self.routes, 'Duplicate error. Change URL'
        if allowed_methods is None:
            allowed_methods = ['get', 'put', 'patch', 'post', 'delete', 
                'options', 'head', 'connect', 'trace']

        self.routes[path] = {'handler': handler, 'allowed_methods': allowed_methods}

    def route(self, path, allowed_methods=None):
        def wrapper(handler):
            self.add_route(path, handler, allowed_methods)
            return handler
        
        return wrapper
    
    def test_session(self):
        session = requests.Session()
        session.mount('http://testserver/', wsgiadapter.WSGIAdapter(self))
        return session

    def template(self, template_name, context):
        template_env = Environment(
            loader=FileSystemLoader(os.path.abspath('templates'))
        )
        if context is None:
            context = {}
        
        return template_env.get_template(template_name).render(**context)    


    def add_middleware(self, middleware_cls):
        self.middleware.add(middleware_cls)

    def add_exemption_handler(self, handler):
        self.exemption_hanlder = handler    