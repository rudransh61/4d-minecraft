from ursina import *
import numpy as np
from perlin_noise import PerlinNoise

# Initialize the Ursina application
app = Ursina()

# Define the size and spacing of the voxels
voxel_size = 0.5
spacing = 0

# Define the number of voxels in each direction
num_voxels = 20

# Initialize Perlin noise generator
noise = PerlinNoise(octaves=2)  # Adjust octaves for detail level

# Define the offset and time-based variable for the Perlin noise
noise_offset = (100, 100)  # Offset to shift the noise pattern
time_variable = 0  # Initial time variable

# Define texture maps for different heights
def get_texture(height):
    if 0 <= height < 1.5:
        return 'water.jfif'  # Water texture
    elif 1.8 <= height :
        return 'grass.jfif'  # Sand texture
    else:
        return 'sand.jfif'  # Grass texture

# Function to create a voxel with Perlin noise-based height and texture
def create_voxel(x, z):
    # Adjust x and z to center the grid around (0, 0)
    x = x - num_voxels // 2
    z = z - num_voxels // 2
    # Generate height based on Perlin noise with offset and time variable
    height = (abs(noise([(x + noise_offset[0]) / 10.0, (z + noise_offset[1]) / 10.0, time_variable / 10.0])) * 4 + 1) * 5
    voxel_texture = get_texture(height)  # Get texture based on height
    voxel = Entity(model='cube', texture=voxel_texture, scale=(voxel_size, voxel_size * height, voxel_size), position=(x * voxel_size, height / 2, z * voxel_size))
    
    # Create a black border around the voxel
    # border_size = 0.1  # Thickness of the border
    # border_color = color.rgb(0, 0, 0)  # Black color
    # Entity(model='cube', color=border_color, scale=(voxel_size + border_size, voxel_size * height + border_size, voxel_size + border_size), position=(x * voxel_size, height / 2, z * voxel_size), parent=voxel)
    
    return voxel

# Create a 2D array to store voxel entities
voxels = np.empty((num_voxels, num_voxels), dtype=object)

# Function to initialize the voxel grid
def initialize_voxels():
    for x in range(num_voxels):
        for z in range(num_voxels):
            voxel = create_voxel(x, z)
            voxels[x, z] = voxel

# Initialize the voxel grid
initialize_voxels()

# Set up the camera
camera.position = (10, 10, 10)
camera.look_at((0, 0, 0))

# Movement and rotation speed
speed = 5
rotation_speed = 90  # Degrees per second

# Create a Text entity to display the 4D coordinates
coordinate_text = Text(
    text=f'X: 0, Z: 0, Time: {time_variable:.2f}',
    position=(0.5, 0.45),
    origin=(0.5, 0.5),
    scale=2
)

# Function to update voxel heights and textures
def update_voxels():
    for x in range(num_voxels):
        for z in range(num_voxels):
            height = abs(noise([(x - num_voxels // 2 + noise_offset[0]) / 10.0, (z - num_voxels // 2 + noise_offset[1]) / 10.0, time_variable / 10.0])) * 4 + 1
            voxel = voxels[x, z]
            voxel.scale = (voxel_size, voxel_size * height, voxel_size)
            voxel.position = ((x - num_voxels // 2) * voxel_size, height / 2, (z - num_voxels // 2) * voxel_size)
            voxel.texture = get_texture(height)

# Function to update camera position and rotation based on user input
def update():
    global time_variable  # Declare time_variable as global to modify it
    
    # Adjust time variable based on key input
    if held_keys['f']:
        time_variable += time.dt * 0.5  # Move time forward
    if held_keys['g']:
        time_variable -= time.dt * 0.5  # Move time backward
    
    # Update voxel heights and textures
    update_voxels()
    
    # Update the 4D coordinate text
    coordinate_text.text = f'X: {camera.position.x:.2f}, Z: {camera.position.z:.2f}, Time: {time_variable:.2f}'
    
    # Camera movement
    if held_keys['w']:
        camera.position += camera.forward * speed * time.dt
    if held_keys['s']:
        camera.position -= camera.forward * speed * time.dt
    if held_keys['a']:
        camera.position -= camera.right * speed * time.dt
    if held_keys['d']:
        camera.position += camera.right * speed * time.dt
    if held_keys['space']:
        camera.position += Vec3(0, speed * time.dt, 0)
    if held_keys['left shift']:
        camera.position -= Vec3(0, speed * time.dt, 0)
    
    # Camera rotation
    if held_keys['left arrow']:
        camera.rotation_y -= rotation_speed * time.dt
    if held_keys['right arrow']:
        camera.rotation_y += rotation_speed * time.dt
    if held_keys['up arrow']:
        camera.rotation_x -= rotation_speed * time.dt
    if held_keys['down arrow']:
        camera.rotation_x += rotation_speed * time.dt

    # Additional camera movement along x and z axes
    if held_keys['r']:  # Move camera right
        camera.position += Vec3(speed * time.dt, 0, 0)
    if held_keys['t']:  # Move camera left
        camera.position -= Vec3(speed * time.dt, 0, 0)
    if held_keys['y']:  # Move camera up
        camera.position += Vec3(0, speed * time.dt, 0)
    if held_keys['u']:  # Move camera down
        camera.position -= Vec3(0, speed * time.dt, 0)

# Run the Ursina application
app.run()
