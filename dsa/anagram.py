class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        table1 = self.prepare(s)
        table2 = self.prepare(t)
        
        for key, value in table1.items():
            if key not in table2:
                return False
            if table2[key] != value:
                return False

        for key, value in table2.items():
            if key not in table1:
                return False
            if table1[key] != value:
                return False

        return True
    
    def prepare(self, string: str) -> dict:
        table = dict()
        for char in string:
            if char in table:
                table[char] = table[char] + 1
            else:
                table[char] = 1
        return table

        