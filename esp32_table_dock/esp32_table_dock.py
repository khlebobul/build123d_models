"""Stretch the original ticker32 stand into a taller one-piece cable dock.

Requires: numpy, manifold3d. Run this file to regenerate the STL.
"""

from pathlib import Path
import struct

import manifold3d as mf
import numpy as np


HERE = Path(__file__).parent
SOURCE = HERE / "ticker32-cfc1.stl"
OUTPUT = HERE / "esp32_table_dock.stl"
LIFT = 15.0
STRETCH_BELOW_Z = 8.0
CABLE_WIDTH = 16.0
CHANNEL_START_Y = 8.0
CHANNEL_TOP_Z = 28.0
ACCESS_WIDTH = 34.0
ACCESS_END_Y = 24.0
ACCESS_TOP_Z = 34.0


def read_stl(path):
    data = path.read_bytes()
    count = struct.unpack_from("<I", data, 80)[0]
    facets = np.frombuffer(
        data,
        dtype=np.dtype([("normal", "<f4", 3), ("vertices", "<f4", (3, 3)), ("attribute", "<u2")]),
        count=count,
        offset=84,
    )
    vertices, indices = np.unique(
        np.round(facets["vertices"].reshape(-1, 3), 6), axis=0, return_inverse=True
    )
    solid = mf.Manifold(mf.Mesh(vertices.astype("f4"), indices.reshape(-1, 3).astype("u4")))
    assert solid.status() == mf.Error.NoError and not solid.is_empty()
    return solid


def write_stl(solid, path):
    mesh = solid.to_mesh()
    triangles = mesh.vert_properties[mesh.tri_verts, :3]
    records = np.zeros(len(triangles), dtype=np.dtype([
        ("normal", "<f4", 3), ("vertices", "<f4", (3, 3)), ("attribute", "<u2")
    ]))
    records["vertices"] = triangles
    normals = np.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0])
    lengths = np.linalg.norm(normals, axis=1)
    records["normal"] = normals / np.maximum(lengths[:, None], 1e-12)
    path.write_bytes(bytes(80) + struct.pack("<I", len(records)) + records.tobytes())


if __name__ == "__main__":
    original = read_stl(SOURCE)
    upper, lower = original.split_by_plane((0, 0, 1), STRETCH_BELOW_Z)
    body = upper.translate((0, 0, LIFT)) + lower.scale(
        (1, 1, (STRETCH_BELOW_Z + LIFT) / STRETCH_BELOW_Z)
    )
    channel = mf.Manifold.cube((CABLE_WIDTH, 51 - CHANNEL_START_Y, CHANNEL_TOP_Z)).translate(
        ((50 - CABLE_WIDTH) / 2, CHANNEL_START_Y, 0)
    )
    access = mf.Manifold.cube((ACCESS_WIDTH, ACCESS_END_Y - CHANNEL_START_Y, ACCESS_TOP_Z)).translate(
        ((50 - ACCESS_WIDTH) / 2, CHANNEL_START_Y, 0)
    )
    opening = channel + access
    result = body - opening
    assert result.status() == mf.Error.NoError and len(result.decompose()) == 1
    assert abs(result.bounding_box()[5] - (40 + LIFT)) < 0.01
    assert len(opening.decompose()) == 1 and (result ^ opening).volume() < 0.01
    write_stl(result, OUTPUT)
    assert read_stl(OUTPUT).status() == mf.Error.NoError
    print(f"Saved {OUTPUT}: {ACCESS_WIDTH:g} mm opening for buttons and cable")
