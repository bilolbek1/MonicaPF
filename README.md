# MonicaPF: Python Web Framework built for learning purposes


![Purpose](https://img.shields.io/badge/:learning-green)
![PyPI - Version](https://img.shields.io/pypi/v/:monicapf)


MonicaPF it is python web framework

It is WSGI Framework and can be used with any WSGI application server such as Gunicorn


# Installation
```shell
pip install monicapf
```

# How To Use It:


### Basic Usage:

    ```python
    from monicapf.app import Monica


    app = Monica()      


# Add Allowed Methods:
    @app.route('/home', allowed_methods=['get'])
    def home(request, response):
        if request.method == 'GET':
            response.text = 'Hello this is home page'
        elif request.method == 'POST':
            response.text = 'POST '


# Simple Route:
    @app.route('/about')
    def about(request, response):
        response.text = 'Hello this is about page'    
        

# Parametrize Route:
    @app.route('/hello/{name}')
    def hello(request, response, name):
        response.text = f"Just say hello. Hello {name}"    


# Class Based Handlers:
    @app.route('/books')
    class Book:
        def get(self, request, response):
            response.text = 'Books GET request'

        def post(self, request, response):
            response.text = 'Books POST request'


    def new_handler(req, res):
        res.text = 'New handler'

    app.add_route('/new-handler', new_handler)




# Json data:
    @app.route('/json')
    def json(req, res):
        res.json = {
            'name': 'Request',
            'Body': 'Json response',
        }
    ```

# Add Template
    Create "templates" folder and save inside that folder htmls

    ```python
    @app.route('/template')
    def template(req, res):
        res.body = app.template(
            'home.html',
            context={'name': 'Bilol', 'title': 'Template working'}
        ) 
    ```       

# Add Static Files
    Create "static" folder and save inside that folder static files

    
    ```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>{{title}}</title>

<link href="/static/main.css" rel="stylesheet" type="text/css">
</head>

<body>
    <h1>{{body}}</h1>
    <p>This is a paragraph</p>
</body>
</html>
    ```



# MiddleWare

You can create custom middleware classes by inheriting from the monicapf.middleware.Middleware class and overriding its two methods that are called before and after each request:

```python
from monicapf.api import API
from minocapf.middleware import Middleware


app = API()


class SimpleCustomMiddleware(Middleware):
    def process_request(self, req):
        print("Before dispatch", req.url)

    def process_response(self, req, res):
        print("After dispatch", req.url)


app.add_middleware(SimpleCustomMiddleware)
```


# Unit Tests

The recommended way of writing unit tests is with pytest. There are two built in fixtures that you may want to use when writing unit tests with MonicaPF. The first one is app which is an instance of the main API class:

```python
def test_route_overlap_throws_exception(app):
    @app.route("/")
    def home(req, resp):
        resp.text = "Welcome Home."

    with pytest.raises(AssertionError):
        @app.route("/")
        def home2(req, resp):
            resp.text = "Welcome Home2."
```

The other one is client that you can use to send HTTP requests to your handlers. It is based on the famous requests and it should feel very familiar:

```python
    def test_parameterized_route(app, client):
    @app.route("/{name}")
    def hello(req, resp, name):
        resp.text = f"hey {name}"

    assert client.get("http://testserver/MonicaPF").text == "hey MonicaPF"
```