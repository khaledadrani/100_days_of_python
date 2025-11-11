# Project 2: Simple Search Program (Find a Number in a List)
# Here, we're honing linear search: iterate until you hit the target. 
# Decomposes to "check each? Yes/no." Patterns: sequential access. 
# Time: O(n) worst-case (scan whole list). 
# Relates to control flow (loops/conditionals) 
# and basics like booleans for "found."


def search_linear(ls, value):
  #todo input validation 

  for i in range(len(ls)):
    if value == ls[i]:
      return i 
  
  return -1


ls = [1,10,55,3,4,2,1,7]

print(search_linear(ls=ls, value=2))