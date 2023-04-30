import cv2
import os
import numpy as np
import pandas as pd
import time
import plotly.graph_objects as go
from PIL import Image

class Trader:
    def __init__(self):
        self.window = 50
        self.current_i = 0

    def isAscendingTriangle(self, data):
        high_prices = data['High'][-self.window:]
        low_prices = data['Low'][-self.window:]
        
        resistance_level = np.max(high_prices)
        
        support_slope, _ = np.polyfit(range(self.window), low_prices, 1)
        
        if support_slope > 0.5:
            return True, resistance_level, support_slope
        else:
            return False, None, None

    def fetch_data(self):
        file_path = "D:/pytorch/training_data/"
        files = os.listdir(file_path)
        data = pd.read_csv(file_path + files[0])
        data = data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        return data

    def get_plot_data(self, data, resistance, slope):
        fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                                             open=data['Open'],
                                             high=data['High'],
                                             low=data['Low'],
                                             close=data['Close'])])

        if resistance is not None and slope is not None:
            date_range = data['Date'][-self.window:]
            low_prices = data['Low'][-self.window:]
            support_line = low_prices.iloc[0] + np.arange(len(date_range)) * slope

            fig.add_trace(go.Scatter(x=date_range, y=support_line, mode='lines', name='Support Line'))
            fig.add_trace(go.Scatter(x=[data['Date'].iloc[-self.window], data['Date'].iloc[-1]], y=[resistance, resistance], mode='lines', name='Resistance Level'))

        fig.update_layout(xaxis_rangeslider_visible=False)
        fig.write_image("temp_plot.png")

    def next_window(self):
        self.data = self.fetch_data()

        if self.current_i + self.window >= len(self.data):
            print("All data processed, starting over...")
            self.current_i = 0

        window_data = self.data.iloc[self.current_i:self.current_i+self.window]
        is_forming, resistance, slope = self.isAscendingTriangle(window_data)

        if is_forming:
            print(f"Ascending triangle pattern detected.")
        else:
            print(f"No ascending triangle pattern detected.")

        self.current_i += 1
        return self.get_plot_data(window_data, resistance, slope)

    def run(self):
        while True:
            self.next_window()
            img = cv2.imread('temp_plot.png')
            cv2.imshow('Trading Chart', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
                cv2.destroyAllWindows()
                break
            time.sleep(0.1)

if __name__ == "__main__":
    trader = Trader()
    trader.run()
