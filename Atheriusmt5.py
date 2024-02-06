import MetaTrader5 as mt5
from datetime import datetime, timedelta
import time
import pandas as pd
import requests
import requests
from finta import TA
import numpy as np
import matplotlib.pyplot as plt
#from mpl_finance import candlestick_ohlc
from matplotlib import dates as mpl_dates
#----------------------#
#data.loc[0:10] เรียกข้อมูล 10 ชุด
#data.loc[0:10].open เรียกข้อมูล 10 ชุด ราคาเปิดแท่งเทียน
#----------------------#
#สร้างโดย    keaykub 
#input      คู่เงิน
#return     bid(ราคาบน)
#----------------------#
def getBidLast(currency):  
    priceCurrency = mt5.symbol_info_tick(currency)
    priceCurrency = priceCurrency.bid
    return priceCurrency
#----------------------#
#สร้างโดย    keaykub 
#input      คู่เงิน
#return     ask(ราคาล่าง)
#----------------------#
def getAskLast(currency):
    priceCurrency = mt5.symbol_info_tick(currency)
    priceCurrency = priceCurrency.ask
    return priceCurrency
    
#----------------------#
#สร้างโดย    keaykub 
#namefunc   ดึงราคาแท่งเทียน 1 วันจากราคาปัจจุบัน 
#input      (CURRENCY, TIMEFRAME, date) ex.('AUDUSD', mt5.TIMEFRAME_M30, [2023,3,15])
#return     ราคาเปิด,ปิด แท่งเทียนที่ต้องการเริ่มวันที่กำหนด - เวลาปัจจุบัน
#detail     -
#----------------------#
def getPriceV1(currency, timeframe, date):
    dateYear = date[0]
    dateMonth = date[1]
    dateDay = date[2]
    now = datetime.now()
    one_hour_later = now + timedelta(hours=3)
    ohlc_data = pd.DataFrame(mt5.copy_rates_range(currency, timeframe, datetime(dateYear,dateMonth,dateDay,hour=7),  one_hour_later))
    ohlc_data['time'] = pd.to_datetime(ohlc_data['time'], unit='s')
    return ohlc_data

#----------------------#
#สร้างโดย    keaykub 
#namefunc   ดึงราคาแท่งเทียน 1 วันจากราคาปัจจุบัน 
#input      (CURRENCY, TIMEFRAME, date) ex.('AUDUSD', mt5.TIMEFRAME_M30, [2023,3,15])
#return     ราคาเปิด,ปิด แท่งเทียนที่ต้องการเริ่มจากวันที่ปัจจุบัน
#detail     -
#----------------------#
def getPriceV2(currency, timeframe):
    now = datetime.now()
    datemidnight = datetime.now()
    midnight = datemidnight.replace(hour=7)
    one_hour_later = now + timedelta(hours=3)
    ohlc_data = pd.DataFrame(mt5.copy_rates_range(currency, timeframe, midnight,  one_hour_later))
    ohlc_data['time'] = pd.to_datetime(ohlc_data['time'], unit='s')
    return ohlc_data
    
#----------------------#
#สร้างโดย    keaykub 
#namefunc   
#input      
#return     
#detail     -
#----------------------#
def getPriceV3(currency, timeframe, day):
    now = datetime.now()
    one_day_ago = datetime.now() - timedelta(days=day)
    midnight = one_day_ago.replace(hour=7)
    one_hour_later = now + timedelta(hours=3)
    ohlc_data = pd.DataFrame(mt5.copy_rates_range(currency, timeframe, midnight,  one_hour_later))
    ohlc_data['time'] = pd.to_datetime(ohlc_data['time'], unit='s')
    return ohlc_data

#----------------------#
#สร้างโดย    keaykub 
#namefunc   
#input      
#return     
#detail     -
#----------------------#
def getPriceV4(currency, timeframe, num):
    now = datetime.now()
    numberTime = 0
    if timeframe == mt5.TIMEFRAME_M1:
        numberTime = num
    elif timeframe == mt5.TIMEFRAME_M5:
        numberTime = num*5
    elif timeframe == mt5.TIMEFRAME_M15:
        numberTime = num*15
    elif timeframe == mt5.TIMEFRAME_M30:
        numberTime = num*30
    elif timeframe == mt5.TIMEFRAME_H1:
        numberTime = num*60
    elif timeframe == mt5.TIMEFRAME_H4:
        numberTime = num*240
    elif timeframe == mt5.TIMEFRAME_D1:
        numberTime = num*1440
    
    timeSetNow = datetime.now()
    timeSetNow = timeSetNow + timedelta(hours=2)
    now = now + timedelta(hours=3)
    pastTime = timeSetNow - timedelta(minutes=numberTime)
    ohlc_data = pd.DataFrame(mt5.copy_rates_range(currency, timeframe, pastTime,  now))
    ohlc_data['time'] = pd.to_datetime(ohlc_data['time'], unit='s')
    return ohlc_data;   
