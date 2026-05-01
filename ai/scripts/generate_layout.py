"""
Generate manufacturing layout 3D scene with boxes and triangles
Represents Pabrik Baja Nirkarat IMIP equipment zones
"""

import numpy as np
import json
from pathlib import Path


def create_box_mesh(name: str, center: tuple, size: tuple, color: tuple = None) -> dict:
    x, y, z = center
    w, h, d = size
    r, g, b = color or (0.5, 0.5, 0.5)

    return {
        "name": name,
        "type": "box",
        "center": center,
        "size": size,
        "color": [r, g, b, 1.0],
        "vertices": [
            [x - w/2, y, z - d/2], [x + w/2, y, z - d/2], [x + w/2, y, z + d/2], [x - w/2, y, z + d/2],
            [x - w/2, y + h, z - d/2], [x + w/2, y + h, z - d/2], [x + w/2, y + h, z + d/2], [x - w/2, y + h, z + d/2]
        ],
        "faces": [
            [0, 1, 2, 3], [4, 5, 6, 7], [0, 4, 5, 1],
            [1, 5, 6, 2], [2, 6, 7, 3], [3, 7, 4, 0]
        ]
    }


def create_cylinder_mesh(name: str, center: tuple, radius: float, height: float, color: tuple = None) -> dict:
    x, y, z = center
    r, g, b = color or (0.5, 0.5, 0.5)
    segments = 12
    vertices = []

    for i in range(segments):
        angle = 2 * np.pi * i / segments
        vertices.append([x + radius * np.cos(angle), y, z + radius * np.sin(angle)])

    for i in range(segments):
        angle = 2 * np.pi * i / segments
        vertices.append([x + radius * np.cos(angle), y + height, z + radius * np.sin(angle)])

    faces = []
    for i in range(segments):
        next_i = (i + 1) % segments
        faces.append([i, next_i, next_i + segments, i + segments])

    for i in range(segments):
        next_i = (i + 1) % segments
        faces.append([i, next_i, next_i + segments])
        faces.append([i, next_i + segments, i + segments])

    return {
        "name": name,
        "type": "cylinder",
        "center": center,
        "radius": radius,
        "height": height,
        "color": [r, g, b, 1.0],
        "vertices": vertices,
        "faces": faces
    }


def create_cone_mesh(name: str, center: tuple, radius: float, height: float, color: tuple = None) -> dict:
    x, y, z = center
    r, g, b = color or (0.6, 0.4, 0.2)
    segments = 12
    vertices = [[x, y, z]]

    for i in range(segments):
        angle = 2 * np.pi * i / segments
        vertices.append([x + radius * np.cos(angle), y, z + radius * np.sin(angle)])

    top_idx = 0
    ring_start = 1

    faces = []
    for i in range(segments):
        next_i = (i + 1) % segments
        faces.append([top_idx, ring_start + i, ring_start + next_i])

    return {
        "name": name,
        "type": "cone",
        "center": center,
        "radius": radius,
        "height": height,
        "color": [r, g, b, 1.0],
        "vertices": vertices,
        "faces": faces
    }


