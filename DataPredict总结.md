## DataPredict 项目总结
####    罗庆鸣
----
### 项目的主要框架结构总结
1.  读取数据文件。设计一个模块FastResearchData用于将数据转化为合适的内部类型，例如DataFrame，然后可以更加进一步转化为内部的一个更快格式的数据类型。
2.  获得预测指标以及将预测指标进行分类。设计第二个模块IndicatorGallexy，将上面所得的数据分类，根据当前数据获得更多可以用于预测的指标，例如均值，MACD等，加入到预测的数据中。
3.  训练和评估。设计第三个模块ModelEngine来管理训练和评估过程，将上一步所得的所有有用的数据传入，决定要预测的Y，选择用于预测的指标X，数据清理及变量筛选（降维），并且选择模型进行预测，最后将预测的结果进行评估和比较。

### Review中提出的问题及改进
- **将可以合并的重复代码进行合并**
    - 例如在代码中选择不同的预测模型的时候，只有模型的实力化一行的内容是不一样的，可以用if elif来根据所选的模型进行实例化，后都是调用模型的predict和fit函数，这些predict和fit部分可以进行合并。
- **命名规范**
    - 在函数、变量命名的时候要注意命名的规范。在代码中可以采用全小写加下划线式的分割法规范（例如：lower_with_under）;或者是首单词小写，后面单词首字母大写拼接在一起的驼峰原则来命名（例如：lowerFirstLetterUpper）。可能公司普遍采纳第二种命名规范，所以为了保持统一，以后尽量都使用第二种命名规范。
    - 类命名应该采用每个单词首字符大写的形式（例如：CapWords）
    - 模块命名为了避免和类名一致引起困扰，一般采用全小写加下划线的方式命名（例如：linear_model）
    - 所有类内部的私有变量在前面加上双下滑线（例如：__var）
    - 常量采用全大写加下划线的方式（例如：GLOBAL_VAR）
- **模块的封装**
    - 将不同的类或者模块按照合适的逻辑封装成单独的包，然后在写main函数的文件内通过import的方式导入模块，使得写main函数的文件中能够快速找到main函数的位置，并且通过main函数能够大致看出每个模块的功能以及用法。
- **命令行参数**
    - 在main函数中要加入获取命令行的参数，可以采用如下的框架读取命令行参数，后面的代码中可以使用args.path这种方式直接获得参数的值，注意前面加了"-"的是可选参数，没有则使用后面的default中设置的默认值，没有加"-"的是必选参数，如果命令行输入中没有输入必选参数在运行的时候会报错。
    ```
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("p", 
                            "--path", 
                            type=str, 
                            default='default path', 
                            help="help message") 
        parser.add_argument("-m", 
                            "--model", 
                            type=str, 
                            default='default model', 
                            help="help message") 
        args = parser.parse_args()
    ```
### 项目中遇到的问题以及解决办法
- 在读入csv文件转为DataFrame之后，对DataFrame按照第一列时间排序后，前面的每一行对应的下标index依旧没有变。解决办法是使用dataframe.reset_index(drop = True)重新设置下标。
- 使用KNN做回归预测时候出现错误。sklearn中的几个算法模型比如说KNN模型可以用来做分类或者做回归预测，但是使用的具体模型不一样，回归用的是KNeighborsRegressor()，而分类用的是KNeighborsClassifier()，不能混淆。
- 使用sys.argv[]数组获取命令行参数的时候要注意第一个参数是py文件的名字，后面的参数才是命令行的其他参数，可以通过sys.argv[1:]的方式获得后面的参数。

### 学习到的知识
- 进一步熟悉了python的语法以及dataframe的使用。
- 了解了强大的库sklearn中用于分类和回归预测的几个基本模型的概念以及使用方法，尝试使用了LinearRegression，neural_network，SVM，KNN，RNN来进行回归预测。
- 学习了如何使用argparse和sys.argv来获取命令行的参数，其中argparse还可以进行help说明的设置。
- 了解了用股票期货数据来做预测的大体框架结构和步骤流程。