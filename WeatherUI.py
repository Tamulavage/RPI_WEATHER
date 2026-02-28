import sys, requests
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout ,QPushButton, QLabel, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import QTimer,Qt
from PyQt5.QtGui import QPixmap, QImage, QFont
from WeatherWidget import WeatherWidget
from WeatherDto import WeatherDto
import Secrets
import Constant

# Location be dynamically loaded config class
WEATHER_URL_HOURLY = "https://api.weather.gov/gridpoints/"+Secrets.LOCATION+"/forecast/hourly"
WEATHER_URL_FORECAST= "https://api.weather.gov/gridpoints/"+Secrets.LOCATION+"/forecast"
HEADERS = Secrets.HEADERS

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

        self.time_frame=Constant.DAILY
                         
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
        self.btn_location.setFont(Constant.NORMAL_FONT)

        self.btn_time_frame = QPushButton(Constant.HOURLY, self)
        self.btn_time_frame.setCheckable(True)
        self.btn_time_frame.clicked.connect(self.on_btn_time_frame)
        self.btn_time_frame.setMaximumHeight(400)
        self.btn_time_frame.setFont(Constant.NORMAL_FONT)
        self.btn_time_frame.setStyleSheet("text-align: left;") 
        
        self.main_period_desc = QLabel("Current :")
        self.main_period_desc.setFont(Constant.LARGE_FONT)
        
        self.main_forecast_label = QLabel("----")
        self.main_forecast_label.setFont(Constant.LARGE_FONT)
        self.main_forecast_label.setWordWrap(True)
        self.main_forecast_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.main_temp_label = QLabel("--°F")
        self.main_temp_label.setFont(Constant.XL_FONT_BOLD)
        
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
        upperBox= QHBoxLayout()
        vboxTopLeft = QVBoxLayout()
        vboxTopRight = QVBoxLayout()

        vboxTopLeft.addWidget(self.btn_location, alignment=Qt.AlignTop | Qt.AlignLeft)
        vboxTopLeft.addWidget(self.btn_time_frame, alignment=Qt.AlignTop | Qt.AlignLeft)
        vboxTopRight.addWidget(quit_button, alignment=Qt.AlignTop | Qt.AlignRight)
        vboxTopRight.addWidget(self.btn_toggle_size, alignment=Qt.AlignTop | Qt.AlignRight)
        upperBox.addLayout(vboxTopLeft)
        upperBox.addLayout(vboxTopRight)
        vbox.addLayout(upperBox)

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
        
        self.main_period_desc.setText("Current :")
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

    def on_btn_time_frame(self, frame):
        self.toggle_time_frame(frame) 

    def toggle_time_frame(self,frame):
        if frame:
            self.main_period = "1"
            #Button shows to switch to hourly
            self.btn_time_frame.setText(Constant.DAILY) 
            #Logic is set to Hourly
            self.time_frame=Constant.HOURLY
            self.refresh()
        else:
            self.main_period = "1"
            self.btn_time_frame.setText(Constant.HOURLY)
            self.time_frame=Constant.DAILY
            self.refresh()        
            
    def refresh(self):
        try:
            
            # Use hourly to get more accurate current temp
            response = requests.get(WEATHER_URL_HOURLY, headers=HEADERS)
            if(response.status_code==200):
                forecast_json = response.json()
                temp = self.parse_response_single_field(forecast_json)
                self.main_temp_label.setText(temp+" °F")
                icon = self.parse_response_single_field(forecast_json, item_value="icon")
                self.update_icon(icon)
            
            if(self.time_frame==Constant.DAILY): 
                response = requests.get(WEATHER_URL_FORECAST, headers=HEADERS)     

            if(response.status_code==200):
                forecast_json = response.json()
      
                # If not not current period , then do not auto refresh
                if(str(self.main_period) == str("1")):

                    # Can this be move to array of DTOs?
                    self.period_1_dto=self.update_dto(self.period_1_dto, 1, forecast_json)
                    self.period_1_widget.update_dataset(self.period_1_dto)
                    self.period_2_dto=self.update_dto(self.period_2_dto, 2, forecast_json)
                    self.period_2_widget.update_dataset(self.period_2_dto)
                    self.period_3_dto=self.update_dto(self.period_3_dto, 3, forecast_json)
                    self.period_3_widget.update_dataset(self.period_3_dto)
                    self.period_4_dto=self.update_dto(self.period_4_dto, 4, forecast_json)
                    self.period_4_widget.update_dataset(self.period_4_dto)
                    self.period_5_dto=self.update_dto(self.period_5_dto, 5, forecast_json)
                    self.period_5_widget.update_dataset(self.period_5_dto)
                    self.period_6_dto=self.update_dto(self.period_6_dto, 6, forecast_json)
                    self.period_6_widget.update_dataset(self.period_6_dto)
                    self.period_7_dto=self.update_dto(self.period_7_dto, 7, forecast_json)
                    self.period_7_widget.update_dataset(self.period_7_dto)
                    self.period_8_dto=self.update_dto(self.period_8_dto, 8, forecast_json)
                    self.period_8_widget.update_dataset(self.period_8_dto)
                    self.period_9_dto=self.update_dto(self.period_9_dto, 9, forecast_json)
                    self.period_9_widget.update_dataset(self.period_9_dto)

                    self.update_main(self.period_1_dto)
                
        except Exception as e:
            print(f"Refresh error: {e}")
            
    def update_dto(self, period_dto, period, forecast_json):
            temp, name, short, long, icon , start_time = self.parse_response_multi_field(forecast_json, period)
            period_dto.update(day=name, temp=temp, short=short, long=long, icon=icon, start_time=start_time)
            return period_dto
            
    def parse_response_single_field(self, response, period = 1, item_value="temperature"):
        periods = response["properties"]["periods"]
        for item in periods:
            #print("day: " , item["name"] , " Temp: " , item["temperature"], " Forecast: ", item["detailedForecast"])
            if item["number"] == period:
                value = item[item_value]
                break
        return str(value)
    
    def parse_response_multi_field(self, response, period = 1,
                                    item_1="temperature",
                                    item_2="name",
                                    item_3="shortForecast",
                                    item_4="detailedForecast",
                                    item_5="icon",
                                    item_6="startTime"):
        periods = response["properties"]["periods"]
        for item in periods:
            #print("day: " , item["name"] , " Temp: " , item["temperature"], " Forcast: ", item["detailedForecast"])
            if item["number"] == period:
                value1 = item[item_1]
                value2 = item[item_2]
                value3 = item[item_3]
                value4 = item[item_4]
                value5 = item[item_5]
                value6 = item[item_6]
                break
        return str(value1), str(value2),str(value3) ,str(value4),str(value5),str(value6)

    def update_icon(self, url):
        img_data = requests.get(f"{url}").content
        img = QImage()
        img.loadFromData(img_data)
        self.icon_label.setPixmap(QPixmap.fromImage(img))
        
    def period_clicked(self, period):
        self.update_main(self.identify_dto(period))
        
    def update_main(self, dto):
        self.main_period=dto.period
        # Main is already set for period 1 for icon and temp, do not overwrite it
        if(dto.period != str("1")): 
            self.main_temp_label.setText(dto.temp)
            self.update_icon(dto.icon)
        if(self.time_frame==Constant.DAILY): 
            self.main_period_desc.setText(dto.full_day+":")
            self.main_forecast_label.setText(dto.long_forecast)
        else:
            self.main_period_desc.setText(dto.start_time+":")
            self.main_forecast_label.setText(dto.short_forecast)
        self.set_font_size(self.main_forecast_label,len(str(self.main_forecast_label.text())) )

    def set_font_size(self, obj, size):
        if(size>200):
            obj.setFont(Constant.SMALL_FONT)
        elif(size>100):
            obj.setFont(Constant.NORMAL_FONT)
        else:
            obj.setFont(Constant.LARGE_FONT)
        
        
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