from PyQt5.QtWidgets import QApplication,QWidget, QLabel, QVBoxLayout, QPushButton, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
import sys

class WeatherWidget(QWidget):
    clickedValue = QtCore.pyqtSignal(str)
    period = '0'
    dataset = None
    
    def __init__(self):
        super().__init__()
        
        self.mainLayout = QVBoxLayout()
        
        button = QPushButton()
        button.setMaximumHeight(200)
        button.setMinimumHeight(50)
        button.setMaximumWidth(200)
        button.setMinimumWidth(50)
        button.setStyleSheet("border: none;")
        
        inner_layout = QVBoxLayout(button)
        self.out_desc = QLabel("Day")
        self.out_desc.setWordWrap(True) 
        self.out_temp = QLabel("--°F")
        self.out_temp.setFont(QFont('Arial', 10))
        self.out_forecast = QLabel("Forecast")
        self.out_forecast.setWordWrap(True)
        self.out_forecast.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        inner_layout.addWidget(self.out_desc)
        inner_layout.addWidget(self.out_temp)
        inner_layout.addWidget(self.out_forecast)
        
        self.mainLayout.addWidget(button)
        
        button.clicked.connect(self.on_click)
        
    def get_layout(self):
        return self.mainLayout
    
    def set_layout(self):
        self.setLayout(self.mainLayout)
    
    def update_dataset(self, dataset):
        self.dataset = dataset
        self.period = dataset.period
        if(dataset.day==''):
            self.out_desc.setText(dataset.start_time)
        else:    
            self.out_desc.setText(dataset.day)
        self.out_temp.setText(dataset.temp)
        self.out_forecast.setText(dataset.short_forecast)
        
    def on_click(self):
        emiting = self.period
        self.clickedValue.emit(emiting)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WeatherWidget()
    window.set_layout()
    window.show()
    sys.exit(app.exec_())