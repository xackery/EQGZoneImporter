import bpy
import os

class NpcType:
    def __init__(npcid, npcname):
        self.id = npcid
        self.name = npcname
npcs = []

class SpawnGroup:
    def __init__(self, id, spawngroupid):
        self.id = 0
        self.name = ""
        self.spawngroupid = 0
        self.spawn_limit = 0
        self.dist = 0
        self.max_x = 0
        self.min_x = 0
        self.max_y = 0
        self.min_y = 0
        self.delay = 0
        self.mindelay = 15000
        self.despawn = 0
        self.despawn_timer = 0
        self.wp_spawns = 0
spawngroups = {}


blend_file_path = bpy.data.filepath
directory = os.path.dirname(blend_file_path)
base_name = os.path.basename(blend_file_path).removesuffix(".blend")
target_file = os.path.join(directory, base_name + '.obj')

fl = open(base_name + "_light.txt", "w+")
fr = open(base_name + "_region.txt", "w+")
fm = open(base_name + "_material.txt", "w+")
fs2 = open(base_name + "_spawn2.sql", "w+")
fsg = open(base_name + "_spawngroup.sql", "w+")

def roundFloatStr(value):
    return str(round(value, 4))

for m in bpy.data.materials:
    fm.write("m " + m.name.replace(" ", "-") + " " + str(m.get("flag", 65536)) + " " + str(m.get("shader", "Opaque_MaxCB1.fx")) + "\n")
    for tree in m.texture_paint_slots:
        print("tree " +tree)
        for node in tree:
            print(node.name)

    for prop in m.items():
        for k in prop:
            if not isinstance(k, str):
                continue
            if k.startswith("e_"):
                fm.write("e " + m.name.replace(" ", "-") + " " +  k + " " + str(m[k]) +"\n")

for o in bpy.data.objects:
    if o.type == 'LIGHT':
        li = o.data
        if li.type == 'POINT':
            fl.write(o.name.replace(" ", "-") + " " + roundFloatStr(o.location.x*2) + " " + roundFloatStr(o.location.y*2) + " " + roundFloatStr(o.location.z*2) + " " + roundFloatStr(li.color[0]) + " " + roundFloatStr(li.color[1]) + " " + roundFloatStr(li.color[2]) + " " + roundFloatStr(li.energy/10) + "\n")
    if o.type == 'EMPTY':
        if o.empty_display_type == 'CUBE':
            fr.write(o.name.replace(" ", "-") + " " + roundFloatStr(o.location.y*2) + " " + roundFloatStr(o.location.x*2) + " " + roundFloatStr(o.location.z*2) + " " + roundFloatStr(o.scale.y*2) + " " + roundFloatStr(-o.scale.x*2) + " " + roundFloatStr((o.scale.z)*2) + " " + roundFloatStr(o.get("unknowna", 0)) + " " + roundFloatStr(o.get("unknownb", 0)) + " " + roundFloatStr(o.get("unknownc", 0)) + "\n")
    if o.type == 'MESH' and o.get("id", "0") != "0" and o.get("spawngroupid", "0") != "0":
        id = o.get("id", 0)
        spawngroupid = o.get("spawngroupid", 0)
        if not spawngroupid in spawngroups:
            spawngroups[spawngroupid] = SpawnGroup(id, spawngroupid)
        if o.get("spawngroup.name", "0") != "0":
            spawngroups[spawngroupid].name = o["spawngroup.name"]
        if o.get("spawngroup.spawn_limit", "0") != "0":
            spawngroups[spawngroupid].spawn_limit = o["spawngroup.spawn_limit"]
        if o.get("spawngroup.dist", "0") != "0":
            spawngroups[spawngroupid].dist = o["spawngroup.dist"]
        if o.get("spawngroup.max_x", "0") != "0":
            spawngroups[spawngroupid].dist = o["spawngroup.max_x"]
        if o.get("spawngroup.max_y", "0") != "0":
            spawngroups[spawngroupid].dist = o["spawngroup.max_y"]
        if o.get("spawngroup.min_x", "0") != "0":
            spawngroups[spawngroupid].dist = o["spawngroup.min_x"]
        if o.get("spawngroup.min_y", "0") != "0":
            spawngroups[spawngroupid].dist = o["spawngroup.min_y"]
        if o.get("spawngroup.delay", "0") != "0":
            spawngroups[spawngroupid].dist = o["spawngroup.delay"]
        if o.get("spawngroup.mindelay", "0") != "0":
            spawngroups[spawngroupid].dist = o["spawngroup.mindelay"]
        if o.get("spawngroup.despawn", "0") != "0":
            spawngroups[spawngroupid].dist = o["spawngroup.despawn"]
        if o.get("spawngroup.despawn_timer", "0") != "0":
            spawngroups[spawngroupid].dist = o["spawngroup.despawn_timer"]
        if o.get("spawngroup.wp_spawns", "0") != "0":
            spawngroups[spawngroupid].dist = o["spawngroup.wp_spawns"]         
        fs2.write("REPLACE INTO spawn2 (id, spawngroupid, x, y, z, heading, respawntime, variance, pathgrid, version) VALUES("+str(o.get("id", "0")) + ", " +str(o.get("spawngroupid", "0"))+ ", "+str(o.location.x*2)+", "+str(o.location.y*2)+", "+str(o.location.z*2)+", "+str(o.rotation_euler.z)+ ", "+str(o.get("respawntime", "0"))+ ", "+str(o.get("variance", "0"))+ ", "+str(o.get("pathgrid", "0"))+ ", "+str(o.get("version", "0"))+");\r\n")
        bpy.data.objects.remove(o, do_unlink=True)
        continue
    if o.type != 'MESH':
        bpy.data.objects.remove(o, do_unlink=True)

for sp in spawngroups:
    fsg.write("REPLACE INTO spawngroup (id, name, spawn_limit, dist, max_x, min_x, max_x, min_y, delay, mindelay, despawn, despawn_timer, wp_spawns) VALUES ("+str(spawngroups[sp].id)+", "+str(spawngroups[sp].name)+", "+str(spawngroups[sp].spawn_limit)+", "+str(spawngroups[sp].dist)+", "+str(spawngroups[sp].max_x)+", "+str(spawngroups[sp].min_x)+", "+str(spawngroups[sp].max_x)+", "+str(spawngroups[sp].min_y)+", "+str(spawngroups[sp].delay)+", "+str(spawngroups[sp].mindelay)+", "+str(spawngroups[sp].despawn)+", "+str(spawngroups[sp].despawn_timer)+", "+str(spawngroups[sp].wp_spawns)+");\r\n")
    
bpy.ops.export_scene.obj(filepath=target_file, check_existing=True, axis_forward='-X', axis_up='Z', filter_glob="*.obj;*.mtl", use_selection=False, use_animation=False, use_mesh_modifiers=True, use_edges=True, use_smooth_groups=False, use_smooth_groups_bitflags=False, use_normals=True, use_uvs=True, use_materials=True, use_triangles=True, use_nurbs=False, use_vertex_groups=False, use_blen_objects=True, group_by_object=False, group_by_material=False, keep_vertex_order=False, global_scale=2, path_mode='AUTO')