#----------------------#
#สร้างโดย    keaykub 
#namefunc   
#input      
#return     
#detail     -
#----------------------#
def getPriceV5(currency, timeframe, num):
    now = datetime.now()
    numberTime = 0
    if timeframe == mt5.TIMEFRAME_M1:
        numberTime = num
    elif timeframe == mt5.TIMEFRAME_M5:
        numberTime = num*5
    elif timeframe == mt5.TIMEFRAME_M15:
        numberTime = num*15
    elif timeframe == mt5.TIMEFRAME_M30:
        numberTime = num*30
    elif timeframe == mt5.TIMEFRAME_H1:
        numberTime = num*60
    elif timeframe == mt5.TIMEFRAME_H4:
        numberTime = num*240
    elif timeframe == mt5.TIMEFRAME_D1:
        numberTime = num*1440

    timeSetNow = datetime.now()
    if timeSetNow.weekday() == 5 or timeSetNow.weekday() == 6:  #เสาร์, อาทิตย์
        start_time = datetime(now.year, now.month, now.day-1, 23, 59, 0)
        start_time = start_time + timedelta(hours=7)
        pastTime = start_time - timedelta(minutes=numberTime)
        ohlc_data = pd.DataFrame(mt5.copy_rates_range(currency, timeframe, pastTime,  start_time))
        ohlc_data['time'] = pd.to_datetime(ohlc_data['time'], unit='s')
        return ohlc_data
    else: #วันธรรมดาแบบปรกติ
        timeSetNow = datetime.now()
        timeSetNow = timeSetNow + timedelta(hours=2)
        now = now + timedelta(hours=3)
        pastTime = timeSetNow - timedelta(minutes=numberTime)
        ohlc_data = pd.DataFrame(mt5.copy_rates_range(currency, timeframe, pastTime,  now))
        ohlc_data['time'] = pd.to_datetime(ohlc_data['time'], unit='s')

        return ohlc_data
#----------------------#
#สร้างโดย    keaykub 
#namefunc   ดึงราคาแท่งเทียนจากราคาปัจจุบัน แบบกำหนด tf และจำนวนได้
#input      symbol = คู่เงิน , n = จำนวนแท่งเทียน , timeframe = TF ที่ต้องการเช่น M30, H1, H4
#return     
#detail     -
#----------------------#
def getData(symbol, n ,timeframe):
    utc_from = datetime.now()
    utc_from = utc_from + timedelta(hours=3)
    rates = mt5.copy_rates_from(symbol, timeframe, utc_from, n)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s', dayfirst=True)

    # เรียงลำดับ index จากมากไปน้อย
    """ rates_frame = rates_frame.sort_index(ascending=False) """

    # reset_index เพื่อเรียกคืน index เป็น column และตั้ง index ใหม่
    """ rates_frame = rates_frame.reset_index(drop=True) """

    return rates_frame



#----------------------#
#สร้างโดย    keaykub 
#namefunc   ช่วงราคาที่ต่ำที่สุดของแท่งเทียนใน 1 วัน
#input      (data) ex.(csTwo.loc[0:10].high)
#return     ราคาที่ต่ำที่สุด
#detail     เช่น high ที่แท่งเทียนลงไปต่ำสุดใน 1 วันคือเท่าไร [high,low,open,close]
#----------------------#
def getTypeMin(datas):
    dataSetHigh = []
    for data in datas:
        dataSetHigh.append(data)
    
    result = min(dataSetHigh)
    return result

#----------------------#
#สร้างโดย    keaykub 
#namefunc   ช่วงราคาที่ต่ำที่สุดของแท่งเทียนใน 1 วัน
#input      (data) ex.(csTwo.loc[0:10].high)
#return     ราคาที่ต่ำที่สุด
#detail     เช่น high ที่แท่งเทียนลงไปต่ำสุดใน 1 วันคือเท่าไร [high,low,open,close]
#----------------------#
def getTypeMax(datas):
    dataSetHigh = []
    for data in datas:
        dataSetHigh.append(data)
    
    result = max(dataSetHigh)
    return result

#----------------------#
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
    elif (message == "notfound"):
        message = "ยังไม่ถึงราคาที่กำหนด"
    token = ''
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {'message': message}
    r = requests.post('https://notify-api.line.me/api/notify', headers=headers, params=payload)
    
    return r.status_code

#----------------------#
#สร้างโดย    keaykub 
#input      numOrders // numOrders = ออเดอร์ทั้งหมดที่ pending
#return     ticket ปัจจุบันทั้งหมด (array)
#detail     ใช้สำหรับเรียกดู ticket ทั้งหมดที่กำลัง pending อยู่(เฉพาะ )
#----------------------#
def getTicketNow(numOrders):
    orderData = mt5.orders_get()[0:numOrders]
    global orderGetAll
    orderGetAll = []
    for order in orderData:
        orderGetAll.append(order.ticket)
    
    return orderGetAll

#----------------------#
#สร้างโดย    keaykub 
#input      data จาก orders_get() 
#return     เวลาปัจจุบันของประเทศไทย
#detail     เปลี่ยนเวลาจากเซิฟเวอร์หลักเป็นเวลาของไทย EX. 2023-04-25 15:54:01
#----------------------#
def convertTimeCurrent(datas):
    datetime = datas.time_setup
    datetime = pd.to_datetime(datetime, unit='s');
    datetime = datetime + timedelta(hours=4)
    
    return datetime
    
