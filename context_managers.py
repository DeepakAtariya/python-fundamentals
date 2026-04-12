'''
What happens behind the scenes:

with calls __enter__ → sets things up
Your code runs inside the block
with calls __exit__ → cleans up (always, even on errors)

Think of it like a sandwich:

`__enter__  →  top bread (setup)
your code  →  filling
__exit__   →  bottom bread (cleanup)`


Why it matters for this role: Every time you connect to a database, 
call OpenAI API, or open a file in production — 
you need guaranteed cleanup. Context managers handle that.

'''


# class DBConnection:
#     def __init__(self, host):
#         self.host = host
    
#     def __enter__(self):
#         print(f"Connected to {self.host}")
#         return self  # this becomes the 'as' variable
    
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         print(f"Disconnected from {self.host}")

# with DBConnection("localhost") as db:
#     print("Running query")

# Connected to localhost
# Running query
# Disconnected from localhost


'''
__exit__ gets 3 arguments — error info if something went wrong:

exc_type → error class (e.g., ValueError)
exc_val → error message
exc_tb → traceback
All three are None if no error happened

'''

#  Now your exercise: Write APISession class:

# class APISession:
#     def __init__(self, api_key):
#         self.api_key = api_key
    
#     def __enter__(self):
#         print("Session started")
#         return self
    
#     def call(self, path):
#         print(f"{path} with key {self.api_key}")
    
#     def __exit__(self, exc_type, exc, tb):
#         print("Session closed")

# def main():
#     with APISession("abc123") as session:
#         session.call("/products")

'''

contextlib — Context Managers Without Classes
Instead of writing a full class with __enter__ and __exit__, you can use a decorator:

'''

# from contextlib import contextmanager

# @contextmanager
# def api_session(api_key):
#     # __enter__ part — setup
#     print("Session started")
    
#     yield api_key    # this value goes to 'as' variable
    
#     # __exit__ part — cleanup
#     print("Session closed")

# with api_session("abc123") as key:
#     print(f"Calling API with {key}")

# Session started
# Calling API with abc123
# Session closed


from contextlib import contextmanager
import time 


@contextmanager
def timer(name):
    start_time = time.time()
    print(f"{name} started")
    try:
        yield
    finally:
        print(f"{name} finished in {time.time()-start_time:.3f}s")
    

def main():
    with timer("API call"):
        time.sleep(1)
    