# -*- coding: utf-8 -*-
__author__ = 'luoqm6'
__date__ = '18-1-26 17:38 p.m'

import datetime as dt
import numpy as np
import pandas as pd


class IndicatorGalaxy(object):

    def __init__(self):
        self.xattri_array = None
        
    def loadCSV(self, path):
        """
        This function load the data in csv file 
        @param path:the path of the csv file
        """
        dtframe = pd.read_csv(path)
        self.loadDataframe(dtframe)
        
        #####

    def loadDataframe(self, dtframe):
        """
        This function load the data in DataFrame directly 
        @param path:the DataFrame variable
        """
        self.colHead = dtframe.columns.values.tolist()
        self.dtframe = dtframe.sort_values(by=self.colHead[0])
        self.dtframe = self.dtframe.reset_index(drop=True)
        # print (self.dtframe)
        date = self.dtframe[self.colHead[0]][0]
        if date.find(':') == -1:
            self.dtframe = self.divDate(self.dtframe)
            self.colHead = self.dtframe.columns.values.tolist()
            self.dtframe = self.dtframe.sort_values(by=self.colHead[0:3], ascending= True)
            #print(self.colHead[0:3])
            self.delColumns(self.colHead[0:3])
        else:
            self.dtframe = self.divTime(self.dtframe)
            self.colHead = self.dtframe.columns.values.tolist()
            self.dtframe = self.dtframe.sort_values(by=self.colHead[0:6], ascending= True)
            #print(self.colHead[0:6])
            self.delColumns(self.colHead[0:6])
    
    def divDate(self, dtframe):
        """
        This function divdes the date to 'year', 'month', 'day'
        @param dtframe :the dtframe has date columns
        """
        colHead = dtframe.columns.values.tolist()
        if 'date' not in colHead:
            print("date is no exit")
            return dtframe
        else:
            date = []
            for no in range(len(dtframe['date'])):
                date.append(dt.datetime.strptime(dtframe['date'][no], "%Y-%m-%d"))
            date_list = []
            for d in date:
                temp = []
                temp.append(d.year)
                temp.append(d.month)
                temp.append(d.day)
                date_list.append(temp)
            del dtframe['date']
            date_frame = pd.DataFrame(date_list, columns=['year', 'month', 'day'])
            result = pd.concat([date_frame, dtframe], axis=1)
            return result

    def divTime(self, data):
        """
        This function divdes the date to 'year','month','day','hour','minute','second'
        @param dtframe :the dtframe has date columns
        """
        colHead = data.columns.values.tolist()
        if 'date' not in colHead:
            print("date is no exist")
            return None
        else:
            date = []
            for no in range(len(data['date'])):
                date.append(dt.datetime.strptime(data['date'][no], "%Y-%m-%d %H:%M:%S"))
            date_list = []
            for d in date:
                temp = []
                temp.append(d.year)
                temp.append(d.month)
                temp.append(d.day)
                temp.append(d.hour)
                temp.append(d.minute)
                temp.append(d.second)
                date_list.append(temp)
            del data['date']
            date_frame = pd.DataFrame(date_list, columns=['year','month','day','hour','minute','second'])
            result = pd.concat([date_frame, data], axis=1)
            return result

    def delColumns(self, collist):
        """
        This function delete the columns when thier name in the collist
        @param collist:The name of the list wants to delete
        """
        for col in collist:
            if col in self.colHead:
                del self.dtframe[col]
            else:
                print(col+" does not exist")
        #print (self.dtframe)

    def selectColumns(self,collist):
        """
        This function select the columns when thier name in the collist
        @param collist:The list of the list wants to select
        @return :return the new selected dataframe
        """
        for col in collist:
            if col not in self.colHead:
                print(col+" does not exist")
                return None
            else:
                pass
        return self.dtframe[collist]
        

    def getColMean(self, col_name, interval=1):
        """
        add the mean of the columns with interval to dtframe
        @param col_name: 

        """
        new_col = []
        ori_col = self.dtframe[col_name].tolist()
        # print(ori_col)
        '''
        add a columns' mean to the dateframe
        '''
        for i in range(interval):
            new_col.append(ori_col[i])
        for i in range(interval,len(self.dtframe[col_name])):
            tmparray = ori_col[i-interval:i]  # i+1???
            #print(tmparray)
            # mean of the columns as a row
            new_col.append(np.mean(tmparray))
            #print(new_col[i])
        return new_col

    def addColMean(self, col_name, interval=1):
        """
        calculate the column's mean with interval, and add to the DataFrame
        @param col_name:the name of the column
        @param interval:the interval to calculate the mean
        """
        self.dtframe[col_name+'_avg'] = self.getColMean(col_name, interval)
        #print(self.dtframe)

    def getEMA(self,col_name):
        """
        calculate EMA of a column
        @param col_name:name of the column
        """
        if col_name not in self.colHead:
            print("The column doesn't exist!")
            return

        price_list = self.dtframe[col_name].tolist()
        self.EMA12 = []
        self.EMA26 = []

        self.EMA12.append(price_list[0])
        self.EMA26.append(price_list[0])
        for i in range(1,len(price_list)):
            yd12 = self.EMA12[i-1]
            yd26 = self.EMA26[i-1]
            tday = price_list[i]
            self.EMA12.append(2/13*tday + 11/13*yd12)
            self.EMA26.append(2/27*tday + 25/27*yd26)
        return self.EMA12,self.EMA26
        
    def addEMA(self, col_name = 'close'):
        """
        This function add the EMA12 and EMA26 to the DataFrame
        @param col_name: name of the column to calculate EMA
        """
        self.getEMA(col_name)
        self.dtframe[col_name+'_EMA12'] = self.EMA12
        self.dtframe[col_name+'_EMA26'] = self.EMA26
        return self.dtframe

    def getDIF(self, col_name = 'close'):
        """
        compute DIFF bitween EMA(12) & EMA(16)
        DIFF = EMA(12) - EMA(26)
        @param col_name:the column's name 
        """
        EMA12,EMA26 = self.getEMA(col_name)
        self.DIF = []
        self.DIF.append(EMA12[0])
        for i in range(1,len(EMA12)):
            self.DIF.append(EMA12[i] - EMA26[i])
        return self.DIF
    
    def addDIF(self, col_name = 'close'):
        """
        This function add the DIF to the DataFrame
        @param col_name: name of the column to calculate DIF
        """
        self.getDIF(col_name)
        self.dtframe[col_name+'_DIF'] = self.DIF
        return self.dtframe

    def getMACD(self,col_name = 'close'):
        """
        compute MACD(DEA)
        DEA(MACD) = DEA * 8/10 + DIF * 2/10
        """
        DIF = self.getDIF(col_name)
        DEA = []

        DEA.append(DIF[0])
        for i in range(1,len(DIF)):
            DEA.append(DEA[i-1]*8/10+DIF[i]*2/10)
        
        self.MACD = []
        for i in range(len(DEA)):
            self.MACD.append(2*(DIF[i]-DEA[i]))
        return self.MACD
    
    def addMACD(self, col_name = 'close'):
        """
        This function add the MACD to the DataFrame
        @param col_name: name of the column to calculate MACD
        """
        self.getMACD(col_name)
        self.dtframe[col_name+'_MACD'] = self.MACD
        return self.dtframe

    def getDtframe(self):
        return self.dtframe
        
    def getColHead(self):
        return self.colHead


if __name__ == "__main__":

    #read the csv to dataframe
    indtr = IndicatorGalaxy()
    indtr.loadCSV("D:/code/python_code/project2_in_quant/data/1day/000001.csv")

    # add some indicator
    indtr.addColMean('p_change')
    indtr.addEMA('p_change')
    indtr.addDIF('p_change')
    indtr.addMACD('p_change')
    indtr.addColMean('volume')
    indtr.addEMA('volume')
    indtr.addDIF('volume')
    indtr.addMACD('volume')
    
    
    
    
    
