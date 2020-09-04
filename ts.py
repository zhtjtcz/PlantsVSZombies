class a():
	def __init__(self,x):
		a.id=x

class b(a):
	def __init__(self,x):
		b.p=x

c=b(2)
print(c.p)
