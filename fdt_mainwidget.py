# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FossilDigToolsWidget
                                 A QGIS plugin
 Interface and tools to help illustrate fossil digs
                             -------------------
        begin    : 2013-07-02
        copyright: (C) 2013 by Black Hills Institute of Geological Research
        email    : larrys@bhigr.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import sys
import math

from qgis.core import *
from qgis.gui import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ui_fdt_mainwidget import Ui_MainWidget
from fdt_settingsdlg import FdtSettingsDialog
from fdt_pindlg import FdtPinDialog

PYDEV_DIR = '/Users/larrys/QGIS/PluginProjects/fossildigtools/pydev'
if not PYDEV_DIR in sys.path:
    sys.path.insert(2, PYDEV_DIR)
import pydevd

class FdtMainWidget(QWidget):
    def __init__(self, parent, iface, settings):
        QWidget.__init__(self, parent)
        self.iface = iface
        self.msgbar = self.iface.messageBar()
        self.settings = settings
        self.qgsettings = QSettings()
        self.proj = QgsProject.instance()
        self.splayers = {}
        self.active = False
        self.datadelim = '|'
        self.curorigin = "{0}{1}{0}".format("-1", self.datadelim)
        self.layerconections = False
        self.init_bad_value_stylesheets()
        self.highlights = []

        # set up the user interface from Designer.
        self.ui = Ui_MainWidget()
        self.ui.setupUi(self)

        # setup toolbar
        self.tb = QToolBar(self)
        self.tb.setOrientation(Qt.Horizontal)
        self.tb.setMovable(False)
        self.tb.setFloatable(False)
        self.tb.setFocusPolicy(Qt.NoFocus)
        self.tb.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.tb.setLayoutDirection(Qt.LeftToRight)
        self.tb.setIconSize(QSize(20, 20))
        self.ui.toolBarFrameLayout.addWidget(self.tb)

        self.setup_toolbar()

        # set collapsible groupboxes settings property
        for gpbx in self.findChildren(QgsCollapsibleGroupBox):
            gpbx.setSettingGroup("digtools")
            gpbx.setSettings(settings)

        self.ui.addGridBtnGrp.setExclusive(False)
        self.set_grid_btns(True)  # default to origin

        # restore current tab
        curtab = self.settings.value("currentTab", 0, type=int)
        if not (curtab + 1) > self.ui.tabWidget.count():
            self.ui.tabWidget.setCurrentIndex(curtab)

        # reference to the canvas
        self.canvas = self.iface.mapCanvas()

        # point tool
        self.pointTool = QgsMapToolEmitPoint(self.canvas)

        self.init_spatialite_layers()
        self.check_plugin_ready()

        # track projects and layer changes
        self.iface.projectRead.connect(self.check_plugin_ready)
        self.iface.newProjectCreated.connect(self.invalid_project)

        QgsMapLayerRegistry.instance().layersAdded["QList<QgsMapLayer *>"].connect(self.layers_added)
        QgsMapLayerRegistry.instance().layersWillBeRemoved["QStringList"].connect(self.layers_to_be_removed)

    def pydev(self):
        pydevd.settrace('localhost', port=53100, stdoutToServer=True, stderrToServer=True)

    def setup_toolbar(self):
        self.pinPlotAct = QAction(
            QIcon(":/plugins/fossildigtools/icons/pinplot.svg"),
            '', self)
        self.pinPlotAct.setToolTip(self.tr('Plot point from pins'))
        self.tb.addAction(self.pinPlotAct)


        spacer = QWidget(self)
        spacer.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Preferred)
        self.tb.addWidget(spacer)

        self.settingsAct = QAction(
            QIcon(":/plugins/fossildigtools/icons/settings.svg"),
            '', self)
        self.settingsAct.setToolTip(self.tr('Settings'))
        self.settingsAct.triggered.connect(self.open_settings_dlg)
        self.tb.addAction(self.settingsAct)

    def is_spatialite_layer(self, layer):
        return (layer.type() == QgsMapLayer.VectorLayer and
                layer.storageType().lower().find("spatialite") > -1)

    def spatialite_layers_dict(self):
        lyrdict = {}
        lyrMap = QgsMapLayerRegistry.instance().mapLayers()
        for lyrid, layer in lyrMap.iteritems():
            if self.is_spatialite_layer(layer):
                lyrdict[lyrid] = layer
        return lyrdict

    def init_spatialite_layers(self):
        self.splayers = self.spatialite_layers_dict()

    def split_data(self, data):
        return data.split(self.datadelim)

    def join_data(self, a, b):
        return "{0}{1}{2}".format(a, self.datadelim, b)

    def get_layer(self, layerid):
        return QgsMapLayerRegistry.instance().mapLayer(layerid)

    def get_feature(self, layerid, featid):
        layer = self.get_layer(str(layerid))
        req = QgsFeatureRequest().setFilterFid(featid)
        feat = QgsFeature()
        layer.getFeatures(req).nextFeature(feat)
        return feat

    def get_features(self, layer, expstr):
        exp = QgsExpression(expstr)
        fields = layer.pendingFields()
        exp.prepare(fields)

        # # works
        # feats = []
        # for feat in layer.getFeatures():
        #     # err = exp.evalErrorString()
        #     if exp.evaluate(feat):
        #         feats.append(feat)
        #
        # # doesn't work!!
        # fit = layer.getFeatures()
        # feat = QgsFeature()
        # while fit.nextFeature(feat):
        #     if exp.evaluate(feat) == 1:
        #         feats.append(feat)
        # fit.close()
        # return feats

        return filter(exp.evaluate, layer.getFeatures())

    def delete_feature(self, layerid, featid):
        layer = self.get_layer(layerid)
        if not layer:
            return
        layer.startEditing()
        layer.deleteFeature(featid)
        layer.commitChanges()
        layer.setCacheImage(None)
        layer.triggerRepaint()

    def add_highlight(self, layerid, geom, color):
        layer = self.get_layer(layerid)
        hl = QgsHighlight(self.canvas, geom, layer)
        self.highlights.append(hl)
        hl.setWidth(0)
        hl.setColor(color)
        hl.show()

    @pyqtSlot()
    def delete_highlights(self):
        for hl in self.highlights:
            del hl
        self.highlights = []

    def pin_layer_id(self):
        return self.proj.readEntry("fdt", "pinsLayerId", "")[0]

    def grids_layer_id(self):
        return self.proj.readEntry("fdt", "gridsLayerId", "")[0]

    def features_layer_id(self):
        return self.proj.readEntry("fdt", "featuresLayerId", "")[0]

    def valid_layer_attributes(self, lyr, attrs):
        flds = lyr.pendingFields()
        for attr in attrs:
            if flds.indexFromName(attr) == -1:
                return False
        return True

    def valid_pin_layer(self, lid=None):
        if id == "invalid":
            return False
        lyrId = lid if lid else self.pin_layer_id()
        if lyrId == "" or lyrId not in self.splayers:
            return False
        lyr = self.get_layer(lyrId)
        if lyr.geometryType() != QGis.Point:
            return False
        attrs = ['pkuid', 'kind', 'name', 'date', 'setter', 'description', 'origin']
        return self.valid_layer_attributes(lyr, attrs)

    def valid_grid_layer(self, lid=None):
        return True

