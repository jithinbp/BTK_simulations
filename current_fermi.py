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
	pg.ylabel('I -->')
	pg.title('Current')

#globals
ev=1.6e-19
k=1#8.617e-5
delta=2*0.001
T=5.0/11605.0 #temperature in eV    1ev=11605k

z=1.0  #Barrier strength at the interface

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



def fermi_fn(E):
		#print 'E,k*T, E/(k*T) = ',E,k*T,E/(k*T) 		
		x= 1.0/(math.exp(E/(T))+1)
		return x
def integ(E,V):
	x=(fermi_fn(E-V)-fermi_fn(E))*(1+PA(E)-PB(E))
	return x

def current(V):
	#integrate between reasonable limits ( not -inf to +inf )
	I=0	
	dE=1.0e-3
	E=0
	while E<0.3:
		Im=integ(E,V)*(dE)
		Ip=integ(-E,V)*(dE)
		I+=Im+Ip
		E+=dE
	#print 'E,I= ',E,I
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
	V=0
	dV=1e-5
	while V<3e-3:
		j=V
		g=current(V)
		V+=dV
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





