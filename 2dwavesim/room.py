import numpy as np
from tqdm import tqdm

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
		self.walls = self.walls + walls

	def create_mask(self):
		def bressenham_ABC(p0, p1):
			A = p1.y - p0.y
			B = -(p1.x - p0.x)
			C = p1.x * p0.y - p0.x * p1.y
			return A,B,C

		for wall in self.walls:
			A, B, C = bressenham_ABC(wall.endpoint1, wall.endpoint2)
			on_line_mask = 0 == np.floor(self.room_points[0] * A + self.room_points[1] * B + C)
			on_line_mask *= max(wall.endpoint1.x, wall.endpoint2.x) >= self.room_points[0]
			on_line_mask *= self.room_points[0] >= min(wall.endpoint1.x, wall.endpoint2.x)
			on_line_mask *= max(wall.endpoint1.y, wall.endpoint2.y) >= self.room_points[1]
			on_line_mask *= self.room_points[1] >= min(wall.endpoint1.y, wall.endpoint2.y)
			self.mask_points[on_line_mask] = wall.absorption

	def run(self, dt, t_final):
		'''Solve the system using a finite differences solver, and return the solved system.
		'''
		wave_constant = (self.wavespeed * dt / self.point_spacing)**2
		damp_constant = self.attenuation * dt / 2

		if 2 * wave_constant > 1:
			raise ValueError(f'CFL condition not satisfied, results won\'t be numerically stable. C is {wave_constant}.')

		time_steps = np.arange(0, t_final, dt)
		room_data = np.zeros((*self.room_points[0].shape, len(time_steps)), dtype=float)

		room_data[:,:,0] = np.multiply(room_data[:,:,0], self.mask_points)

		for t in tqdm(range(1, len(time_steps)-1)):
			room_data[:,:,t] = np.multiply(room_data[:,:,t], self.mask_points)
			D2x = room_data[:-2,1:-1,t] - 2 * room_data[1:-1,1:-1,t] + room_data[2:,1:-1,t]
			D2y = room_data[1:-1,:-2,t] - 2 * room_data[1:-1,1:-1,t] + room_data[1:-1,2:,t]
			room_data[1:-1,1:-1,t+1] = wave_constant * (D2x + D2y) + 2 * room_data[1:-1,1:-1,t] + (damp_constant - 1) * room_data[1:-1,1:-1,t-1]
			for source in self.func_sources:
				loc = source[1]
				source_func = source[2]
				room_data[loc.x, loc.y, t+1] = dt**2 * source_func(time_steps[t])
			for source in self.data_sources:
				loc = source[1]
				source_data = source[2]
				room_data[loc.x, loc.y, t+1] = dt**2 * source_data[t]
		room_data /= (1 + damp_constant)

		run_data = {'time params': {'dt': dt,
									't_final': t_final},
					'walls': self.walls,
					'sources': self.func_sources +  self.data_sources,
					'results': room_data
					}
		self.runs.append(run_data)

	def plot_mask(self):
		import matplotlib.pyplot as plt
		plt.imshow(self.mask_points)
		plt.show()

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

def animate(data, name, *, walls=[]):
	import matplotlib.animation as animation
	import matplotlib as m

	frame_space = 10
	frame_max = data.shape[-1]
	print(frame_max)
	fig, [ax, cax] = plt.subplots(1, 2, gridspec_kw={'width_ratios':[10,1]})

	maximum = np.amax(data)
	minimum = np.amin(data)

	norm = m.colors.Normalize(vmin=minimum, vmax=maximum)
	cb1 = m.colorbar.ColorbarBase(cax, norm=norm, orientation='vertical')

	ims = []
	for i in range(0, frame_max, frame_space):
		im = ax.imshow(data[:,:,i], vmin=minimum, vmax=maximum, animated=True)
		wallims = []
		for wall in walls:
			wallim, = ax.plot([wall.endpoint1.x, wall.endpoint2.x], [wall.endpoint1.y, wall.endpoint2.y], color='black', linewidth=1, alpha=1-wall.absorption)
			wallims.append(wallim)

		ims.append([im] + wallims)

	ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=1000)
	plt.show()
	#ani.save(f'D:\\Repos\\2dwavesim\\2dwavesim\\{name}.webp', writer=animation.PillowWriter(fps=24))

pp = {'wavespeed': 343, 'attenuation': 0}
ds = 1
width = 70
height = 70
driving_func = lambda x: np.sin(50*2*np.pi*x)
dt = ds / (np.sqrt(2) * pp['wavespeed'])
print(dt)
t_final = 4

walls_square = [
		 Wall(Coordinate(10,10), Coordinate(10,20), 0),
		 Wall(Coordinate(10,21), Coordinate(10,30), 0.5),
		 Wall(Coordinate(10,31), Coordinate(10,45), 0),
		 Wall(Coordinate(10,46), Coordinate(45,46), 0),
		 Wall(Coordinate(46,46), Coordinate(46,10), 0),
		 Wall(Coordinate(45,10), Coordinate(11,10), 0)
		 ]

walls_plus = [
		 Wall(Coordinate(20,53), Coordinate(32,53), 0),
		 Wall(Coordinate(32,53), Coordinate(32,31), 0),
		 Wall(Coordinate(32,31), Coordinate(53,31), 0),
		 Wall(Coordinate(53,31), Coordinate(53,20), 0.4),
		 Wall(Coordinate(53,20), Coordinate(32,20), 0),
		 Wall(Coordinate(32,20), Coordinate(32,0), 0),
		 Wall(Coordinate(32,0), Coordinate(20,0), 0),
		 Wall(Coordinate(20,0), Coordinate(20,20), 0),
		 Wall(Coordinate(20,20), Coordinate(0,20), 0),
		 Wall(Coordinate(0,20), Coordinate(0,31), 0),
		 Wall(Coordinate(0,31), Coordinate(20,31), 0),
		 Wall(Coordinate(20,31), Coordinate(20,53), 0)
		]

walls_triangle = [
		 Wall(Coordinate(10,10), Coordinate(50,10), 0),
		 Wall(Coordinate(50,10), Coordinate(10,50), 0),
		 Wall(Coordinate(10,50), Coordinate(10,10), 0)
		]

room = Room(ds, width, height, physics_params=pp)
room.add_walls(walls_triangle)
room.create_mask()
import matplotlib.pyplot as plt
#room.plot_mask()

room.add_source_func(Coordinate(15,15), driving_func)
room.run(dt, t_final)
#plt.imshow(room.runs[0]['results'][:,:,-1])
#plt.show()

animate(room.runs[0]['results'], 'test', walls=walls_triangle)