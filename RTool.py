# Copyright (c) 2022 Ultimaker B.V.
# Modification 2022 5@xes
# Uranium is released under the terms of the LGPLv3 or higher.

VERSION_QT5 = False
try:
    from PyQt6.QtCore import Qt, QTimer
    from PyQt6.QtWidgets import QApplication
except ImportError:
    from PyQt5.QtCore import Qt, QTimer
    from PyQt5.QtWidgets import QApplication
    VERSION_QT5 = True
    


from UM.Event import Event, MouseEvent, KeyEvent
from UM.Job import Job
from UM.Math.Plane import Plane
from UM.Math.Quaternion import Quaternion
from UM.Math.Vector import Vector
from UM.Message import Message
from UM.Logger import Logger
from UM.Operations.GravityOperation import GravityOperation
from UM.Operations.GroupedOperation import GroupedOperation
from UM.Operations.RotateOperation import RotateOperation
from UM.Operations.SetTransformOperation import SetTransformOperation
from UM.Scene.SceneNode import SceneNode
from UM.Scene.Selection import Selection

from UM.Tool import Tool
from UM.Version import Version
from UM.View.GL.OpenGL import OpenGL


import math
import time

from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("uranium")


class RTool(Tool):
    """Provides the tool to rotate meshes and groups
       On the XZ plane
    """

    def __init__(self):
        super().__init__()

        self._shortcut_key = Qt.Key.Key_Z
        # Logger.log('d', "OpenGL Version    :{}".format(OpenGL.getInstance().getOpenGLVersion()))
        self.setExposedProperties("SelectFaceSupported")

        self._select_face_mode = True
        # Selection.selectedFaceChanged.connect(self._ifSelectedFaceChanged)
        

    def event(self, event):
        """Handle mouse events

        :param event: type(Event)
        """

        super().event(event)

        if event.type == Event.MousePressEvent :
            
            #if not self._select_face_mode:
            #    return
            selected_face = Selection.getSelectedFace()
            
            #if not Selection.getSelectedFace() or not (Selection.hasSelection() and Selection.getFaceSelectMode()):
            if not Selection.getSelectedFace() or not (Selection.hasSelection()):
                return
            
            Logger.log('d', "selected_face    :{}".format(selected_face))
            
            # Just for personnal test and analyse of the code
            if self._selection_pass is None:
                # The selection renderpass is used to identify objects in the current view
                self._selection_pass = CuraApplication.getInstance().getRenderer().getRenderPass("selection")            
            face_id = self._selection_pass.getFaceIdAtPosition(event.x, event.y)
            Logger.log('d', "Event face_id    :{}".format(face_id))
            
            self._ifSelectedFaceChanged()

    def _ifSelectedFaceChanged(self):
        #Logger.log('d', "_onSelectedFaceChanged    :{}".format(self._select_face_mode))
        #if not self._select_face_mode:
        #    return

        selected_face = Selection.getSelectedFace()
        
        if not Selection.getSelectedFace() or not (Selection.hasSelection() and Selection.getFaceSelectMode()):
            return

        original_node, face_id = selected_face
        Logger.log('d', "selected_face    :{}".format(selected_face))
        Logger.log('d', "face_id          :{}".format(face_id))
        meshdata = original_node.getMeshDataTransformed()
        if not meshdata or face_id < 0:
            return
        if face_id > (meshdata.getVertexCount() / 3 if not meshdata.hasIndices() else meshdata.getFaceCount()):
            return

        face_mid, face_normal = meshdata.getFacePlane(face_id)
        object_mid = original_node.getBoundingBox().center
        rotation_point_vector = Vector(object_mid.x, object_mid.y, face_mid[2])
        face_normal_vector = Vector(face_normal[0], face_normal[1], face_normal[2])
        rotation_quaternion = Quaternion.rotationTo(face_normal_vector.normalized(), Vector(0.0, 0.0, 1.0))

        operation = GroupedOperation()
        current_node = None  # type: Optional[SceneNode]
        for node in Selection.getAllSelectedObjects():
            current_node = node
            parent_node = current_node.getParent()
            while parent_node and parent_node.callDecoration("isGroup"):
                current_node = parent_node
                parent_node = current_node.getParent()
        if current_node is None:
            return

        rotate_operation = RotateOperation(current_node, rotation_quaternion, rotation_point_vector)
        gravity_operation = GravityOperation(current_node)
        operation.addOperation(rotate_operation)
        operation.addOperation(gravity_operation)
        Selection.clearFace()
        operation.push()
        #Logger.log('d', "rotate_operation    :{}".format(rotate_operation))
        # NOTE: We might want to consider unchecking the select-face button after the operation is done.


    
    def getSelectFaceSupported(self) -> bool:
        """Get whether the select face feature is supported.

        :return: True if it is supported, or False otherwise.
        """
        # Use a dummy postfix, since an equal version with a postfix is considered smaller normally.
        return Version(OpenGL.getInstance().getOpenGLVersion()) >= Version("4.1 dummy-postfix")

    def getSelectFaceToLayFlatMode(self) -> bool:
        """Whether the rotate tool is in 'Lay flat by face'-Mode."""

        if not Selection.getFaceSelectMode():
            self._select_face_mode = False  # .. but not the other way around!
        return self._select_face_mode

    def setSelectFaceToLayFlatMode(self, select: bool) -> None:
        """Set the rotate tool to/from 'Lay flat by face'-Mode."""
        Selection.selectedFaceChanged.connect(self._ifSelectedFaceChanged)
        if select != self._select_face_mode or select != Selection.getFaceSelectMode():
            self._select_face_mode = select
            if not select:
                Selection.clearFace()
            Selection.setFaceSelectMode(self._select_face_mode)
            self.propertyChanged.emit()

    def resetRotation(self):
        """Reset the orientation of the mesh(es) to their original orientation(s)"""

        for node in self._getSelectedObjectsWithoutSelectedAncestors():
            node.setMirror(Vector(1, 1, 1))

        Selection.applyOperation(SetTransformOperation, None, Quaternion(), None)







