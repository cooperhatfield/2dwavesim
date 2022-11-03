import numpy as np

def animate(data, *, filepath='', frame_space=10, walls=[]):
	'''Create an animation of the data.
	`data`: 3D array of waveform over time
	`filename`: name and path of output file. Leave blank to not save. Output formats are those supported by `matplotlib.animation.ArtistAnimation`
	`frame_space`: temporal resolution of resulting animation. Make sure this isn't too small!
	`walls`: optionally include the walls in the animation. They won't be visible if this isn't included.
	'''
	import matplotlib.animation as animation
	import matplotlib.pyplot as plt
	import matplotlib as m

	frame_space = frame_space
	frame_max = data.shape[-1]
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
			wallim, = ax.plot([wall.endpoint1.x, wall.endpoint2.x], [wall.endpoint1.y, wall.endpoint2.y], color='black', linewidth=1, alpha=1-wall.transmission)
			wallims.append(wallim)

		ims.append([im] + wallims)

	ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=1000)
	plt.show()
	if '.' in filename: 
		ani.save(filepath, writer=animation.PillowWriter(fps=24))

def get_steady_state_index(data, *, sample_points, rms_tolerance=0.1, window_size=0.1):
	''' Estimate the earliest index the system is in steady state by calculating the difference in 
	RMS over time at each of the sample points. Returns the intex into the time dimension of the 
	data which is the earliest point steady state is reached at all of the sample_points.
	`data`: 3D array of waveform over time
	`sample_points`: list of coordinates which will be checked for RMS
	`rms_tolerance`: the percent of change in the RMS to no longer be considered in steady state
	`window_size`: percent of the total data which should be included in the calculation window
	'''
	earliest_time_index = data.shape[-1]
	window_length = int(np.floor(window_size * data.shape[-1]))
	for point in sample_points:
		wave = data[point[0], point[1], :]
		reference_rms = np.sqrt(np.mean(wave[data.shape[-1] - window_length:]))
		for i in range(data.shape[-1] - 2 * window_length, 0, -1):
			rms = np.sqrt(np.mean(wave[i:i+window_length]))
			if rms >= rms_tolerance * reference_rms and i < earliest_time_index:
				earliest_time_index = i
	return earliest_time_index

def get_standing_waves(data, *, steady_state_kwargs=None):
	''' Returns a 2D array containing values representing the standing waves in steady-state.
	`data`: 3D array of waveform over time
	`steady_state_kwargs`: kwargs to pass to get_steady_state. Uses default values if not
	used.
	'''
	if steady_state_kwargs is None:
		steady_state_kwargs = {'sample_points': [(data.shape[0]//2, data.shape[1]//2)]}
	steady_state_index = get_steady_state_index(data, **steady_state_kwargs)
	return np.mean(np.abs(data[:,:,steady_state_index:]), axis=-1)