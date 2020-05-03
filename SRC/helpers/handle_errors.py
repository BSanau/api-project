class APIError(Exception): # Create a class Error for our API
    statusCode = 500


class Error404(APIError): 
    statusCode = 404


def errorHandler(fn):
    def wrapper(*args,**kwargs):
        try:
            return fn(*args,**kwargs) # Try to do the function with those parameters
        except APIError as e: # if can't, I raise this error
            print(e)
            return {
                "status":"error",
                "message":str(e)
            }, e.statusCode
    wrapper.__name__ = fn.__name__ # Call the wraper with the function name
    return wrapper