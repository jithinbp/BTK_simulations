import math
import pygrace
import pygame,os,time,sys
import numpy as np


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
T=1/11605.0 #temperature in eV    1ev=11605k

z=0.2  #Barrier strength at the interface

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
		try:
			x= 1.0/(np.exp2(E/T)+1)
		except:
			print 'Something went wrong  |E/t , E , T',E/T,E,T
			return 0
		return x
def integ(E,V):
	x=(fermi_fn(E-V)-fermi_fn(E))*(1+PA(E)-PB(E))
	return x

def current(V):
	#integrate between reasonable limits ( not -inf to +inf )
	I=0	
	dE=1.0e-4
	E=0
	while E<0.01:
		Im=integ(E,V)*(dE)
		Ip=integ(-E,V)*(dE)
		I+=Im+Ip
		E+=dE
		#print 'Im,Ip,V= ',Im,Ip,V

	return I
		
from Tkinter import *
root=Tk()
def inc_z():
	global z
	z+=0.1
	refresh(z)
def dec_z():
	global z
	if z>0:
		z-=0.1
		refresh(z)

Button(root,text='increase____________________',command=inc_z).pack()
Button(root,text='decrease____________________',command=dec_z).pack()


xmgrace()
pg.hold(1)

dump=open('TandR_Z0.txt','wt')
#XMGRACE PLOT FEATURES
# A=Black , B=red , C in green , D in Blue

def refresh(z):
	pg.xlabel('E  (Z = %2.2f) -->'%(z))
	pg.clear()
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
	dy=[]
	for a in range(len(x)-1):
		dy.append((y[a+1]-y[a])/dV)
	pg.hold(1)
	pg.plot(x,y)	
	x.pop()
	pg.plot(x,dy)
	dump.write('\n')
	dump.close()
ll=0
refresh(z)
run=True




root.mainloop()
try:
	pg.exit()
except:
	pass



