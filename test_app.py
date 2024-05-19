import pytest
from conftest import app, test_client
from monicapf.middleware import Middleware



def test_route_is_work(app):
    @app.route('/home')
    def home(req, res):
        res.text = 'Hello home page'


def test_route_duplicate_is_work(app):
    @app.route('/home')
    def home(req, res):
        res.text = 'Hello Home'

    with pytest.raises(AssertionError):
        @app.route('/home')
        def home1(req, res):
            res.text = 'Hello Home'


def test_route_parametrize_client(app, test_client):
    @app.route('/home/{name}')
    def hello(req, res, name):
        res.text = f'Hello {name}'

    response = test_client.get('http://testserver/home/Bilol')
    assert response.text == 'Hello Bilol'


def test_route_client(app, test_client):
    @app.route('/home')
    def home(req, res):
        res.text = f'Home page'

    assert test_client.get('http://testserver/home').text == 'Home page'    



def test_class_route_is_work(app, test_client):
    @app.route('/cars')
    class Cars:
        def get(self, req, res):
            res.text = 'Cars list here'

        def post(self, req, res):
            res.text = 'Car created'    

    get_res = test_client.get('http://testserver/cars')        
    post_res = test_client.post('http://testserver/cars')        
    put_res = test_client.put('http://testserver/cars')        

    assert get_res.text == 'Cars list here'
    assert post_res.text == 'Car created'
    assert put_res.status_code == 405
    assert put_res.text == 'Method not Allowed'


def test_default_response(app, test_client):
    response = test_client.get("http://testserver/none")
    
    assert response.text == 'Not found'   
    assert response.status_code == 404 


def test_new_handler_route(app, test_client):
    def new_handler(req, res):
        res.text = 'New handler'

    app.add_route('/new-handler', new_handler)  

    assert test_client.get('http://testserver/new-handler').text == 'New handler'
 
 
def test_template_is_work(app, test_client):
    @app.route('/test-template')
    def template(req, res):
        res.body = app.template(
            'test.html',
            context = {'title': 'Template working', 'name': 'Bilol'}
        )
    
    response = test_client.get('http://testserver/test-template')    
    
    assert 'Bilol' in response.text
    assert 'Template working' in response.text
    assert 'text/html' in response.headers['Content-Type']    
                
                
def test_static_files(test_client):
    response = test_client.get('http://testserver/static/style.css')
    
    assert response.text == 'body{\n    background-color: burlywood;\n} '


def test_check_middleware(app, test_client):
    process_request_called = False
    process_response_called = False

    class Simple_middleware(Middleware):
        def __init__(self, app):
            super().__init__(app)

        def process_request(self, req):
            nonlocal process_request_called
            process_request_called = True

        def process_response(self, req, res):
            nonlocal process_response_called
            process_response_called = True

    app.add_middleware(Simple_middleware)        

    @app.route('/home')
    def home(req, res):
        res.text = 'Home page'        

    test_client.get('http://testserver/home')

    assert process_request_called is True
    assert process_response_called is True


def test_allowed_methods(app, test_client):
    @app.route('/home', allowed_methods=['get'])
    def home(req, res):
        if req.method == 'GET':
            res.text = 'Get response'
        elif req.method == 'POST':
            res.text = 'Method not Allowed'

    get_response = test_client.get('http://testserver/home')            
    post_response = test_client.post('http://testserver/home')

    assert get_response.text == 'Get response'
    assert post_response.text == 'Method not Allowed'            


def test_html_response_helper(app, test_client):
    @app.route('/html')
    def html(req, res):
        res.body = app.template(
            'test.html',
            context = {'title': 'Template working', 'name': 'Bilol'}
        )
    
    response = test_client.get('http://testserver/html')

    assert 'text/html' in response.headers['Content-Type']
    assert 'Template working' in response.text
    assert 'Bilol' in response.text


def test_json_response_helper(app, test_client):
    @app.route('/json')
    def json(req, res):
        res.json = {'name': 'name', 'body': 'body'}

    response = test_client.get('http://testserver/json')
    response_data = response.json()

    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['name'] == 'name'

def test_text_response_helper(app, test_client):
    @app.route('/text')
    def text(req, res):
        res.text = 'Text'

    response = test_client.get('http://testserver/text')        

    assert 'text/plain' in response.headers['Content-Type']
    assert response.text == 'Text'


def test_exemption_handler(app, test_client):
    def on_exepmtion(req, res, exe):
        res.text = 'Something wrong here !'

    app.add_exemption_handler(on_exepmtion)

    @app.route('/exemption')
    def exemption(req, res):
        raise AttributeError('Something exeptions')
    
    response = test_client.get('http://testserver/exemption')

    assert response.text == 'Something wrong here !'
    