import sys, requests
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout ,QPushButton, QLabel, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import QTimer,Qt
from PyQt5.QtGui import QPixmap, QImage, QFont
from WeatherWidget import WeatherWidget
from WeatherDto import WeatherDto
import secrets

#TODO : Split grid and constants out
# Move GRIDS to secrets file
# Location be new class: ? GRIDS/name/
#WEATHER_URL_HOURLY = "https://api.weather.gov/gridpoints/PHI/39,67/forecast/hourly"
WEATHER_URL_HOURLY = "https://api.weather.gov/gridpoints/"+secrets.LOCATION+"/forecast/hourly"
WEATHER_URL_FORECAST= "https://api.weather.gov/gridpoints/PHI/39,67/forecast"
#HEADERS = {"User-Agent":"PICO RPI4"}
HEADERS = secrets.HEADERS

class WeatherUI(QWidget):
    def __init__(self):
        super().__init__()
        self.main_period="1"
        #TODO : switch to array
        self.period_1_dto = WeatherDto("1")
        self.period_2_dto = WeatherDto("2")
        self.period_3_dto = WeatherDto("3")
        self.period_4_dto = WeatherDto("4")
        self.period_5_dto = WeatherDto("5")
        self.period_6_dto = WeatherDto("6")
        self.period_7_dto = WeatherDto("7")
        self.period_8_dto = WeatherDto("8")
        self.period_9_dto = WeatherDto("9")
        
        self.init_Weather_UI()
        
        # Refresh timer: 30 min (1800000)
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(180000)
                         
        self.refresh()
        self.showFullScreen()
        
    def init_Weather_UI(self):
        
        quit_button = QPushButton('Quit', self)
        quit_button.clicked.connect(QApplication.instance().quit)
        quit_button.setMaximumWidth(80) 
        quit_button.setMaximumHeight(40)
        
        self.btn_toggle_size = QPushButton('Min', self)
        self.btn_toggle_size.setCheckable(True)
        self.btn_toggle_size.clicked.connect(self.on_btn_toggle_size)
        self.btn_toggle_size.setMaximumWidth(80) 
        self.btn_toggle_size.setMaximumHeight(40)
        
        # TODO: add code to switch location: Switch to drop down 
        self.btn_location = QPushButton('Wilmington', self)
        self.btn_location.setCheckable(True)
        self.btn_location.clicked.connect(self.on_btn_location)
        self.btn_location.setMaximumHeight(400)
        self.btn_location.setFont(QFont('Arial', 14, QFont.Bold))
        
        self.main_period_desc = QLabel("Current :")
        self.main_period_desc.setFont(QFont('Arial', 20))
        
        self.main_forecast_label = QLabel("----")
        self.main_forecast_label.setFont(QFont('Arial', 20))
        self.main_forecast_label.setWordWrap(True)
        self.main_forecast_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.main_temp_label = QLabel("--°F")
        self.main_temp_label.setFont(QFont('Arial', 40, QFont.Bold))
        
        lower_box= QHBoxLayout()
        
        self.period_1_widget  = WeatherWidget()
        self.period_1_widget.clickedValue.connect(self.period_clicked)
        self.period_1_widget.update_dataset(self.period_1_dto)
        
        self.period_2_widget  = WeatherWidget()
        self.period_2_widget.clickedValue.connect(self.period_clicked)
        self.period_2_widget.update_dataset(self.period_2_dto)
        
        self.period_3_widget  = WeatherWidget()
        self.period_3_widget.clickedValue.connect(self.period_clicked)
        self.period_3_widget.update_dataset(self.period_3_dto)
        
        self.period_4_widget  = WeatherWidget()
        self.period_4_widget.clickedValue.connect(self.period_clicked)
        self.period_4_widget.update_dataset(self.period_4_dto)
        
        self.period_5_widget  = WeatherWidget()
        self.period_5_widget.clickedValue.connect(self.period_clicked)
        self.period_5_widget.update_dataset(self.period_5_dto)
        
        self.period_6_widget  = WeatherWidget()
        self.period_6_widget.clickedValue.connect(self.period_clicked)
        self.period_6_widget.update_dataset(self.period_6_dto)
        
        self.period_7_widget  = WeatherWidget()
        self.period_7_widget.clickedValue.connect(self.period_clicked)
        self.period_7_widget.update_dataset(self.period_7_dto)
        
        self.period_8_widget  = WeatherWidget()
        self.period_8_widget.clickedValue.connect(self.period_clicked)
        self.period_8_widget.update_dataset(self.period_8_dto)
        
        self.period_9_widget  = WeatherWidget()
        self.period_9_widget.clickedValue.connect(self.period_clicked)
        self.period_9_widget.update_dataset(self.period_9_dto)         
        
        lower_box.addLayout(self.period_2_widget.get_layout())
        lower_box.addLayout(self.period_3_widget.get_layout())
        lower_box.addLayout(self.period_4_widget.get_layout())
        lower_box.addLayout(self.period_5_widget.get_layout())
        lower_box.addLayout(self.period_6_widget.get_layout())
        lower_box.addLayout(self.period_7_widget.get_layout())
        lower_box.addLayout(self.period_8_widget.get_layout())
        lower_box.addLayout(self.period_9_widget.get_layout())
        
        self.icon_label = QLabel()
    
        vbox = QVBoxLayout()
        vbox.addWidget(quit_button, alignment=Qt.AlignTop | Qt.AlignRight)
        vbox.addWidget(self.btn_toggle_size, alignment=Qt.AlignTop | Qt.AlignRight)
        vbox.addWidget(self.btn_location, alignment=Qt.AlignTop | Qt.AlignLeft)
        vbox.addStretch()
        vbox.addWidget(self.main_period_desc, alignment=Qt.AlignCenter)
        vbox.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        vbox.addWidget(self.main_temp_label, alignment=Qt.AlignCenter)
        vbox.addWidget(self.main_forecast_label)
        
        forecast_bar = QWidget()
        forecast_bar.setAutoFillBackground(True)
        forecast_bar.setStyleSheet("background-color: #221252;")
        forecast_bar.setMinimumHeight(3)
        vbox.addWidget(forecast_bar)

        vbox.addLayout(lower_box)
        self.setLayout(vbox)

        self.setWindowTitle('Weather')
        self.setStyleSheet("background-color: #121212; color: white;")
        
        
    def on_btn_toggle_size(self, fullScreen):
        self.toggle_full_screen(fullScreen)
        
    def toggle_full_screen(self,fullScreen):
        if fullScreen:
            self.showNormal()
            self.btn_toggle_size.setText('Max')
        else:
            self.showFullScreen()
            self.btn_toggle_size.setText('Min')
        self.refresh()
            
    #Currently between 2 locations: CHange to dropdown/dynamic populated
    def on_btn_location(self, location):
        
        self.main_period_desc.setText("Current:")
        self.toggle_location(location)      
        
    def toggle_location(self,location):
        if location:
            print("switch location - not turned on yet - refresh only now")
            self.main_period = "1"
            self.refresh()
        else:
            print("switch location - not turned on yet - refresh only now")
            self.main_period = "1"
            self.refresh()
            
    def refresh(self):
        try:
            print("Refreshing data")
            
            # Use hourly to get more accurate current temp
            response = requests.get(WEATHER_URL_HOURLY, headers=HEADERS)
            if(response.status_code==200):
                forecastJson = response.json()
                temp = self.parse_response_single_field(forecastJson)
                self.main_temp_label.setText(temp+" °F")
            
            response = requests.get(WEATHER_URL_FORECAST, headers=HEADERS)
            if(response.status_code==200):
                forecastJson = response.json()
                forecast = self.parse_response_single_field(forecastJson, itemValue="detailedForecast")
                
                # If not not current period , then do not auto refresh
                if(str(self.main_period) == str("1")):
                    forecast = self.parse_response_single_field(forecastJson, itemValue="detailedForecast")
                    #print(forecast)
                    icon = self.parse_response_single_field(forecastJson, itemValue="icon")
                    self.main_forecast_label.setText(forecast)
                    self.main_forecast_label.setWordWrap(True)
                    self.main_forecast_label.resize(self.main_forecast_label.sizeHint())
                    self.update_icon(icon)
                    
                # Can this be move to array of DTOs?
                self.period_1_dto=self.update_dto(self.period_1_dto, 1, forecastJson)
                self.period_1_widget.update_dataset(self.period_1_dto)
                self.period_2_dto=self.update_dto(self.period_2_dto, 2, forecastJson)
                self.period_2_widget.update_dataset(self.period_2_dto)
                self.period_3_dto=self.update_dto(self.period_3_dto, 3, forecastJson)
                self.period_3_widget.update_dataset(self.period_3_dto)
                self.period_4_dto=self.update_dto(self.period_4_dto, 4, forecastJson)
                self.period_4_widget.update_dataset(self.period_4_dto)
                self.period_5_dto=self.update_dto(self.period_5_dto, 5, forecastJson)
                self.period_5_widget.update_dataset(self.period_5_dto)
                self.period_6_dto=self.update_dto(self.period_6_dto, 6, forecastJson)
                self.period_6_widget.update_dataset(self.period_6_dto)
                self.period_7_dto=self.update_dto(self.period_7_dto, 7, forecastJson)
                self.period_7_widget.update_dataset(self.period_7_dto)
                self.period_8_dto=self.update_dto(self.period_8_dto, 8, forecastJson)
                self.period_8_widget.update_dataset(self.period_8_dto)
                self.period_9_dto=self.update_dto(self.period_9_dto, 9, forecastJson)
                self.period_9_widget.update_dataset(self.period_9_dto)
                
        except Exception as e:
            print(f"Refresh error: {e}")
            
    def update_dto(self, period_dto, period, forecastJson):
            temp, name, short, long, icon = self.parse_response_multi_field(forecastJson, period )
            period_dto.update(day=name, temp=temp, short=short, long=long, icon=icon)
            #print(name)
            return period_dto
            
    def parse_response_single_field(self, response, period = 1, itemValue="temperature"):
        
        periods = response["properties"]["periods"]
        for item in periods:
            #print("day: " , item["name"] , " Temp: " , item["temperature"], " Forecast: ", item["detailedForecast"])
            if item["number"] == period:
                value = item[itemValue]
                break
        return str(value)
    
    def parse_response_multi_field(self, response, period = 1, itemValue1="temperature", itemValue2="name", itemValue3="shortForecast",itemValue4="detailedForecast", itemValue5="icon"):
        periods = response["properties"]["periods"]
        for item in periods:
            #print("day: " , item["name"] , " Temp: " , item["temperature"], " Forcast: ", item["detailedForecast"])
            if item["number"] == period:
                value1 = item[itemValue1]
                value2 = item[itemValue2]
                value3 = item[itemValue3]
                value4 = item[itemValue4]
                value5 = item[itemValue5]
                break
        return str(value1), str(value2),str(value3) ,str(value4),str(value5)

    def update_icon(self, url):
        img_data = requests.get(f"{url}").content
        img = QImage()
        img.loadFromData(img_data)
        self.icon_label.setPixmap(QPixmap.fromImage(img))
        
    def period_clicked(self, period):
        print(period)
        self.update_main(self.identify_dto(period))
        
    def update_main(self, dto):
        self.main_period=dto.period
        self.main_temp_label.setText(dto.temp)
        self.update_icon(dto.icon)
        self.main_forecast_label.setText(dto.long_forecast)
        self.main_period_desc.setText(dto.full_day+":")
        
    def identify_dto(self, period):
        if(self.period_2_dto.period==period):
            return self.period_2_dto
        if(self.period_3_dto.period==period):
            return self.period_3_dto
        if(self.period_4_dto.period==period):
            return self.period_4_dto
        if(self.period_5_dto.period==period):
            return self.period_5_dto
        if(self.period_6_dto.period==period):
            return self.period_6_dto
        if(self.period_7_dto.period==period):
            return self.period_7_dto
        if(self.period_8_dto.period==period):
            return self.period_8_dto
        if(self.period_9_dto.period==period):
            return self.period_9_dto

def main():
    app = QApplication(sys.argv)
    window =WeatherUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
