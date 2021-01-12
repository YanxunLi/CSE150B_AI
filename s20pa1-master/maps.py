Maps = []
Ans = []
m0, m1, m2 = {}, {}, {}
for i in range(30):
	for j in range(30):
		m0[(i,j)]=0
		if i%5 and j%5:
			m1[(i,j)] = 2
			m2[(i,j)] = 1
		else:
			m1[(i,j)] = 1
			m2[(i,j)] = 0
Maps.extend([m0,m1,m2])
Ans.extend([41,410,41])
