import sys
from tempfile import tempdir
import requests
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta as td
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, QComboBox, QGridLayout
from PyQt5.QtCore import QTimer, QTime, Qt, QDateTime
from sklearn.semi_supervised import LabelSpreading
from weather_api_test import main_weather



def get_seven_days():
    
    today = dt.now()
    now = dt.now()
    today = str(today.strftime('%Y-%m-%d'))
    list = [today]

    for i in range(1,7):
        delta = td(days = i)
        tomorrow = now + delta
        tomorrow = str(tomorrow.strftime('%Y-%m-%d'))
        list.append(tomorrow)

    return list




class MainWindow(QWidget):
    def __init__(self):
        super().__init__()


        self.labels = ['self.label_chance_rain',
                  'self.label_weather_icon',
                  'self.label_temp',
                  'self.label_cloud',
                  'self.label_wind',
                  'self.label_humidity',
                  'self.label_visibility',
                  'self.label_pressure']
           
        self.line_edit = QLineEdit(self)
        self.hour_combobox = QComboBox(self)
        self.date_combobox = QComboBox(self)

        self.label_chance_rain = QLabel("Chance of rain", self)
        self.label_weather_icon = QLabel("sloneczko/ksiezyc/chmurka", self)
        self.label_temp = QLabel("temperature", self)
        self.label_clouds = QLabel("clouds", self)
        self.label_wind = QLabel("wind", self)
        self.label_humidity = QLabel("humidity", self)
        self.label_visibility = QLabel("visibility", self)
        self.label_pressure = QLabel("pressure", self)
        

        self.initUI()
    
      

    def initUI(self):
        
        

        self.setGeometry(400, 600, 400, 800)
        self.setWindowTitle("My Weather App")
        
        vbox = QVBoxLayout()

        vbox.addWidget(self.line_edit)    
        vbox.addWidget(self.label_chance_rain)
        vbox.addWidget(self.label_weather_icon)
        vbox.addWidget(self.label_temp)
        vbox.addWidget(self.label_clouds)

        self.setLayout(vbox)

        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.label_wind)
        hbox2.addWidget(self.label_humidity)
        hbox3.addWidget(self.label_visibility)
        hbox2.addWidget(self.label_pressure)
        hbox1.addWidget(self.hour_combobox)
        hbox1.addWidget(self.date_combobox)

        vbox.addLayout(hbox3)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox1)


        self.label_chance_rain.setAlignment(Qt.AlignCenter)
        self.label_weather_icon.setAlignment(Qt.AlignCenter)
        self.label_temp.setAlignment(Qt.AlignCenter)
        self.label_clouds.setAlignment(Qt.AlignCenter)
        self.label_wind.setAlignment(Qt.AlignCenter)
        self.label_humidity.setAlignment(Qt.AlignCenter)
        self.label_visibility.setAlignment(Qt.AlignCenter)
        self.label_pressure.setAlignment(Qt.AlignCenter)
        

    
        self.hour_combobox.addItems([f"{i:02d}:00" for i in range(25)])
        self.date_combobox.addItems(get_seven_days())
        
    
        self.line_edit.setStyleSheet("font-size: 25px")
        self.hour_combobox.setStyleSheet("font-size: 25px")
        self.date_combobox.setStyleSheet("font-size: 25px")
        
        self.line_edit.returnPressed.connect(self.get_city)


    def get_city(self):
        city = self.line_edit.text()
        chosen_hour = str(self.hour_combobox.currentText())
        print(f"DEBUG: {chosen_hour}")
        chosen_date = str(self.date_combobox.currentText())
        print(f"DEBUG: {chosen_date}")

        self.get_weather_data(city,chosen_date,chosen_hour)
        
    
    def get_weather_data(self,city,chosen_date,chosen_hour):
        data = main_weather(city)
        data = data['hourly']
        df = pd.DataFrame({
            'time': data['time'],
            'temperature': data['temperature_2m'],
            'humidity': data['relative_humidity_2m'],
            'precipitation': data['precipitation'],
            'pressure': data['surface_pressure'],
            'cloud_cover': data['cloud_cover'],
            'visibility': data['visibility'],
            'wind_speed': data['wind_speed_10m']})
        

        df[['date', 'hour']] = df.time.str.split("T", expand = True)
        df = df.drop('time', axis=1)
        print(df)
        print(chosen_date)
        print(chosen_hour)
        df = df.loc[(df['date'] == chosen_date) & (df['hour'] == chosen_hour)]
        print(df)
    


        temperature = df['temperature'].to_string(index=False)
        humidity = df['humidity'].to_string(index=False)
        precipitation = df['precipitation'].to_string(index=False)
        pressure = df['pressure'].to_string(index=False)
        cloud_cover = df['cloud_cover'].to_string(index=False)
        visibility = df['visibility'].to_string(index=False)
        wind_speed = df['wind_speed'].to_string(index=False)
        
        self.label_chance_rain.setText(precipitation)
        self.label_temp.setText(temperature)
        self.label_clouds.setText(cloud_cover)
        self.label_wind.setText(wind_speed)
        self.label_humidity.setText(humidity)
        self.label_visibility.setText(visibility)
        self.label_pressure.setText(pressure)

            

        

    



        
    
       
    


       


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    


