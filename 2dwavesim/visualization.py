def get_steady_state_index(data, sample_points, *, rms_tolerance=0.1, window_size=0.1):
	''' Estimate the earliest index the system is in steady state by calculating the difference in 
	RMS over time at each of the sample points. Returns the intex into the time dimension of the 
	data which is the earliest point steady state is reached at all of the sample_points.
	`data`: 3D array of waveform over time
	`sample_points`: list of coordinates which will be checked for RMS
	`rms_tolerance`: the percent of change in the RMS to no longer be considered in steady state
	`window_size`: percent of the total data which should be included in the calculation window
	'''
	earliest_time_index = data.shape[-1]
	window_length = window_size * data.shape[-1]
	for point in sample_points:
		wave = data[point[0], point[1], :]
		reference_rms = np.sqrt(np.mean(wave[data.shape[-1] - window_length:]))
		for i in range(0, data.shape[-1] - 2 * window_length, -1):
			rms = np.sqrt(np.mean(wave[i:i+window_length]))
			if rms >= rms_tolerance * reference_rms and i < earliest_time_index:
				earliest_time_index = i
	return earliest_time_index
