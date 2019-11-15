lst = []
def average_init(a):
  lst = a
 
def update(n):
  lst.append(lst.pop(0))
  lst[len(lst) - 1] = n
  return sum(lst)/len(lst)
