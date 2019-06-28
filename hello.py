from flask import Flask, jsonify, request, Response
import json
from settings import  *
from BookModel import *


#GET /books
@app.route("/books")
def get_books():
    ## we use jsonify to convert a python list to json file
    return jsonify({'books': Book.get_all_books()})

#GET /books/
@app.route("/books/<int:isbn>")
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    return jsonify(return_value)


def validBookObject(bookObject):
    if ('name' and 'price' and 'isbn'  in bookObject):
        print('entro a validBook')
        return True
    else:
        return False
#POST /books
@app.route("/books", methods=['POST'])
def add_book():
    request_data = request.get_json()
    if (validBookObject(request_data)):
        Book.add_book(request_data['name'],request_data['price'],request_data['isbn'])
        # First parameter is a response body, second parameter is the status code, third is the content type header that will be sent
        response = Response('',201, mimetype='application/json')
        response.headers['Location'] = '/books/' + str(request_data['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            'error': 'Invalid book obhect passed in request',
            'helpString': "Data passed in similiar to this {'name': 'F','price': '6.99','isbn': 012345}"
        }
        ## invalidBookObjectErrorMsg is a dictionary and  we need conver to json
        response = Response(json.dumps(invalidBookObjectErrorMsg),status=400, mimetype='application/json')
        return response
    
def valid_put_request_data(request_data):
    if ('name' and 'price' in request_data):
        print('entro a validBook')
        return True
    else:
        return False

#PUT
@app.route("/books/<int:isbn>", methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    if(not valid_put_request_data(request_data)):
        invalidBookObjectErrorMsg = {
            'error': 'Book with the ISBN number that was provided was not found',        }
        ## invalidBookObjectErrorMsg is a dictionary and  we need conver to json
        response = Response(json.dumps(invalidBookObjectErrorMsg),status=400, mimetype='application/json')
        return response
    
    Book.replace_book(isbn, request_data['name'], request_data['price'])
    response = Response('', status=204)
    return response

def valid_patch_request_data(request_data):
    if ('name' or 'price' in request_data):
        return True
    else:
        return False

#PATCH
@app.route("/books/<int:isbn>", methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    if(not valid_patch_request_data(request_data)):
        invalidBookObjectErrorMsg = {
            'error': 'Book with the ISBN number that was provided was not found',        }
        ## invalidBookObjectErrorMsg is a dictionary and  we need conver to json
        response = Response(json.dumps(invalidBookObjectErrorMsg),status=400, mimetype='application/json')
        return response
    
    if('name' in request_data):
        Book.update_book_name(isbn, request_data['name'])
    if('price' in request_data):
        Book.update_book_price(isbn, request_data['price'])
    response = Response('', status=204)
    response.headers['Location'] = '/books/' + str(isbn)
    return response

#DELETE
@app.route("/books/<int:isbn>", methods=['DELETE'])
def delete_book(isbn):
    if(Book.delete_book(isbn)):
        response = Response('', status=204)
        response.headers['Location'] = '/books/' + str(isbn)

    invalidBookObjectErrorMsg = {
        'error': 'Book with the ISBN number that was provided was not found, so therefore unable to delete',
    }
    ## invalidBookObjectErrorMsg is a dictionary and  we need conver to json
    response = Response(json.dumps(invalidBookObjectErrorMsg),status=404, mimetype='application/json')
    return response
    
## app run is not necesary when use flask run
app.run(port=5000)