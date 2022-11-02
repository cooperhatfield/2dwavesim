import numpy as np
import matplotlib.pyplot as plt

from room import Room, Coordinate, Wall, animate

pp = {'wavespeed': 343, 'attenuation': 0}
ds = 1
width = 70
height = 70
driving_func = lambda x: np.sin(50*2*np.pi*x) + np.sin(15*2*np.pi*x)
dt = ds / (np.sqrt(2) * pp['wavespeed'])
print(dt)
t_final = 4

walls_square = [
		 Wall(Coordinate(10,10), Coordinate(10,20), 0),
		 Wall(Coordinate(10,21), Coordinate(10,30), 0.7),
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

walls_u = [
		 Wall(Coordinate(10,10), Coordinate(10,46), 0),
		 Wall(Coordinate(10,46), Coordinate(46,46), 0),
		 Wall(Coordinate(46,46), Coordinate(46,10), 0),
		 Wall(Coordinate(46,10), Coordinate(10,10), 0),
		 Wall(Coordinate(23,10), Coordinate(23,35), 0)
		]

room = Room(ds, width, height, physics_params=pp)
room.add_walls(walls_u)
room.create_mask()
import matplotlib.pyplot as plt
#room.plot_mask()

room.add_source_func(Coordinate(15,15), driving_func)
room.run(dt, t_final)
#plt.imshow(room.runs[0]['results'][:,:,-1])
#plt.show()

animate(room.runs[0]['results'], 'test', walls=walls_u)

plt.plot(room.runs[0]['results'][15,15,:], label='Driving Force')
plt.plot(room.runs[0]['results'][15,28,:], label='Force on opposite room')
plt.legend()
plt.show()