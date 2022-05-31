# -*- coding: utf-8 -*-
"""lr_model_binary.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mPlA8Q02JgM8J4-RAGx2ZvfZ_9-Lh_jg
"""

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.model_selection import train_test_split
import os
import matplotlib.pyplot as plt

def import_data(file_name):
    #EH:  Create DataFrame from csv
    sector_data_df = pd.read_csv(
    Path('Data_Prep_Output/'+file_name+'.csv'))
    
    #EH: create binary column for roi positive
    sector_data_df['roi_positive'] = sector_data_df['q_roi'] >0
      
    #EH:  Drop unnamed, currency, ticker, sector columns from the DataFrame
    sector_data_df = sector_data_df.drop(columns=['Unnamed: 0','reportedCurrency','ticker','Sector','close','q_roi'],axis=1)
    
    #EH: rename date_x
    sector_data_df=sector_data_df.rename(columns={'date_x':'date'})

    #EH: change date to datetime format
    sector_data_df['date']=pd.to_datetime(sector_data_df['date'])
    

    
    return sector_data_df

def data_prep(dataframe):
    #Isolating the categorical variables
    categorical_variables = list(dataframe.dtypes[dataframe.dtypes == "datetime64[ns]"].index)

    #Calling an instance of OneHotEncoder
    enc = OneHotEncoder(sparse=False)
    
    #Encoding the categorical variables
    encoded_data = enc.fit_transform(dataframe[categorical_variables])

    #Creating a new dataframe of the categorical variables
    encoded_df = pd.DataFrame(encoded_data,columns = enc.get_feature_names_out(categorical_variables))

    #Combining the newly encoded categorical variables with the original dataframe again
    encoded_df = pd.concat([dataframe.drop(columns = categorical_variables),encoded_df], axis=1)
    
    return encoded_df

def data_separation(df, dependent_variable):
    #Separating and scaling the dependent and independent variables
    
    y = df[dependent_variable]
    X = df.drop([dependent_variable],axis=1)
    
    #Splitting the training and testing datasets
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    
    #Scaling the data
    scaler = StandardScaler()

    # Fit the scaler to the features training dataset
    X_scaler = scaler.fit(X_train)

    # Fit the scaler to the features training dataset
    X_train_scaled = X_scaler.transform(X_train)
    X_test_scaled = X_scaler.transform(X_test)
    
    return y_train, y_test,  X_train_scaled, X_test_scaled

def log_reg(y_train, y_test,  X_train_scaled, X_test_scaled):
    #Create an instance of the logistic regression model
    lr_model = LogisticRegression()

    # Fit the model
    lr_model.fit(X_train_scaled, y_train)

    # Generate predictions from the model we just fit
    training_predictions = lr_model.predict(X_train_scaled)

    # Convert those predictions (and actual values) to a DataFrame
    # results_df = pd.DataFrame({"Predicted": predictions, "Actual":  y_train})
    # results_df

    
    # Testing the model
    testing_predictions = lr_model.predict(X_test_scaled)

    # Save both the test predictions and actual test values to a DataFrame
    #results_df = pd.DataFrame({
        #"Testing Predictions": testing_predictions,
        #"Testing Actual Values": testing_targets})
    #results_df
    evaluate=classification_report(y_train,training_predictions,output_dict=True)
    score= accuracy_score(y_test, testing_predictions)
    return evaluate, score

#read directory filenames

file_list=[]
for path, subdirs,files in os.walk("Data_Prep_Output"):
    for name in files:
        if name[-4:]=='.csv':
            file_list.append(name[:-4])
file_list=file_list[:-2]
file_list

#evaluation, score, plot(turn it into a function)

