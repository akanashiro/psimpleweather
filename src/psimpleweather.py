#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'psimpleweather.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!
import os
import urllib
import sys
import requests
import json
import sqlite3
import xml.etree.ElementTree as etree

from datetime import datetime
from PyQt5 import Qt, QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
# from PyQt5.QtCore import QDir, QUrl, QFileInfo
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QLineEdit, QComboBox,
                             QApplication, QGridLayout, QMessageBox, QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QPixmap


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(600, 500)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(10, 30, 560, 450))
        self.tabWidget.setTabBarAutoHide(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

        self.gridLayoutWidget = QtWidgets.QWidget(self.tabWidget)

        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        self.lineEdit.setGeometry(QtCore.QRect(10, 10, 191, 32))
        self.lineEdit.setObjectName("lineEdit")

        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(210, 10, 88, 34))
        self.pushButton.setObjectName("pushButton")

        self.radioBtnToday = QtWidgets.QRadioButton(self.tab)
        self.radioBtnToday.setGeometry(QtCore.QRect(10, 50, 104, 22))
        self.radioBtnToday.setObjectName("radioBtnToday")
        self.radioBtnToday.setChecked(True)

        self.radioBtnNext = QtWidgets.QRadioButton(self.tab)
        self.radioBtnNext.setGeometry(QtCore.QRect(170, 50, 104, 22))
        self.radioBtnNext.setObjectName("radioBtnNext")

        self.textBrowser = QtWidgets.QTextBrowser(self.tab)
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setGeometry(QtCore.QRect(10, 110, 520, 300))

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

