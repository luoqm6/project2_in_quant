# -*- coding: utf-8 -*-
__author__ = 'luoqm6'
__date__ = '18-1-26 17:38 p.m'

from sklearn import preprocessing
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression
from sklearn import svm
from sklearn import neighbors
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame
from sklearn.metrics import mean_squared_error
import numpy as np


class ModelEngine(object):

    def __init__(self, dtframe):
        self.xattri_array = None
        self.dtframe = dtframe
        self.colHead = self.dtframe.columns.values.tolist()
        # print(self.dtframe)
        self.ylabel_name = None
        self.model_name = 'Linearregression'
        self.model_name_list = ['Linearregression', 'NuetrualNetwork', 'SVM', 'KNN', 'RNN']
        self.duration = 1

    def setYLabel(self, ylabel_name = 'price_change'):
        """
        This function set the y train
        @param ylabel_name:the name of y train
        """
        if(ylabel_name in self.colHead):
            self.ylabel_name = ylabel_name
        else:
            self.ylabel_name = self.colHead[-1]
        return self.ylabel_name

    def setModelName(self, model_name ='Linearregression' ):
        """
        This function set the model to predict
        @param ylabel_name:the name of model to predict
        """
        if model_name in self.model_name_list:
            self.model_name = model_name
        else:
            self.model_name = self.model_name_list[1]

    def setYLabelArray(self, ylabelname = 'price_change'):
        """
        set a column as the ylabel
        @param ylabel_name:the name of model to predict
        """
        self.setYLabel(ylabelname)
        self.ylabel_array = np.array(self.dtframe[self.ylabel_name])
        self.y_ori_array = self.ylabel_array
        self.ylabel_array = self.ylabel_array[self.duration:-5]

        # 
        # min_max_scaler = preprocessing.MinMaxScaler()
        # self.y_ori_array = min_max_scaler.fit_transform(self.y_ori_array)
        # self.ylabel_array = min_max_scaler.fit_transform(self.ylabel_array)
        return self.ylabel_array

    def setDuration(self, duration = 1):
        """
        set the duratioin to cal the mean
        @param duration: duratioin to cal the mean
        """
        if duration > 0:
            self.duration = duration
        else:
            self.duration = 1

    def setXAttriArray(self, xattri_name_list):
        """
        set the xattri_array with strategy that find mean from the previous duration 
        @param: list name of x train
        """
        xattri = self.dtframe
        xattri = xattri[xattri_name_list]

        self.xattri_array = np.array(xattri)
        tmpxattri = []
        '''
        select the mean of duration to predict a ylabel
        the final xattri_array is origin xattri_array[duration,len-1] mean list
        '''
        for i in range(self.duration, len(self.xattri_array)):
            tmparray = self.xattri_array[i-self.duration:i]  # i+1???
            # print(DataFrame(tmparray))
            tmpxattri.append(np.mean(tmparray, axis=0))  # mean of the columns as a row
        self.xattri_array = tmpxattri[:-5]
        self.xpre_array = tmpxattri[5:]
        
        #   n
        # normalization
        min_max_scaler = preprocessing.MinMaxScaler()
        self.xattri_array = min_max_scaler.fit_transform(self.xattri_array)
        self.xpre_array = min_max_scaler.fit_transform(self.xpre_array)
        # print(self.xattri_array[-5:])
        # print(self.xpre_array[-5:])
        return self.xattri_array

    def NNPredict(self, hidden_layer_sizes = 50):
        """
            predict by the NuetrualNetwork model
            @param hidden_layer_sizes: as it means

        """
        neural_network = MLPRegressor(hidden_layer_sizes=(hidden_layer_sizes,), activation='relu', solver='adam',
            alpha=0.0001, batch_size='auto', learning_rate='adaptive', learning_rate_init=0.001)
        return neural_network
    
    def LinRPredict(self):
        """
            predict by the Linearregression model
        """
        lin_reg = LinearRegression()
        return lin_reg

    def SVM_predict(self):
        """
            predict by the SVM model
            @param 
        """
        clf = svm.SVR()
        return clf

    def KNNPredict(self, n_neighbors=5):
        """
            predict by the KNN model
            @param n_neighbors: the number of K
        """
        KNN_clf = neighbors.KNeighborsRegressor(n_neighbors=n_neighbors)
        return KNN_clf

    def RNNPredict(self, rad = 1.0):
        """
            predict by the RNN model
            @param rad:the radius of the RNN
        """
        RNN_clf = neighbors.RadiusNeighborsRegressor(radius=rad)
        return RNN_clf

    def predictFit(self,  xattri_array, ylabel_array, xpre_array, model_name = 'Linearregression'):
        """
            This function fits the model
            @param model_name:the model used to predict
            return the result array
        """
        # if self.xattri_array.all() == None or self.ylabel_array.all() == None:
        #     print("set xattri_array and ylabel_array first")
        self.setModelName(model_name)
        clf = LinearRegression()
        if model_name == self.model_name_list[1]:
            print(self.model_name)
            # hidden_layer_sizes = input("Please input the hidden layer sizes:")
            clf = self.NNPredict(50)
            

        elif model_name == self.model_name_list[0]:
            print(self.model_name)
            clf = self.LinRPredict()
            

        elif model_name == self.model_name_list[2]:
            print(self.model_name)
            clf = self.SVM_predict()
             

        elif model_name == self.model_name_list[3]:
            print(self.model_name)
            # n_neighbors = input("Please input the number of neighbors:")
            clf = self.KNNPredict(10)
            
        
        elif model_name == self.model_name_list[4]:
            print(self.model_name)
            # radius = input("Please input the value of radius:")
            clf = self.RNNPredict(1.0)
            
        clf.fit(xattri_array, ylabel_array)
        self.predict_result = clf.predict(xpre_array)
        # min_max_scaler = preprocessing.MinMaxScaler()
        # self.y_ori_array = min_max_scaler.fit_transform(self.y_ori_array)
        # self.predict_result = min_max_scaler.fit_transform(self.predict_result)
        return self.predict_result

    def getError(self):
        """
        calculate the mean squared error between the y and predict result
        """
        mean_err = mean_squared_error(self.y_ori_array[self.duration+5:], self.predict_result)
        return mean_err

    ###########
    def compareModel(self):
        """
        This function compares the predict result of 
            five model we offer in our ModelEngine
        """
        errorlist = []
        for model in self.model_name_list:
            self.predictFit(self.xattri_array, self.ylabel_array, self.xpre_array, model)
            err = self.getError()
            errorlist.append(err)
            self.plotPredict(0,len(self.ylabel_array))
        errframe = DataFrame(errorlist)
        errframe.plot(kind = 'bar')
        plt.show()

    def plotPredict(self, begin=0, end = -1):
        """
        This function plot the result of the predict
        @param begin: start of the index to draw on graph
        @param end: the last index to draw on graph
        """
        err = self.getError()
        print("The mean  error of model:"+self.model_name)
        print(err)
        plt.plot(self.y_ori_array[self.duration+5:][begin:end], label=self.ylabel_name)
        plt.plot(self.predict_result[begin:end], label=self.ylabel_name+'_predict')
        plt.title(self.model_name)
        plt.legend()
        plt.show()
        plt.plot(self.y_ori_array[self.duration+5:][begin:end]-self.predict_result[begin:end], label='error')
        plt.title(self.model_name+' error')
        plt.legend()
        plt.show()

    def getColHead(self):
        return self.colHead
    
    def getModelName(self):
        return self.model_name

    def getModelNameList(self):
        return self.model_name_list

    def getXAttriArray(self):
        return self.xattri_array

    def getYLabelArray(self):
        return self.ylabel_array

    def getXPreArray(self):
        return self.xpre_array

if __name__ == "__main__":

    #read the csv to dataframe
    dtframe = pd.read_csv("D:/code/python_code/project2_in_quant/data/1day/000001.csv")
    
    # build the model and predict
    pre = ModelEngine(dtframe)

    # print(pre.getXattriArray)
    pre.setDuration(10)
    pre.setYLabelArray('close')
    pre.setXAttriArray(pre.colHead[1:])
    
    result = pre.predictFit(pre.getXattriArray(), pre.getYLabelArray(), pre.getXPreArray(), 'Linearregression')
    pre.plotPredict()
    pre.compareModel()