def generate_imip_layout() -> dict:
    objects = []

    objects.append(create_box_mesh("Raw Material Storage", (0, 1.5, -20), (8, 3, 6), (0.4, 0.35, 0.3)))
    objects.append(create_box_mesh("Conveyor A", (-5, 1, -12), (2, 1, 10), (0.3, 0.3, 0.35)))
    objects.append(create_box_mesh("Conveyor B", (5, 1, -12), (2, 1, 10), (0.3, 0.3, 0.35)))

    objects.append(create_cylinder_mesh("EAF Furnace 1", (-8, 3, -4), 3, 6, (0.8, 0.2, 0.1)))
    objects.append(create_cylinder_mesh("EAF Furnace 2", (0, 3, -4), 3, 6, (0.8, 0.2, 0.1)))
    objects.append(create_cylinder_mesh("EAF Furnace 3", (8, 3, -4), 3, 6, (0.8, 0.2, 0.1)))

    objects.append(create_box_mesh("AOD Converter", (0, 1.5, 4), (5, 4, 4), (0.7, 0.4, 0.2)))

    objects.append(create_box_mesh("Continuous Caster", (0, 1, 12), (4, 3, 8), (0.5, 0.5, 0.55)))

    objects.append(create_box_mesh("Rolling Mill Main", (0, 2, 22), (6, 4, 10), (0.35, 0.4, 0.5)))
    objects.append(create_box_mesh("Rolling Mill Roll 1", (-3, 2, 20), (1, 3, 2), (0.4, 0.4, 0.45)))
    objects.append(create_box_mesh("Rolling Mill Roll 2", (3, 2, 20), (1, 3, 2), (0.4, 0.4, 0.45)))
    objects.append(create_box_mesh("Rolling Mill Roll 3", (-3, 2, 24), (1, 3, 2), (0.4, 0.4, 0.45)))
    objects.append(create_box_mesh("Rolling Mill Roll 4", (3, 2, 24), (1, 3, 2), (0.4, 0.4, 0.45)))

    objects.append(create_box_mesh("Finishing Area", (0, 1, 32), (8, 2, 6), (0.45, 0.45, 0.4)))
    objects.append(create_cone_mesh("Stack 1", (-10, 8, -8), 1.5, 16, (0.6, 0.6, 0.65)))
    objects.append(create_cone_mesh("Stack 2", (10, 8, -8), 1.5, 16, (0.6, 0.6, 0.65)))
    objects.append(create_cone_mesh("Stack 3", (-10, 8, 14), 1.5, 16, (0.6, 0.6, 0.65)))
    objects.append(create_cone_mesh("Stack 4", (10, 8, 14), 1.5, 16, (0.6, 0.6, 0.65)))

    objects.append(create_box_mesh("Control Room", (15, 3, 0), (4, 3, 6), (0.2, 0.3, 0.5)))

    for i, obj in enumerate(objects):
        obj["id"] = i

    return {"objects": objects, "metadata": {
        "plant": "Pabrik Baja Nirkarat IMIP",
        "location": "Morowali, Sulawesi Tengah",
        "capacity": "1.2 juta ton/tahun",
        "zones": ["Raw Material", "EAF", "AOD", "Casting", "Rolling", "Finishing"]
    }}


def save_json_scene(scene: dict, output_path: str):
    with open(output_path, 'w') as f:
        json.dump(scene, f, indent=2)
    print(f"Saved JSON scene to {output_path}")


def save_obj_file(scene: dict, output_path: str):
    vertices = []
    faces = []
    vertex_offset = 0

    for obj in scene["objects"]:
        for v in obj["vertices"]:
            vertices.append(v)
        for face in obj["faces"]:
            faces.append([f + vertex_offset for f in face])
        vertex_offset += len(obj["vertices"])

    with open(output_path, 'w') as f:
        f.write("# Manufacturing Layout - Pabrik Baja Nirkarat IMIP\n")
        f.write("# Generated by AI Twin Factory\n\n")

        for v in vertices:
            f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")

        f.write("\n")

        for fa in faces:
            f.write(f"f {fa[0]+1} {fa[1]+1} {fa[2]+1}\n")

    print(f"Saved OBJ file to {output_path}")


def save_simple_glb(scene: dict, output_path: str):
    import struct

    with open(output_path, 'wb') as f:
        f.write(b'glTF')
        f.write(struct.pack('<I', 2))
        f.write(struct.pack('<I', 0))

    print(f"Saved minimal GLB placeholder to {output_path}")


if __name__ == "__main__":
    output_dir = Path("/Users/dikaizm/Documents/PROGRAMMING/ml-ai/hackathon-ai-elevate/frontend/public/models")
    output_dir.mkdir(parents=True, exist_ok=True)

    scene = generate_imip_layout()

    save_json_scene(scene, str(output_dir / "manufacturing_layout.json"))
    save_obj_file(scene, str(output_dir / "manufacturing_layout.obj"))

    scene_data = json.dumps(scene)
    glb_path = output_dir / "manufacturing_layout.glb"

    import struct

    with open(glb_path, 'wb') as f:
        header = b'glTF'
        version = struct.pack('<I', 2)
        length = struct.pack('<I', 0)

        f.write(header + version + length)

        json_bytes = scene_data.encode('utf-8')
        padding = (4 - len(json_bytes) % 4) % 4
        json_bytes_padded = json_bytes + b' ' * padding

        f.write(struct.pack('<I', len(json_bytes_padded)))
        f.write(b'JSON')
        f.write(json_bytes_padded)

    print(f"Saved GLB to {glb_path}")
    print(f"\nScene contains {len(scene['objects'])} objects:")
    for obj in scene['objects']:
        print(f"  - {obj['name']} ({obj['type']}) at {obj['center']}")
