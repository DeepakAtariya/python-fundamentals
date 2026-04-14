# Given string s containing only '(', ')', '{', '}', '[', ']'
# Return True if brackets are valid
#
# "()[]{}" → True
# "(]"     → False
# "({[]})" → True
# "([)]"   → False

def solution(parantheses: str) -> bool:

    stack = []
    matches = { '(':')', '{':'}', '[':']' }
    
    for char in parantheses:
        match char:
            case '(' | '[' | '{':
                stack.append(char)
            case '}' | ')' | ']':
                if not stack or matches[stack[-1]] != char:
                    return False    
                stack.pop()

    return len(stack) == 0
        

def main():
    print(solution("()[]{}"))
    print(solution("(]"))
    print(solution("({[]})"))
    print(solution("([)]"))