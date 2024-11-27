import sys
from tempfile import tempdir
import requests
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta as td
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, QComboBox
from PyQt5.QtCore import QTimer, QTime, Qt, QDateTime
from weather_API import main_weather

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
    #adddasdad


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.line_edit = QLineEdit(self)
        self.button_submit = QPushButton('SUBMIT', self)
        self.weather_label = QLabel("test", self)
        self.hour_combobox = QComboBox(self)
        self.date_combobox = QComboBox(self)

        self.initUI()
      

      

    def initUI(self):
        
        self.setGeometry(400, 600, 800, 600)
        self.setWindowTitle("My Weather App")
        

        vbox = QVBoxLayout()
    
        vbox.addWidget(self.weather_label)
        vbox.addWidget(self.line_edit)
        vbox.addWidget(self.hour_combobox)
        vbox.addWidget(self.date_combobox)
        vbox.addWidget(self.button_submit)

        self.setLayout(vbox)

        self.hour_combobox.addItems([f"{i:02d}:00" for i in range(25)])
        self.date_combobox.addItems(get_seven_days())
        
        

        self.weather_label.setAlignment(Qt.AlignCenter)
        self.weather_label.setStyleSheet("font-size: 20px;"
                                         "background-color: green;")
        self.button_submit.setStyleSheet("font-size: 25px")
        self.line_edit.setStyleSheet("font-size: 25px")
        self.hour_combobox.setStyleSheet("font-size: 25px")
        self.date_combobox.setStyleSheet("font-size: 25px")

        self.button_submit.clicked.connect(self.city_weather)


    def city_weather(self):
        city = self.line_edit.text()
        chosen_hour = str(self.hour_combobox.currentText())
        print(f"DEBUG: {chosen_hour}")
        chosen_date = str(self.date_combobox.currentText())
        print(f"DEBUG: {chosen_date}")

        self.print_weather(city, chosen_date,chosen_hour)
        
    
    def print_weather(self,city,chosen_date,chosen_hour):
        df = main_weather(city)
        df = df['hourly']
        df = pd.DataFrame({
            'time': df['time'],
            'temp': df['temperature_2m']
        })
        df[['date', 'hour']] = df.time.str.split("T", expand = True)
        df = df.drop('time', axis = 1)
        result_df = df.loc[(df['date'] == chosen_date) & (df['hour'] == chosen_hour)]
        self.weather_label.setText(result_df.to_string())



        


       
        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    


