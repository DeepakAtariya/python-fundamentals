class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        n = len(nums)
        prefix = [1] * n
        suffix = [1] * n
        
        for i in range(1, n):
            prefix[i] = prefix[i-1] * nums[i-1]
        print(prefix)

        for i in range(n-2, -1, -1):
            print(i, suffix[i+1], nums[i+1])
            suffix[i] = suffix[i+1] * nums[i+1]
        print(suffix)

        return [prefix[i] * suffix[i] for i in range(n)]
    
print (Solution().productExceptSelf([1,2,3,4]))
# print (Solution().productExceptSelf([-1,1,0,-3,3]))
