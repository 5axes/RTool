// Copyright (c) 2021 Ultimaker B.V.
// Uranium is released under the terms of the LGPLv3 or higher.

import QtQuick 2.2
import UM 1.6 as UM

Item
{
    width: childrenRect.width
    height: childrenRect.height
    UM.I18nCatalog { id: catalog; name: "rtool"}

    UM.ToolbarButton
    {
        id: resetRotationButton

        anchors.left: parent.left;

        text: catalog.i18nc("@action:button", "Reset")
        toolItem: UM.ColorImage
        {
            source: UM.Theme.getIcon("ArrowReset")
            color: UM.Theme.getColor("icon")
        }
        property bool needBorder: true

        z: 1

        onClicked: UM.ActiveTool.triggerAction("resetRotation")
    }

    UM.ToolbarButton{
        id: alignFaceButton

		anchors.left: resetRotationButton.right
        anchors.leftMargin: UM.Theme.getSize("default_margin").width
        width: visible ? UM.Theme.getIcon("LayFlatOnFace").width : 0

        text: catalog.i18nc("@action:button", "Select face to align to the XZ Plane")

        toolItem: UM.ColorImage
        {
            source: UM.Theme.getIcon("LayFlatOnFace")
            color: UM.Theme.getColor("icon")
        }
		property bool needBorder: true

        checkable: true

        enabled: UM.Selection.selectionCount == 1
        checked: UM.ActiveTool.properties.getValue("SelectFaceToLayAxisMode")
        onClicked: UM.ActiveTool.setProperty("SelectFaceToLayAxisMode", checked)

        visible: UM.ActiveTool.properties.getValue("SelectFaceSupported") == true //Might be undefined if we're switching away from the RotateTool!
    }

    Binding
    {
        target: alignFaceButton
        property: "checked"
        value: UM.ActiveTool.properties.getValue("SelectFaceToLayAxisMode")
    }
}
