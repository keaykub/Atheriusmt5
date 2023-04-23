import MetaTrader5 as mt5
from datetime import datetime, timedelta
import datetime as dt
import time
import pandas as pd
import requests
from flask import Flask, request, abort
import requests
import json
from PIL import ImageGrab

#----------------------#
#data.loc[0:10] เรียกข้อมูล 10 ชุด
#data.loc[0:10].open เรียกข้อมูล 10 ชุด ราคาเปิดแท่งเทียน
#----------------------#
#สร้างโดย    keaykub 
#input      คู่เงิน
#return     bid(ราคาบน)
#----------------------#
def getBidLast(currency):  
    priceCurrency = mt5.symbol_info_tick(currency);
    priceCurrency = priceCurrency.bid;
    return priceCurrency;
    
#----------------------#
#สร้างโดย    keaykub 
#input      คู่เงิน
#return     ask(ราคาล่าง)
#----------------------#
def getAskLast(currency):
    priceCurrency = mt5.symbol_info_tick(currency);
    priceCurrency = priceCurrency.ask;
    return priceCurrency;
    
#----------------------#
#สร้างโดย    keaykub 
#namefunc   ดึงราคาแท่งเทียน 1 วันจากราคาปัจจุบัน 
#input      (CURRENCY, TIMEFRAME, date) ex.('AUDUSD', mt5.TIMEFRAME_M30, [2023,3,15])
#return     ราคาเปิด,ปิด แท่งเทียนที่ต้องการเริ่มวันที่กำหนด - เวลาปัจจุบัน
#detail     -
#----------------------#
def getPriceV1(currency, timeframe, date):
    dateYear = date[0];
    dateMonth = date[1];
    dateDay = date[2];
    now = datetime.now()
    one_hour_later = now + timedelta(hours=3)
    ohlc_data = pd.DataFrame(mt5.copy_rates_range(currency, timeframe, datetime(dateYear,dateMonth,dateDay,hour=7),  one_hour_later))
    ohlc_data['time'] = pd.to_datetime(ohlc_data['time'], unit='s');
    return ohlc_data;
    
#----------------------#
#สร้างโดย    keaykub 
#namefunc   ช่วงราคาที่ต่ำที่สุดของแท่งเทียนใน 1 วัน
#input      (data) ex.(csTwo.loc[0:10].high)
#return     ราคาที่ต่ำที่สุด
#detail     เช่น high ที่แท่งเทียนลงไปต่ำสุดใน 1 วันคือเท่าไร [high,low,open,close]
#----------------------#
def getTypeMin(datas):
    dataSetHigh = [];
    for data in datas:
        dataSetHigh.append(data);
    
    result = min(dataSetHigh);
    return result;

#สร้างโดย    keaykub 
#input      message
#return     status
#detail     ส่ง linenotify
#----------------------#
def send_line_notify(message):
    if (message == 'buy'):
        message = "AUDUSD [BUY ALERT]"
    elif (message == 'sell'):
        message = "AUDUSD [SELL ALERT]"
    elif (message == 'start'):
        message = "ระบบแจ้งสัญญาณเข้าเทรดคู่เงิน กำลังทำงาน!!!"
    elif (message == "alert"):
        message = ""
    token = 'TkUFU9vJOdIB5AWigKIJWhByNK8F9cNhkWTi2obtaC5';
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {'message': message}
    r = requests.post('https://notify-api.line.me/api/notify', headers=headers, params=payload)
    
    return r.status_code