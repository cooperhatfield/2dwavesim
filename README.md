# 2dwavesim
 
This is a project that simulates waves on 2D plates/rooms. Given boundaries (or walls) and points where oscillation will be forced, this will simulate the resulting wavemodes! 

Currently it supports setting the attenuation properties of individual boundaries, multiple forcing points based on either data or a function, and any wall shape you want. It also supports variable time and space steps and spans (as long as you keep numerically stable!), as well as custom wavespeed and attenuation on the material.

![example](https://github.com/cooperhatfield/2dwavesim/blob/main/exampleimages/example.webp)

TODO:
- add tests
- frequency-dependant wall transmission values
- 3D??

## Usage
There are two main Classes:

`Room(ds, width, height,*, walls=[], physics_params={})`

<ul>

This creates an instance of a `Room` class, which contains any walls or sources of the system.

`ds` is a float which defines the unit of distance between two grid points.

`width` and `height` and floats which define the dimentions of the grid. If they are not exact multiples of `ds`, then they are upper bounds on the number of points above the nearest multiple.
    
`walls` is a list of `Wall` objects. This can be optionally set after construction as well.
    
`physics_params` is a dict with structure `{'wavespeed':float, 'attenuation':float}`. Wavespeed represents the speed of the propigating wave on the room's medium, and attenuation represents the attenuation factor of waves on the medium. By defaut, wavespeed is assumed to be 343 units/s and attenuation is assumed to be $2^{-2}$ units 
$^{-1}$.
 
**`Room.add_source_func(loc, func)`**

 <ul>
 
Add a source based on a function.
  
`loc` is the room-specific coordinate of the source. Note: unless `ds=1`, this is not the same as the list indices of the point in the room.

`func` is a function taking a float (the time) and outputing a float (the value of the wave at that time). This should be something like `lambda t: np.sin(t)`, for example.
 
</ul>
 
**`Room.add_source_data(loc, data)`**

 <ul>
 
Add a source based on a list of values. Careful! Make sure you use a `dt` value that matches the table data, as an entry of the data list will be used on every time tick. For example, if you make the data table represent the value of the wave every 200ms, then be sure to set `dt` to 200ms as well when you run the simulation. If there are less points in the list of values than there are time steps, then a value of 0 is used for all time steps past the last data point.
  
`loc` is the room-specific coordinate of the source. Note: unless `ds=1`, this is not the same as the list indices of the point in the room.

`data` is a list of floats (the value of the wave at that time). This should be something like `np.sin(np.arange(0, 10, 0.2))`, for example.
 
</ul>
 
**`Room.add_walls(walls)`**

 <ul>
 
Add walls to the system after constructing the Room object. 
  
`walls` is a list of `Wall` objects to add the the system.
 
</ul>
 
**`Room.create_mask()`**

<ul>
 
Create a mask for the values of the room based on the currently set walls. This is automatically done when running the simulation, but it can be run beforehand if you want to plot the mask for visualization.
 
</ul>
 
**`Room.get_mask()`**

 <ul>
 
Returns a 2D array of the wall mask as currently calculated.
 
</ul>

**`Room.run(dt, t_final)`**

<ul>
 
Calculate the wave propagation from the set sources and using the set walls. This will simulate from `t=0` to `t_final` at `dt` time steps. If `t_final` isn't an exact multiple of `dt`, then it acts like an upper bound. 
  
`dt` a float giving the time step for the simulation. A smaller value means more time resolution. WARNING: Numerical stability will almost certainly be lost if this is not set to satisfy the [CFL Condition](https://en.wikipedia.org/wiki/Courant%E2%80%93Friedrichs%E2%80%93Lewy_condition), namely $\frac{u*dt}{ds} \leq C_{max}$ where $u$ is the `wavespeed` and $c_{max}$ is approximately 1 for the numerical method being used. 

`t_final` a float giving an upper limit for the amount of time to be simulated. A higher value will take more time to simulate, and will likely just repeat the steady state after a certain point in time...
 
</ul>

</ul>
 
`Wall(endpoint1, endpoint2, transmission)`

<ul>

This creates an instance of a `Wall` class, which contains the wall's endpoints and transmission factor.  

`endpoint1` and `endpoint2` are tuple2 or 2-list2 of floats giving the position of each end of the wall in the room-specific coordinates. Note: unless `ds=1`, this is not the same as the list indices of the point in the room.

`transmission` is a float in [0,1] which defines the proportion of wave amplitude able to penetrate the wall. If 0, then all energy is reflected back inwards, and if 1 then the wall "isn't there".
</ul>

## Visualization

The `visualization` module contains a few functions for visualizing results, or processing results into an easily displayed format.

**`animate(data, *, filepath='', frame_space=10, walls=[])`**

<ul>

Automatically animate the given data using `matplotlib.animation.ArtistAnimation`. The animation file can optionally be saved to a file.

`data` is a 3D array of waveform over time, which is the output from running the simulation.

`filename` is the name and path of output file. Leave this blank to not save. Output formats are those supported by `matplotlib.animation.ArtistAnimation`, which is at least ".gif" and ".webp".

`frame_space` is the temporal resolution of resulting animation. Make sure this isn't too small!

`walls` is to optionally include the walls in the animation. They won't be visible if this isn't included.

</ul>

**`get_steady_state_index(data, *, sample_points, rms_tolerance=0.1, window_size=0.1)`**

<ul>

This function calculates the windowed RMS of the given points over time. This data is compared to the RMS value at the end of the simulation. Then the latest time index where all point RMS's are within a tolerance to the final RMS is taken as the time index where steady-state is reached.

`data` is a 3D array of waveform over time, which is the output from running the simulation.

`sample_points` is a list of points in the room which will be checked for RMS.

`rms_tolerance` is a float in [0, 1] defining the limit on the amount the RMS is allowed to change from the final value and still be considered steady-state.

`window_size` is a float in [0, 1] defining the percent of total points to consider in the window.

</ul>

**`get_standing_waves(data, *, steady_state_kwargs=None)`**

<ul>

This function calculates when the steady state begins, and returns a 2D array which is the average of the absolute value of all of the rooms points across all steady state times.

`data` is a 3D array of waveform over time, which is the output from running the simulation.

`steady_state_kwargs` is a dict of the keyword arguments to pass to `get_steady_state_index`. If `None`, then the default parameters and a sample point at the middle of the room are used.

</ul>
