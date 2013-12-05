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
delta=0.00001
T=0.5/11605.0 #temperature in eV    1ev=11605k
z=0
#fix V    // eV>>delta
#delta waqs 2mili
V=10 #looks reasonable

#general form
def gamma2(u2):
	global z
	return (u2+z*z*(2*u2-1) )**2

def u2(E):
	global z
	return 0.5*(1+math.sqrt((E**2-delta**2)/(E**2)) )


def PA(E): #probability of andreev reflection
	global z
	if E<delta:
		t2=E*E + (delta*delta-E*E)*( (1+2*z*z)**2 )
		return (delta*delta)/t2
	else:
		u=u2(E)
		return u*(1-u)/gamma2(u)

def PB(E): #probability of ordinary reflection
	global z
	if E<delta:
		return 1-PA(E)
	else:
		u=u2(E)
		return (2*u-1)*(2*u-1)*(1+z*z)*z*z/gamma2(u)

def PB_inf(): # at E =infinity
	global z
	return z*z/(1+z*z)



def integ(E):
	global z
	x=(PA(E)-PB(E)+PB_inf())
	return x

def exc_current():
	global z
	#integrate between reasonable limits ( 0 - inf )
	I=0	
	dE=1.0e-4
	E=0
	while E<0.05:
		I+=integ(E)*(dE)
		E+=dE
		#print 'Im,Ip,V= ',Im,Ip,V

	r=I/(1-PB_inf())
	#print 'z, =',z,r
	return r
'''		
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
'''

xmgrace()
pg.hold(1)

dump=open('TandR_Z0.txt','wt')


def refresh():
	global z
	pg.xlabel('Z -->')
	pg.clear()
	dump=open('exc_I.txt','wt')
	y=[]
	x=[]
	dz=0.01
	while z<2.0:
		j=z
		g=exc_current()
		z+=dz
		x.append(j)
		y.append(g)
		dump.write('%f %f\n'%(j,g) )
	pg.hold(1)
	pg.plot(x,y)	
	dump.write('\n')
	dump.close()
ll=0
refresh()
run=True




#root.mainloop()



