from flask import Flask, jsonify, request, Response
import json
app = Flask(__name__)
books = [{
    'name': 'Green eggs and ham',
    'price': 8.5,
    'isbn': 97866552323
}, 
{
    'name': 'The cat in the hat',
    'price': 6.99,
    'isbn': 653258225
}]

#GET /books
@app.route("/books")
def get_books():
    ## we use jsonify to convert a python list to json file
    return jsonify({'books': books})

#GET /books/
@app.route("/books/<int:isbn>")
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                'name': book['name'],
                'price': book['price']
            }
    return jsonify(return_value)

#POST /books
def validBookObject(bookObject):
    if ('name' and 'price' and 'isbn'  in bookObject):
        print('entro a validBook')
        return True
    else:
        return False

@app.route("/books", methods=['POST'])
def add_book():
    request_data = request.get_json()
    if (validBookObject(request_data)):
        print('imprime el request data ', request_data)
        new_book ={
            'name': request_data['name'],
            'price': request_data['price'],
            'isbn': request_data['isbn']
        }
        books.insert(0, new_book)
        # First parameter is a response body, second parameter is the status code, third is the content type header that will be sent
        response = Response('',201, mimetype='application/json')
        response.headers['Location'] = '/books/' + str(new_book['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            'error': 'Invalid book obhect passed in request',
            'helpString': "Data passed in similiar to this {'name': 'F','price': '6.99','isbn': 012345}"
        }
        ## invalidBookObjectErrorMsg is a dictionary and  we need conver to json
        response = Response(json.dumps(invalidBookObjectErrorMsg),status=400, mimetype='application/json')
        return response
    

#PUT

def valid_put_request_data(request_data):
    if ('name' and 'price' in request_data):
        print('entro a validBook')
        return True
    else:
        return False

@app.route("/books/<int:isbn>", methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    if(not valid_put_request_data(request_data)):
        invalidBookObjectErrorMsg = {
            'error': 'Book with the ISBN number that was provided was not found',        }
        ## invalidBookObjectErrorMsg is a dictionary and  we need conver to json
        response = Response(json.dumps(invalidBookObjectErrorMsg),status=400, mimetype='application/json')
        return response
    
    new_book ={
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': isbn
    }
    i = 0;
    for book in books:
        currentIsbn = book['isbn']
        if currentIsbn == isbn:
            books[i] = new_book
        i +=1
    response = Response('', status=204)
    return response


@app.route("/books/<int:isbn>", methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    update_book = {}
    if('name' in request_data):
        update_book['name'] = request_data['name']
    if('price' in request_data):
        update_book['price'] = request_data['price']
    for book in books:
        if book['isbn'] == isbn:
            book.update(update_book)
         
    response = Response('', status=204)
    response.headers['Location'] = '/books/' + str(isbn)
    return response

@app.route("/books/<int:isbn>", methods=['DELETE'])
def delete_book(isbn):
    i=0;
    for book in books:
        if book['isbn'] == isbn:
            books.pop(i)
            response = Response('', status=204)
            return response
        i += 1
        invalidBookObjectErrorMsg = {
            'error': 'Book with the ISBN number that was provided was not found, so therefore unable to delete',
        }
        ## invalidBookObjectErrorMsg is a dictionary and  we need conver to json
        response = Response(json.dumps(invalidBookObjectErrorMsg),status=400, mimetype='application/json')
        return response
    
## app run is not necesary when use flask run
app.run(port=5000)