import math
import pygrace

def xmgrace():
	global pg
	try:
		import pygrace
	except:
		print 'damn'
		return
	pg = pygrace.grace()
	pg.xlabel('Temperature')
	pg.ylabel('Specific heat')
	pg.title('Specific heat ')

#globals
nA=6.023e23
k=1.38e-23
theta=1
def Cv(T):
	return 3*nA*k*math.pow(theta/T,2)*math.exp(theta/T)/( math.pow(math.exp(theta/T)-1,2) )

xmgrace()

dump=open('dataset.txt','wt')
y=[]
x=[]
for a in range(1,300):
	j=a/100.0
	g=Cv(a/100.0)
	x.append(j)
	y.append(g)
	dump.write('%f %f\n'%(j,g) )
pg.plot(x,y)
dump.close()
