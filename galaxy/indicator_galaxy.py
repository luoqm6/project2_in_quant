# -*- coding: utf-8 -*-
__author__ = 'luoqm6'
__date__ = '18-1-26 17:38 p.m'

import datetime as dt
import numpy as np
import pandas as pd


class IndicatorGalaxy:

    def __init__(self):
        self.xattri_array = None
        
    def load_CSV(self, path):
        """
        This function load the data in csv file 
        @param path:the path of the csv file
        """
        self.dtframe = pd.read_csv(path)
        self.colHead = self.dtframe.columns.values.tolist()
        self.dtframe = self.dtframe.sort_values(by=self.colHead[0])
        self.dtframe = self.dtframe.reset_index(drop=True)
        # print (self.dtframe)
        date = self.dtframe[self.colHead[0]][0]
        if date.find(':') == -1:
            self.dtframe = self.div_date(self.dtframe)
            self.colHead = self.dtframe.columns.values.tolist()
            self.dtframe = self.dtframe.sort_values(by=self.colHead[0:3], ascending= True)
            #print(self.colHead[0:3])
            self.del_columns(self.colHead[0:3])
        else:
            self.dtframe = self.div_time(self.dtframe)
            self.colHead = self.dtframe.columns.values.tolist()
            self.dtframe = self.dtframe.sort_values(by=self.colHead[0:6], ascending= True)
            #print(self.colHead[0:6])
            self.del_columns(self.colHead[0:6])
        
        #####
    
    def div_date(self, dtframe):
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

    def div_time(self, data):
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

    def del_columns(self, collist):
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

    def select_columns(self,collist):
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
        

    def get_col_mean(self, col_name, interval=1):
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

    def add_col_mean(self, col_name, interval=1):
        """
        calculate the column's mean with interval
        @param col_name:the name of the column
        @param interval:the interval to calculate the mean
        """
        self.dtframe[col_name+'_avg'] = self.get_col_mean(col_name, interval)
        #print(self.dtframe)

    def get_EMA(self,col_name):
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
        
    def add_EMA(self, col_name = 'close'):
        self.get_EMA(col_name)
        self.dtframe[col_name+'_EMA12'] = self.EMA12
        self.dtframe[col_name+'_EMA26'] = self.EMA26
        return self.dtframe

    def get_DIF(self, col_name = 'close'):
        """
        compute DIFF bitween EMA(12) & EMA(16)
        DIFF = EMA(12) - EMA(26)
        @param col_name:the column's name 
        """
        EMA12,EMA26 = self.get_EMA(col_name)
        self.DIF = []
        self.DIF.append(EMA12[0])
        for i in range(1,len(EMA12)):
            self.DIF.append(EMA12[i] - EMA26[i])
        return self.DIF
    
    def add_DIF(self, col_name = 'close'):
        self.get_DIF(col_name)
        self.dtframe[col_name+'_DIF'] = self.DIF
        return self.dtframe

    def get_MACD(self,col_name = 'close'):
        """
        compute MACD(DEA)
        DEA(MACD) = DEA * 8/10 + DIF * 2/10
        """
        DIF = self.get_DIF(col_name)
        DEA = []

        DEA.append(DIF[0])
        for i in range(1,len(DIF)):
            DEA.append(DEA[i-1]*8/10+DIF[i]*2/10)
        
        self.MACD = []
        for i in range(len(DEA)):
            self.MACD.append(2*(DIF[i]-DEA[i]))
        return self.MACD
    
    def add_MACD(self, col_name = 'close'):
        self.get_MACD(col_name)
        self.dtframe[col_name+'_MACD'] = self.MACD
        return self.dtframe

    def get_dtframe(self):
        return self.dtframe
        
    def get_colHead(self):
        return self.colHead



if __name__ == "__main__":

    #read the csv to dataframe
    indtr = IndicatorGalaxy()
    indtr.load_CSV("D:/code/python_code/project2_in_quant/data/1day/000001.csv")

    # add some indicator
    indtr.add_col_mean('p_change')
    indtr.add_EMA('p_change')
    indtr.add_DIF('p_change')
    indtr.add_MACD('p_change')
    indtr.add_col_mean('volume')
    indtr.add_EMA('volume')
    indtr.add_DIF('volume')
    indtr.add_MACD('volume')
    
    
    
    
    
