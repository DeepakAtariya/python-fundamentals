# def f():  
#     name = "deepak"
#     print(name)

#     age = 25
#     print(age)

#     profit = 4.8    
#     print(profit)

#     is_active = True
#     print(is_active)

#     # array
#     fruits = ["apple", "banana", "cherry"]
#     print(fruits)

#     # dictionary
#     candidate = {"name":"deepak", "skills":"python", "last employer":"google"}
#     print(candidate)

#     # tuple
#     numbers = (1, 2, 3, 4, 5)
#     print(numbers)

#     # set
#     unique_ids = {22,12,22,22}
#     print(unique_ids)
    
#     print(3**2)
# f()

# results = [ i**2 if i % 2 == 0 else i**3 for i in range(5) ]

# # for i in range(5):
# #     if(i%2==0):
# #         results.append(i**2)
        
# print(results) 

# # results1 = [i**2 for i in range(5) if i%2==0]
        
# # print(results1)             
# # d = 
# print([ i*3 for i in range(10) if i % 2 != 0  ])



# def build_api_uri(base_uri, version="v1", **kwargs):
#     url = base_uri+'/'+version
#     if kwargs:
#         first = True
#         for key, value in kwargs.items():
#             if not first:
#                 url = f"{url}&{key}={value}"
#             else:
#                 url = f"{url}?{key}={value}"
#                 first = False
#     return url

# def build_api_uri(base_uri, version="v1", **kwargs):
#     url = base_uri+'/'+version
#     if kwargs:
#         params = "&".join([f"{key}={value}" for key, value in kwargs.items()])
#         url = f"{url}?{params}" 
#     return url

# print(build_api_uri('abc.com', page=1, pagesize=100, page1=1, pagesize1=100))

# class APIClient:
#     def __init__(self, host, api_key="noapi"):
#         self.host = host
#         self.apiKey = api_key
#         pass
    
#     def get(self, path):
#         if not path.startswith("/"):
#             raise InternalError(f"Path must start with '/', got: '{path}'")
#         url = f"{self.host}{path}"
#         headers = {"Authorization": f"Bearer {self.apiKey}"}
#         return {"url":url, "headers":headers}
    
#     def __repr__(self):
#         return f"APIClient({self.host})"
    
    
# class InternalError(ValueError):
#     pass


# client = APIClient("https://api.noon.com", api_key="abc123")
# client.get("products")  # Should raise ValueError
# client.get("/products") # Should work fine

