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
import time
import json
import sqlite3
import xml.etree.ElementTree as etree

from datetime import date, datetime
from PyQt5 import Qt, QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
# from PyQt5.QtCore import QDir, QUrl, QFileInfo
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QComboBox, QApplication, QGridLayout, QMessageBox, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap, QPainter


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")  
        #Form.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint)     
        Form.resize(600, 500)
        
        self.tabWidget = QtWidgets.QWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(10, 30, 550, 450))

        self.gridLayoutWidget = QtWidgets.QWidget(self.tabWidget)

        self.lineEdit = QtWidgets.QLineEdit(self.tabWidget)
        #self.lineEdit.setGeometry(QtCore.QRect(10, 1, 191, 32))
        self.lineEdit.setObjectName("lineEdit")

        self.btnSearch = QtWidgets.QPushButton(self.tabWidget)
        #self.btnSearch.setGeometry(QtCore.QRect(210, 1, 88, 34))
        self.btnSearch.setObjectName("btnSearch")

        self.btnRefresh = QtWidgets.QPushButton(self.tabWidget)
        iconButton = QtGui.QIcon()        
        pixmapRefresh = QPixmap(os.path.join(dirname, "icons/refresh.png"))
        iconButton.addPixmap(pixmapRefresh, QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnRefresh.setIcon(iconButton)
        #self.btnRefresh.setIconSize(QSize(20,20))
        self.btnRefresh.setToolTip("Refresh")

        self.textBrowser = QtWidgets.QTextBrowser(self.tabWidget)
        self.textBrowser.setObjectName("textBrowser")
        #self.textBrowser.setGeometry(QtCore.QRect(10, 120, 520, 300))

        # City Label
        self.labelCity = QtWidgets.QLabel(self.tabWidget)
        #self.labelCity.setGeometry(QtCore.QRect(280,55,191,20))
        self.labelCity.setObjectName("labelCity")
        
        # Image Label
        self.labelPixmap = QtWidgets.QLabel(self.tabWidget)
        #self.labelPixmap.setGeometry(QtCore.QRect(210,60,30,30)) 
        self.labelPixmap.setObjectName("labelPixmap")

        # Temperature Label
        self.labelDegrees = QtWidgets.QLabel(self.tabWidget)
        self.labelDegrees.setObjectName("labelDegrees")

        # Forecast Label
        self.labelForecast = QtWidgets.QLabel(self.tabWidget)
        self.labelForecast.setObjectName("labelForecast")

        # Wind Label
        self.labelWind = QtWidgets.QLabel(self.tabWidget)
        self.labelWind.setObjectName("labelWind")

        # Pressure Label
        self.labelPressure = QtWidgets.QLabel(self.tabWidget)
        self.labelPressure.setObjectName("labelPressure")
        
        # YR Label
        self.labelYR = QtWidgets.QLabel(self.tabWidget)
        self.labelYR.setObjectName("labelYR")
        self.labelYR.setText("Weather forecast from Yr, delivered by the Norwegian Meteorological Institute and NRK")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

# ================       LAYOUT       ================

        # Layout arriba izquierda
        hboxTopLeft = QHBoxLayout()
        hboxTopLeft.setObjectName("hboxTopLeft")
        hboxTopLeft.addWidget(self.textBrowser)

        hboxTop = QHBoxLayout()        
        #hboxTop.addStretch(1)
        hboxTop.addWidget(self.lineEdit)
        hboxTop.addWidget(self.btnSearch)
        hboxTop.addWidget(self.btnRefresh)
        hboxTop.setObjectName("hboxTop")

        hboxCity = QHBoxLayout()
        hboxCity.addWidget(self.labelCity)
        hboxCity.setAlignment(Qt.AlignCenter)

        hboxWeatherTop = QHBoxLayout()
        hboxWeatherTop.addWidget(self.labelPixmap)
        hboxWeatherTop.addWidget(self.labelDegrees)
        hboxWeatherTop.setAlignment(Qt.AlignCenter)

        hboxWeatherMiddle = QHBoxLayout()
        hboxWeatherMiddle.addWidget(self.labelForecast)
        hboxWeatherMiddle.setAlignment(Qt.AlignCenter)

        hboxWeatherBottom = QHBoxLayout()
        hboxWeatherBottom.addWidget(self.labelWind)
        hboxWeatherBottom.addWidget(self.labelPressure)
        hboxWeatherBottom.setAlignment(Qt.AlignCenter)

        vboxWeather = QVBoxLayout()
        vboxWeather.addLayout(hboxCity)
        vboxWeather.addLayout(hboxWeatherTop)
        vboxWeather.addLayout(hboxWeatherMiddle)
        vboxWeather.addLayout(hboxWeatherBottom)

        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 5, 530, 430))
        self.gridLayout1 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout1.setContentsMargins(0, 0, 0, 0)
        self.gridLayout1.layout().setContentsMargins(0,0,0,0)
        self.gridLayout1.addLayout(hboxTop, 0, 0)        
        #self.gridLayout1.addWidget(self.labelCity, 1, 0, Qt.AlignCenter)
        self.gridLayout1.addLayout(vboxWeather, 1, 0, Qt.AlignCenter)
        self.gridLayout1.addWidget(self.textBrowser, 2, 0)
        self.gridLayout1.addWidget(self.labelYR,4,0)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Pretty Simple Weather App"))
        self.btnSearch.setText(_translate("Form", "Search"))


