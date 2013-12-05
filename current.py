import math
import pygrace
import pygame,os,time,sys
WIDTH=400
HEIGHT=100
size = [WIDTH,HEIGHT]
flags=pygame.SRCALPHA|pygame.HWSURFACE|pygame.HWACCEL
os.environ['SDL_VIDEO_WINDOW_POS'] = '700,100'

screen = pygame.display.set_mode(size,flags)
pygame.display.set_caption("Transmission and reflection")


def xmgrace():
	global pg
	try:
		import pygrace
	except:
		print 'damn'
		return
	pg = pygrace.grace()
	pg.xlabel('V -->>')
	pg.ylabel('dI/dV -->')
	pg.title('Current')

#globals
m=1.0
k=1.38e-23
ev=1.6e-19
Ef=1e-3*ev
delta=20*ev
T=(1.0/11600)/100 #temperature in eV    1ev=11600k

z=1.0   #Barrier strength at the interface

#general form
def gamma2(u2):
	return (u2+z*z*(2*u2-1) )**2

def u2(E):
	return 0.5*(1+math.sqrt((E**2-delta**2)/(E**2)) )


def PA(E): #probability of andreev reflection
	if E<delta:
		t2=E*E + (delta*delta-E*E)*( (1+2*z*z)**2 )
		return (delta*delta)/t2
	else:
		u=u2(E)
		return u*(1-u)/gamma2(u)

def PB(E): #probability of ordinary reflection
	if E<delta:
		return 1-PA(E)
	else:
		u=u2(E)
		return (2*u-1)*(2*u-1)*(1+z*z)*z*z/gamma2(u)


def PC(E): #probability of transmission sans branch crossing
	if E<delta:
		return 0
	else:
		u=u2(E)
		return u*(2*u-1)*(1+z*z)/gamma2(u)


def PD(E): #probability of transmission with branch crossing
	if E<delta:
		return 0
	else:
		u=u2(E)
		return (1-u)*(2*u-1)*(z*z)/gamma2(u)


def fermi_fn(E):
		#print '(E-Ef)/(k*T) = ',(E-Ef)/(k*T)
		return 1.0/(math.exp((E-Ef)/(k*T))+1)

def integ(E,V):
	x=(fermi_fn(E-ev*V)-fermi_fn(E))*(1+PA(E)-PB(E))
	print 'fermi_fn(E-ev*V) , E-ev*V = ',fermi_fn(E-ev*V),E-ev*V
	return x

def current(V):
	#integrate between reasonable limits ( not -inf to +inf )
	dE=1e-3*ev
	E=Ef
	I=0	
	#print 'E,V =',E,V
	for a in range(20):
		I+=integ(E,V)*dE
		E+=dE
	return I

xmgrace()
pg.hold(1)

dump=open('TandR_Z0.txt','wt')
#XMGRACE PLOT FEATURES
# A=Black , B=red , C in green , D in Blue

def refresh(z):
	pg.xlabel('E  (Z = %2.2f) -->'%(z))
	pg.clear()
	pg.hold(1)
	dump=open('I.txt','wt')
	y=[]
	x=[]
	for V in range(0,300):
		j=ev*V/(delta*10000.0)
		g=current(V/10000.0)
		if(j):
			#print j,g
			x.append(j)
			y.append(g)
		dump.write('%f %f\n'%(j,g) )
	pg.plot(x,y)
	dump.write('\n')
	dump.close()
ll=0
refresh(z)
run=True
while run:
	event=pygame.event.wait()
	if event.type == pygame.QUIT:
		try:
			pg.exit()
			run=False
		except:
			sys.exit()

	ll=0
	try:
		ll=event.button
		if(ll==4):z+=0.1
		elif (ll==5): z-=0.1
		if z<0: z=0
	except:
		continue
	if(ll):refresh(z)





