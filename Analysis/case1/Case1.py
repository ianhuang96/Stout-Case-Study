#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from sklearn.metrics import f1_score, confusion_matrix


# In[2]:


data = pd.read_csv('PS_20174392719_1491204439457_log.csv')
data.head(10)


# # Data Overview and Processing 

# In[3]:


# check data type of each column
data.dtypes


# In[4]:


#  there is no mssing value
data.isnull().sum()


# In[5]:


# there is no duplicate rows
data.duplicated().sum()


# In[6]:


# basic statistical info
data.describe()


# In[7]:


# remove unnecessary columns
data = data.drop(columns=['nameOrig', 'nameDest'])
data.head(10)


# In[8]:


tran_type = data.groupby('type')['amount'].count()
tran_type


# In[9]:


pie_plot = tran_type.plot.pie(figsize=(12, 8), autopct='%1.0f%%')
pie_plot.legend(loc="upper right")
plt.title('Amount of each type')
plt.show()


# In[10]:


am_type = data.groupby('type')['amount'].sum()
am_type


# In[11]:


pie_plot = am_type.plot.pie(figsize=(12, 8), autopct='%1.0f%%')
pie_plot.legend(loc="upper right")
plt.title('Transaction amount of each type')
plt.show()


# In[12]:


fraud_cnt = data['isFraud'].sum()
not_fraud_cnt = len(data)-fraud_cnt


# In[13]:


objects = ('Not Fraud', 'Fraud')
y_pos = np.arange(len(objects))
performance = [not_fraud_cnt, fraud_cnt]
plt.barh(y_pos, performance, align='center', alpha=0.5)
plt.yticks(y_pos, objects)
plt.xlabel('Count')
plt.show()


# In[14]:


fraud_amount = data[data['isFraud']==1]['amount'].sum()
not_fraud_amount = data[data['isFraud']==0]['amount'].sum()

y_pos = np.arange(len(objects))
performance_amount = [not_fraud_amount, fraud_amount]
plt.barh(y_pos, performance_amount, align='center', alpha=0.5)
plt.yticks(y_pos, objects)
plt.xlabel('Amount')
plt.show()


# In[15]:


data = pd.get_dummies(data, prefix=['type'])
data.head(10)


# In[16]:


# change the order of columns
cols = ['step',
 'amount',
 'oldbalanceOrg',
 'newbalanceOrig',
 'oldbalanceDest',
 'newbalanceDest',
 'type_CASH_IN',
 'type_CASH_OUT',
 'type_DEBIT',
 'type_PAYMENT',
 'type_TRANSFER',
 'isFraud',
 'isFlaggedFraud',]
data = data[cols]
data.head(10)


# In[17]:


# check correlation between different variables and make a heatmap
plt.figure(figsize=(12, 10))
cor = data.corr()
ax = sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
ax.set_ylim(8, 0)
ax.xaxis.tick_top()
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
plt.show()


# # Models and Evaluation

# •  This dataset is extremely imbalanced, so I choose F1-score and Confusion Matrix as metric instead of accuracy.<br>
# •  I will use three models to make classification: Logistic Regression, Decision Tree and XGBoost.<br>
# •  Dataset will be splited in to training data and validation data. Both of the performance will be compared in order to detect potential overfitting issue.<br>
# •  F1-score of Logistic Regression model is 0.59.<br>
# •  F1-score of Decision Tree model is 0.87(overfitting might occurr).<br>
# •  F1-score of XGBoost model is 0.61.<br>
# •  Logistics Regression model as a baseline model has the lowest F1-score. Decision Tree model has the best performance, but it still needs to be improved. <br>
# •  Confusion Matrix is shown as follow. XGBoost model successfully detected most fraudulent transactions, thouth its F1-score is not high. XGBoot model can handle imbalanced data because it gives minority class more weight. 

# In[18]:


# split target and features 
data = data.drop(columns=['isFlaggedFraud']) #we don't use this column in prediction.
y = data.pop('isFraud')
X = data


# In[19]:


# split traing data and validation data
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state = 2)
# standardize features
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_val = scaler.transform(X_val)


# ### Model One: Logistic Regression

# In[20]:


lr_clf = LogisticRegression(random_state = 2).fit(X_train, y_train)
y_train_pred = lr_clf.predict(X_train)
lr_train_f1 = f1_score(y_train, y_train_pred)
lr_train_cm = confusion_matrix(y_train, y_train_pred)
print('F1-score of training data: ' + str(lr_train_f1))
print('Confusion matrix of training data: \n' + str(lr_train_cm))

y_val_pred = lr_clf.predict(X_val)
lr_val_f1 = f1_score(y_val, y_val_pred)
lr_val_cm = confusion_matrix(y_val, y_val_pred)
print('F1-score of validation data: ' + str(lr_val_f1))
print('Confusion matrix of validation data: \n' + str(lr_val_cm))


# ### Model Two: Decision Tree

# In[21]:


dt_clf = DecisionTreeClassifier(random_state = 2).fit(X_train, y_train)
y_train_pred = dt_clf.predict(X_train)
dt_train_f1 = f1_score(y_train, y_train_pred)
dt_train_cm = confusion_matrix(y_train, y_train_pred)
print('F1-score of training data: ' + str(dt_train_f1))
print('Confusion matrix of training data: \n' + str(dt_train_cm))

y_val_pred = dt_clf.predict(X_val)
dt_val_f1 = f1_score(y_val, y_val_pred)
dt_val_cm = confusion_matrix(y_val, y_val_pred)
print('F1-score of validation data: ' + str(dt_val_f1))
print('Confusion matrix of validation data: \n' + str(dt_val_cm))


# ### Model Three: XGBoost

# In[22]:


weight = (y == 0).sum() / (1.0 * (y == 1).sum())
xgb_clf = XGBClassifier(scale_pos_weight=weight).fit(X_train, y_train)
y_train_pred = xgb_clf.predict(X_train)
xgb_train_f1 = f1_score(y_train, y_train_pred)
xgb_train_cm = confusion_matrix(y_train, y_train_pred)
print('F1-score of training data: ' + str(xgb_train_f1))
print('Confusion matrix of training data: \n' + str(xgb_train_cm))

y_val_pred = xgb_clf.predict(X_val)
xgb_val_f1 = f1_score(y_val, y_val_pred)
xgb_val_cm = confusion_matrix(y_val, y_val_pred)
print('F1-score of validation data: ' + str(xgb_val_f1))
print('Confusion matrix of validation data: \n' + str(xgb_val_cm))


# # Future Work

# •	This dataset is imbalanced, we can randomly oversampling minority class or randomly undersampling majority class to make our data balanced. We can build more accurate models with balanced data.<br>
# •	In this case, Decision Tree model performs well but has overfitting issue, which is very common in Decision Tree models. I will do tuning and use bagging method such as Random Forest to avoid overfitting.<br>
# •	Check feature importances and detect what features or attributes are most likely to represent fraud when they have large values.<br>
# •	Draw AUC curves and find best threshold that can detect as more fraudulent transactions as possible.
# 
