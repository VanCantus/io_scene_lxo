# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Import Modo Objects",
    "author": "Bernd Moeller",
    "version": (0, 0, 1),
    "blender": (2, 90, 1),
    "location": "File > Import > Modo Object (.lxo)",
    "description": "Imports a LXO file (including any UV, Morph and Color maps.)"
    "Does nothing yet",
    "warning": "",
    "wiki_url": ""
    "",
    "category": "Import-Export",
}

# Copyright (c) Bernd Moeller 2020
#
# 1.0 First Release

# When bpy is already in local, we know this is not the initial import...
if "bpy" in locals():
    import importlib
    # ...so we need to reload our submodule(s) using importlib
    if "build_scene" in locals():
        importlib.reload(build_scene)

import os
import bpy

from . import build_scene
from bpy.props import (
    StringProperty,
    BoolProperty
    )
from bpy_extras.io_utils import (
    orientation_helper
    )

class _choices:
    """__slots__ = (
        "add_subd_mod",
        "load_hidden",
        #"skel_to_arm",
        #"use_existing_materials",
        #"search_paths",
        #"cancel_search",
        #"images",
        "recursive",
    )"""

    def __init__(
        self,
        ADD_SUBD_MOD=True,
        LOAD_HIDDEN=False,
        SKEL_TO_ARM=True,
        USE_EXISTING_MATERIALS=False,
        clean_import = False
    ):
        self.add_subd_mod = ADD_SUBD_MOD
        self.load_hidden = LOAD_HIDDEN
        self.clean_import = clean_import
        #self.skel_to_arm = SKEL_TO_ARM
        #self.use_existing_materials = USE_EXISTING_MATERIALS
        #self.search_paths = []
        #self.cancel_search = False
        #self.images = {}
        self.recursive = True

@orientation_helper(axis_forward='-Z', axis_up='Y')
class IMPORT_OT_lxo(bpy.types.Operator):
    """Import LXO Operator"""

    bl_idname = "import_scene.lxo"
    bl_label = "Import LXO"
    bl_description = "Import a Modo Object file"
    bl_options = {"REGISTER", "UNDO"}

    bpy.types.Scene.ch = None
    #bpy.types.Scene.lxo = None

    filepath: StringProperty(
        name="File Path",
        description="Filepath used for importing the LXO file",
        maxlen=1024,
        default="",
    )

    ADD_SUBD_MOD: BoolProperty(
        name="Apply SubD Modifier",
        description="Apply the Subdivision Surface modifier to layers with Subpatches",
        default=True,
    )
    LOAD_HIDDEN: BoolProperty(
        name="Load Hidden Layers",
        description="Load object layers that have been marked as hidden",
        default=False,
    )
    CLEAN_IMPORT: BoolProperty(
        name="Clean Import",
        description="Import to empty scene",
        default=False,
    )
    # SKEL_TO_ARM: BoolProperty(
    #     name="Create Armature",
    #     description="Create an armature from an embedded Skelegon rig",
    #     default=True,
    # )
    # USE_EXISTING_MATERIALS: BoolProperty(
    #     name="Use Existing Materials",
    #     description="Use existing materials if a material by that name already exists",
    #     default=False,
    # )

    def invoke(self, context, event):  # gui: no cover
        wm = context.window_manager
        wm.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        #keywords = self.as_keywords(ignore=("filepath"))
        #return build_scene.load(self, context, filepath=self.filepath, **keywords)
        return build_scene.load(self, context, filepath=self.filepath,
                                axis_forward=self.axis_forward,
                                axis_up=self.axis_up,
                                ADD_SUBD_MOD=self.ADD_SUBD_MOD,
                                LOAD_HIDDEN=self.LOAD_HIDDEN,
                                CLEAN_IMPORT=self.CLEAN_IMPORT)


def menu_func(self, context):  # gui: no cover
    self.layout.operator(IMPORT_OT_lxo.bl_idname, text="Modo Object (.lxo)")


# Panel
class IMPORT_PT_Debug(bpy.types.Panel):
    bl_idname = "IMPORT_PT_Debug"

    # region = "UI"
    region = "WINDOW"
    # region = "TOOLS"
    space = "PROPERTIES"

    bl_label = "DEBUG"
    bl_space_type = space
    bl_region_type = region
    bl_category = "Tools"

    def draw(self, context):  # gui: no cover
        layout = self.layout

        col = layout.column(align=True)
        col.operator("import_scene.lxo", text="Import LXO")
        col.operator("open.browser", text="File Browser")


classes = (
    IMPORT_OT_lxo,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_file_import.append(menu_func)

    ch = _choices()
    bpy.types.Scene.ch = ch


def unregister():  # pragma: no cover
    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.TOPBAR_MT_file_import.remove(menu_func)

    del bpy.types.Scene.ch


if __name__ == "__main__":  # pragma: no cover
    register()