#for sector_file in file_list:
def evaluate_plot(sector_file):
    sector_data=import_data(sector_file)
    encoded_df=data_prep(sector_data)
    y_train, y_test,  X_train_scaled, X_test_scaled=data_separation(encoded_df,'roi_positive')
    #print('=============================' *6)
   
    evaluate, score=log_reg(y_train, y_test,  X_train_scaled, X_test_scaled)
    output=f'Logistic Regression Model-  \033[1m{sector_file} \033[0m Classification report'

    #print(evaluate)
    '''
    print(f'Logistic Regression Model-  \033[1m{sector_file} \033[0m Accuracy score')
    display(score)
    
    #Scatter plot
    plt.scatter(
        # One feature on the x-axis
        x=sector_data['changeInCashAndCashEquivalents'],

        y=sector_data['surprise'],

        c=sector_data['roi_positive'])
    plt.xlabel('Change in Cash')
    plt.ylabel('EPS delta from est')
    plt.title(f'Logistic Regression Model-{sector_file}Plot- Postive Quarterly ROI')
    
    plt.show()
    '''
    return evaluate,score

#     display(sns.heatmap(sector_data.corr()))

    
#     plt.scatter(
#         # One feature on the x-axis
#         x=sector_data['inflation'],

#         y=sector_data['surprise'],

#         c=sector_data['roi_positive'])
#     plt.xlabel('inflation indicator')
#     plt.ylabel('EPS delta from est')
#     plt.title(f'Linear Regression Model-{sector_file}Plot- Postive Quarterly ROI')

#import seaborn as sns
'''''
for sector_file in file_list:
    sector_data=import_data(sector_file)
    sector_data.head()
    # inflation_roi=sector_data['inflation','roi_positive']
    # inflation_roi.head()

sector_data=import_data('Consumer Non-Durables')
sector_data.head()
# inflation_rio_binary=sector_data.loc[['inflation']]
# # inflation_rio_binary.head()
inflat_roi_binary=pd.concat([sector_data[['inflation']],sector_data[['roi_positive']]])
inflat_roi_binary.head()

sector_data['roi_positive']
# sns.heatmap([sector_data['inflation'],sector_data['roi_positive']],

sector_data_df = pd.read_csv(
    Path('Data_Prep_Output/Consumer Non-Durables.csv'))
sector_data_df.head()
inflat_roi_binary=pd.concat([sector_data_df[['inflation']],sector_data_df[['q_roi']],sector_data_df[['surprise']],
                             sector_data_df[['changeInCashAndCashEquivalents']],sector_data_df[['netIncome']],
                             sector_data_df[['changeInReceivables']],sector_data_df[['dividendPayout']],
                            sector_data_df[['reportedEPS']]],axis=1)
inflat_roi_binary.head()

#sns.heatmap(inflat_roi_binary.corr())

sector_data_df = pd.read_csv(
    Path('Data_Prep_Output/Consumer Non-Durables.csv'))
sector_data_df.head()

ticker_qroi=pd.concat([sector_data_df[['ticker']],sector_data_df[['q_roi']]],axis=1)
ticker_qroi.unstack(level=1)
ticker_qroi.head()

sns.heatmap(ticker_qroi.corr())

corr_df=sector_data.loc[:,    [
     'operatingCashflow',
     'paymentsForOperatingActivities',
     'changeInOperatingLiabilities',
     'changeInOperatingAssets',
     'depreciationDepletionAndAmortization',
     'capitalExpenditures',
     'changeInReceivables',
     'changeInInventory',
     'profitLoss',
     'cashflowFromInvestment',
     'cashflowFromFinancing',
     'proceedsFromRepaymentsOfShortTermDebt',
     'paymentsForRepurchaseOfCommonStock',
     'paymentsForRepurchaseOfEquity',
     'dividendPayout',
     'dividendPayoutCommonStock',
     'proceedsFromIssuanceOfCommonStock',
     'proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet',
     'proceedsFromRepurchaseOfEquity',
     'changeInCashAndCashEquivalents',
     'changeInExchangeRate',
     'netIncome',
     'reportedEPS',
     'estimatedEPS',
     'surprise',
     'surprisePercentage',
     'inflation',
     'cs_sentiment']]

sns.heatmap(corr_df.corr(),size)

'''