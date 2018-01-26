from sklearn import preprocessing
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression
from sklearn import svm
from sklearn import neighbors
from sklearn import tree
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame
import sklearn.metrics as mtc
from sklearn.metrics import mean_squared_error
import numpy as np

class ModelEngine:

    def __init__(self, dtframe):
        self.xattri_array = None
        self.dtframe = dtframe
        self.colHead = self.dtframe.columns.values.tolist()
        # print(self.dtframe)
        self.ylabel_name = None
        self.model_name = 'Linearregression'
        self.model_name_list = ['Linearregression', 'NuetrualNetwork', 'SVM', 'KNN', 'RNN']
        self.duration = 1

    def set_ylabel(self, ylabel_name = 'price_change'):
        """
        This function set the y train
        @param ylabel_name:the name of y train
        """
        if(ylabel_name in self.colHead):
            self.ylabel_name = ylabel_name
        else:
            self.ylabel_name = self.colHead[-1]
        return self.ylabel_name

    def set_model_name(self, model_name ='Linearregression' ):
        """
        This function set the model to predict
        @param ylabel_name:the name of model to predict
        """
        if model_name in self.model_name_list:
            self.model_name = model_name
        else:
            self.model_name = self.model_name_list[1]

    def set_ylabel_array(self, ylabelname = 'price_change'):
        """
        set a column as the ylabel
        @param ylabel_name:the name of model to predict
        """
        self.set_ylabel(ylabelname)
        self.ylabel_array = np.array(self.dtframe[self.ylabel_name])
        self.ylabel_array = self.ylabel_array[self.duration:]
        return self.ylabel_array

    def set_duration(self, duration = 1):
        """
        set the duratioin to cal the mean
        @param duration: duratioin to cal the mean
        """
        if duration > 0:
            self.duration = duration
        else:
            self.duration = 1

    def set_xattri_array(self, xattri_name_list):
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
        self.xattri_array = tmpxattri[:-1]
        self.xpre_array = tmpxattri[1:]
        self.xattri_array = tmpxattri
        self.xpre_array = tmpxattri
        min_max_scaler = preprocessing.MinMaxScaler()
        #   n
        # normalization
        self.xattri_array = min_max_scaler.fit_transform(self.xattri_array)
        self.xpre_array = min_max_scaler.fit_transform(self.xpre_array)
        # print(self.xattri_array[-5:])
        # print(self.xpre_array[-5:])
        return self.xattri_array

    def NN_predict(self, xattri_array, ylabel_array, xpre_array):
        """
        predict by the NuetrualNetwork model
        @param: the x train array
        @param: the y train array
        @param: the x predict array
        """
        neural_network = MLPRegressor(hidden_layer_sizes=(50,), activation='relu', solver='adam',
            alpha=0.0001, batch_size='auto', learning_rate='adaptive', learning_rate_init=0.001)
        neural_network.fit(self.xattri_array, self.ylabel_array)
        result = neural_network.predict(xpre_array)
        return result
    
    def LinR_predict(self, xattri_array, ylabel_array, xpre_array):
        """
        predict by the Linearregression model
        @param: the x train array
        @param: the y train array
        @param: the x predict array
        """
        lin_reg = LinearRegression()
        lin_reg.fit(xattri_array, ylabel_array)
        result = lin_reg.predict(xpre_array)
        return result

    def SVM_predict(self, xattri_array, ylabel_array, xpre_array):
        """
        predict by the SVM model
        @param: the x train array
        @param: the y train array
        @param: the x predict array
        """
        clf = svm.SVR()
        clf.fit(xattri_array, ylabel_array)
        result = clf.predict(xpre_array)
        return result

    def KNN_predict(self, xattri_array, ylabel_array, xpre_array):
        """
        predict by the KNN model
        @param: the x train array
        @param: the y train array
        @param: the x predict array
        """
        KNN_clf = neighbors.KNeighborsRegressor(n_neighbors=5)
        KNN_clf.fit(xattri_array, ylabel_array)
        result = KNN_clf.predict(xpre_array)
        return result

    def RNN_predict(self, xattri_array, ylabel_array, xpre_array):
        """
        predict by the RNN model
        @param: the x train array
        @param: the y train array
        @param: the x predict array
        """
        RNN_clf = neighbors.RadiusNeighborsRegressor(radius=1.0)
        RNN_clf.fit(xattri_array, ylabel_array)
        result = RNN_clf.predict(xpre_array)
        return result

    def predict_fit(self, model_name = 'Linearregression', ):
        """
        This function fits the model
        @param model_name:the model used to predict
        return the result array
        """
        # if self.xattri_array.all() == None or self.ylabel_array.all() == None:
        #     print("set xattri_array and ylabel_array first")
        self.set_model_name(model_name)
        if model_name == self.model_name_list[1]:
            print(self.model_name)
            self.predict_result = self.NN_predict(self.xattri_array, self.ylabel_array, self.xpre_array)
            return self.predict_result

        elif model_name == self.model_name_list[0]:
            print(self.model_name)
            self.predict_result = self.LinR_predict(self.xattri_array, self.ylabel_array, self.xpre_array)
            return self.predict_result

        elif model_name == self.model_name_list[2]:
            print(self.model_name)
            self.predict_result = self.SVM_predict(self.xattri_array, self.ylabel_array, self.xpre_array)
            return self.predict_result 

        elif model_name == self.model_name_list[3]:
            print(self.model_name)
            self.predict_result = self.KNN_predict(self.xattri_array, self.ylabel_array, self.xpre_array)
            return self.predict_result
        
        elif model_name == self.model_name_list[4]:
            print(self.model_name)
            self.predict_result = self.RNN_predict(self.xattri_array, self.ylabel_array, self.xpre_array)
            return self.predict_result

    def get_error(self):
        """
        calculate the mean squared error between the y and predict result
        """
        mean_err = mean_squared_error(self.ylabel_array, self.predict_result)
        return mean_err

    ###########
    def compare_model(self):
        errorlist = []
        for model in self.model_name_list:
            self.predict_fit(model)
            err = self.get_error()
            errorlist.append(err)
            self.plot_predict(0,len(self.ylabel_array))
        errframe = DataFrame(errorlist)
        errframe.plot(kind = 'bar')
        plt.show()

    def plot_predict(self, begin=0, end = -1):
        """
        This function plot the result of the predict
        @param begin: start of the index to draw on graph
        @param end: the last index to draw on graph
        """
        err = self.get_error()
        print("The mean  error of model:"+self.model_name)
        print(err)
        plt.plot(self.ylabel_array[begin:end], label=self.ylabel_name)
        plt.plot(self.predict_result[begin:end], label=self.ylabel_name+'_predict')
        plt.legend()
        plt.show()
        plt.plot(self.ylabel_array[begin:end]-self.predict_result[begin:end], label='error')
        plt.legend()
        plt.show()

    def get_colHead(self):
        return self.colHead
    
    def get_model_name(self):
        return self.model_name

    def get_model_name_list(self):
        return self.model_name_list

    def get_xattri_array(self):
        return self.xattri_array

    def get_xpre_array(self):
        return self.xpre_array