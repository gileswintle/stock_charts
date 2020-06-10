import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import datetime as dt
from datetime import timedelta
import mplfinance as mpf
import tkinter.font as tkFont
from Classes import *

# Globals
ticker_list = ['DIS', 'AMZN', 'TSLA', 'FB', 'ORCL', 'MSFT', 'AAPL', 'UBER', 'SPOT', 'SHOP', 'IBM', 'GOOGL', 'DELL', 'CRM',\
               'XRX', 'STX', 'NFLX', 'SPY']


days_default = 100
mav1_default = 20
mav2_default = 50



def candlestick_chart():
        days = int(ip_days.get())
        mav1 = int(ip_mav1.get())
        mav2 = int(ip_mav2.get())
        ticker = ip_ticker.get()

        end = dt.datetime.today()
        start = end - timedelta(days=days)

        df = web.DataReader(ticker, 'yahoo', start, end)
        # df2 = web.DataReader('SPY', 'yahoo', start, end)
        # print(df2.head())
        mpf.plot(df, type='candle', mav=(mav1, mav2), style='charles',
                title=ticker,
                ylabel='',
                ylabel_lower='',
                volume=True)
        # plt.plot(df2.index, df2['Adj Close'])

        plt.show()

def all_to_file():
        days = int(ip_days.get())
        mav1 = int(ip_mav1.get())
        mav2 = int(ip_mav2.get())

        end = dt.datetime.today()
        start = end - timedelta(days=days)

        for i, ticker in enumerate(ticker_list):
                df = web.DataReader(ticker, 'yahoo', start, end)
                mpf.plot(df, type='candle', mav=(mav1, mav2), style='charles',
                        title=ticker,
                        ylabel='',
                        ylabel_lower='',
                        volume=True, savefig=f'{ticker}.png' )


def compare_chart():
        days = int(ip_days.get())

        end = dt.datetime.today()
        start = end - timedelta(days=days)

        ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
        comp_list = pd.DataFrame()
        for i, item in enumerate(ticker_list):
                df = web.DataReader(item, 'yahoo', start, end)
                coef = 100 / df.iat[0, 5]
                comp_list[item] = df['Adj Close'] * coef
                ax1.plot(df.index, df['Adj Close'] * coef, label=item)
                ax1.legend()
        plt.show()

# # GUI STARTS HERE >>>>>>

form = tk.Tk()
form.title("Winkle's stock charter")
form.geometry ("600x230")

tab_parent = ttk.Notebook(form)

tab1 = ttk.Frame (tab_parent)


tab_parent.add(tab1, text = "Options")


# === WIDGETS FOR TAB ONE
fontStyle1 = tkFont.Font(family="Arial", size=20) #title
fontStyle2 = tkFont.Font(family="Courier", size=14) #subhead
fontStyle3 = tkFont.Font(family="Courier", size=10) #tables
fontStyle4 = tkFont.Font(family="Courier", size=12) #main body


# buttons tab 1 - row 3
compare_chart_button = tk.Button(tab1, text="Compare group", command=compare_chart, height=2, width=20)
candlestick_chart_button = tk.Button(tab1, text="Candlestick chart", command=candlestick_chart, height=2, width=20)
all_to_file_chart_button = tk.Button(tab1, text="Make files of all", command=all_to_file, height=2, width=20)

ip_ticker = AutocompleteCombobox(tab1)
ip_ticker.set_completion_list(ticker_list)
ip_ticker.focus_set()

ip_days = tk.Entry(tab1, width=8, bg = 'white', fg = 'black', justify='right', font=fontStyle3)
ip_mav1 = tk.Entry(tab1, width=8, bg = 'white', fg = 'black', justify='right', font=fontStyle3)
ip_mav2 = tk.Entry(tab1, width=8, bg = 'white', fg = 'black', justify='right', font=fontStyle3)


ip_days.insert(0, days_default)
ip_mav1.insert(0, mav1_default)
ip_mav2.insert(0, mav2_default)

lab_spacer1 = tk.Label(tab1, text='                  ', fg = 'midnight blue', bg = 'gray92', width=15, justify='left', anchor='w', font=fontStyle3)

lab_1 = tk.Label(tab1, text='Ticker', fg = 'midnight blue', bg = 'gray92', width=15, justify='left', anchor='w', font=fontStyle3)
lab_2 = tk.Label(tab1, text='Days history', fg = 'midnight blue', bg = 'gray92', width=15, justify='left', anchor='w', font=fontStyle3)
lab_3 = tk.Label(tab1, text='Moving av one', fg = 'midnight blue', bg = 'gray92', width=15, justify='left', anchor='w', font=fontStyle3)
lab_4 = tk.Label(tab1, text='Moving av two', fg = 'midnight blue', bg = 'gray92', width=15, justify='left', anchor='w', font=fontStyle3)
# === placement

lab_spacer1.grid(row=5, column=2, rowspan=1, columnspan=1, padx=5, pady=5)

ip_ticker.grid(row=2, column=1, rowspan=1, columnspan=2, padx=5, pady=5)
ip_days.grid(row=3, column=1, rowspan=1, columnspan=1, padx=5, pady=5)
ip_mav1.grid(row=4, column=1, rowspan=1, columnspan=1, padx=5, pady=5)
ip_mav2.grid(row=5, column=1, rowspan=1, columnspan=1, padx=5, pady=5)

lab_1.grid(row=2, column=0, rowspan=1, columnspan=1, padx=5, pady=5)
lab_2.grid(row=3, column=0, rowspan=1, columnspan=1, padx=5, pady=5)
lab_3.grid(row=4, column=0, rowspan=1, columnspan=1, padx=5, pady=5)
lab_4.grid(row=5, column=0, rowspan=1, columnspan=1, padx=5, pady=5)

candlestick_chart_button.grid(row=3, column=3, rowspan=1, columnspan=1, padx=5, pady=5)
compare_chart_button.grid(row=4, column=3, rowspan=1, columnspan=1, padx=5, pady=5)
all_to_file_chart_button.grid(row=5, column=3, rowspan=1, columnspan=1, padx=5, pady=5)

tab_parent.pack (expand=1, fill="both")

form.mainloop()

# GUI END >>>>>>
