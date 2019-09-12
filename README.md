# Cruet
Cruet is a simple toolkit for building microservices with flask. It works with both, function based and class based views.

It is built on top of:
- flask
- marshmallow
- webargs

## Example
```python
from flask import Flask
from marshmallow import fields
from cruet import Cruet, use_args, ApiError, ApiResponse

app = Flask(__name__)
cruet = Cruet(app)

@app.route('/')
@use_args({'name': fields.Str(required=True)})
def index(args):
    if len(args['name']) < 3:
        raise ApiError('Name has to be at least 3 characters', 400)
    
    return ApiResponse({'msg': 'Hello ' + args['name']})

if __name__ == '__main__':
    app.run()

# curl http://localhost:5000/?name='World'
# {"data": {"msg": "Hello World"}}
```


## Installation
Cruet is available from PyPi
```
pip install cruet
```

## Response
Cruet provides the `ApiResponse` class for building json responses that are formatted consistently across all endpoints.


## Error Handling
Cruet provides the `ApiError` exception class for raising an exception and returning a formatted json response with the error message. 


## Input Validation
Cruet uses the excellent [webargs](https://github.com/marshmallow-code/webargs) library for validating HTTP requests. It integrates the library in a very transparent way, which doesn't change the way webargs is being used and their [documentation](https://webargs.readthedocs.io/en/latest) should be used as the reference.
Cruet only adds its own error handling to webargs and provides convenient decorators for different HTTP request input types.  

For general use, the `use_args` and `use_kwargs` decorators can be used. The example above uses `use_args` to check for a parameter called `name`. The webargs library uses the concept of [locations](https://webargs.readthedocs.io/en/latest/quickstart.html#request-locations) to define where it should look for the HTTP request data.
Cruet provides a few convenient decorators for the most common locations.

### Query
The `query` decorator looks for the data as part of the arguments in the URL query string.

```python
from cruet import query

@app.route('/')
@query({'name': fields.Str(required=True)})
def index(args):
    if len(args['name']) < 3:
        raise ApiError('Name has to be at least 3 characters', 400)
    
    return ApiResponse({'msg': 'Hello ' + args["name"]})

# curl http://localhost:5000/?name='World'
# {"data": {"msg": "Hello World"}}
``` 

### Body
The `body` decorator looks for json formatted data in the request body.

```python
from cruet import body

@app.route('/', methods=['POST'])
@body({'name': fields.Str(required=True)})
def index(args):
    if len(args['name']) < 3:
        raise ApiError('Name has to be at least 3 characters', 400)
    
    return ApiResponse({'msg': 'Hello ' + args["name"]})

# curl -d '{"name":"World"}' -H "Content-Type: application/json" -X POST http://localhost:5000
# {"data": {"msg": "Hello World"}}
``` 

### Form
The `form` decorator looks for form-urlencoded data.

```python
from cruet import form

@app.route('/', methods=['POST'])
@form({'name': fields.Str(required=True)})
def index(args):
    if len(args['name']) < 3:
        raise ApiError('Name has to be at least 3 characters', 400)
    
    return ApiResponse({'msg': 'Hello ' + args["name"]})

# curl -d "name=World" -X POST http://localhost:5000
# {"data": {"msg": "Hello World"}}
``` 
