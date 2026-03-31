import sys,requests 
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

import Constant
import Secrets
from WeatherDto import WeatherDto
from WeatherWidget import WeatherWidget

# Location could be loaded from a config class in the future.
WEATHER_URL_HOURLY = f"https://api.weather.gov/gridpoints/{Secrets.LOCATION}/forecast/hourly"
WEATHER_URL_FORECAST = f"https://api.weather.gov/gridpoints/{Secrets.LOCATION}/forecast"
HEADERS = Secrets.HEADERS
PICO_URL = f"http://{Secrets.PICO_IP}:80/data"

class WeatherUI(QWidget):
    def __init__(self):
        super().__init__()
        self.main_period = "1"
        self.period_dtos = [WeatherDto(str(index)) for index in range(1, 10)]
        self.period_widgets = []
        
        self.init_Weather_UI()
        
        # Refresh timer: 30 min (1800000)
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(1800000)

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
        
        # Location selection can later be switched to a dropdown.
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

        self.indoor_label_desc = QLabel("Indoors :")
        self.indoor_label_desc.setFont(Constant.LARGE_FONT)
        self.indoor_temp = QLabel("Connecting...")
        self.indoor_temp.setFont(Constant.XL_FONT_BOLD)
        self.indoor_temp.setStyleSheet(Constant.LIGHT_BLUE)
        self.indoor_humidity = QLabel("...")
        self.indoor_humidity.setFont(Constant.NORMAL_FONT)
        self.indoor_humidity.setStyleSheet(Constant.LIGHT_BLUE)
        self.indoor_air_qlty = QLabel("...")
        self.indoor_air_qlty.setFont(Constant.NORMAL_FONT)
        self.indoor_air_qlty.setStyleSheet(Constant.LIGHT_BLUE)
        
        lower_box = QHBoxLayout()

        self.period_widgets = []
        for period_dto in self.period_dtos[1:]:
            period_widget = WeatherWidget()
            period_widget.clickedValue.connect(self.period_clicked)
            period_widget.update_dataset(period_dto)
            self.period_widgets.append(period_widget)
            lower_box.addLayout(period_widget.get_layout())
        
        self.icon_label = QLabel()
    
        vbox = QVBoxLayout()
        upper_box= QHBoxLayout()
        vbox_top_left = QVBoxLayout()
        vbox_top_right = QVBoxLayout()


        vbox_top_left.addWidget(self.btn_location, alignment=Qt.AlignTop | Qt.AlignLeft)
        vbox_top_left.addWidget(self.btn_time_frame, alignment=Qt.AlignTop | Qt.AlignLeft)
        vbox_top_right.addWidget(quit_button, alignment=Qt.AlignTop | Qt.AlignRight)
        vbox_top_right.addWidget(self.btn_toggle_size, alignment=Qt.AlignTop | Qt.AlignRight)
        upper_box.addLayout(vbox_top_left)
        upper_box.addLayout(vbox_top_right)
        vbox.addLayout(upper_box)
        
        inner_middle_layout = QHBoxLayout()

        inner_main_layout = QVBoxLayout()
        inner_main_layout.addWidget(self.main_period_desc, alignment=Qt.AlignCenter)
        inner_main_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        inner_main_layout.addWidget(self.main_temp_label, alignment=Qt.AlignCenter)

        inner_middle_layout.addLayout(inner_main_layout)
             
        if(Constant.LOCAL_TEMP_ON):
            inner_local_sensor_layout = QVBoxLayout()
            inner_local_sensor_layout.addWidget(self.indoor_label_desc)
            inner_local_sensor_layout.addWidget(self.indoor_temp)
            inner_local_sensor_layout.addWidget(self.indoor_humidity)
            inner_local_sensor_layout.addWidget(self.indoor_air_qlty)
            inner_middle_layout.addLayout(inner_local_sensor_layout)

        vbox.addLayout(inner_middle_layout)

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
                
    def on_btn_toggle_size(self, full_screen):
        self.toggle_full_screen(full_screen)

    def toggle_full_screen(self, full_screen):
        if full_screen:
            self.showNormal()
            self.btn_toggle_size.setText('Max')
        else:
            self.showFullScreen()
            self.btn_toggle_size.setText('Min')
        self.refresh()

    # Currently only a refresh action; multi-location support can be added later.
    def on_btn_location(self, _checked):
        self.main_period_desc.setText("Current :")
        self.toggle_location()

    def toggle_location(self):
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
            self.update_current_conditions()
            self.update_forecast_periods()
            if Constant.LOCAL_TEMP_ON:
                self.update_local_sensor_data()
        except Exception as e:
            print(f"Refresh error: {e}")
            self.main_period_desc.setText("Error fetching data")
            

    def update_current_conditions(self):
        response = requests.get(WEATHER_URL_HOURLY, headers=HEADERS, timeout=Constant.REQUEST_TIMEOUT_SECONDS)
        if response.status_code != 200:
            return

        forecast_json = response.json()
        temp = self.parse_response_single_field(forecast_json)
        self.main_temp_label.setText(f"{temp} °F")
        icon = self.parse_response_single_field(forecast_json, item_value="icon")
        self.update_icon(icon)

    def update_forecast_periods(self):
        forecast_url = WEATHER_URL_FORECAST if self.time_frame == Constant.DAILY else WEATHER_URL_HOURLY
        response = requests.get(forecast_url, headers=HEADERS, timeout=Constant.REQUEST_TIMEOUT_SECONDS)
        if response.status_code != 200 or str(self.main_period) != "1":
            return

        forecast_json = response.json()
        for index, period_dto in enumerate(self.period_dtos, start=1):
            updated_dto = self.update_dto(period_dto, index, forecast_json)
            self.period_dtos[index - 1] = updated_dto
            if index > 1:
                self.period_widgets[index - 2].update_dataset(updated_dto)

        self.update_main(self.period_dtos[0])

    def update_local_sensor_data(self):
        try:
            local_temp_response = requests.get(PICO_URL, timeout=Constant.REQUEST_TIMEOUT_SECONDS)
            local_temp_response.raise_for_status()
            local_temp_json = local_temp_response.json()
            self.indoor_label_desc.setText("Indoors :")
            self.indoor_temp.setText(f"{local_temp_json['Temp']} °F")
            self.indoor_humidity.setText(f"Humidity: {local_temp_json['Humidity']} %")
            self.determine_air_qty(local_temp_json['co2_ppm'], "CO2", 850, 1800)
        except requests.RequestException as exc:
            print(f"Local sensor update error: {exc}")
            self.indoor_label_desc.setText("Error connecting...")
            return

    def determine_air_qty(self, ppm, gas, normal,  high):
        if ppm > high:
            self.indoor_air_qlty.setText(gas + " ELEVATED")         
            self.indoor_air_qlty.setStyleSheet(Constant.VIVID_RED)
        elif ppm > normal:
            self.indoor_air_qlty.setText(gas + " HIGH")
            self.indoor_air_qlty.setStyleSheet(Constant.YELLOW)
        else:
            self.indoor_air_qlty.setText(gas + " Normal")
            self.indoor_air_qlty.setStyleSheet(Constant.LIGHT_BLUE)
            
    def update_dto(self, period_dto, period, forecast_json):
            temp, name, short, long, icon , start_time = self.parse_response_multi_field(forecast_json, period)
            period_dto.update(day=name, temp=temp, short=short, long=long, icon=icon, start_time=start_time)
            return period_dto
            
    def parse_response_single_field(self, response, period=1, item_value="temperature"):
        periods = response.get("properties", {}).get("periods", [])
        matched_period = next((item for item in periods if item.get("number") == period), {})
        return str(matched_period.get(item_value, ""))

    def parse_response_multi_field(
        self,
        response,
        period=1,
        item_1="temperature",
        item_2="name",
        item_3="shortForecast",
        item_4="detailedForecast",
        item_5="icon",
        item_6="startTime",
    ):
        periods = response.get("properties", {}).get("periods", [])
        matched_period = next((item for item in periods if item.get("number") == period), {})
        return (
            str(matched_period.get(item_1, "")),
            str(matched_period.get(item_2, "")),
            str(matched_period.get(item_3, "")),
            str(matched_period.get(item_4, "")),
            str(matched_period.get(item_5, "")),
            str(matched_period.get(item_6, "")),
        )

    def update_icon(self, url):
        try:
            img_data = requests.get(url, timeout=Constant.REQUEST_TIMEOUT_SECONDS).content
        except requests.RequestException as exc:
            print(f"Icon update error: {exc}")
            return

        img = QImage()
        if img.loadFromData(img_data):
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
        for period_dto in self.period_dtos:
            if period_dto.period == period:
                return period_dto
        return self.period_dtos[0]

def main():
    app = QApplication(sys.argv)
    app.main_window = WeatherUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()