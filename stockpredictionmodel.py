# -*- coding: utf-8 -*-
"""StockPredictionModel.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1P2jVt0QWsAWdU84WPy3b_eB6oAdvtDSR
"""

import pandas as pd

df = pd.read_csv('AXP.csv')
df

df = df[['Date','Close']]
df

df['Date']

import datetime

def string_to_datetime(s):
  split = s.split('-')
  year, month, day = int(split[0]), int(split[1]), int(split[2])
  return datetime.datetime(year=year, month=month, day=day)

datetime_obj = string_to_datetime('2010-10-20')
datetime_obj

df['Date'] = df['Date'].apply(string_to_datetime)
df['Date']

df

df.index = df.pop('Date')
df

import matplotlib.pyplot as plt
plt.plot(df.index, df['Close'])

import numpy as np

def df_to_windowed_df(dataframe, first_date_str, last_date_str, n=3):
  first_date = string_to_datetime(first_date_str)
  last_date  = string_to_datetime(last_date_str)

  target_date = first_date
  
  dates = []
  X, Y = [], []

  last_time = False
  while True:
    df_subset = dataframe.loc[:target_date].tail(n+1)
    
    if len(df_subset) != n+1:
      print(f'Error: Window of size {n} is too large for date {target_date}')
      return

    values = df_subset['Close'].to_numpy()
    x, y = values[:-1], values[-1]

    dates.append(target_date)
    X.append(x)
    Y.append(y)

    next_week = dataframe.loc[target_date:target_date+datetime.timedelta(days=7)]
    next_datetime_str = str(next_week.head(2).tail(1).index.values[0])
    next_date_str = next_datetime_str.split('T')[0]
    year_month_day = next_date_str.split('-')
    year, month, day = year_month_day
    next_date = datetime.datetime(day=int(day), month=int(month), year=int(year))
    
    if last_time:
      break
    
    target_date = next_date

    if target_date == last_date:
      last_time = True
    
  ret_df = pd.DataFrame({})
  ret_df['Target Date'] = dates
  
  X = np.array(X)
  for i in range(0, n):
    X[:, i]
    ret_df[f'Target-{n-i}'] = X[:, i]
  
  ret_df['Target'] = Y

  return ret_df

# Start day second time around: '2021-03-25'
windowed_df = df_to_windowed_df(df, 
                                '1972-06-06', 
                                '2023-02-28', 
                                n=3)
windowed_df

def wdf_to_date_ip_op(windowed_df):
  df_as_np = windowed_df.to_numpy()

  dates = df_as_np[:,0]
  middle_matrix = df_as_np[:,1:-1]
  x = middle_matrix.reshape((len(dates),middle_matrix.shape[1],1))
  y = df_as_np[:,-1]
  return dates, x, y

dates, x, y = wdf_to_date_ip_op(windowed_df)
dates.shape, x.shape, y.shape

# TRAIN VALIDATION AND TESTING

i_80 = int(len(dates)*.8)
i_90 = int(len(dates)*.9)

dates_train, x_train, y_train = dates[:i_80], x[:i_80], y[:i_80]
dates_val, x_val, y_val = dates[i_80:i_90], x[i_80:i_90], y[i_80:i_90]
dates_test, x_test, y_test = dates[i_90:], x[i_90:], y[i_90:]

plt.plot(dates_train, y_train)
plt.plot(dates_val, y_val)
plt.plot(dates_test, y_test)

plt.legend(['Train','Validation','Test'])
