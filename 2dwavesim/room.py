import numpy as np

class Room:
	def __init__(self, ds, width, height,*, walls=[], physics_params={}):
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
		self.room_points = np.meshgrid(np.arange(0, width, ds), np.arange(0, height, ds))
		self.mask_points = np.ones(self.room_points[0].shape)
		self.point_spacing = ds
		self.wavespeed = physics_params.get('wavespeed', 343)
		self.attenuation = physics_params.get('attenuation', 0)
		self.walls = walls
		self.func_sources = []
		self.data_sources = []
		self.runs = []

	def add_source_func(self, loc, func):
		true_loc = Coordinate(int(loc.x // self.point_spacing), int(loc.y // self.point_spacing))
		self.func_sources.append((loc, true_loc, func))

	def add_source_data(self, loc, data):
		true_loc = Coordinate(int(loc.x // self.point_spacing), int(loc.y // self.point_spacing))
		self.data_sources.append((loc, true_loc, data))

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
		'''Solve the system using a finite differences solver, and return the solved system.
		'''
		time_steps = np.arange(0, t_final, dt)
		room_data = np.zeros((*self.room_points[0].shape, len(time_steps)), dtype=float)

		for t in range(1, len(time_steps)-1):
			room_data[:,:,t] = np.multiply(room_data[:,:,t], self.mask_points)
			D2x = room_data[:-2,1:-1,t] - 2 * room_data[1:-1,1:-1,t] + room_data[2:,1:-1,t]
			D2y = room_data[1:-1,:-2,t] - 2 * room_data[1:-1,1:-1,t] + room_data[1:-1,2:,t]
			room_data[1:-1,1:-1,t+1] = self.wavespeed * (D2x + D2y) + 2 * room_data[1:-1,1:-1,t] + (self.attenuation - 1) * room_data[1:-1,1:-1,t-1]
			for source in self.func_sources:
				loc = source[1]
				source_func = source[2]
				room_data[loc.x, loc.y, t+1] = source_func(time_steps[t])
			for source in self.data_sources:
				loc = source[1]
				source_data = source[2]
				room_data[loc.x, loc.y, t+1] = source_data[t]
		room_data /= (1 + self.attenuation)

		run_data = {'time params': {'dt': dt,
									't_final': t_final},
					'walls': self.walls,
					'sources': self.func_sources +  self.data_sources,
					'results': room_data
					}
		self.runs.append(run_data)

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
room.add_source_func(Coordinate(5,7), driving_func)
result = room.run()