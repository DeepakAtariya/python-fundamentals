'''

1. Dunder Methods (Magic Methods)
You already know __init__ and __repr__. Here are the ones interviewers care about:

`
class Money:
    def __init__(self, amount, currency="AED"):
        self.amount = amount
        self.currency = currency
    
    def __repr__(self):
        return f"Money({self.amount}, {self.currency})"
    
    def __eq__(self, other):
        return self.amount == other.amount and self.currency == other.currency
    
    def __lt__(self, other):
        return self.amount < other.amount
    
    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)
    
    def __len__(self):
        return self.amount

a = Money(100)
b = Money(50)
print(a + b)      # Money(150, AED)
print(a == b)      # False
print(a > b)       # True
print(len(a))      # 100

`

Key dunder methods to know:

__init__     →  constructor
__repr__     →  string representation
__str__      →  user-friendly string
__eq__       →  ==
__lt__       →  
__gt__       →  >
__add__      →  +
__len__      →  len()
__hash__     →  makes object usable in sets/dict keys
__call__     →  makes object callable like a function

2. __call__ — making objects behave like functions:

`
class Multiplier:
    def __init__(self, factor):
        self.factor = factor
    
    def __call__(self, value):
        return value * self.factor

double = Multiplier(2)
print(double(5))    # 10 — calling object like a function!
print(double(100))  # 200

`

Exercise: Create a class LLMCostCalculator that:

Takes price_per_token in constructor
Has __call__ so you can use it like a function — pass token count, returns cost
Has __add__ to combine two calculators (adds their prices)
Has __repr__

'''

class LLMCostCalculator:
    def __init__(self, temp, model):
        self.temp = temp
        self.model = model
    
    def __call__(self, value):
        return self.temp * value
    
    def __repr__(self):
        return f"LLMCostCalculator({self.temp}, {self.model})"
        
    def __add__(self, other):
        return LLMCostCalculator(self.temp+other.temp, 'combined')
        
        

def main1():
    gpt4 = LLMCostCalculator(0.03, "gpt-4")
    mini = LLMCostCalculator(0.01, "gpt-4o-mini")

    print(gpt4(1000))       # 30.0 (cost for 1000 tokens)
    print(mini(1000))        # 10.0
    combined = gpt4 + mini
    print(combined)          # LLMCostCalculator(0.04, combined)
    print(combined(1000))    # 40.0

'''1. @property — Controlled Access to Attributes
Instead of writing get_name() / set_name() like Java, Python uses @property:'''

class User:
    def __init__(self, first, last):
        self.first = first
        self.last = last
    
    @property
    def full_name(self):
        return f"{self.first} {self.last}"
    
    @full_name.setter
    def full_name(self, value):
        first, last = value.split(" ")
        self.first = first
        self.last = last

    @full_name.getter
    def full_name(self, value):
        return f"{self.first} {self.last}"

def main2():
    u = User("Deepak", "Raju")
    print(u.full_name)          # "Deepak Raju" — no parentheses!
    u.full_name = "John Doe"    # calls the setter
    print(u.full_name)              # "John"
    

'''
Why use it?

Looks like an attribute but runs logic behind the scenes
Can add validation without breaking existing code
Read-only properties — just skip the setter

'''

class APIConfig:
    def __init__(self, key):
        self._key = key    # _ means "private by convention"
    
    @property
    def key(self):
        return self._key
    
    # No setter → read-only!

config = APIConfig("abc123")
# print(config.key)        # "abc123"
# config.key = "new"       # AttributeError! Read-only

'''
2. dataclasses — Less Boilerplate
Writing __init__, __repr__, __eq__ every time is tedious. dataclass generates them for you:

a = [1, 2, 3]
b = a
b.append(4)
print(a)  # [1, 2, 3, 4] — both point to same list

Same problem happens with class defaults:
The bug — mutable default shared:


@dataclass
class APIRequest:
    endpoint: str
    headers: dict = {}      # ❌ DANGER

r1 = APIRequest("/products")
r2 = APIRequest("/users")

r1.headers["Authorization"] = "Bearer abc"

print(r2.headers)  # {"Authorization": "Bearer abc"} 

r1 and r2 share the same {} object in memory. Changing one changes both.
Why does this happen?

# Python creates the default {} ONCE when class is defined
# Not once per instance

headers: dict = {}
#                ↑ this ONE dict object is shared by ALL instances

# It's like:
shared_dict = {}
r1.headers = shared_dict    # same object
r2.headers = shared_dict    # same object

The fix — default_factory creates a NEW dict each time:

@dataclass
class APIRequest:
    endpoint: str
    headers: dict = field(default_factory=dict)  # ✅ SAFE

r1 = APIRequest("/products")
r2 = APIRequest("/users")

r1.headers["Authorization"] = "Bearer abc"

print(r2.headers)  # {} — separate object, unaffected ✅

default_factory=dict tells Python: "call dict() fresh for every new instance."
Same applies to lists and sets:

# ❌ Wrong
tags: list = []
items: set = set()

# ✅ Correct
tags: list = field(default_factory=list)
items: set = field(default_factory=set)

Only immutable defaults are safe directly:

# These are fine — immutable, can't be changed
name: str = "default"
count: int = 0
rate: float = 0.5
active: bool = True
coords: tuple = (0, 0)

Quick rule: If the default is dict, list, or set → always use field(default_factory=...).


'''

# from dataclasses import dataclass, field

# @dataclass(frozen=True)
# class Sample:
#     abc: str
#     xyz: int
#     obj: dict = field(default_factory=dict)


# def main():
#     s1 = Sample("s",1, {"a":1})
#     s2 = Sample("q",2, {"a":2})
#     print(s1)
#     s1.obj['a']=2
#     print(s1)
#     print(s2)


'''
__slots__ — Memory Optimization
Normally, Python stores object attributes in a __dict__ (a dictionary). __slots__ replaces it with a fixed array:

# Normal — each object gets its own dict
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

u = User("Deepak", 28)
print(u.__dict__)   # {"name": "Deepak", "age": 28}

# With __slots__ — no dict, fixed structure
class User:
    __slots__ = ["name", "age"]
    
    def __init__(self, name, age):
        self.name = name
        self.age = age

u = User("Deepak", 28)
u.__dict__          # AttributeError! No dict
u.email = "test"    # AttributeError! Can't add new attributes

Normal          __slots__
Memory/object   ~300 bytes      ~100 bytes
Add new attrs   Yes             No
Speed           Slower          Faster

When to use: When you create millions of objects (like processing millions of API logs or LLM tokens).

With dataclass:

@dataclass(slots=True)    # Python 3.10+
class Token:
    text: str
    score: float


'''

'''
Exercise: Create a dataclass called LLMResponse that:

Has fields: model (str), content (str), tokens_used (int), cost (float)
Has a default model of "gpt-4o"
Is frozen (immutable)
Has a @property called cost_per_token that returns cost / tokens_used
'''

from dataclasses import dataclass

@dataclass(frozen=True)
class LLMResponse:
    content:str
    tokens_used:int
    cost:float
    model:str = "gpt-4o"
    
    @property
    def cost_per_token(self):
        return self.cost / self.tokens_used



def main():
    resp = LLMResponse(content="Hello world", tokens_used=50, cost=1.5)
    print(resp)                  # shows all fields
    print(resp.model)            # "gpt-4o"
    print(resp.cost_per_token)   # 0.03
    resp.content = "new"         # should raise error (frozen)
