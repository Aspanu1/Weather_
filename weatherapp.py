import sys
from tempfile import tempdir
import requests
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta as td
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, QComboBox, QGridLayout
from PyQt5.QtCore import QTimer, QTime, Qt, QDateTime
from PyQt5.QtGui import QPixmap
from weather_api_test import main_weather, get_ip_location
  


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
           
        self.line_edit = QLineEdit(self)
        self.hour_combobox = QComboBox(self)
        self.date_combobox = QComboBox(self)

        self.label_chance_rain = QLabel("Chance of rain", self)
        self.label_weather_icon = QLabel("sloneczko", self)
        self.label_temp = QLabel("temperature", self)
        self.label_clouds = QLabel("clouds", self)
        self.label_wind = QLabel("wind", self)
        self.label_humidity = QLabel("humidity", self)
        self.label_visibility = QLabel("visibility", self)
        self.label_pressure = QLabel("pressure", self)
        self.label_forecast_time = QLabel("11/29 23:35", self)
    
        self.initUI()
    
    def initUI(self):

       
        self.setGeometry(400, 600, 400, 800)
        self.setWindowTitle("My Weather App")
        
        
        vbox = QVBoxLayout()

        vbox.addWidget(self.line_edit)    
        vbox.addWidget(self.label_forecast_time)    
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

        self.setStyleSheet("background-color: #11111b;")

        self.line_edit.setStyleSheet("font-size: 25px")
        self.hour_combobox.setStyleSheet("font-size: 25px")
        self.date_combobox.setStyleSheet("font-size: 25px")

        self.label_chance_rain.setStyleSheet(self.labelStyleSheet())
      
        self.label_wind.setStyleSheet(self.labelStyleSheet())
        self.label_humidity.setStyleSheet(self.labelStyleSheet())
        self.label_visibility.setStyleSheet(self.labelStyleSheet())
        self.label_pressure.setStyleSheet(self.labelStyleSheet())

        self.label_chance_rain.setStyleSheet(self.mid_up_labelStyleSheet())
        self.label_weather_icon.setStyleSheet(self.mid_up_labelStyleSheet())
        self.label_temp.setStyleSheet(self.mid_up_labelStyleSheet())
        self.label_clouds.setStyleSheet(self.mid_up_labelStyleSheet())
        self.label_forecast_time.setStyleSheet(self.mid_up_labelStyleSheet())

        self.line_edit.setStyleSheet(self.labelStyleSheet())
        self.hour_combobox.setStyleSheet(self.labelStyleSheet())
        self.date_combobox.setStyleSheet(self.labelStyleSheet())

        self.line_edit.returnPressed.connect(self.display_data)
        self.line_edit.returnPressed.connect(self.set_data_in_combo_boxes)
        self.is_first_loop = True
        self.set_data_in_combo_boxes()
        self.set_data_in_combo_boxes()
        self.display_data()

    def mid_up_labelStyleSheet(self):
        return"""
        QLabel{
            color: #cdd6f4;
            font-size: 20px;
            font-family: Consolas;
        }

        """
    def labelStyleSheet(self):
            return """
                background-color: #45475a;
                opacity: 0.6;
                color: #cdd6f4;
                font-size: 20px;
                font-family: Consolas;
                border-radius: 15px;
                border-style: hidden;
            """
            
    def window_styleSheet(self):
        return"background: #11111b;"
        

    def set_data_in_combo_boxes(self):
        self.hour_combobox.clear()
        today = dt.now()
        now = dt.now()
        today = today.strftime('%Y-%m-%d')
        list_days = [today]
       
        for i in range(1,7):
            delta = td(days = i)
            tomorrow = now + delta
            tomorrow = str(tomorrow.strftime('%Y-%m-%d'))
            list_days.append(tomorrow)  
        
            self.date_combobox.addItems(list_days)
            self.hour_combobox.addItems([f"{i:02d}:00" for i in range(25)])
            
    def fetch_data_API(self):

        if not self.is_first_loop == False:
            print('123')
            city = get_ip_location()
            today = dt.now()
            chosen_date = str(today.strftime('%Y-%m-%d'))
            print(chosen_date)
            now = int(today.strftime('%H'))
            chosen_hour = f"{now:02d}:00"   
            self.is_first_loop = False

            
        else:
            city = self.line_edit.text()

            print(city)
            chosen_hour = str(self.hour_combobox.currentText())
            print(f"DEBUG: {chosen_hour}")
            chosen_date = str(self.date_combobox.currentText())
            print(f"DEBUG: {chosen_date}")

        df = self.get_weather_data(city,chosen_date,chosen_hour)
        self.label_forecast_time.setText(f"{chosen_hour} {chosen_date}")
        return df
    
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
        df = df.loc[(df['date'] == chosen_date) & (df['hour'] == chosen_hour)]
        return df

    def display_data(self):

        nl = '\n'
        df = self.fetch_data_API()
    
        temperature = df['temperature'].to_string(index=False)
        humidity = df['humidity'].to_string(index=False)
        precipitation = df['precipitation'].to_string(index=False)
        pressure = df['pressure'].to_string(index=False)
        visibility = (df['visibility'] / 1000).to_string(index=False)
        wind_speed = df['wind_speed'].to_string(index=False)
        cloud_cover = int(df['cloud_cover'].to_string(index=False))
        
        self.label_chance_rain.setText(f"Chance of rain: {precipitation}%")
        self.label_temp.setText(f"{temperature}°C")
        self.label_wind.setText(f"Wind{nl}{wind_speed} km/h")
        self.label_humidity.setText(f"Humidity{nl}{humidity}%")
        self.label_visibility.setText(f"Visibility{nl}{visibility} km")
        self.label_pressure.setText(f"Pressure{nl}{pressure} hPa")

        if cloud_cover >= 0 and cloud_cover <= 33:
            self.sun_pix = QPixmap('Weather_app\Assets\sun_11845224.png')
            self.label_clouds.setText("Sunny")

        elif cloud_cover > 33 and cloud_cover <= 66:
            self.sun_pix = QPixmap('Weather_app\Assets\clouds-sun_10961135.png')
            self.label_clouds.setText("Partly cloudy")

        else:
            self.sun_pix = QPixmap('Weather_app\Assets\clouds_10961174.png')
            self.label_clouds.setText("Mostly cloudy")
            

        self.sun_pix_scaled = self.sun_pix.scaled(170, 170, Qt.KeepAspectRatio)
        self.label_weather_icon.setPixmap(self.sun_pix_scaled) 
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    


