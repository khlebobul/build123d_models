"""
name: closet_rod_adapter.py
desc:
    Накладка на штангу для узких шкафов с наклонными пазами для вешалок.
    Вешалки размещаются под углом, чтобы поместиться в узком шкафу.
"""
from build123d import *
from ocp_vscode import show_object
import math

# Параметры накладки
rod_diameter = 25       # Диаметр штанги
rod_length = 300        # Длина накладки
wall_thickness = 3      # Толщина стенки накладки
num_slots = 10          # Количество пазов для вешалок
slot_width = 5          # Ширина паза
slot_depth = 30         # Глубина паза (увеличена)
slot_angle = 45         # Угол наклона паза (градусы)
gap_width = 8           # Ширина разреза снизу для надевания

with BuildPart() as adapter:
    # Создаем основную трубу (накладка на штангу)
    with BuildSketch() as profile:
        Circle(rod_diameter / 2 + wall_thickness)
        Circle(rod_diameter / 2, mode=Mode.SUBTRACT)
    
    extrude(amount=rod_length)
    
    # Создаем продольный разрез снизу для надевания на штангу
    with BuildSketch(Plane.XY) as gap_sketch:
        with Locations((0, 0)):
            Rectangle(gap_width, rod_length + 10)
    
    extrude(amount=rod_diameter, mode=Mode.SUBTRACT, dir=(0, -1, 0))
    
    # Вычисляем расстояние между пазами
    spacing = rod_length / (num_slots + 1)
    
    # Создаем наклонные пазы для вешалок
    for i in range(num_slots):
        z_pos = spacing * (i + 1)
        
        # Создаем паз как вырез
        with BuildSketch(Plane.XZ.offset(rod_diameter / 2 + wall_thickness)) as slot_sketch:
            with Locations((0, z_pos)):
                with PolarLocations(0, 1):
                    Rectangle(slot_depth, slot_width, rotation=slot_angle)
        
        extrude(amount=-wall_thickness * 2, mode=Mode.SUBTRACT)
    
    # Добавляем скругления для прочности (опционально)
    try:
        edges_to_fillet = adapter.edges().filter_by(GeomType.CIRCLE)
        fillet(edges_to_fillet, radius=0.5)
    except:
        pass

# Отображаем результат
show_object(adapter.part, name="closet_rod_adapter")

# Экспортируем в STL
adapter.part.export_stl("closet_rod_adapter.stl")
print("Модель экспортирована в closet_rod_adapter.stl")