"""
347. Top K Frequent Elements
Medium
Topics
premium lock icon
Companies
Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.



Example 1:

Input: nums = [1,1,1,2,2,3], k = 2

Output: [1,2]

Example 2:

Input: nums = [1], k = 1

Output: [1]

Example 3:

Input: nums = [1,2,1,2,1,2,3,1,3,2], k = 2

Output: [1,2]


Constraints:

1 <= nums.length <= 105
-104 <= nums[i] <= 104
k is in the range [1, the number of unique elements in the array].
It is guaranteed that the answer is unique.

Follow up: Your algorithm's time complexity must be better than O(n log n), where n is the array's size.    
"""

""" 
Algorithm :
create hashtable and find max k times and once found then take value from hash table

"""

from typing import List


nums = [1,1,1,2,2,3]
k = 2

def solution (nums: list, k:int):
    hash_table: dict = {}
    for i in range(len(nums)) :
        if nums[i] in hash_table:
            hash_table[nums[i]] = hash_table[nums[i]] + 1
        else:
            hash_table[nums[i]] = 1
    found_keys = []
    for q in range(k):
        max: int = 0
        key_of_max: int = -1
        for key, value in hash_table.items():
            if max < value :
                max = value
                key_of_max = key
        found_keys.append(key_of_max)
        hash_table[key_of_max] = 0
    print (found_keys)

nums = [1,2,1,2,1,2,3,1,3,2]
k = 2
solution(nums, k)


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        hash_table: dict = {}
        for i in range(len(nums)) :
            if nums[i] in hash_table:
                hash_table[nums[i]] = hash_table[nums[i]] + 1
            else:
                hash_table[nums[i]] = 1
            found_keys = []
        for q in range(k):
            max: int = 0
            key_of_max: int = -1
            for key, value in hash_table.items():
                if max < value :
                    max = value
                    key_of_max = key
            found_keys.append(key_of_max)
            hash_table[key_of_max] = 0
        return found_keys
