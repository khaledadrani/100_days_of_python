def reverse_list(ls:list):
  # not memory
  length = len(ls)

  ls_new = []

  for i in range(length):
    ls_new.append(ls[length-i-1])

  return ls_new 

def reverse_list(lst):
    left, right = 0, len(lst) - 1
    while left < right:
        lst[left], lst[right] = lst[right], lst[left]  # Swap
        left += 1
        right -= 1
    return lst  # Returns the modified list


def reverse_list(ls:list[int]):
   left, right = 0, len(ls) - 1 

   while left < right: 
      tmp = int(ls[left])
      ls[left] = ls[right]
      ls[right] = tmp
      left += 1 
      right -= 1
   return ls
    

ls = [1,2,3,4,5]

print(reverse_list(ls))