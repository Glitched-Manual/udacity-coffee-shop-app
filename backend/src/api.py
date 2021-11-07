import os, sys
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# to reset the db
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def get_drinks():
    
    try:
        
        drinks = Drink.query.all()
        
        if len(drinks) == 0:
            print("No drinks found")
            abort(404)
        
        # format the return drinks with short
        #all_drinks = [drink.short() for drink in drinks]
        all_drinks = []
        
        #print(drinks[0].id)
        
        
        for drink in drinks:
            
            print(type(drink.recipe))
            
            drink_param = {
                'title': drink.title,
                'recipe': drink.recipe
            }
            
        
            all_drinks.append(drink_param)
        
        return jsonify({
            'success' : True,
            'drinks' : [drink.short() for drink in drinks]

        })
    
    except Exception as e:
        print(e)
        abort(404)

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    
    try:
        
        drinks = Drink.query.all()
        
        if len(drinks) < 1:
            abort(404)
        
        # format the return drinks with short

        return jsonify({
            'success' : True,
            'drinks' : [drinks.long() for drink in drinks]

        })
    
    except:
        abort(404)

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=["POST"])
@requires_auth('post:drinks')
def create_drink(jwt): 
    
    try:
        body = request.get_json()
        #print(f'{body}')
        #sprint(f'body.find(\'recipe\') = {body.find("recipe")}')
        if not ('title' in body and 'recipe' in body):
                print("failed")
                abort(422)

        drink_title = body.get('title')
        #print(f'{drink_title}')
        drink_recipe = body.get('recipe')
        
        #print(f'878787 drink_title ={drink_title}\n drink_title = {drink_recipe} 67676')

        new_drink = Drink(title=drink_title, recipe=json.dumps(drink_recipe))
        new_drink.insert()
        return jsonify({
            'success': True,
            'drink': new_drink.long()
    })


    except Exception as e:
        print('ERROR: ', str(e))
        abort(422)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404
'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(401)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 401,
                    "message": "resource not found"
                    }), 401