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
	pg.xlabel('Ek')
	pg.ylabel('k -->')
	pg.title('fourfold degeneracy of relevant states of E')

#globals
nA=6.023e23
#k=1.38e-23

delta=1.0
m=1.0
h=2.0
eps_fermi=2.0
delta=10.0

def eps(k):
	a=(h*k*h*k)/(2*m) - eps_fermi
	return a

def Ek(k):
	return math.sqrt( delta*delta + eps(k)**2 )

xmgrace()

dump=open('dataset.txt','wt')
y=[]
x=[]
for k in range(-2000,2000):
	j=k/100.0
	g=Ek(k/100.0)
	x.append(j)
	y.append(g)
	dump.write('%f %f\n'%(j,g) )

pg.plot(x,y)
dump.close()
