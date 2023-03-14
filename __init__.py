# Copyright (c) 2015 Ultimaker B.V.
# 2023 5axes
# Uranium is released under the terms of the LGPLv3 or higher.

VERSION_QT5 = False
try:
    from PyQt6.QtCore import QT_VERSION_STR
except ImportError:
    VERSION_QT5 = True
    
    
from . import RTool

from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("rtool")

def getMetaData():
    if not VERSION_QT5:
        QmlFile="qml/qml_qt6/RTool.qml"
    else:
        QmlFile="qml/qml_qt5/RTool.qml"
        
    return {
        "tool": {
            "name": i18n_catalog.i18nc("@label", "Rotate XZ plane"),
            "description": i18n_catalog.i18nc("@info:tooltip", "Rotate Model To XZ plane"),
            "icon": "tool_icon.svg",
            "tool_panel": QmlFile,
            "weight": 1
        }
    }

def register(app):
    return { "tool": RTool.RTool() }
