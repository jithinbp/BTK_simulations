import math
import pygrace
import pygame,os
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
	pg.xlabel('E -->>')
	pg.ylabel('Probability -->')
	pg.title('Transmission and reflection probabilities')

#globals
delta=1.0
m=1.0
h=2.0
eps_fermi=2.0
delta=10.0


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
	return 1/(math.exp((E-Ef)/(k*T))+1)

def integ(E,V):
	e=1.6e-19
	return (fermi_fn(E-e*V)-fermi_fn(E))*(1+PA(E)-PB(E))



xmgrace()
pg.hold(1)

dump=open('TandR_Z0.txt','wt')
#XMGRACE PLOT FEATURES
# A=Black , B=red , C in green , D in Blue

def refresh(z):
   pg.xlabel('E  (Z = %2.2f) -->'%(z))
   pg.clear()
   pg.hold(1)
   dump=open('TandR.txt','wt')
   for fn in [PA,PB,PC,PD]:
	y=[]
	x=[]
	for E in range(0,1000):
		j=E/10.0
		g=fn(E/10.0)
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
		run=False
		continue
	ll=0
	try:
		ll=event.button
		if(ll==4):z+=0.1
		elif (ll==5): z-=0.1
		if z<0: z=0
	except:
		continue
	if(ll):refresh(z)





