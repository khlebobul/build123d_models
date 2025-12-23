"""
name: closet_rod_adapter.py
desc:
    Adapter for closet rod for narrow closets with angled slots for hangers.
    Hangers are placed at an angle to fit in narrow closet.
    Octagonal shape for greater slot height.
"""
from build123d import *
from ocp_vscode import show_object
import math

# Adapter parameters
rod_diameter = 25       # Rod diameter
rod_length = 40        # Adapter length
wall_thickness = 3      # Adapter wall thickness
slot_spacing = 30       # Distance between slot centers (adjust as needed)
slot_width = 5          # Slot width
slot_depth = 45         # Slot depth
slot_angle = 45         # Slot angle (degrees)
gap_width = 15          # Width of bottom cut for installation

# Calculate number of slots based on length and spacing
num_slots = max(1, int((rod_length - slot_spacing) / slot_spacing))

# Octagon parameters
outer_radius = rod_diameter / 2 + wall_thickness + 5  # Increased radius for height

with BuildPart() as adapter:
    # Create octagonal tube (rod adapter)
    with BuildSketch() as profile:
        RegularPolygon(outer_radius, 8)  # Outer octagon
        Circle(rod_diameter / 2, mode=Mode.SUBTRACT)  # Inner circle for rod
    extrude(amount=rod_length)
    
    # Calculate octagon face heights
    top_offset = outer_radius * math.cos(math.pi / 8)  # Top face height
    bottom_offset = -outer_radius * math.cos(math.pi / 8)  # Bottom face height
    
    # Create longitudinal cut at BOTTOM for installing on rod
    # Start lower and cut deeper
    with BuildSketch(Plane.XZ.offset(bottom_offset - 5)) as gap_sketch:
        with Locations((0, rod_length / 2)):
            Rectangle(gap_width, rod_length)
    extrude(amount=outer_radius + 10, mode=Mode.SUBTRACT)  # Cut much deeper upward
    
    # Calculate spacing between slots
    spacing = rod_length / (num_slots + 1)
    
    # Create angled slots for hangers at TOP (opposite side)
    for i in range(num_slots):
        z_pos = spacing * (i + 1)
        
        # Create slot from top - cut deep
        with BuildSketch(Plane.XZ.offset(top_offset + 5)) as slot_sketch:  # Start higher
            with Locations((0, z_pos)):
                Rectangle(slot_depth, slot_width, rotation=slot_angle)
        
        # Cut to greater depth
        extrude(amount=-(outer_radius + 10), mode=Mode.SUBTRACT)
    
    # Add fillets for strength (optional)
    try:
        edges_to_fillet = adapter.edges().filter_by(GeomType.CIRCLE)
        fillet(edges_to_fillet, radius=0.5)
    except:
        pass

# Display result
show_object(adapter.part, name="closet_rod_adapter")

# Export to STL
adapter.part.export_stl("closet_rod_adapter/closet_rod_adapter.stl")
print(f"Model exported to closet_rod_adapter.stl")
print(f"Rod length: {rod_length}mm, Number of slots: {num_slots}, Spacing: {spacing:.1f}mm")