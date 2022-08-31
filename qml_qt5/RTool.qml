// Copyright (c) 2022 5@xes.

import QtQuick 2.2
import QtQuick.Controls 1.2

import UM 1.1 as UM

Item
{
    width: childrenRect.width
    height: childrenRect.height
    UM.I18nCatalog { id: catalog; name: "uranium"}

    Button
    {
        id: resetRotationButton

        anchors.left: parent.left;

        text: catalog.i18nc("@action:button", "Reset")
        iconSource: UM.Theme.getIcon("ArrowReset")
        property bool needBorder: true
		
		style: UM.Theme.styles.tool_button;
        z: 1

        onClicked: UM.ActiveTool.triggerAction("resetRotation");
    }

    Button
	{
        id: alignFaceButton

		anchors.left: resetRotationButton.right;
        anchors.leftMargin: UM.Theme.getSize("default_margin").width;
        width: visible ? UM.Theme.getIcon("LayFlatOnFace").width : 0;

        text: catalog.i18nc("@action:button", "Select face to align to the XZ Plane")

        iconSource:  UM.Theme.getIcon("LayFlatOnFace")
		property bool needBorder: true
		
        style: UM.Theme.styles.tool_button;


        enabled: UM.Selection.selectionCount == 1
        checked: UM.ActiveTool.properties.getValue("SelectFaceToLayFlatMode")
        onClicked: UM.ActiveTool.setProperty("SelectFaceToLayFlatMode", !checked)

        visible: UM.ActiveTool.properties.getValue("SelectFaceSupported") == true //Might be undefined if we're switching away from the RotateTool!
    }

    Binding
    {
        target: alignFaceButton
        property: "checked"
        value: UM.ActiveTool.properties.getValue("SelectFaceToLayFlatMode")
    }
}
