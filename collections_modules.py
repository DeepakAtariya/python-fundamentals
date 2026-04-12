# '''
# collections module
#  │
#  ├── defaultdict(dict)     → hash table + auto default
#  ├── Counter(dict)         → hash table + counting
#  ├── OrderedDict(dict)     → hash table + order tracking
#  ├── deque                 → doubly-linked list
#  └── namedtuple            → immutable struct (like lightweight class)
 
 
# Python dict — the foundation

# All three (defaultdict, Counter, OrderedDict) are built ON TOP of dict. Python's dict internally uses a hash table.

# dict
#  ├── defaultdict  (dict + default factory)
#  ├── Counter      (dict + counting methods)
#  └── OrderedDict  (dict + insertion order tracking)
 
# d = {"name": "Deepak"}

# # Step 1: hash("name") → some integer like 2314567
# # Step 2: index = hash_value % table_size → position in array
# # Step 3: store ("name", "Deepak") at that position

# # Lookup: same process — hash key → find position → O(1)

# # That's why dict lookups are O(1) — it doesn't search through everything, it jumps directly to the position.

# defaultdict — what's different?
# Regular dict throws KeyError on missing key. defaultdict overrides one method — __missing__:

# '''

# # Regular dict internally:
# class dict:
#     def __getitem__(self, key):
#         if key not in self.data:
#             raise KeyError(key)      # crashes
#         return self.data[key]

# # defaultdict internally:
# class defaultdict(dict):
#     def __init__(self, factory):
#         self.factory = factory       # int, list, set, etc.
    
#     def __missing__(self, key):
#         value = self.factory()       # creates default: int()=0, list()=[]
#         self[key] = value            # stores it
#         return value                 # returns it
    

# counts = defaultdict(int)
# counts["apple"] += 1

# # Behind the scenes:
# # 1. "apple" not found
# # 2. __missing__ called
# # 3. int() creates 0
# # 4. counts["apple"] = 0
# # 5. counts["apple"] += 1 → now it's 1

# '''
# Counter — what's different?
# Counter is a dict where values are always counts. It adds special methods on top:
# '''

# # Counter internally:
# class Counter(dict):
#     def __init__(self, iterable):
#         for item in iterable:
#             self[item] = self.get(item, 0) + 1
    
#     def most_common(self, n):
#         return sorted(self.items(), key=lambda x: x[1], reverse=True)[:n]
    
#     def __missing__(self, key):
#         return 0    # missing key returns 0, not KeyError

    
# c = Counter(["a", "a", "b"])
# # Internally: {"a": 2, "b": 1}

# c["z"]  # returns 0, no error (like defaultdict(int))

# # Counter also supports math:
# c1 = Counter(["a", "a", "b"])
# c2 = Counter(["a", "b", "b"])

# c1 + c2  # Counter({"a": 3, "b": 3})
# c1 - c2  # Counter({"a": 1})

# '''
# deque — completely different structure
# deque is NOT based on dict. It's a doubly-linked list internally.


# List (array):
# [1, 2, 3, 4, 5]
#  ↑ inserting here shifts everything → O(n)

# Deque (doubly-linked list):
# None ← [1] ⇄ [2] ⇄ [3] ⇄ [4] ⇄ [5] → None
#        ↑ insert here → just update pointers → O(1)
       

# Operation         list      deque
# ─────────────────────────────────
# append right      O(1)      O(1)
# pop right         O(1)      O(1)
# append left       O(n) ❌   O(1) ✅
# pop left          O(n) ❌   O(1) ✅
# access by index   O(1) ✅   O(n) ❌

# Use deque when: you need fast operations on both ends (BFS, sliding window, rate limiter)
# Use list when: you need random access by index

# '''

# # BFS uses deque — popleft every iteration
# from collections import deque

# queue = deque([start_node])
# while queue:
#     node = queue.popleft()       # O(1) — fast!
#     queue.append(neighbor)

# # With list this would be:
# queue = [start_node]
# node = queue.pop(0)              # O(n) — slow!


# Exercise 

logs = [
    {"endpoint": "/products", "status": 200},
    {"endpoint": "/users", "status": 500},
    {"endpoint": "/products", "status": 200},
    {"endpoint": "/orders", "status": 404},
    {"endpoint": "/products", "status": 500},
    {"endpoint": "/users", "status": 200},
    {"endpoint": "/orders", "status": 500},
]

# def main():
#     from collections import Counter
#     endpointList = []
#     for element in logs:
#         endpointList.append(element["endpoint"])
    
#     freq = Counter(endpointList)
#     print(f"Task 1 : {dict(freq)}")

#     from itertools import groupby

#     data_sorted = sorted(logs, key=lambda x : x['status'])
    
#     grouped_logs = {}
#     for key, records in groupby(data_sorted, key=lambda x: x['status']):
#         grouped_logs[key] = list(records)
    
#     print(f"Task 2 : {grouped_logs}")

#     print(f"Task 3 : {list(freq)[0]}")

def main():
    from collections import Counter, defaultdict
 
    freq = Counter([log["endpoint"] for log in logs])
    print(f"Task 1 : {dict(freq)}")

    grouped = defaultdict(list)
    
    for log in logs:
        grouped[log['status']].append(log)
    
    print(f"Task 2 : {dict(grouped)}")

    print(f"Task 3 : {freq.most_common(1)[0][0]}")



# Task 1: Count how many times each endpoint was called
# Task 2: Group logs by status code
# Task 3: Find the most called endpoint
