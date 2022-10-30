import numpy as np

class Room:
	def __init__(self, ds, width, height, physics_params, *, walls):
		'''Create a 'room' system, with parameters for simulation.
		Params:
			ds: (float) size of unit step in space
			width: (float) width of room, rounded down to nearest multiple of ds
			height: (float) height of room, rounded down to nearest multiple of ds
			physics_params: (dict{str:float}) dictionary of physics params for the
				system. Contains 'wavespeed': speed of waves in medium (float) and
				'attenuation': attenuation of waves in medium (float).
		Keyword params:
			walls: (Wall) List of wall objects containing position and absorbtion 
				data.
		'''
		self.room_points = np.meshgrid(np.linspace(0, width, ds), np.linspace(0, height, ds))
		self.wavespeed = phsyics_params.get('wavespeed', 343)
		self.attenuation = physics_params.get('attenuation', 0)
		self.walls = walls

	def add_source_func(self, loc, func):
		pass

	def add_source_data(self, loc, data):
		pass

	def add_walls(self, walls):
		self.walls + walls

	def run(self, dt, t_final):
		'''Solve the system using a finite differences solver, and returned the solved system.
		'''






class Wall:
	def __init__(self, endpoint1, endpoint2, absorbtion):
		self.endpoint1 = endpoint1
		self.endpoint2 = endpoint2
		self.absorbtion = absorbtion


pp = {'wavespeed': 343, 'attenuation': 2e-2}
ds = 1
width = 10
height = 15
driving_func = lambda x: np.sin(0.5*x)
dt = 0.5
t_final = 

room = Room(ds, width, height, pp)
room.add_source_func((5,7), driving_func)
result = room.run()