def average_init(a):
  global lst
  lst = a
  print (lst)
 
def update(n):
  global lst
  lst.append(lst.pop(0))
  lst[len(lst) - 1] = n
  return sum(lst)/len(lst)

lst = []