#สร้างโดย    keaykub   
#input      
#return     
#detail     
#----------------------#
def convertList(datas, type):
    returndata = ''
    if type == 'open':
        returndata = datas.loc[0:].open.tolist()
    elif type == 'close':
        returndata = datas.loc[0:].close.tolist()
    elif type == 'low':
        returndata = datas.loc[0:].low.tolist()
    elif type == 'high':
        returndata = datas.loc[0:].high.tolist()
    elif type == 'spread':
        returndata = datas.loc[0:].spread.tolist()
    elif type == 'tick_volume':
        returndata = datas.loc[0:].tick_volume.tolist()

    return returndata

#สร้างโดย    keaykub 
#input      
#return     
#detail     
#----------------------#
def lastCandle(datas):
    count = len(datas)
    position = count-1
    data = datas[position]
    
    return data

#สร้างโดย    keaykub 
#input      
#return     
#detail     
#----------------------#
def lastCandleV2(datas, position):
    count = len(datas)
    position = count-position 
    data = datas[position]
    return data

#สร้างโดย    keaykub 
#descrip    แปลงให้เป็นรูปแบบที่ง่ายต่อการนำไปใช้งานเช่นใช้ควบคู่กับการทำ indicator
#input      
#return     
#detail     
#----------------------#
def convertDataCandleToPd(datas):
    close_values = convertList(datas,'close')
    open_values = convertList(datas,'open')
    high_values = convertList(datas,'high')
    low_values = convertList(datas,'low')
    df = pd.DataFrame({
        'high': high_values,
        'open': open_values,
        'low': low_values,
        'close': close_values
    })

    return df

#สร้างโดย    keaykub 
#input      
#return     
#detail     
#----------------------#
def requestdealV1(currency, lot, typedeal, sl=None, tp=None): 
    if typedeal == 'sell':
        typedeal = mt5.ORDER_TYPE_SELL
        sl = mt5.symbol_info_tick(currency).ask + 0.00150
        tp = mt5.symbol_info_tick(currency).ask - 0.00150
    elif typedeal == 'buy':
        typedeal = mt5.ORDER_TYPE_BUY
        sl = mt5.symbol_info_tick(currency).ask - 0.00150
        tp = mt5.symbol_info_tick(currency).ask + 0.00150
        
    request ={
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": currency,
        "volume": lot,
        "type": typedeal,
        "price": mt5.symbol_info_tick(currency).ask,
        "sl": sl,
        "tp": tp,
        "deviation": 20,
        "magic": 234000,
        "comment": "send",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    order = mt5.order_send(request)
    return order

#----------------------#
#สร้างโดย    keaykub 
#namefunc   หาราคาทั้งหมดของ 1 แท่งเทียน
#descrip    -
#input      datas = ข้อมูลแท่งเทียนทั้งหมด, numAll = จำนวนแท่งเทียนทั้งหมด, position = แท่งที่ต้องการ 1 คือแท่งล่าสุด, All = ท้งหมด
#return     Open/Close/Low/High/  หรือ ALL
#detail     
#----------------------#
def findPriceCandleV1(datas, numAll, position, allData=None):
    if allData is None:
        positionCandle = numAll-position
        dataOpen = datas.loc[positionCandle].open
        dataClose = datas.loc[positionCandle].close
        dataLow = datas.loc[positionCandle].low
        dataHigh = datas.loc[positionCandle].high
        dataAll = {'Open': dataOpen, 'Close': dataClose, 'Low': dataLow, 'High': dataHigh}
    else:
        positionCandle = numAll-position
        dataOpen = datas.loc[positionCandle].open
        dataClose = datas.loc[positionCandle].close
        dataLow = datas.loc[positionCandle].low
        dataHigh = datas.loc[positionCandle].high
        dataTick_volume = datas.loc[positionCandle].tick_volume
        dataSpread = datas.loc[positionCandle].spread
        dataReal_volume = datas.loc[positionCandle].real_volume
        dataAll = {'Open': dataOpen, 'Close': dataClose, 'Low': dataLow, 'High': dataHigh, 'Tick': dataTick_volume, 'Spread': dataSpread
                   , 'Volume': dataReal_volume}
    
    return dataAll

#----------------------#
#สร้างโดย    keaykub 
#namefunc   หาราคาทั้งหมดของ 1 แท่งเทียน
#descrip    -
#input      datas = ข้อมูลแท่งเทียนทั้งหมด, numAll = จำนวนแท่งเทียนทั้งหมด, position = แท่งที่ต้องการ 1 คือแท่งล่าสุด, All = ท้งหมด
#return     Open/Close/Low/High/  หรือ ALL
#detail     -
#----------------------#
def findPriceCandleClose(datas, numAll):
    positionCandle = numAll - 1
    dataReturn = datas.loc[0:positionCandle].close.tolist()
    dataAll = pd.DataFrame({'close': dataReturn})
    return dataAll
