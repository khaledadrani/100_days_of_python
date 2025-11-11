# Find Max: Simple linear scan—iterate once, 
# track the biggest. Ties to min/max algorithms and control flow (conditionals).

def find_max(ls:list[int])->int:
  if not ls:
    raise Exception("Empty List!")
  is_max = ls[0]
  for i in range(1, len(ls)):
    if ls[i]>is_max:
      is_max = ls[i]
  return is_max 


ls = [10,7,8,99,10,2]

print(find_max(ls=ls))