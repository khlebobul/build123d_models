"""
name: ring_clamp.py
desc:
    Creating a ring with a cutout section and 4 ears.
    The part is created by:
    - Creating a ring profile with a cutout
    - Extruding the profile to create the main body
    - Adding 4 ears at 90-degree increments
"""
from build123d import *
from ocp_vscode import show_object
import math


# Part parameters
outer_radius = 25      # Outer radius of the ring
inner_radius = 37.2/2  # Inner radius of the ring
# inner_radius = 38.5/2  # Inner radius of the ring
thickness = 5          # Part thickness (ring height)
cutout_angle = 70      # Cutout angle in degrees
ear_radius = 3         # Ear width (half)
ear_height = 9.8       # Length of the ear protrusion
num_ears = 4           # Number of ears


with BuildPart() as ring_clamp:
    # Create the main ring with a cutout
    with BuildSketch() as profile:
        # Full ring
        Circle(outer_radius)
        Circle(inner_radius, mode=Mode.SUBTRACT)
        
        # Cut out a sector
        with BuildSketch(mode=Mode.SUBTRACT) as cutout:
            with Locations((0, 0)):
                # Create a triangle for the cutout
                cutout_start = -cutout_angle / 2
                cutout_end = cutout_angle / 2
                
                # Radius larger than the outer radius for a complete cut
                cut_radius = outer_radius * 1.5
                
                with BuildLine():
                    l1 = Line((0, 0), 
                             (cut_radius * math.cos(math.radians(cutout_start)), 
                              cut_radius * math.sin(math.radians(cutout_start))))
                    l2 = Line(l1 @ 1, 
                             (cut_radius * math.cos(math.radians(cutout_end)), 
                              cut_radius * math.sin(math.radians(cutout_end))))
                    Line(l2 @ 1, l1 @ 0)
                
                make_face()
    
    # Extrude the profile
    extrude(amount=thickness)
    
    # Add ears at 90-degree increments
    # Start at 45 degrees (between the cutout and the first axis)
    start_angle = 45
    angle_step = 90  # Exactly 90 degrees between ears
    
    for i in range(num_ears):
        angle = start_angle + angle_step * i
        angle_rad = math.radians(angle)
        
        # Position: outer edge of the ring + offset so the ear starts from the edge
        # The ear should touch the ring with its inner edge
        ear_offset = outer_radius + ear_height / 2 - ear_radius
        base_x = ear_offset * math.cos(angle_rad)
        base_y = ear_offset * math.sin(angle_rad)
        
        # Create a flat ear as a protrusion with a rounded profile
        with BuildSketch(Plane.XY.offset(0)) as ear_sketch:
            with Locations((base_x, base_y)):
                # Create a rectangle with rounded corners
                # The corner radius should be less than half of the minimum side
                corner_radius = min(ear_height, ear_radius * 2) * 0.4
                with PolarLocations(0, 1):
                    RectangleRounded(ear_height, ear_radius * 2, 
                                   corner_radius,  # Corner radius
                                   rotation=math.degrees(angle_rad))
        
        extrude(amount=thickness)


# Display the result in the OCP CAD Viewer
show_object(ring_clamp.part, name="ring_clamp")
ring_clamp.part.export_stl("ring_clamp/ring_clamp.stl")