#        lyrId = self.grids_layer_id()

    def valid_feature_layer(self, lid=None):
        return True

#        lyrId = self.features_layer_id()

    @pyqtSlot("QList<QgsMapLayer *>")
    def layers_added(self, layers):
        check = False
        for layer in layers:
            if self.is_spatialite_layer(layer):
                self.splayers[layer.id()] = layer
                check = True
        if check:
            self.check_plugin_ready()

    @pyqtSlot("QStringList")
    def layers_to_be_removed(self, lids):
        check = False
        for lid in lids:
            if self.splayers.has_key(lid):
                del self.splayers[lid]
                check = True
        if check:
            self.check_plugin_ready()

    def check_linked_layers(self):
        return (self.valid_pin_layer() and
                self.valid_grid_layer() and
                self.valid_feature_layer())

    def zoom_canvas(self, rect):
        self.canvas.setExtent(rect)
        self.canvas.refresh()

    def to_meters(self, size, unit):
        if unit == 'cm':
            return size * 0.01
        elif unit == 'in':
            return size * 0.0254
        elif unit == 'feet':
            return size * 0.3048

    def grid_unit_index(self):
        return self.proj.readNumEntry("fdt", "gridSquaresUnit", 0)[0]

    def grid_unit(self):
        return 'cm' if self.grid_unit_index() == 0 else 'in'

    def major_grid(self):
        return self.proj.readNumEntry("fdt", "gridSquaresMajor", 0)[0]

    def major_grid_m(self):
        return self.to_meters(self.major_grid(), self.grid_unit())

    def minor_grid(self):
        return self.proj.readNumEntry("fdt", "gridSquaresMinor", 0)[0]

    def minor_grid_m(self):
        return self.to_meters(self.minor_grid(), self.grid_unit())

    def major_grid_buf(self):
        return self.major_grid_m() + (2 * self.minor_grid_m())

    def rect_buf_point(self, pt, rect):
        return QgsRectangle(pt.x() - rect / 2, pt.y() - rect / 2,
                            pt.x() + rect / 2, pt.y() + rect / 2,)

    def valid_squares(self, major, minor):
        return (major != 0 and minor != 0 and
                major >= minor and major % minor == 0)

    def check_grid_squares(self):
        return self.valid_squares(self.major_grid(), self.minor_grid())

    @pyqtSlot()
    def check_plugin_ready(self):
        # log splayers
        spLyrs = "Spatialite layers\n"
        for lyrid, lyr in self.splayers.iteritems():
            spLyrs += "  Name: {0}\n  Id: {1}\n\n".format(lyr.name(), lyrid)
        QgsMessageLog.logMessage(spLyrs, self.tr("Fdt"), QgsMessageLog.INFO)

        checks = (self.check_grid_squares() and
                  self.check_linked_layers())
        if checks:
            self.enable_plugin(True)
            self.init_plugin()
            self.clear_notice()
        else:
            self.invalid_project()

    @pyqtSlot()
    def invalid_project(self):
        self.active = False  # must come first
        self.remove_layer_connections()
        self.clear_plugin()
        self.enable_plugin(False)

    def init_plugin(self):
        if self.active:
            return
        self.active = True  # must come first
        self.load_pins()
        self.make_layer_connections()

    def clear_plugin(self):
        if not self.active:
            self.notice(self.tr("Project unsupported. Define settings."))
        # location pins
        self.ui.originPinCmbBx.blockSignals(True)
        self.ui.originPinCmbBx.clear()
        self.ui.originPinCmbBx.blockSignals(False)
        self.ui.originEditFrame.setEnabled(False)
        self.ui.directPinList.clear()
        self.ui.directPinFrame.setEnabled(False)
        self.ui.directPinEditFrame.setEnabled(False)
        # grids
        self.ui.gridsCmbBx.blockSignals(True)
        self.ui.gridsCmbBx.clear()
        self.ui.gridsCmbBx.blockSignals(False)
        self.ui.gridsRemoveBtn.setEnabled(False)
        self.ui.gridFrame.setEnabled(False)

    def enable_plugin(self, enable):
        self.ui.tabWidget.setEnabled(enable)
        for act in self.tb.actions():
            if act != self.settingsAct:
                act.setEnabled(enable)

    def make_layer_connections(self):
        if self.layerconections:
            return

        layerids = [self.pin_layer_id(), self.grids_layer_id()]
        methods = [self.load_pins, self.load_origin_grids()]

        for i in range(len(layerids)):
            layer = self.get_layer(layerids[i])
            if layer:
                layer.editingStopped.connect(methods[i])
                layer.updatedFields.connect(self.check_plugin_ready)

    def remove_layer_connections(self):
        if not self.layerconections:
            return

        layerids = [self.pin_layer_id(), self.grids_layer_id()]
        methods = [self.load_pins, self.load_origin_grids()]

        for i in range(len(layerids)):
            layer = self.get_layer(layerids[i])
            if layer:
                layer.editingStopped.disconnect(methods[i])
                layer.updatedFields.disconnect(self.check_plugin_ready)

    @pyqtSlot()
    def load_pins(self):
        if not self.active:
            return

        self.clear_plugin()

        # load origins
        self.load_origin_pins()
        self.update_current_origin()
        self.load_origin_children()

    def update_current_origin(self):
        if self.ui.originPinCmbBx.count() > 0:
            self.curorigin = self.ui.originPinCmbBx.itemData(
                    self.ui.originPinCmbBx.currentIndex())
        else:
            self.curorigin = "{0}{1}{0}".format("-1", self.datadelim)

        self.settings.setValue("currentOrigin", self.current_origin())

    def current_origin(self):
        return self.split_data(self.curorigin)[1]

    def current_origin_fid(self):
        return int(self.split_data(self.curorigin)[0])

    def current_origin_feat(self):
        #self.pydev()
        return self.get_feature(self.pin_layer_id(), self.current_origin_fid())

    def origin_pins(self):
        expstr = " \"kind\"='origin' "
        layer = self.get_layer(self.pin_layer_id())
        return self.get_features(layer, expstr)

    def load_origin_pins(self):
        self.ui.originPinCmbBx.clear()
        pins = self.origin_pins()
        haspins = pins and len(pins) > 0
        # self.pydev()
        if haspins:
            self.ui.originEditFrame.setEnabled(True)
            self.ui.originPinCmbBx.blockSignals(True)

            curorig = self.settings.value("currentOrigin", "-1", type=str)
            curindx = -1
            for i in range(len(pins)):
                pin = pins[i]
                pkuid = pin['pkuid']
                self.ui.originPinCmbBx.addItem(
                    pin['name'], self.join_data(pin.id(), pkuid))
                if curorig != "-1" and curorig == str(pkuid):
                    curindx = i
            if curindx > -1:
                self.ui.originPinCmbBx.setCurrentIndex(curindx)

            self.ui.originPinCmbBx.blockSignals(False)

        self.ui.directPinFrame.setEnabled(haspins)

    def load_origin_children(self):
        # load directional pins associated with the current origin
        self.load_directional_pins()
        # load grids associated with the current origin
        self.load_origin_grids()

    def current_directional_item(self):
        return self.ui.directPinList.currentItem()

    def current_directional(self):
        return self.split_data(
            self.current_directional_item().data(Qt.UserRole))[1]

    def current_directional_fid(self):
        return int(self.split_data(
            self.current_directional_item().data(Qt.UserRole))[0])

    def current_directional_feat(self):
        #self.pydev()
        return self.get_feature(self.pin_layer_id(),
                                self.current_directional_fid())

    def directional_pins(self, origin=-1):
        if origin == -1:
            origin = self.current_origin()
        if origin == -1:
            return
        expstr = " \"kind\"='directional' AND \"origin\"={0} ".format(origin)
        layer = self.get_layer(self.pin_layer_id())
        return self.get_features(layer, expstr)

    def load_directional_pins(self):
        self.ui.directPinList.clear()
        pins = self.directional_pins(self.current_origin())
        haspins = pins and len(pins) > 0
        if haspins:
            self.ui.directPinList.blockSignals(True)
            for pin in pins:
                lw = QListWidgetItem(pin['name'])
                lw.setData(Qt.UserRole, self.join_data(pin.id(), pin['pkuid']))
                self.ui.directPinList.addItem(lw)
            self.ui.directPinList.blockSignals(False)

    def origin_grids(self, origin=-1):
        pass

    def load_origin_grids(self):
        pass

    def init_bad_value_stylesheets(self):
        self.badLineEditValue = \
            "QLineEdit {background-color: rgb(255, 210, 208);}"
        self.badSpinBoxValue = \
            "QSpinBox {background-color: rgb(255, 210, 208);}"
        self.badDblSpinBoxValue = \
            "QDoubleSpinBox {background-color: rgb(255, 210, 208);}"
        self.badValueLabel = "QLabel {color: rgb(225, 0, 0);}"

    def active_feature_layer(self):
        avl = self.iface.activeLayer()
        if not avl:
            self.msg_bar(self.tr("No active layer"),
                         QgsMessageBar.INFO)
            return False
        if avl.id() != self.features_layer_id():
            self.msg_bar(self.tr("Features layer not active"),
                         QgsMessageBar.INFO)
            return False
        return True

    def selected_features(self):
        ids = []
        if not self.active_feature_layer():
            return ids
        fids = self.iface.activeLayer().selectedFeatures()
        if not fids:
            self.msg_bar(self.tr("Nothing selected"), QgsMessageBar.INFO)
        return fids

    def msg_bar(self, msg, kind):
        self.msgbar.pushMessage(self.tr( "Fossil Dig Tools" ),
                                msg,
                                kind,
                                self.iface.messageTimeout())

    def notice(self, notice):
        self.ui.noticeLabel.show()
        self.ui.noticeLabel.setText(notice)

    def clear_notice(self):
        self.ui.noticeLabel.setText("")
        self.ui.noticeLabel.hide()

    def reset_add_grid_btns(self):
        for btn in self.ui.addGridBtnGrp.buttons():
            btn.setEnabled(True)
            if btn.isCheckable():
                btn.setChecked(False)

    def set_grid_btns(self, origin=False):
        if origin:
            self.ui.addGridNBtn.setEnabled(False)
            self.ui.addGridSBtn.setEnabled(False)
            self.ui.addGridWBtn.setEnabled(False)
            self.ui.addGridEBtn.setEnabled(False)

    def open_settings_dlg(self):
        settingsDlg = FdtSettingsDialog(self, self.iface, self.settings)
        settingsDlg.exec_()
        self.check_plugin_ready()

    @pyqtSlot(int)
    def on_originPinCmbBx_currentIndexChanged(self, int):
        self.update_current_origin()
        self.load_origin_children()

    @pyqtSlot()
    def on_originPinAddBtn_clicked(self):
        pinDlg = FdtPinDialog(self, self.iface, 'origin')
        # pinDlg.accepted.connect(self.load_pins)
        pinDlg.show()

    @pyqtSlot()
    def on_originPinEditBtn_clicked(self):
        feat = self.current_origin_feat()
        if feat.isValid():
            pinDlg = FdtPinDialog(self, self.iface, 'origin', -1, feat)
            # pinDlg.accepted.connect(self.load_pins)
            pinDlg.show()

    @pyqtSlot()
    def on_originPinRemoveBtn_clicked(self):
        res = QMessageBox.warning(
            self.parent(),
            self.tr("Caution!"),
            self.tr("Really delete current origin pin?\n\n"
                    "Doing so will orphan any associated grids, "
                    "which will have to be manually deleted."),
            QMessageBox.Ok | QMessageBox.Cancel,
            QMessageBox.Cancel)
        if res != QMessageBox.Ok:
            return
        self.delete_feature(self.pin_layer_id(), self.current_origin_fid())

    @pyqtSlot()
    def on_originPinGoToBtn_clicked(self):
        feat = self.current_origin_feat()
        pt = feat.geometry().asPoint()
        rect = self.rect_buf_point(pt, self.major_grid_buf())
        self.zoom_canvas(rect)

        hlrect = self.rect_buf_point(pt, self.minor_grid_m())
        self.flash_highlight(self.pin_layer_id(), hlrect)

    @pyqtSlot("QListWidgetItem *", "QListWidgetItem *")
    def on_directPinList_currentItemChanged(self, cur, prev):
        self.ui.directPinEditFrame.setEnabled(cur is not None)

    @pyqtSlot()
    def on_directPinAddBtn_clicked(self):
        pinDlg = FdtPinDialog(self, self.iface, 'directional',
                              self.current_origin())
        # pinDlg.accepted.connect(self.load_pins)
        pinDlg.show()

    @pyqtSlot()
    def on_directPinEditBtn_clicked(self):
        feat = self.current_directional_feat()
        if feat.isValid():
            pinDlg = FdtPinDialog(self, self.iface, 'directional',
                                  self.current_origin(), feat)
            # pinDlg.accepted.connect(self.load_pins)
            pinDlg.show()

    @pyqtSlot()
    def on_directPinRemoveBtn_clicked(self):
        res = QMessageBox.warning(
            self.parent(),
            self.tr("Caution!"),
            self.tr("Really delete current directional pin ?"),
            QMessageBox.Ok | QMessageBox.Cancel,
            QMessageBox.Cancel)
        if res != QMessageBox.Ok:
            return
        self.delete_feature(self.pin_layer_id(), self.current_directional_fid())

    @pyqtSlot()
    def on_directPinGoToBtn_clicked(self):
        layer = self.get_layer(self.pin_layer_id())
        layer.setSelectedFeatures([self.current_origin_fid(),
                                   self.current_directional_fid()])
        self.canvas.zoomToSelected(layer)
        layer.setSelectedFeatures([])

        feat1 = self.current_origin_feat()
        pt1 = feat1.geometry().asPoint()
        rect1 = self.rect_buf_point(pt1, self.minor_grid_m())
        geom1 = QgsGeometry.fromRect(rect1)
        self.add_highlight(self.pin_layer_id(), geom1, QColor(225, 0, 0))

          # for ( int i = 0; i <= RADIUS_SEGMENTS; ++i )
          # {
          #   double theta = i * ( 2.0 * M_PI / RADIUS_SEGMENTS );
          #   QgsPoint radiusPoint( mRadiusCenter.x() + r * cos( theta ),
          #                         mRadiusCenter.y() + r * sin( theta ) );
          #   mRubberBand->addPoint( radiusPoint );
          # }

        feat2 = self.current_directional_feat()
        pt2 = feat2.geometry().asPoint()
        geom2 = QgsGeometry().asPolygon()
        pts2 = []
        r2 = self.minor_grid_m() / 4
        for i in range(32):
            theta = i * (2.0 * math.pi / 32 )
            pt = QgsPoint(pt2.x() + r2 * math.cos(theta),
                          pt2.y() + r2 * math.sin(theta))
            pts2.append(pt)
        geom2 = QgsGeometry.fromPolygon([pts2])

        # rb2 = QgsRubberBand(self.canvas, QGis.Polygon)
        # # pts2 = []
        # r2 = self.minor_grid_m() / 4
        # for i in range(32):
        #     theta = i * (2.0 * math.pi / 32 )
        #     pt = QgsPoint(pt2.x() + r2 * math.cos(theta),
        #                   pt2.y() + r2 * math.sin(theta))
        #     rb2.addPoint(pt)
        # geom2 = rb2.asGeometry()
        # rb2.reset(QGis.Polygon)
        # del rb2

        self.add_highlight(self.pin_layer_id(), geom2, QColor(0, 0, 225))

        # feat2 = self.current_directional_feat()
        # pt2 = feat2.geometry().asPoint()
        # hlrect2 = self.rect_buf_point(pt2, self.minor_grid_m())
        # self.add_highlight(self.pin_layer_id(), hlrect2, QColor(0, 0, 225))

        QTimer.singleShot(2000, self.delete_highlights)

    @pyqtSlot()
    def on_attributesOpenFormBtn_clicked(self):
        for f in self.selected_features():
            self.iface.openFeatureForm(self.iface.activeLayer(), f)

    @pyqtSlot(QAbstractButton)
    def on_addGridRadioGrp_buttonClicked(self, btn):
        self.reset_add_grid_btns()
        origin = False
        if btn is self.ui.addGridGridRadio:
            self.ui.addGridIconLabel.setPixmap(
                QPixmap(":/plugins/fossildigtools/icons/grid.svg"))
        elif btn is self.ui.addGridOriginRadio:
            self.ui.addGridIconLabel.setPixmap(
                QPixmap(":/plugins/fossildigtools/icons/origin.svg"))
            origin = True
        self.set_grid_btns(origin)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    toolwidget = FdtMainWidget()
    toolwidget.show()
    toolwidget.raise_()
    toolwidget.activateWindow()
    sys.exit(app.exec_())