class SimpleWeather(QtWidgets.QMainWindow):
    def __init__(self):
        super(SimpleWeather, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # self.ui.btnSearch.clicked.connect(self.parseXML)
        self.ui.btnSearch.clicked.connect(self.findCity)
        self.ui.btnRefresh.clicked.connect(self.findCity)
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

            strCity = ""
            strCountry = ""

            if len(splitCity) > 1:
                strCity = splitCity[0].strip()
                strCountry = splitCity[1].strip()
            else:
                strCity = splitCity[0].strip()        


            if len(splitCity) < 2:
                cursor.execute("select city, country_descr, xml from cities where upper(city) like ?", (strCity.upper(),))
            else:
                cursor.execute("select city, country_descr, xml from cities where upper(city) like ? and upper(country_descr) like ?",
                            (strCity.upper(), strCountry.upper()))

            data = cursor.fetchone()
            
            if data == None:
                return None
            else:            
                # SQL output
                strOutCity = data [0] # City
                strOutCountry = data[1] # Country
                strOutXml = data[2] # XML

                db.close()

                # Prints the city in the Window
                self.ui.labelCity.setText(strOutCity + ", " + strOutCountry)

                # print(strOutXml)
                self.parseXML(strOutXml)

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

        html = "<table cellspacing='2' width = '100%'><tbody>"
        strIconForecast = "<img src='" + os.path.join(dirname, "icons/time.svg") + "'>"
        strIconTemp = "<img src='" + os.path.join(dirname, "icons/temp.svg") + "'>"
        strIconRain = "<img src='" + os.path.join(dirname, "icons/umbrella.svg") + "'>"
        html += "<tr><th width='35'></th><th align='center'>"+strIconForecast+"</th><th align='center'>"+strIconTemp+"</th>"
        html += "<th align='center'>"+strIconRain+"</th></tr>" #<th align='center'>Wind</th><th align='center'>Pressure</th></tr>"

        self.ui.textBrowser.setText("")

        for child in root:
            if child.tag == 'forecast':
                for tagTabular in child:
                    boolChange = False
                    tempMax = -1000
                    tempMax2 = -1000
                    stepBreak = False
                    for tagTime in tagTabular:
                        
                        # Obtener Fecha Origen
                        strDttmFrom = tagTime.get('from')
                        dtmFrom = datetime.strptime(strDttmFrom, "%Y-%m-%dT%H:%M:%S")
                        dtFrom = dtmFrom.date()
                        dtToday = date.today()

                        strPeriod = tagTime.get('period')
                        nbrPeriod = int(strPeriod)

                        # Temperature
                        tagTemperature = tagTime.find('temperature')
                        #strUnit = tagTemperature.get('unit')
                        strTemperature = tagTemperature.get('value')
                        # print("Temperatura: " + strTemperature + "° " + strUnit)
                        
                        # Icon
                        tagSymbol = tagTime.find('symbol')
                        strForecast = tagSymbol.get('name')
                        strIcon = tagSymbol.get('var')+".png"
                        #print("Pronóstico de: " + dtFrom.strftime('%d/%m/%Y') + " a " + dtTo.strftime('%d/%m/%Y'))

                        # Precipitación
                        tagPrecipitation = tagTime.find('precipitation')
                        strPrecipitation = tagPrecipitation.get('value')
                        # print("Precipitación: " + strPrecipitation + " mm")
                        
                        # Velocidad del viento
                        tagWindSpeed = tagTime.find('windSpeed')
                        strMps = tagWindSpeed.get('mps')
                        #strWind = tagWindSpeed.get('name')

                        # Wind direction
                        # tagWindDirection = tagTime.find('windDirection')
                        #strDegree = tagWindDirection.get('deg')
                        #strDirection = tagWindDirection.get('name')
                        #strWindDirCode = tagWindDirection.get('code')

                        # Pressure
                        tagPressure = tagTime.find('pressure')
                        strPresUnit = tagPressure.get('unit')
                        strPresValue = tagPressure.get('value')
                        
                        comparison1 = dtToday == dtFrom 
                        comparison2 = dtToday != dtFrom
   
                        if (comparison1 and not(boolChange))  or (comparison2 and not(boolChange)):

                            # Stores max temperature                            
                            if tempMax < float(strTemperature):
                                tempMax = float(strTemperature)
                            
                            # if it reaches the last period, then write the main temperature and icon
                            if nbrPeriod == 3:
                                # Icon
                                pixmap = QPixmap(os.path.join(dirname, "icons/" + strIcon))
                                pixmap = pixmap.scaled(50,50,Qt.KeepAspectRatio, Qt.FastTransformation)
                                self.ui.labelPixmap.setPixmap(pixmap)
                                
                                # Forecast
                                #debug only - print("Forecast: " + strForecast)
                                self.ui.labelForecast.setText(strForecast)

                                # Temperature
                                #debug only - print ("Temperature: " + strTemperature)
                                self.ui.labelDegrees.setFont(QtGui.QFont("Droid Sans", 20, QtGui.QFont.Bold))
                                self.ui.labelDegrees.setText(strTemperature  + "° C")

                                # Precipitation
                                #debug only - print ("Precipitation: " + strPrecipitation + " mm")

                                # Wind
                                #debug only - print (strWind + ", " + strMps + " from " + strDirection)
                                self.ui.labelWind.setText("Wind: " + strMps)

                                # Pressure
                                self.ui.labelPressure.setText("Pressure: " + strPresValue + " " + strPresUnit)
                                boolChange = True
                        else:
                            # Following days
                            if dtToday < dtFrom:
                                if nbrPeriod >= 0 and nbrPeriod <= 3:
                                  
                                    # stores the max temperature
                                    if tempMax2 < float(strTemperature):
                                        tempMax2 = float(strTemperature)
                                        
                                        tdDateFrom = dtFrom.strftime('%d/%m/%Y')
                                        tdTemperature = strTemperature
                                        tdForecast = strForecast
                                        tdPixmap = os.path.join(dirname, "icons/" + strIcon)
                                        tdPrecipitation = strPrecipitation

                                    # When it reaches the last period, it draws a line
                                    if nbrPeriod == 3:
                                         html += "<tr>"
                                        htmlPixmap = "<td align='center'><img src='" + tdPixmap +"' width='25'></td>"
                                        htmlWeather = "<td align='center'>" + tdDateFrom +"</td>"
                                        htmlTemperature = "<td align='center'>" + tdTemperature + "° C " + tdForecast + "</td>"
                                        htmlPrecipitation = "<td align='center'>" + tdPrecipitation + " mm</td>"
                                        #htmlWind = "<td align='center'>" + strWind + ", " + strMps + " mp/s, " + strDirection + "</td>"
                                        #htmlPressure = "<td align='center'>" + strPresValue + " " + strPresUnit + "</td>"
                                        html += htmlPixmap + htmlWeather + htmlTemperature + htmlPrecipitation #+ htmlWind + htmlPressure
                                        html += "</tr>"

                                        tempMax2 = -1000 # reset
                                        # stepBreak = False
                    html += "</tbody></table>"
                        
                    # print(html)
                    self.ui.textBrowser.append(html)
                    break


file = sys.argv[0]
dirname = os.path.dirname(file)
strOutXml = ""

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = SimpleWeather()
    ex.show()
    sys.exit(app.exec())
