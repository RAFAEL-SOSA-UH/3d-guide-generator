"""Builds and renders the example treasure chest.

    pip install bpy            (Blender as a Python module, same version as Blender 5.1)
    python make_chest.py [OUTPUT_FOLDER] [still|video]

still: chest.png + chest.blend.  video: frames/f_0001.png ... (parts appear, then a turntable);
join them with  ffmpeg -framerate 24 -i frames/f_%04d.png -pix_fmt yuv420p chest_build_turntable.mp4
"""
import bpy, bmesh, math, sys
from mathutils import Matrix
from pathlib import Path
out = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parent)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
col = sc.collection

def mat(name, rgb, metal=0.0, rough=0.6):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough
    return m
wood = mat("Wood", (0.30, 0.13, 0.05), 0, 0.7)
metal = mat("Metal", (0.22, 0.22, 0.24), 1.0, 0.45)
gold = mat("Gold", (0.85, 0.6, 0.18), 1.0, 0.3)
floor_m = mat("Floor", (0.55, 0.55, 0.58), 0, 0.9)

def obj(name, bm, m, parent=None, bevel=0.0):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); col.objects.link(o); me.materials.append(m)
    for p in me.polygons: p.use_smooth = False
    if bevel:
        md = o.modifiers.new("Bevel", "BEVEL"); md.width = bevel; md.segments = 2
    if parent: o.parent = parent
    return o

def box(sx, sy, sz, loc):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x = v.co.x * sx + loc[0]; v.co.y = v.co.y * sy + loc[1]; v.co.z = v.co.z * sz + loc[2]
    return bm

def half_cyl(r, length, x0, z0, segs=32):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=segs, radius1=r, radius2=r, depth=length)
    bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.radians(90), 3, 'Y'))
    res = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, 0), plane_no=(0, 0, 1), clear_inner=True)
    edges = [e for e in bm.edges if e.is_boundary]
    bmesh.ops.holes_fill(bm, edges=edges, sides=0)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(x0, 0, z0))
    return bm

root = bpy.data.objects.new("Chest", None); col.objects.link(root)
W, D, H, R = 1.0, 0.6, 0.45, 0.3
body = obj("Body", box(W, D, H, (0, 0, H / 2)), wood, root, bevel=0.015)
lid = obj("Lid", half_cyl(R, W, 0, H), wood, root, bevel=0.01)
bands = []
for i, x in enumerate((-0.38, 0.38)):
    bands.append(obj(f"BandBody{i}", box(0.06, D + 0.02, H + 0.01, (x, 0, H / 2)), metal, root))
    bands.append(obj(f"BandLid{i}", half_cyl(R + 0.01, 0.06, x, H), metal, root))
lock = obj("Lock", box(0.12, 0.04, 0.14, (0, -(D / 2 + 0.02), H - 0.01)), gold, root, bevel=0.008)

bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=6)
obj("Floor", bm, floor_m)

sun = bpy.data.lights.new("Sun", "SUN"); sun.energy = 3.5; sun.angle = math.radians(8)
so = bpy.data.objects.new("Sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(35))
world = bpy.data.worlds.new("World"); sc.world = world; world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.75, 0.8, 0.88, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.8

cam = bpy.data.cameras.new("Cam"); cam.lens = 50
co = bpy.data.objects.new("Cam", cam); col.objects.link(co); sc.camera = co
co.location = (2.3, -2.9, 1.7)
tgt = bpy.data.objects.new("Target", None); col.objects.link(tgt); tgt.location = (0, 0, 0.42)
tc = co.constraints.new("TRACK_TO"); tc.target = tgt; tc.track_axis = 'TRACK_NEGATIVE_Z'; tc.up_axis = 'UP_Y'

sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"
sc.cycles.use_denoising = True
sc.view_settings.view_transform = "AgX"

mode = sys.argv[2] if len(sys.argv) > 2 else "still"
if mode == "still":
    sc.cycles.samples = 96
    sc.render.resolution_x, sc.render.resolution_y = 1200, 900
    sc.render.filepath = f"{out}/chest.png"
    bpy.ops.render.render(write_still=True)
    bpy.ops.wm.save_as_mainfile(filepath=f"{out}/chest.blend")
else:
    sc.cycles.samples = 12
    sc.render.resolution_x, sc.render.resolution_y = 640, 480
    sc.frame_start, sc.frame_end = 1, 120
    parts = [[body], [lid], bands, [lock]]
    for i, group in enumerate(parts):
        for o in group:
            show = 1 + i * 12
            if show > 1:
                o.hide_render = True; o.keyframe_insert("hide_render", frame=1)
                o.hide_render = False; o.keyframe_insert("hide_render", frame=show)
    root.rotation_euler = (0, 0, 0); root.keyframe_insert("rotation_euler", frame=49)
    root.rotation_euler = (0, 0, math.radians(360)); root.keyframe_insert("rotation_euler", frame=120)
    for fc in root.animation_data.action.layers[0].strips[0].channelbags[0].fcurves:
        for k in fc.keyframe_points: k.interpolation = "LINEAR"
    sc.render.filepath = f"{out}/frames/f_"
    bpy.ops.render.render(animation=True)
print("done")
