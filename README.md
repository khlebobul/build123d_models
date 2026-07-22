# build123d models

A collection of 3D models created using [build123d](https://github.com/build123d/build123d)

### Credits

- [build123d](https://github.com/build123d/build123d)

### Models

- [Ring Clamp](#ring-clamp)
- [Closet Rod Adapter](#closet-rod-adapter)
- [Mug Dust Cover](#mug-dust-cover)
- [Hockey Player Holder](#hockey-player-holder)

### Requirements

To use build123d, you need to install the following dependencies:

```bash
pip install build123d
```

For model visualization (optional, used in examples):
```bash
pip install ocp-vscode
```

**System requirements:**
- Python 3.8 or higher
- OpenCASCADE (installed automatically with build123d)

### How to use

```python
from build123d import *
```

### Models

#### Ring Clamp

<img src="ring_clamp/ring_clamp.png" alt="Ring Clamp" width="50%">

E27 ring clamp created for [The Swirl Lamp](https://makerworld.com/en/models/738820-the-swirl-lamp#profileId-671097) model on Makerworld.

**Customizable Parameters:**

You can modify the following parameters in `clamp.py` to customize the ring clamp:

- `outer_radius` (default: 25) - Outer radius of the ring in mm
- `inner_radius` (default: 37.2/2) - Inner radius of the ring in mm (adjust for different bulb sizes)
- `thickness` (default: 5) - Part thickness/height in mm
- `cutout_angle` (default: 70) - Angle of the cutout section in degrees
- `ear_radius` (default: 3) - Half-width of each ear protrusion in mm
- `ear_height` (default: 9.8) - Length of the ear protrusion in mm
- `num_ears` (default: 4) - Number of ears around the ring

**Files:**
- [clamp.py](ring_clamp/clamp.py) - Source code
- [ring_clamp.stl](ring_clamp/ring_clamp.stl) - 3D model file

#### Closet Rod Adapter

<img src="closet_rod_adapter/closet_rod_adapter.png" alt="Closet Rod Adapter" width="50%">

Adapter for closet rod for narrow closets with angled slots for hangers. Hangers are placed at an angle to fit in narrow closet. Octagonal shape for greater slot height.

**Customizable Parameters:**

You can modify the following parameters in `closet_rod_adapter.py` to customize the adapter:

- `rod_diameter` (default: 25) - Rod diameter in mm
- `rod_length` (default: 120) - Adapter length in mm
- `wall_thickness` (default: 3) - Adapter wall thickness in mm
- `slot_spacing` (default: 30) - Distance between slot centers in mm
- `slot_width` (default: 5) - Slot width in mm
- `slot_depth` (default: 45) - Slot depth in mm
- `slot_angle` (default: 20) - Slot angle in degrees
- `gap_width` (default: 15) - Width of bottom cut for installation in mm

**Files:**
- [closet_rod_adapter.py](closet_rod_adapter/closet_rod_adapter.py) - Source code
- [closet_rod_adapter.stl](closet_rod_adapter/closet_rod_adapter.stl) - 3D model file
- [Model on Makerworld](https://makerworld.com/en/models/2172973-closet-rod-adapter-customisable-with-build123d#profileId-2357070)
- [Model on Printables](https://www.printables.com/model/1533332-closet-rod-adapter-customisable-with-build123d)

#### Mug Dust Cover

| 3D Model | Real |
|:---:|:---:|
| <img src="mug_dust_cover/mug_dust_cover.png" alt="Mug Dust Cover" width="100%"> | <img src="mug_dust_cover/mug_dust_cover_real.png" alt="Mug Dust Cover real" width="100%"> |

Dust cover for a mug. Bottom channels let moisture escape sideways while
keeping the top closed against falling dust.

**Customizable Parameters:**

- `mug_outer_diameter` - Mug outside diameter
- `overhang` - Cover overhang beyond the mug
- `top_thickness` - Cover thickness
- `vent_count` - Number of ventilation channels
- `vent_width` - Width of each ventilation channel
- `vent_height` - Height of each ventilation channel

**Files:**
- [mug_dust_cover.py](mug_dust_cover/mug_dust_cover.py) - Source code
- [mug_dust_cover.stl](mug_dust_cover/mug_dust_cover.stl) - 3D model file
- [Model on Makerworld](https://makerworld.com/en/models/3019858-mug-dust-cover#profileId-3392740)
- [Model on Printables](https://www.printables.com/model/1774129-mug-dust-cover)

#### Hockey Player Holder

| 3D Model | Real // TODO |
|:---:|:---:|
| <img src="hockey_player_holder/hockey_player_holder.png" alt="Hockey Player Holder" width="100%"> | <img src="hockey_player_holder/hockey_player_holder_real.jpg" alt="Hockey Player Holder real" width="100%"> |

Holder for tabletop hockey game player figures. Tubular body with a wider collar and slits at the end for inserting player pieces.

**Customizable Parameters:**

- `tube_length` (default: 35) - Total tube length in mm
- `tube_dia` (default: 3.9) - Tube diameter in mm
- `collar_pos` (default: 7) - Distance from short end to collar in mm
- `collar_length` (default: 1) - Collar thickness in mm
- `collar_dia` (default: 6) - Collar outer diameter in mm
- `slit_depth` (default: 1) - How deep the notch cuts into the tube in mm
- `slit_height` (default: 6) - Length of slit along the tube axis in mm

**Files:**
- [hockey_player_holder.py](hockey_player_holder/hockey_player_holder.py) - Source code
- [hockey_player_holder.stl](hockey_player_holder/hockey_player_holder.stl) - 3D model file
- [Model on Makerworld]() // TODO
- [Model on Printables]() // TODO

### License

[MIT](https://github.com/khlebobul/build123d_models/blob/main/LICENSE)
