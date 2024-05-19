from monicapf.app import Monica


app = Monica()   


@app.route('/home', allowed_methods=['get'])
def home(request, response):
    if request.method == 'GET':
        response.text = 'Hello this is home page'
    elif request.method == 'POST':
        response.text = 'POST '



@app.route('/about')
def about(request, response):
    response.text = 'Hello this is about page'    
    

@app.route('/hello/{name}')
def hello(request, response, name):
    response.text = f"Just say hello. Hello {name}"    


@app.route('/books')
class Book:
    def get(self, request, response):
        response.text = 'Books GET request'

    def post(self, request, response):
        response.text = 'Books POST request'


def new_handler(req, res):
    res.text = 'New handler'

app.add_route('/new-handler', new_handler)




@app.route('/template')
def template(req, res):
    res.body = app.template(
        'home.html',
        context={'name': 'Bilol', 'title': 'Template working'}
    )    

@app.route('/json')
def json(req, res):
    res.json = {
        'name': 'Bilolbek',
        'Body': 'Json response',
    }    