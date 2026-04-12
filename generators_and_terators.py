
# Generators
# def batch_processor(arr, batch):

#     for i in range(0, len(arr), batch):
#         yield arr[i:i+batch]


# gen = batch_processor([1,2,3,4,5,6,7], 3)
# print(next(gen))
# print(next(gen))
# print(next(gen))
# print(list(batch_processor([1,2,3,4,5,6,7], 3)))


# slow_function took 0.045s

# # Eager — computes ALL immediately, stores in memory
# squaresEager = [x**2 for x in range(10)]  # ~80MB in memory

# # Lazy — computes ONE at a time
# squaresLazy = (x**2 for x in range(10))  # ~120 bytes



def main():
    models = ["gpt-4o", "gpt-4o-mini", "claude"]
    temperatures = [0.0, 0.5, 1.0]

    import itertools as itr
    print(list(itr.product(models, temperatures)))
    
    

# Expected: [("gpt-4o", 0.0), ("gpt-4o", 0.5), ... ] — 9 combinations
