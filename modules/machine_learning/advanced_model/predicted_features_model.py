import modules.machine_learning.ml_methods.help_model as hm
import modules.machine_learning.ml_methods.machine_learning  as ml
from sklearn.metrics import mean_squared_error
from math import sqrt
import pandas as pd
from sklearn import preprocessing


def predictedFeaturesModel(targetFeature, df, method,end,trainRange,showPreds):

    df = df.fillna(df.median())

    df[targetFeature] = df[targetFeature]*1000
    df[targetFeature] = df[targetFeature].fillna(0.0).astype(int)

    trainX = df[df.Season < end] # Remove the last season from the train data


    max = trainX["Season"].max()
    min = max-trainRange
    trainX = trainX[trainX.Season>min]

    trainY = trainX[targetFeature] # Team and Season are required for later sorting
    trainY = pd.DataFrame(trainY)

    trainX = trainX.drop([targetFeature], axis=1)

    trainX = hm.get_numerical_data(trainX)
    trainX = preprocessing.scale(trainX)
    trainX = pd.DataFrame(trainX)

    #The same  process is used for the test data

    testX = df[df.Season == end]
    showPreds = testX[["Team", "Season",targetFeature]] # used to show the results of the model
    showPreds['Season'] = end

    testY = testX[targetFeature]
    testY = pd.DataFrame(testY)
    testX = testX.drop([targetFeature], axis=1)
    testX = hm.get_numerical_data(testX)
    testX = preprocessing.scale(testX)
    testX = pd.DataFrame(testX)

    trainX = trainX.fillna(trainX.median())
    trainY = trainY.fillna(trainY.median())
    testY = testY.fillna(testY.median())


    trainX = trainX.values
    testX = testX.values

    if method == "XGB":
        preds = ml.XGB(trainX,trainY,testX)

    if method == "LRFS":
        preds = ml.LRFS(trainX,trainY,testX) #notice how it does not have feature selection
    if  method == "SVM":
        preds = ml.SVM(trainX,trainY,testX)

    if method == "LR":
        preds = ml.LR(trainX, trainY, testX)

    testY[targetFeature] = testY[targetFeature] / 1000
    preds = preds / 1000

    showPreds["prediction"] = preds
    #   showPreds["difference"] = showPreds["difference"].abs()
    showPreds = showPreds.sort_values(by="Team", ascending=True)

    showPreds["W"] = showPreds["W"]/1000
    #showPreds["difference"] = showPreds[targetFeature] - showPreds["prediction"]


    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(showPreds)

    testY = testY.fillna(testY.median())

    RMSE = sqrt(mean_squared_error(testY, preds))
    print("++++++++++++++++++")

    return 0, RMSE  #to do: fix return average error, you will need to divide the value of the target feature in show preds
