# Decorators

def log_call(function):
    def wrapper(*args, **kwargs):
        print("calling the function")
        result = function(*args, *kwargs)
        print("finished the function")
        return result
    return wrapper

@log_call
def sum(a, b):
    return a+b

print(sum(1,2))

# Decorator task : Exercise: Write a decorator called timer that prints how long a function takes to execute.

import time

from functools import wraps

def timer(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = function(*args, **kwargs)
        end_time = time.time() - start_time
        print(f"{function.__name__} executed in {end_time:.3f}s")
        return result
    return wrapper

@timer
def slow_function():
    for i in range(1000000):
        pass

print(slow_function.__name__)
slow_function()