# ================       LAYOUT       ================

        # Layout arriba izquierda
        hboxTopLeft = QHBoxLayout()
        hboxTopLeft.setObjectName("hboxTopLeft")
        hboxTopLeft.addWidget(self.textBrowser)

        # Layout arriba derecha
        #vboxTopRight = QVBoxLayout()
        # vboxTopRight.setAlignment(Qt.AlignTop)
        #vboxTopRight.setContentsMargins(0, -1, -1, 10)
        #self.pic = QLabel()
        #pixmap = QPixmap(os.path.join(dirname, "../icons/none.png"))

        # self.pic.setPixmap(pixmap)
        # vboxTopRight.addWidget(self.pic)

        # Layout que contiene los dos layouts Top
        #vboxFirst = QHBoxLayout()
        # vboxFirst.addLayout(hboxTopLeft)
        # vboxFirst.addLayout(vboxTopRight)

        #self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 110, 520, 320))
        #self.gridLayout1 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        #self.gridLayout1.setContentsMargins(0, 0, 0, 0)
        #self.gridLayout1.addLayout(vboxFirst, 0, 0)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Pretty Simple AppWeather"))
        self.pushButton.setText(_translate("Form", "Search"))
        self.radioBtnToday.setText(_translate("Form", "&Today"))
        self.radioBtnNext.setText(_translate("Form", "Ne&xt days"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab),
                                  _translate("Form", "Location 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tab_2), _translate("Form", "Location 2"))


class SimpleWeather(QtWidgets.QMainWindow):
    def __init__(self):
        super(SimpleWeather, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # self.ui.pushButton.clicked.connect(self.parseXML)
        self.ui.pushButton.clicked.connect(self.findCity)
        # self.ui.lineEdit.textChanged.connect(self.findCity)

    def geoLocation(self, strLat, strLon):
        send_url = 'http://freegeoip.net/json'
        strRequest = requests.get(send_url)
        strJson = json.loads(strRequest.text)
        strLat = strJson['latitude']
        strLon = strJson['longitude']

    def findCity(self):

        if not self.ui.lineEdit.text():
            msgError = QMessageBox()
            msgError.setIcon(QMessageBox.Critical)
            msgError.setWindowTitle("Error")
            msgError.setText("You must enter a location")
            msgError.setStandardButtons(QMessageBox.Ok)
            msgError.show()
            raise Exception
        else:
            # db = sqlite3.connect(':memory:')
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(BASE_DIR, "cities.db")

            db = sqlite3.connect(db_path)
            cursor = db.cursor()

            textCity = self.ui.lineEdit.text()
            splitCity = textCity.split(",")
            strCity = splitCity[0].strip()
            strCountry = splitCity[1].strip()
            print(strCity.upper())
            print(strCountry.upper())
            cursor.execute("select xml from cities where upper(city) like ? and upper(country_descr) like ?",
                           (strCity.upper(), strCountry.upper()))

            data = cursor.fetchone()
            strXml = data[0]
            db.close()
            print(strXml)
            self.parseXML(strXml)

    def parseXML(self, inXml):

        #xmlWeather = "http://www.yr.no/place/Chile/Santiago/Santiago_de_Chile/forecast.xml"
        xmlWeather = inXml
        resXml = requests.get(xmlWeather)
        # res = etree.parse('/home/akanashiro/Proyectos/psimpleweather/forecast_sample.xml')
        # print(res.text)
        root = etree.fromstring(resXml.text)
        # root = res.getroot()

        # root = etree.fromstring(res.text)
        # print(root.tag)
        # print(root.attrib)

        html = "<table cellspacing='2'><tbody>"
        html += "<tr><th width='25'></th><th align='center'>Forecast</th><th align='center'>Temp</th>"
        html += "<th align='center'>Precipitation</th><th align='center'>Wind</th><th align='center'>Pressure</th></tr>"
        html += "<tr>"
        self.ui.textBrowser.setText("")

        for child in root:
            if child.tag == 'forecast':
                for tagTabular in child:
                    for tagTime in tagTabular:
                        # Hora
                        strDttmFrom = tagTime.get('from')
                        dtmFrom = datetime.strptime(strDttmFrom, "%Y-%m-%dT%H:%M:%S")
                        dtFrom = dtmFrom.date()
                        dtFromTime = dtmFrom.time()

                        strDttmTo = tagTime.get('to')
                        dtmTo = datetime.strptime(strDttmTo, "%Y-%m-%dT%H:%M:%S")
                        dtTo = dtmTo.date()
                        dtToTime = dtmTo.time()

                        print("Pronóstico de: " + dtFrom.strftime('%d/%m/%Y') +
                              " a " + dtTo.strftime('%d/%m/%Y'))
                        # self.ui.textBrowser.append("<strong>Forecast:</strong> " + dtFrom.strftime('%d/%m/%Y') + " " + dtFromTime.strftime(
                        #    '%H:%M') + " to " + dtTo.strftime('%d/%m/%Y') + " " + dtToTime.strftime('%H:%M'))
                        strWeather = "<td align='left'>"+dtFrom.strftime('%d/%m/%Y') + " " + dtFromTime.strftime(
                            '%H:%M') + " to <br>" + dtTo.strftime('%d/%m/%Y') + " " + dtToTime.strftime('%H:%M')+"</td>"

                        # Ícono
                        tagSymbol = tagTime.find('symbol')
                        strDescr = tagSymbol.get('name')
                        strIcon = tagSymbol.get('var')+".png"
                        # print('Clima: ' + strDescr)
                        # self.ui.textBrowser.append("<strong>Clima:</strong> " + strDescr)
                        strClima = "<td><strong>Weather:</strong> " + strDescr + "</td>"

                        htmlPixmap = "<td align='center'><img src='" + \
                            os.path.join(dirname, "icons/" + strIcon)+"' width='25'></td>"
                        # debug only - print(htmlPixmap)
                        # pic = QLabel(self)
                        # self.ui.pic.setPixmap(pixmap)
                        
                        # Temperatura
                        tagTemperature = tagTime.find('temperature')
                        strUnit = tagTemperature.get('unit')
                        strTemperature = tagTemperature.get('value')
                        # print("Temperatura: " + strTemperature + "° " + strUnit)
                        # self.ui.textBrowser.append(
                        #    "<strong>Temperature:</strong> " + strTemperature + "° " + strUnit)
                        strTemperature = "<td align='center'>" + strTemperature + "° C</td>"

                        # Precipitación
                        tagPrecipitation = tagTime.find('precipitation')
                        # print("Precipitación: " + tagPrecipitation.get('value') + " mm")
                        # self.ui.textBrowser.append(
                        #    "<strong>Precipitation:</strong> " + tagPrecipitation.get('value') + " mm")
                        strPrecipation = "<td align='center'>" + \
                            tagPrecipitation.get('value') + " mm</td>"

                        # Velocidad del viento
                        tagWindSpeed = tagTime.find('windSpeed')
                        strMps = tagWindSpeed.get('mps')
                        strWind = tagWindSpeed.get('name')

                        # Dirección del viento
                        tagWindDirection = tagTime.find('windDirection')
                        strDegree = tagWindDirection.get('deg')
                        strDirection = tagWindDirection.get('name')
                        strWindDirCode = tagWindDirection.get('code')

                        # self.ui.textBrowser.append("<strong>Wind speed & direction: </strong>" +
                        #                           strMps + " mp/s, " + strWindDirCode)
                        htmlWind = "<td align='center'>" + strMps + " mp/s, " + strWindDirCode + "</td>"

                        # Presión
                        tagPressure = tagTime.find('pressure')
                        strPresUnit = tagPressure.get('unit')
                        strPresValue = tagPressure.get('value')
                        # self.ui.textBrowser.append(
                        #    "<strong>Pressure: </strong>" + strPresValue + " " + strPresUnit)
                        htmlPressure = "<td align='center'>" + strPresValue + " " + strPresUnit + "</td>"

                        html += htmlPixmap + strWeather + strTemperature + strPrecipation + htmlWind + htmlPressure

                        html += "</tr>"

                        if self.ui.radioBtnToday.isChecked():
                            break
                        else:
                            html += "<tr>"

                    html += "</tbody></table>"
                    # debug only - print(html)
                    self.ui.textBrowser.append(html)
                    break


file = sys.argv[0]
dirname = os.path.dirname(file)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = SimpleWeather()
    ex.show()
    sys.exit(app.exec())
