#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from collections import Counter
import warnings
warnings.filterwarnings('ignore')


# In[2]:


data = pd.read_csv('casestudy.csv')


# In[3]:


# preview data
data.head(10)


# ## For each year we need the following information:<br>
# •	Total revenue for the current year<br>
# •	New Customer Revenue e.g. new customers not present in previous year only<br>
# •	Existing Customer Growth. To calculate this, use the Revenue of existing customers for current year –(minus) Revenue of existing customers from the previous year<br>
# •	Revenue lost from attrition<br>
# •	Existing Customer Revenue Current Year<br>
# •	Existing Customer Revenue Prior Year<br>
# •	Total Customers Current Year<br>
# •	Total Customers Previous Year<br>
# •	New Customers<br>
# •	Lost Customers<br>
# 

# In[4]:


# split data by year and check duplicates
data_2015 = data[data['year']==2015]
if len(data_2015['customer_email']) == len(set(data_2015['customer_email'])):
    print("Data in 2015 has no duplicates")
data_2016 = data[data['year']==2016]
if len(data_2016['customer_email']) == len(set(data_2016['customer_email'])):
    print("Data in 2016 has no duplicates")
data_2017 = data[data['year']==2017]
if len(data_2017['customer_email']) == len(set(data_2017['customer_email'])):
    print("Data in 2017 has no duplicates")


# # Total revenue for the current year

# In[5]:


total_revenue_2015 = np.sum(data_2015['net_revenue'])
print('Total Revenue in '+str(2015)+': '+str(total_revenue_2015))

total_revenue_2016 = np.sum(data_2016['net_revenue'])
print('Total Revenue in '+str(2016)+': '+str(total_revenue_2016))

total_revenue_2017 = np.sum(data_2017['net_revenue'])
print('Total Revenue in '+str(2017)+': '+str(total_revenue_2017))


# # New Customer Revenue e.g. new customers not present in previous year only

# In[6]:


# 2015 has no previous data
# split data by year
data_2015 = data[data['year']==2015]
data_2016 = data[data['year']==2016]
data_2017 = data[data['year']==2017]

df_new_customer_2016 = pd.merge(data_2015, data_2016, how='right', on=['customer_email'], indicator=True)
df_new_customer_2016 = df_new_customer_2016[df_new_customer_2016['_merge']=='right_only']
new_customer_revenue_2016 = np.sum(df_new_customer_2016['net_revenue_y'])
print('New Customer Revenue in '+str(2016)+': '+str(new_customer_revenue_2016))
      
df_new_customer_2017 = pd.merge(data_2016, data_2017, how='right', on=['customer_email'], indicator=True)
df_new_customer_2017 = df_new_customer_2017[df_new_customer_2017['_merge']=='right_only']
new_customer_revenue_2017 = np.sum(df_new_customer_2017['net_revenue_y'])
print('New Customer Revenue in '+str(2017)+': '+str(new_customer_revenue_2017))


# # Existing Customer Growth

# In[7]:


# 2015 has no previous data
df_existing_customer_2016 = pd.merge(data_2015, data_2016, how='right', on=['customer_email'], indicator=True)
df_existing_customer_2016 = df_existing_customer_2016[df_existing_customer_2016['_merge']=='both']
existing_customer_growth_2016 = np.sum(df_existing_customer_2016['net_revenue_y']) - np.sum(df_existing_customer_2016['net_revenue_x'])
print('Existing Customer Growth in '+str(2016)+': '+str(existing_customer_growth_2016))

df_existing_customer_2017 = pd.merge(data_2016, data_2017, how='right', on=['customer_email'], indicator=True)
df_existing_customer_2017 = df_existing_customer_2017[df_existing_customer_2017['_merge']=='both']
existing_customer_growth_2017 = np.sum(df_existing_customer_2017['net_revenue_y']) - np.sum(df_existing_customer_2017['net_revenue_x'])
print('Existing Customer Growth in '+str(2017)+': '+str(existing_customer_growth_2017))


# # Revenue lost from attrition

# In[8]:


# 2015 has no previous data
df_lost_customer_2016 = pd.merge(data_2015, data_2016, how='left', on=['customer_email'], indicator=True)
df_lost_customer_2016 = df_lost_customer_2016[df_lost_customer_2016['_merge']=='left_only']
revenue_lost_2016 = np.sum(df_lost_customer_2016['net_revenue_x'])
print('Revenue lost from attrition in '+str(2016)+': '+str(revenue_lost_2016))

df_lost_customer_2017 = pd.merge(data_2016, data_2017, how='left', on=['customer_email'], indicator=True)
df_lost_customer_2017 = df_lost_customer_2017[df_lost_customer_2017['_merge']=='left_only']
revenue_lost_2017 = np.sum(df_lost_customer_2017['net_revenue_x'])
print('Revenue lost from attrition in '+str(2017)+': '+str(revenue_lost_2017))


# # Existing Customer Revenue Current Year

# In[9]:


# 2015 has no previous data
existing_customer_revenue_2016 = np.sum(df_existing_customer_2016['net_revenue_y'])
print('Existing Customer Revenue in '+str(2016)+': '+str(existing_customer_revenue_2016))

existing_customer_revenue_2017 = np.sum(df_existing_customer_2017['net_revenue_y'])
print('Existing Customer Revenue in '+str(2017)+': '+str(existing_customer_revenue_2017))


# # Existing Customer Revenue Prior Year

# In[10]:


# 2015 has no previous data
existing_customer_revenue_2016 = np.sum(df_existing_customer_2016['net_revenue_x'])
print('Existing Customer Revenue in '+str(2016)+': '+str(existing_customer_revenue_2016))

existing_customer_revenue_2017 = np.sum(df_existing_customer_2017['net_revenue_x'])
print('Existing Customer Revenue in '+str(2017)+': '+str(existing_customer_revenue_2017))


# # Total Customers Current Year

# In[11]:


# Since we checked that there is no duplicate data in each year, we can just calculate the length of each sub-dataset
total_customers_2015 = len(data_2015)
print('Total Customers in '+str(2015)+': '+str(total_customers_2015))

total_customers_2016 = len(data_2016)
print('Total Customers in '+str(2016)+': '+str(total_customers_2016))

total_customers_2017 = len(data_2017)
print('Total Customers in '+str(2017)+': '+str(total_customers_2017))


# # Total Customers Previous Year

# In[12]:


# 2015 has no previous data
print('Total Customers in Previous Year('+str(2016)+'): '+str(total_customers_2015))

print('Total Customers in Previous Year('+str(2017)+'): '+str(total_customers_2016))


# # New Customers

# In[13]:


# 2015 has no previous data
new_customers_2016 = len(df_new_customer_2016)
print('New Customers in '+str(2016)+': '+str(new_customers_2016))

new_customers_2017 = len(df_new_customer_2017)
print('New Customers in '+str(2017)+': '+str(new_customers_2017))


# # Lost Customers

# In[14]:


# 2015 has no previous data
lost_customers_2016 = len(df_lost_customer_2016)
print('Lost Customers in '+str(2016)+': '+str(lost_customers_2016))

lost_customers_2017 = len(df_lost_customer_2017)
print('Lost Customers in '+str(2017)+': '+str(lost_customers_2017))


# In[ ]:




