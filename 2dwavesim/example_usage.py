import numpy as np
import matplotlib.pyplot as plt

from room import Room, Wall, animate

pp = {'wavespeed': 343, 'attenuation': 0}
ds = 1
width = 70
height = 70
driving_func = lambda x: np.sin(50*2*np.pi*x) + np.sin(15*2*np.pi*x)
dt = ds / (np.sqrt(2) * pp['wavespeed'])
print(dt)
t_final = 4

walls_square = [
		 Wall((10,10), (10,20), 0),
		 Wall((10,21), (10,30), 0.7),
		 Wall((10,31), (10,45), 0),
		 Wall((10,46), (45,46), 0),
		 Wall((46,46), (46,10), 0),
		 Wall((45,10), (11,10), 0)
		 ]

walls_plus = [
		 Wall((20,53), (32,53), 0),
		 Wall((32,53), (32,31), 0),
		 Wall((32,31), (53,31), 0),
		 Wall((53,31), (53,20), 0.4),
		 Wall((53,20), (32,20), 0),
		 Wall((32,20), (32,0), 0),
		 Wall((32,0), (20,0), 0),
		 Wall((20,0), (20,20), 0),
		 Wall((20,20), (0,20), 0),
		 Wall((0,20), (0,31), 0),
		 Wall((0,31), (20,31), 0),
		 Wall((20,31), (20,53), 0)
		]

walls_triangle = [
		 Wall((10,10), (50,10), 0),
		 Wall((50,10), (10,50), 0),
		 Wall((10,50), (10,10), 0)
		]

walls_u = [
		 Wall((10,10), (10,46), 0),
		 Wall((10,46), (46,46), 0),
		 Wall((46,46), (46,10), 0),
		 Wall((46,10), (10,10), 0),
		 Wall((23,10), (23,35), 0)
		]

room = Room(ds, width, height, physics_params=pp)
room.add_walls(walls_u)
room.create_mask()
import matplotlib.pyplot as plt
#room.plot_mask()

room.add_source_func((15,15), driving_func)
room.run(dt, t_final)
#plt.imshow(room.runs[0]['results'][:,:,-1])
#plt.show()

animate(room.runs[0]['results'], 'test', walls=walls_u)

plt.plot(room.runs[0]['results'][15,15,:], label='Driving Force')
plt.plot(room.runs[0]['results'][15,28,:], label='Force on opposite room')
plt.legend()
plt.show()