"""
name: closet_rod_adapter.py
desc:
    Накладка на штангу для узких шкафов с наклонными пазами для вешалок.
    Вешалки размещаются под углом, чтобы поместиться в узком шкафу.
    Восьмиугольная форма для большей высоты пазов.
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
slot_depth = 46         # Глубина паза
slot_angle = 45         # Угол наклона паза (градусы)
gap_width = 8           # Ширина разреза снизу для надевания

# Параметры восьмиугольника
outer_radius = rod_diameter / 2 + wall_thickness + 5  # Увеличенный радиус для высоты

with BuildPart() as adapter:
    # Создаем восьмиугольную трубу (накладка на штангу)
    with BuildSketch() as profile:
        RegularPolygon(outer_radius, 8)  # Внешний восьмиугольник
        Circle(rod_diameter / 2, mode=Mode.SUBTRACT)  # Внутренний круг под штангу
    extrude(amount=rod_length)
    
    # Вычисляем высоту граней восьмиугольника
    top_offset = outer_radius * math.cos(math.pi / 8)  # Высота верхней грани
    bottom_offset = -outer_radius * math.cos(math.pi / 8)  # Высота нижней грани
    
    # Создаем продольный разрез ВНИЗУ для надевания на штангу
    # Начинаем ниже и прорезаем глубже
    with BuildSketch(Plane.XZ.offset(bottom_offset - 5)) as gap_sketch:
        with Locations((0, rod_length / 2)):
            Rectangle(gap_width, rod_length)
    extrude(amount=outer_radius + 10, mode=Mode.SUBTRACT)  # Прорезаем намного глубже вверх
    
    # Вычисляем расстояние между пазами
    spacing = rod_length / (num_slots + 1)
    
    # Создаем наклонные пазы для вешалок НАВЕРХУ (противоположная сторона)
    for i in range(num_slots):
        z_pos = spacing * (i + 1)
        
        # Создаем паз сверху - прорезаем глубоко
        with BuildSketch(Plane.XZ.offset(top_offset + 5)) as slot_sketch:  # Начинаем выше
            with Locations((0, z_pos)):
                Rectangle(slot_depth, slot_width, rotation=slot_angle)
        # Прорезаем на большую глубину
        extrude(amount=-(outer_radius + 10), mode=Mode.SUBTRACT)
    
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