# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 11:29:38 2016

@author: yiran.zhou
"""

import pandas as pd
import numpy as np
import sys
sys.path.append('..')
import taifook.taifook as tf
import zigzag_c as zz
import pylab as pl
import matplotlib.pyplot as plt


def plot_pivots(X, pivots):
    pl.xlim(0, len(X))
    pl.ylim(X.min()*0.99, X.max()*1.01)
    pl.plot(np.arange(len(X)), X, 'k:', alpha=0.8)
    pl.plot(np.arange(len(X))[pivots != 0], X[pivots != 0], 'k-')
    pl.scatter(np.arange(len(X))[pivots == 1], X[pivots == 1], color='g')
    pl.scatter(np.arange(len(X))[pivots == -1], X[pivots == -1], color='r')


if __name__ == '__main__':
    
    # 读入数据
    pos = pd.read_excel('INPUT COT.xls', sheetname = 'Sheet1 (2)')
    pos.set_index('Date', inplace = True)
    price = pd.read_excel('INPUT COT.xls', sheetname = 'Sheet2')
    label = price.columns[0]
    price.set_index(label, inplace = True)

#    posDate = pos.index #统计pos的日期是周二，但是release是周末
#    priceDate = posDate.shift(6, 'D') #所以下个周一（6天后）是第一个公布数据后的交易日
#    selDatePrice = price.ix[priceDate].copy()

    #取出周一的价格（和pos的时间index一致）
    monIdx = [x for x in price.index if x.weekday() == 0]
    monPrice = price.ix[monIdx]
    monPrice['W_PCT'] = monPrice['PX_OPEN'].pct_change()
    monPrice['W_PCT'] = monPrice['W_PCT'].shift(-1)
    
    #找出高低点-----------------------------------------------------------------------------------------------------------------
    ust = price.ix[:, 'PX_LAST'] 
    pivots = zz.peak_valley_pivots(ust, 0.015, -0.015)  
#    plot_pivots(ust, pivots)   
    price['pivots'] = pivots
#    price.to_excel('price with pivots.xls')
    
    #找出高低点对应的CFTC时间（顶点）
    selPeakPrice = price[price.pivots == 1]
    nextMonPeak = tf.findNearbyDate(selPeakPrice.index, 7, 'W-MON')
    prevMonPeak = tf.findNearbyDate(selPeakPrice.index, -7, 'W-MON')
    monPeak = pd.DataFrame()
    monPeak['nextMon'] = nextMonPeak
    monPeak['prevMon'] = prevMonPeak
#    monPeak.to_excel('peak Mon.xls')
    
    #找出高低点对应的CFTC时间（底点）
    selValleyPrice = price[price.pivots == -1]
    nextMonValley = tf.findNearbyDate(selValleyPrice.index, 7, 'W-MON')
    prevMonValley = tf.findNearbyDate(selValleyPrice.index, -7, 'W-MON')
    monValley = pd.DataFrame()
    monValley['nextMon'] = nextMonValley
    monValley['prevMon'] = prevMonValley
#    monValley.to_excel('valley Mon.xls')
    
    # 找出高低点的时间
#    peakIdx = pd.DatetimeIndex(monPeak['prevMon'])
#    valleyIdx = pd.DatetimeIndex(monValley['prevMon'])    
    peakIdx = pd.DatetimeIndex(monPeak['nextMon'])
    valleyIdx = pd.DatetimeIndex(monValley['nextMon'])  
  
    # 调整pos数据（标准化:占open interest的比）----------------------------------------------------------------------------------------------------------  
    strPCT = '_PCT'
    strCHG = '_CHG'  
    pos = pos.ix[600:, :]
    posPCT = pos.ix[:,:-1].copy()
    posPCT.columns = pos.columns[:-1] + strPCT
    i = 0    
    while i < len(posPCT.columns):
        posPCT.ix[:, i] = pos.ix[:, i] / pos.ix[:, -1]  # 占Open int比
        i += 1       
    posCHG = posPCT.diff(1).dropna()  # 每周变化
    cols = [x.replace(strPCT, strCHG) for x in list(posCHG.columns)]
    posCHG.columns = cols
    posPCT.index = posPCT.index.shift(6, 'D') #把日期index调整为下周一，原来是周二，和高低点日期一致
    posCHG.index = posCHG.index.shift(6, 'D')
       
    # pos在高低点的绝对值
    posPCT_peak = posPCT.ix[peakIdx].copy().dropna()
    posPCT_valley = posPCT.ix[valleyIdx].copy().dropna()   
    
    # pos在高低点的变化值
    posCHG_peak = posCHG.ix[peakIdx].copy().dropna()
    posCHG_valley = posCHG.ix[valleyIdx].copy().dropna()
    
    # pos在高低点的绝对值的Zscore
    span = -100
    strZS = '_SZ'
    colNames = list(posPCT.columns)
    newColNames = [x + strZS for x in colNames]
    funcList = [tf.zscore] * len(posPCT.columns)    
    posPCT_ZS = tf.rolling(posPCT.copy(), span, funcList, colNames, newColNames)\
    .ix[:, len(posPCT.columns):-1 ].dropna()    
    posPCT_peak_ZS = posPCT_ZS.ix[peakIdx].copy().dropna()
    posPCT_valley_ZS = posPCT_ZS.ix[valleyIdx].copy().dropna()
    
    # pos在高低点的变化值的Zscore
    span2 = -25
    strZS = '_SZ'
    colNames = list(posCHG.columns)
    newColNames = [x + strZS for x in colNames]
    funcList = [tf.zscore] * len(posCHG.columns)    
    posCHG_ZS = tf.rolling(posCHG.copy(), span2, funcList, colNames, newColNames)\
    .ix[:, len(posCHG.columns):-1 ].dropna()    
    posCHG_peak_ZS = posCHG_ZS.ix[peakIdx].copy().dropna()
    posCHG_valley_ZS = posCHG_ZS.ix[valleyIdx].copy().dropna()
    
    # 高低点的统计数据----------------------------------------------------------------------------------------------------------
    des = posPCT.describe()
    peakDes = posPCT_peak.describe()
    valleyDes = posPCT_valley.describe()
    
    # 合并pos和价格
    monPrice['pivots'] = 0
    monPrice.ix[peakIdx, 'pivots'] = 1
    monPrice.ix[valleyIdx, 'pivots'] = -1
    posPCT_M = pd.concat([monPrice, posPCT], axis = 1, join = 'inner')
    posCHG_M = pd.concat([monPrice, posCHG], axis = 1, join = 'inner')
    posPCT_ZS_M = pd.concat([monPrice, posPCT_ZS], axis = 1, join = 'inner')
    
#    posPCT_M.to_excel('posPCT_M.xls')
#    posCHG_M.to_excel('posCHG_M.xls')
#    posPCT_ZS_M.to_excel('posPCT_ZS_M.xls')
    

#    # 画每列的直方分布图(Open interest pct)----------------------------------------------------------------------------------------------------------
#    i = 0 
#    figList = []
#    while i < len(posPCT.columns):
#        figList.append(plt.figure())
#        plt.title(posPCT.columns[i]  + ' ' + str(span))        
#        posPCT_peak.ix[:,i].hist(bins = 50, alpha = 0.5, color = 'r')
#        posPCT_valley.ix[:,i].hist(bins = 50, alpha = 0.5, color = 'g')
#        posPCT.ix[:,i].hist(bins = 50, alpha = 0.5, color = 'b')
#        i += 1

       
#    # 画每列的直方分布图(Open interest pct change)
#    i = 0 
#    figList = []
#    while i < len(posCHG.columns):
#        figList.append(plt.figure())
#        plt.title(posCHG.columns[i]  + ' ' + str(span2))        
#        posCHG_peak.ix[:,i].hist(bins = 50, alpha = 0.5, color = 'r')
#        posCHG_valley.ix[:,i].hist(bins = 50, alpha = 0.5, color = 'g')
#        posCHG.ix[:,i].hist(bins = 50, alpha = 0.5, color = 'b')
#        i += 1
    

    # 画每列的直方分布图(Open interest pct Zscore)
    i = 0 
    figList = []
    while i < len(posPCT_ZS.columns):
        figList.append(plt.figure())
        plt.title(posPCT_ZS.columns[i] + ' ' + str(span))        
        posPCT_peak_ZS.ix[:,i].hist(bins = 50, alpha = 0.5, color = 'r')
        posPCT_valley_ZS.ix[:,i].hist(bins = 50, alpha = 0.5, color = 'g')
        posPCT_ZS.ix[:,i].hist(bins = 50, alpha = 0.5, color = 'b')
        i += 1

#    # 画每列的直方分布图(Open interest pct Zscore)
#    i = 0 
#    figList = []
#    while i < len(posCHG_ZS.columns):
#        figList.append(plt.figure())
#        plt.title(posCHG_ZS.columns[i] + ' ' + str(span2))        
#        posCHG_peak_ZS.ix[:,i].hist(bins = 50, alpha = 0.5, color = 'r')
#        posCHG_valley_ZS.ix[:,i].hist(bins = 50, alpha = 0.5, color = 'g')
#        posCHG_ZS.ix[:,i].hist(bins = 50, alpha = 0.5, color = 'b')
#        i += 1
    
#    pivots = zz.peak_valley_pivots(ust, 0.03, -0.03)
#    plot_pivots(ust, pivots)
    