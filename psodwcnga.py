import random
from operator import add

def func1(x):
	total=0
	for i in range(len(x)):
		total+=x[i]**2
	return total

def dist(a,b):
	val=0
	for i in range(len(a)):
		val=val+(a[i]-b[i])**2
	return val

class Particle:
	def __init__(self,x0):
		self.position_i=[]
		self.velocity_i=[]
		self.pos_best_i=[]
		self.err_best_i=-1
		self.err_i=-1

		for i in range(0,num_dimensions):
			self.velocity_i.append(random.uniform(-1,1))
			self.position_i.append(x0[i])

	def evaluate(self,costFunc):
		self.err_i=costFunc(self.position_i)

		if self.err_i < self.err_best_i or self.err_best_i==-1:
			self.pos_best_i=self.position_i
			self.err_best_i=self.err_i

	def update_velocity(self,pos_best_g):
		w=0.5
		c1=1
		c2=2

		for i in range(0,num_dimensions):
			r1=random.random()
			r2=random.random()

			vel_cognitive=c1*r1*(self.pos_best_i[i]-self.position_i[i])
			vel_social=c2*r2*(pos_best_g[i]-self.position_i[i])
			self.velocity_i[i]=w*self.velocity_i[i]+vel_cognitive+vel_social

	def update_position(self,bounds):
		for i in range(0,num_dimensions):
			self.position_i[i]=self.position_i[i]+self.velocity_i[i]

			if self.position_i[i]>bounds[1][i]:
				self.position_i[i]=bounds[1][i]

			if self.position_i[i] < bounds[0][i]:
				self.position_i[i]=bounds[0][i]
				
class PSO():
	def __init__(self,costFunc,x0,bounds,num_particles,maxiter):
		global num_dimensions

		probab= 0
		radius= 100
		num_dimensions=len(x0)
		err_best_g=-1
		pos_best_g=[]

		swarm=[]
		for i in range(0,num_particles):
			swarm.append(Particle(x0))

		i=0
		while i < maxiter:
			for j in range(0,num_particles):
				swarm[j].evaluate(costFunc)

				if swarm[j].err_i < err_best_g or err_best_g == -1:
					pos_best_g=list(swarm[j].position_i)
					err_best_g=float(swarm[j].err_i)

			for j in range(0,num_particles):
				pos=list(swarm[j].position_i)
				err=float(swarm[j].err_i)
				for k in range(0,num_particles):
					if dist(list(swarm[j].position_i),list(swarm[k].position_i))<=radius:
						if swarm[k].err_i<err:
							err=float(swarm[k].err_i)
							pos=list(swarm[k].position_i)
					else:
						if random.random()<=probab and swarm[k].err_i<err:
							err=float(swarm[k].err_i)
							pos=list(swarm[k].position_i)
				swarm[j].update_velocity(pos)
				swarm[j].update_position(bounds)
			i+=1
			probab=probab+1.0/maxiter
			#GA
			particles=[]			
			for j in range(0,num_particles):
				particles.append([swarm[j].err_i,j])
			particles.sort()
			j=particles[num_particles-1][1]
			i1=particles[0][1]
			i2=particles[1][1]
			swarm[j].position_i=map(add,swarm[i1].position_i,swarm[i2].position_i)
			swarm[j].position_i=[x/2.0 for x in swarm[j].position_i]
			swarm[j].velocity_i=map(add,swarm[i1].velocity_i,swarm[i2].velocity_i)
			swarm[j].velocity_i=[x/2.0 for x in swarm[j].velocity_i]
			swarm[j].err_best_i=-1
			swarm[j].evaluate(costFunc)			
		print 'FINAL:'
		print pos_best_g
		print err_best_g

initial=[5,5,5,5,5]
bounds=[(-100,-100,-100,-100,-100),(100,100,100,100,100)]
PSO(func1,initial,bounds,num_particles=20,maxiter=1000)