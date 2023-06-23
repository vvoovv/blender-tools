bl_info = {
	"name": "Target Mesh Reizer & Scaling",
	"author": "Vladimir Elistratov <vladimir.elistratov@gmail.com>",
    "modified_by": "Regis Nde Tene",
	"version": (1, 0, 3),
	"blender": (3, 5, 1),
	"location": "View 3D > Edit Mode > Tool Shelf",
	"description": "Scale your model to the correct target size",
	"warning": "",
	"wiki_url": "https://github.com/vvoovv/blender-geo/wiki/Target-Scaling",
	"tracker_url": "https://github.com/vvoovv/blender-geo/issues",
	"support": "COMMUNITY",
	"category": "3D View",
}


import bpy, bmesh, mathutils

class TargetScalingPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "mesh_edit"
    bl_label = "Target Scaling"

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.operator("edit.select_target_edge")
        col.separator()
        col.operator("edit.do_target_scaling")
        col.operator("edit.apply_target_scaling")
        col.operator("edit.copy_and_scale")

def getSelectedEdgeLength(context):
    obj = context.active_object
    bm = bmesh.from_edit_mesh(obj.data)
    edge = bm.select_history.active
    l = -1
    if isinstance(edge, bmesh.types.BMEdge):
        v1 = obj.matrix_world @ edge.verts[0].co
        v2 = obj.matrix_world @ edge.verts[1].co
        l = (v1 - v2).length
        l = round(l, 5)
    return l

class SelectTargetEdge(bpy.types.Operator):
    bl_idname = "edit.select_target_edge"
    bl_label = "Select a target edge"
    bl_description = "Select a target edge"

    def execute(self, context):
        l = getSelectedEdgeLength(context)
        if l > 0:
            _.target_length = l
            self.report({"INFO"}, "The target edge length is {}".format(l))
        else:
            self.report({"ERROR"}, "Select a single target edge!")
        return {"FINISHED"}

class DoTargetScaling(bpy.types.Operator):
    bl_idname = "edit.do_target_scaling"    
    bl_label = "Perform mesh scaling"
    bl_description = "Perform whole mesh scaling, so the selected edge will be equal to the target one."
    bl_options = {"UNDO"}

    def execute(self, context):
        l = getSelectedEdgeLength(context)
        if l > 0:
            scale = _.target_length/l
            bpy.ops.transform.resize(value=(scale, scale, scale))
            bpy.ops.mesh.select_all(action="DESELECT")
        else:
            self.report({"ERROR"}, "Select a single edge for target scaling!")
        return {"FINISHED"}

class ApplyTargetScaling(bpy.types.Operator):
    bl_idname = "edit.apply_target_scaling"    
    bl_label = "Apply target scaling"
    bl_description = "Apply target scaling to selected edges."
    bl_options = {"UNDO"}

    def execute(self, context):
        scale = _.target_length/getSelectedEdgeLength(context)
        bpy.ops.transform.resize(value=(scale, scale, scale))
        bpy.ops.mesh.select_all(action="DESELECT")
        return {"FINISHED"}

class CopyAndScale(bpy.types.Operator):
    bl_idname = "edit.copy_and_scale"
    bl_label = "Copy and scale"
    bl_description = "Create a copy of the object and perform target scaling on it."
    bl_options = {"UNDO"}

    def execute(self, context):
        # Ensure we are in object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # duplicate the active object
        bpy.ops.object.duplicate()
        new_obj = context.active_object

        # switch to edit mode on the new object
        bpy.ops.object.mode_set(mode='EDIT')

        scale = _.target_length/getSelectedEdgeLength(context)
        
        # do scaling on the new object
        bpy.ops.transform.resize(value=(scale, scale, scale))
        
        # deselect everything
        bpy.ops.mesh.select_all(action="DESELECT")

        # switch back to object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # set origin to the center of object's bounding box
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')

        return {"FINISHED"}

class _:
    target_length = -1

def register():
    classes = (TargetScalingPanel, SelectTargetEdge, DoTargetScaling, ApplyTargetScaling, CopyAndScale)
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    classes = (TargetScalingPanel, SelectTargetEdge, DoTargetScaling, ApplyTargetScaling, CopyAndScale)
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
