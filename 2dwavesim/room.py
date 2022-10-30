import numpy as np

class Room:
	def __init__(self, ds, width, height,*, walls, physics_params={}):
		'''Create a 'room' system, with parameters for simulation.
		Params:
			ds: (float) size of unit step in space
			width: (float) width of room, rounded down to nearest multiple of ds
			height: (float) height of room, rounded down to nearest multiple of ds
			physics_params: (dict{str:float}) dictionary of physics params for the
				system. Contains 'wavespeed': speed of waves in medium (float) and
				'attenuation': attenuation of waves in medium (float).
		Keyword params:
			walls: (Wall) List of wall objects containing position and absorption 
				data.
		'''
		self.room_points = np.meshgrid(np.linspace(0, width, ds), np.linspace(0, height, ds))
		self.mask_points = np.ones(self.room_points[0].shape())
		self.wavespeed = phsyics_params.get('wavespeed', 343)
		self.attenuation = physics_params.get('attenuation', 0)
		self.walls = walls

	def add_source_func(self, loc, func):
		pass

	def add_source_data(self, loc, data):
		pass

	def add_walls(self, walls):
		self.walls + walls

	def create_mask(self):
		def bressenham_ABC(p0, p1):
			A = p1.y - p0.y
			B = -(p1.x - p0.x)
			C = p1.x * p0.y - p0.x * p1.y
			return A,B,C

		for wall in self.walls:
			A, B, C = bressenham_ABC(wall.endpoint1, wall.endpoint2)
			on_line_mask = 0 == np.round(self.room_points[0] * A + self.room_points[1] * B + C)
			self.mask_points[on_line_mask] = wall.absorption

	def run(self, dt, t_final):
		'''Solve the system using a finite differences solver, and returned the solved system.
		'''




class Coordinate:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __repr__(self):
		return (self.x, self.y)

	def __str__(self):
		return f'({self.x}, {self.y})'

	def __add__(self, other):
		return Coordinate(self.x + other.x, self.y + other.y)

class Wall:
	def __init__(self, endpoint1, endpoint2, absorption):
		self.endpoint1 = endpoint1
		self.endpoint2 = endpoint2
		self.absorption = absorption


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