# Given nums and target, return indices of two numbers that add up to target
# nums = [2, 7, 11, 15], target = 9
# Output: [0, 1] because 2 + 7 = 9

# Constraint: exactly one solution exists

def solution(input:list, target:int) -> list: 
    findItem = target - input[0] 
    otherItem = [i for i in range(len(input)) if input[i] == findItem ]
    
    return [findItem, otherItem]



def main():
    print(solution([2, 7, 11, 15],7))