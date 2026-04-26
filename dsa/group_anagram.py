# Input: ["eat", "tea", "tan", "ate", "nat", "bat"]
# Output: [["eat","tea","ate"], ["tan","nat"], ["bat"]]

from collections import defaultdict

def solution(strings: list) -> bool:
    group_anagram = defaultdict(list)
    
    for i in range(len(strings)):
        sortedStr = str(sorted(strings[i]))
        group_anagram[sortedStr].append(strings[i])

    return list(group_anagram.values()) 

def main():
    print(solution(["eat", "tea", "tan", "ate", "nat", "bat"]))