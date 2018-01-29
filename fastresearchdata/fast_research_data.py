from pandas import DataFrame
import pandas as pd


class FastResearchData(object):
    def __init__(self):
        """
        初始化stock_dict股票字典
        """
        self.stockDict = {}
    
    def loadFromDataFrame(self,stockID,df):
        """
        直接读取DatafRame
        """
        if stockID not in self.stockDict.keys():
            self.stockDict[stockID] = df
        else:
            pd.concat([self.stockDict[stockID],df])

    def loadFromCSV(self,stockIDList, fileNamesList):
        """
        加载csv:使用pandas
        """
        for (stockID,fileName) in zip (stockIDList,fileNamesList):
            dtframe = pd.read_csv(fileName)
            dtframe = DataFrame(dtframe)
            self.loadFromDataFrame(stockID,dtframe)

    def loadFromPickle(self,stockCodeList,fileNamesList):
        """
        加载pickle
        python的pickle模块实现了基本的数据序列和反序列化。
        通过pickle的序列化操作能够将程序中运行的对象保存到文件中去，永久存储。(dump()方法)
        通过pickle的反序列化操作，可以从文件中创建上一次程序保存的对象取出来。(load()方法)
        """
        for (stockID,fileName) in zip(stockCodeList,fileNamesList):
            pickleFile = open(fileName,'rb')
            dtframe = pickle.load(pickleFile)
            dtframe = DataFrame(dtframe)
            self.loadFromDataFrame(stockID,dtframe)
    
    def getDataFrame(self,stockID):
        """
        返回某一只股票
        """
        return self.stockDict[stockID]

    def getStockDictionary(self):
        """
        返回所有股票的字典
        """
        return self.stockDict

if __name__ == "__main__":
    stockIDList = ['000001']
    fileNamesList = ["D:/code/python_code/project2_in_quant/data/1day/000001.csv"]
    frData = FastResearchData()
    frData.loadFromCSV(stockIDList,fileNamesList)
    stock = frData.getDataFrame(stockIDList[0])
    print(stock)