# Given nums and target, return indices of two numbers that add up to target
# nums = [2, 7, 11, 15], target = 9
# Output: [0, 1] because 2 + 7 = 9

# Constraint: exactly one solution exists

def solution(input:list, target:int) -> list: 
    index1 = -1 
    index2 = -1
    for i in range(len(input)):
        index1 = i
        findItem = target - input[index1]
        for j in range(i+1, len(input)):
            if input[j] == findItem:
                index2 = j
                break;
        if index2 > -1: 
            break;
                
    
    if(index2 == -1):
        return [-1,-1]
    
    return [index1, index2]


def betterSolution(nums: list, target: int)-> list:
    checked = {}
    for i, num in enumerate(nums):
        findItem = target - num
        if findItem in checked:
            return [checked[findItem], i]
        checked[num] = i

    return [-1,-1]
        



def main():
    print(betterSolution([2, 7, 11, 15],9))