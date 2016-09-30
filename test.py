# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 19:23:48 2016

@author: yiran.zhou
"""

#des = posPCT_ZS.describe()
#peakDes = posPCT_peak_ZS.describe()
#valleyDes = posPCT_valley_ZS.describe()
#
#i = 0 
#figList = []
#while i < len(posPCT_ZS.columns):
#    figList.append(plt.figure())
#    plt.title(posPCT_ZS.columns[i])        
#    posPCT_peak_ZS.ix[:,i].hist(bins = 50, alpha = 0.5, color = 'r')
#    posPCT_valley_ZS.ix[:,i].hist(bins = 50, alpha = 0.5, color = 'g')
#    posPCT_ZS.ix[:,i].hist(bins = 50, alpha = 0.5, color = 'b')
#    i += 1
#
#monIdx = [x for x in price.index if x.weekday() == 0]
#monPrice = price.ix[monIdx]
#monPrice['W_PCT'] = monPrice['PX_OPEN'].pct_change()
#monPrice['W_PCT'] = monPrice['W_PCT'].shift(-1)

#monPrice.ix[peakIdx, 'pivots'] = 1
#monPrice.ix[valleyIdx, 'pivots'] = -1
#posPCT_M = pd.concat([monPrice, posPCT], axis = 1, join = 'inner')
#posCHG_M = pd.concat([monPrice, posCHG], axis = 1, join = 'inner')
#posPCT_ZS_M = pd.concat([monPrice, posPCT_ZS], axis = 1, join = 'inner')

#posPCT_M.to_excel('posPCT_M.xls')
#posCHG_M.to_excel('posCHG_M.xls')
#posPCT_ZS_M.to_excel('posPCT_ZS_M.xls')

plt.figure()
plt.title('test')
a.ix[:,].hist(bins = 50,alpha = 0.5,color = 'r')
b.ix[:,].hist(bins = 50,alpha = 0.5,color = 'g')

#plt.figure()
#plt.title(posPCT_ZS.columns[1] + ' ' + str(20))        
#posPCT_peak_ZS.ix[:,1].hist(bins = 50, alpha = 0.5, color = 'r')
#posPCT_valley_ZS.ix[:,1].hist(bins = 50, alpha = 0.5, color = 'g')
#posPCT_ZS.ix[:,1].hist(bins = 50, alpha = 0.5, color = 'b')