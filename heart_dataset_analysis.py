# -*- coding: utf-8 -*-
"""Heart_Dataset_Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Sq71mFG8ECbg3mdjjqFgrrSUFuFlDUHD

**Import libraries**

---
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#import missingno as msno
# %matplotlib inline
from scipy import stats

"""**Import data file**

---
"""

df = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/heart_statlog_cleveland_hungary_final.csv")
df.head(10)

from google.colab import files
uploaded= files.upload()

df = pd.read_csv("heart_statlog_cleveland_hungary_final.csv")
df.head(10)

#Verifying the number of columns and rows
df.shape

# Column names
df.columns

#Data type information
df.info()

"""**Data Cleaning and pre-processing**

---


"""

df.columns = ['age', 'sex', 'chest_pain_type', 'resting_blood_pressure', 'cholesterol', 'fasting_blood_sugar', 'rest_ecg', 'max_heart_rate',
       'exercise_induced_angina', 'st_depression', 'st_slope','target']

df.info()

#Replacing the values to categorical values
df['chest_pain_type'][df['chest_pain_type'] == 1] = 'typical angina'
df['chest_pain_type'][df['chest_pain_type'] == 2] = 'atypical angina'
df['chest_pain_type'][df['chest_pain_type'] == 3] = 'non-anginal pain'
df['chest_pain_type'][df['chest_pain_type'] == 4] = 'asymptomatic'

df['rest_ecg'][df['rest_ecg'] == 0] = 'normal'
df['rest_ecg'][df['rest_ecg'] == 1] = 'ST-T wave abnormality'
df['rest_ecg'][df['rest_ecg'] == 2] = 'left ventricular hypertrophy'

df['st_slope'][df['st_slope'] == 1] = 'upsloping'
df['st_slope'][df['st_slope'] == 2] = 'flat'
df['st_slope'][df['st_slope'] == 3] = 'downsloping'

df['sex'] = df['sex'].apply(lambda  x: 'male' if x==1 else 'female')

df['target'] = df['target'].apply(lambda  x:'Cardiac_Disease' if x==1 else 'No_Cardiac_Disease')

df['chest_pain_type'].value_counts()

df['rest_ecg'].value_counts()

df['st_slope'].value_counts()

#remove the values which has 0
df.drop(df[df.st_slope ==0].index, inplace=True)
#checking distribution
df['st_slope'].value_counts()

"""1. Data types verification
---
"""

df.nunique()

df.dtypes

"""2. Finding the missing values and replace them

---


"""

df.isnull().sum()

"""There is no missing values in the dataset

3. Finding the duplicate rows
---
"""

repeated=df.duplicated().sum()
if repeated:
  print("Available duplicate rows are: {}".format(repeated))
else:
  print("There is no duplicate records")

repeated=df[df.duplicated(keep=False)]
repeated.head()

df=df.drop_duplicates()
df.shape

"""4. Statistics summary
---
"""

df.head()

df.describe()

df.describe(include=[np.object])

"""5. Find outliers and remove them
---
"""

df.shape

#Setting the style for visualization
plt.style.use('seaborn')
#Assign the sizing parameters
plt.rcParams['figure.figsize'] = [20, 10]

df.plot(kind='box', subplots=True, layout=(3,4),
        sharex=False,sharey=False, figsize=(20,10),
        color='purple');

"""Define the continuous variables and listing the outliers"""

Continuous_var=['age','resting_blood_pressure','cholesterol','max_heart_rate','st_depression']
def outliers(df_out, drop = False):
  for each_var in df_out.columns:
    feature_data = df_out[each_var]
    # 25th percentile of the data of the given feature
    Q1 = np.percentile(feature_data, 25.)
    # 75th percentile of the data of the given feature
    Q3 = np.percentile(feature_data, 75.)
    #Interquartile Range
    IQR = Q3-Q1
    Outlier_stage=IQR * 1.5
    outliers = feature_data[~((feature_data >= Q1 - Outlier_stage) & (feature_data <= Q3 + Outlier_stage))].index.tolist()
    if not drop:
            print('For the feature {}, No of Outliers is {}'.format(each_var, len(outliers)))
    if drop:
            df.drop(outliers, inplace = True, errors = 'ignore')
            print('Outliers from {} feature removed'.format(each_var))
outliers(df[Continuous_var])

#Removing outliers
outliers(df[Continuous_var],drop=True)

"""**HYPOTHESIS**

---

H1 : The higher the level of age , the higher the risk of getting cardiovascular disease among the male demographic.

H2 : The average age of a person who is having cardiovascular disease is higher than the the average age of a person who doesn't have a cardiovascular disease.

H3 : There is significant difference in the heart rate of the person who have cardiovascular disease compared to the person the who don't have cardiovascular disease.

H4 : The conditional probability of a cardiac person is relatively high when they have an angina after excercise.

H5 : There is an association between asymptomatic chestpain type and cardiovascular disease.The higher the level of asymptomatic chest pain , the higher the probability of having heart disease.

**Feature distribution and relationship among each others**

---

1. Continuous Features Distribution

---
"""

plt.style.use("dark_background")
plt.figure(figsize=(18,12))
plt.subplot(321)
diag= sns.distplot(df['age'], rug=True, color='yellow',label='Skewness : %.2f'%df['age'].skew())
plt.title("Age Distribution",fontsize=20,fontweight="bold")
plt.grid(False)
plt.legend()
plt.subplot(322)
plt.style.use("dark_background")
#sns.set(style='ticks')
diag= sns.distplot(df['cholesterol'], rug=True, color='cyan',label='Skewness : %.2f'%df['cholesterol'].skew())
plt.title("Cholesterol distribution", fontsize=20,fontweight="bold")
plt.grid(False)
plt.legend()
plt.show()
plt.figure(figsize=(18,12))
plt.subplot(323)
diag= sns.distplot(df['max_heart_rate'], rug=True, color='orange',label='Skewness : %.2f'%df['max_heart_rate'].skew())
plt.title("Max_Heart_Rate Distribution",fontsize=20,fontweight="bold")
plt.grid(False)
plt.legend()
plt.subplot(324)
#plt.style.use("dark_background")
#sns.set(style='ticks')
diag= sns.distplot(df['resting_blood_pressure'], rug=True, color='deeppink',label='Skewness : %.2f'%df['resting_blood_pressure'].skew())
plt.title("Resting Blood Pressure distribution", fontsize=20,fontweight="bold")
plt.grid(False)
plt.legend()
plt.show()
plt.figure(figsize=(18,4))
sns.distplot(df['st_depression'],color='blue',label='Skewness : %.2f'%df['st_depression'].skew())
plt.title("ST_Depression distribution", fontsize=20,fontweight="bold")
plt.grid(False)
plt.legend()

"""**Skewness** - It is a measurement to check whether the feature is normally distributed or not. If the skewness value is near to 0 then the particular feature is normally distributed.

From the above visualization, looks like all the features are normally distributed except st_depression.

To confirm this again, we will perform the normality test.
"""

CF = ['age','resting_blood_pressure','cholesterol','st_depression','max_heart_rate']
for i in CF:
    alpha= 0.005 #singificance-level
    c,p = stats.normaltest(df[i],nan_policy='omit')
    
    if p>alpha:
        print('{} ----> Normally distributed'.format(i))
    else:
        print('{} ---->  Not normally distributed'.format(i))

"""**H1 : The higher the level of age , the higher the risk of getting cardiovascular disease among the male demographic.**

**H2 : The average age of a person who is having cardiovascular disease is higher than the the average age of a person who doesn't have a cardiovascular disease.**
"""

#sns.set_style("ticks")
d1=df[df['target']=='No_Cardiac_Disease']
d2=df[df['target']=='Cardiac_Disease']
plt.style.use('dark_background')
age_heart_disease = df.groupby('target')['age']
fig, (axis1,axis2,axis3) = plt.subplots(1,3,figsize=(20,5))
ax = sns.distplot(df['age'],color='cyan',ax=axis1).set_title("Age Distribution")
plt.grid(False)
#ax.set(xlabel='Age')
#ax = sns.distplot(age_heart_disease.get_group('Cardiac_Disease'),ax=axis2)
ax = sns.distplot(d1['age'],color='yellow',ax=axis2)
ax.set(title="Age Distribution with No Cardiac Disease")
plt.grid(False)
#ax.set(xlabel='Age With No Cardiac Disease')
ax = sns.distplot(d2['age'],color='deeppink',ax=axis3)
ax.set(title="Age Distribution with Cardiac Disease")
#ax.set(xlabel='Age With Cardiac Disease')
plt.grid(False)

#Explore the average of age feature for Patients
print("Minimum Age:{}".format(min(df['age'])))
print("Maximum Age:{}".format(max(df['age'])))
print("Mean value of Age:{}".format(round(df.age.mean())))

#Explore the average of age feature for Non-Cardiac Patients
print("Minimum Age:{}".format(min(d1['age'])))
print("Maximum Age:{}".format(max(d1['age'])))
print("Mean value of Age:{}".format(round(d1.age.mean())))

#Explore the average of age feature for Cardiac Patients
print("Minimum Age:{}".format(min(d2['age'])))
print("Maximum Age:{}".format(max(d2['age'])))
print("Mean value of Age:{}".format(round(d2.age.mean())))

"""Target Variable Distribution

---


"""

print(df.target.value_counts())

plt.style.use('dark_background')
df['target'] = df.target.replace({1: "Cardio_Disease", 0: "No_Cardio_Disease"})
figure, axis = plt.subplots(figsize=(5,4))
category = ["Cardio_Disease", "No_Cardio_Disease"]
axis = df.target.value_counts().plot(kind='bar')
axis.set_title("Cardiovascular Disease category", fontsize = 18, weight = 'bold')
axis.set_xticklabels (category, rotation = 0)

#Percentage calculation for cardio disease category
aggregated = []
for i in axis.patches:
    aggregated.append(i.get_height())
total = sum(aggregated)
for i in axis.patches:
    axis.text(i.get_x()+.09, i.get_height()-50, \
            str(round((i.get_height()/total)*100, 2))+'%', fontsize=14,
                color='blue', weight = 'bold')    
plt.tight_layout()
plt.show()

#Plotting based on the target variable
plt.style.use('seaborn')
figure, (axis1, axis2) = plt.subplots(nrows=1, ncols=2, sharey=False, figsize=(14,6))
colors = ("lightgreen","cyan")
axis1 = df['target'].value_counts().plot.pie( x="Cardiovascular disease" ,y ='Patients Count', 
                                             autopct = "%1.0f%%",labels=["Cardiac_disease","No_Cardiac_disease"], startangle = 60, ax=axis1, colors=colors)
axis1.set(title = 'Percentage of Cardiovascular disease patients')

axis2 = df["target"].value_counts().plot.barh(ax =axis2, color=colors)
for i,j in enumerate(df["target"].value_counts().values):
    axis2.text(.5,i,j,fontsize=12)
axis2.set(title = 'No.of patients affected by cardiovascular disease')
plt.subplots_adjust(left=0.1,
                    right=1.5)
plt.show()

plt.style.use('seaborn-bright')
sns.distplot(d1['age'],label='Non_Cardiac_Disease',color='#03ED3A')
sns.distplot(d2['age'],label='Cardiac_Disease',color='#E8000B')
plt.legend()
plt.grid(False)
plt.title('Density of Age')

x = []
for i in range(0,len(df)):
    if((df['age'].iloc[i] > 0) & (df['age'].iloc[i] < 20)):
        x.append('0-20')
    elif((df['age'].iloc[i] > 20) & (df['age'].iloc[i] < 40) ):
        x.append('21-50')
    elif((df['age'].iloc[i] > 40) & (df['age'].iloc[i] < 60) ):
        x.append('51-60')
    else:
        x.append('> 60')
        
df['Group_Age'] = x

!pip install squarify

import matplotlib.pyplot as plt
import squarify

df['target'] = df['target'].apply(lambda  x:1 if x=='Cardiac_Disease' else 0)

df['target']

fig,(axis1,axis2) = plt.subplots(1,2,figsize=(20,5))
df['Group_Age'].value_counts()
labels = df['Group_Age'].value_counts().index
sizes = df['Group_Age'].value_counts().values
colors = ['lightgreen', 'cyan', 'pink']

perc = [str('{:5.2f}'.format(i/df['Group_Age'].value_counts().sum()*100)) + "%" for i in df['Group_Age'].value_counts()]
lbl = ["Age" + " " + el[0] + " = " + el[1] for el in zip(df['Group_Age'].value_counts().index, perc)]
#squarify.plot(sizes=sizes, label=lbl, alpha=.8,ax=axis1)
#squarify.plot(label=lbl,ax=axis,sizes=sizes)
squarify.plot(sizes=sizes,color=colors,label = lbl,ax=axis1)
#plt.axis('off')


plt.title('Age group Category')
sns.barplot(x='Group_Age',y='target',hue='sex',data=df,palette="rocket",ci=None,ax=axis2)
plt.figure(figsize=(18,12))
plt.subplot(233)
df["sex"].value_counts().plot.pie(autopct = "%1.0f%%",colors = sns.color_palette("gist_rainbow",5),startangle = 60,labels=["Male","Female"],
wedgeprops={"linewidth":2,"edgecolor":"k"},explode=[.1,.1],shadow =True)
plt.title("Gender Distribution",fontsize=20,fontweight="bold")
#plt.title('Age Group Vs Sex Vs Target')
#sns.barplot(x='sex',y='target',data=df,palette="coolwarm",ci=None,ax=axis3)
#plt.title('Sex Vs Target')

import scipy.stats as st
import math
t,p=st.ttest_ind(d1['age'], d2['age'], equal_var = False)
r = math.sqrt(t**2/(t**2 + ( 507+ 410 - 2)))
print("T-Test result for H1 Hypothesis:")
print("T Value =", round(t, 3))
print("P value =", round(p, 3))
print("Effect Size (r) =", round(r, 3))

"""**RESULT:**
From the above Density of Age visualization, we can observe that age distribution of the Non-Cardic patient is shifted downward when compared to the age distribution of cardiac patient.

The maximum cardiovascular disease is affected by the people aged over 55.

Based on the testing, p value is less than 0.05 and the effect size (r) is 
0.279 which indicates that our alternate hypothesis true that is the average age of a person is having cardiovascular disease is higher than the person who doesn't have a cardiovascular disease and mostly among the male demographic.

**H3 : The probability of the Cardiovascular disease patient heart rate is higher than the non-cardiovascular disease patient heart rate.**

Maximum Heart Rate

---
"""

plt.style.use('dark_background')
#age_heart_disease = df.groupby('target')['max_heart_rate']
fig, (axis1,axis2,axis3) = plt.subplots(1,3,figsize=(20,5))
ax = sns.distplot(df['max_heart_rate'],color='cyan',ax=axis1).set_title("Max_Heart_Rate Distribution")
plt.grid(False)
#ax.set(xlabel='Age')
#ax = sns.distplot(age_heart_disease.get_group('Cardiac_Disease'),ax=axis2)
ax = sns.distplot(d1['max_heart_rate'],color='yellow',ax=axis2)
ax.set(title="Max_Heart_Rate Distribution with No Cardiac Disease")
plt.grid(False)
#ax.set(xlabel='Age With No Cardiac Disease')
ax = sns.distplot(d2['max_heart_rate'],color='deeppink',ax=axis3)
ax.set(title="Max_Heart_Rate Distribution with Cardiac Disease")
plt.grid(False)
#ax.set(xlabel='Age With Cardiac Disease')

"""Two Sample T-test with unequal Variance

---


"""

mean = df.groupby('target')['max_heart_rate'].mean()
std = df.groupby('target')['max_heart_rate'].std()
stat = pd.DataFrame({'Group':['No_Cardiac_Disease','Cardiac_Disease'],'Max_heart_rate_Mean':mean.values,'Max_heart_rate_Std':std.values,
                       'Sample_Size':[len(d1['max_heart_rate']),len(d2['max_heart_rate'])]})
stat

plt.style.use('seaborn-whitegrid')
d1['max_heart_rate'].plot.hist(bins = 30, color='m',edgecolor = 'white', 
linewidth = 1.0, label = 'Non_Cardiac Patients')
d2['max_heart_rate'].plot.hist(bins = 30, color='#00D7FF',edgecolor = 'white', 
linewidth = 1.0, alpha = 0.6, label = 'Cardiac_Patients')
plt.title('Cardiac Patient Heart Rate Vs Non-Cardiac Patient Heart Rate', 
fontsize = 20)
plt.xlabel('Heart_Rate', fontsize = 14)
plt.ylabel('Frequency', fontsize = 14)
plt.legend(fontsize = 14)
plt.grid(False)

plt.style.use('seaborn-talk')
#sns.distplot(d1['max_heart_rate'],label='Non_Cardiac_Disease',color='#03ED3A')
sns.distplot(d1['max_heart_rate'],label='Non_Cardiac_Disease',color='m')
sns.distplot(d2['max_heart_rate'],label='Cardiac_Disease',color='y')
#sns.distplot(d2['max_heart_rate'],label='Cardiac_Disease',color='#E8000B')
plt.legend()
plt.grid(False)
plt.title('Density of Heart Rate')

t,p=st.ttest_ind(d1['max_heart_rate'], d2['max_heart_rate'], equal_var = False)
r = math.sqrt(t**2/(t**2 + ( 507+ 410 - 2)))
print("T-Test result for H2 Hypothesis:")
print("T Value =", round(t, 3))
print("P Value =", round(p, 3))
print("Effect Size (r) =", round(r, 3))

"""**RESULT**:

Based on the above figure and testing, the p value is 0.00 and the effect size is 0.401. This resultant that the heart rate of the cardiac person is significantly different from the non-cardiac patient.

**H4 : The conditional probability of a cardiac person is relatively high when they have an angina after excercise.**
"""

figure, axis = plt.subplots(figsize=(8,5))
Category = d2['exercise_induced_angina']
axis = sns.countplot(x='exercise_induced_angina', hue='target', data=df, palette='hsv')
axis.set_title("Exang Distribution based on the Target", fontsize = 16, weight = 'bold')
axis.set_xticklabels (Category, rotation = 0)

Aggregated = []
for i in axis.patches:
    Aggregated.append(i.get_height())
total = sum(Aggregated)
for i in axis.patches:
    axis.text(i.get_x()+.05, i.get_height()-15,
            str(round((i.get_height()/total)*100, 2))+'%', fontsize=14,
                color='white', weight = 'bold')  
plt.tight_layout()
plt.grid(False)

cp =pd.crosstab(df['target'],df['exercise_induced_angina'],margins=True)
cp

!pip install researchpy
import researchpy as rp

df['target'] = df.target.replace({1: "Cardio_Disease", 0: "No_Cardio_Disease"})

crtb, test, expt = rp.crosstab(df['chest_pain_type'], df['target'], test = "chi-square", expected_freqs = True)
#crtb, test, expt = rp.crosstab(df['exercise_induced_angina'], df['target'], test = "chi-square", expected_freqs = True)
print('\033[1m' + 'CROSSTAB:'+ '\033[0m'+ '\n{}'.format(crtb))
print('\033[1m' + '\nCHI-SQUARE TEST:'+ '\033[0m'+ '\n{}'.format(test))
print('\033[1m' + '\nEXPECTED COUNT:'+ '\033[0m'+ '\n{}'.format(expt))

#Calculate the confidence
mp = (371/917)
support=(316/917)
confidence=(support/mp)
print("Confidence: {}".format(confidence))

"""**RESULT**:

The confidence rate is 85% which indicates that if the person is having exercise induced angina then he/she has 85% of probability to have a cardiac disease.

**H5 : There is an association between asymptomatic chestpain type and cardiovascular disease impact**

Chestpain distribution with respect to target variable

---
"""

df['target'] = df['target'].apply(lambda  x:'Cardiac_Disease' if x==1 else 'Non_Cardiac_Disease')

plt.style.use("dark_background")
figure, axis = plt.subplots(figsize=(10,5))
Category = d2['chest_pain_type']
axis = sns.countplot(x='chest_pain_type', hue='target', data=df, palette='Set1')
axis.set_title("Chest Pain Distribution based on the Target", fontsize = 16, weight = 'bold')
axis.set_xticklabels (Category, rotation = 0)

Aggregated = []
for i in axis.patches:
    Aggregated.append(i.get_height())
total = sum(Aggregated)
for i in axis.patches:
    axis.text(i.get_x()+.03, i.get_height()-5,
            str(round((i.get_height()/total)*100, 2))+'%', fontsize=14,
                color='white', weight = 'bold')  
plt.tight_layout()
plt.grid(False)

d2['chest_pain_type'].value_counts()
pd.crosstab(df['chest_pain_type'], df['target'],margins = True,normalize = 'index')

plt.style.use('dark_background')
#plt.title('Chest Pain Type Vs Gender')
#pd.crosstab(d2['chest_pain_type'], d2['sex'],normalize = 'columns').plot.bar(title='Chest Pain Type Vs Gender',color=['lightgreen','m'])
pd.crosstab(df['chest_pain_type'], df['target'],normalize = 'columns').plot.bar(title='Chest Pain Type Vs Target',color=['m','lightgreen'],stacked=True)
#ax.get_xaxis().set_visible(True)
plt.grid(False)

"""As it is a categorical feature, we are running a chi-square test"""

!pip install researchpy
import researchpy as rp

#crtb, test, expt = rp.crosstab(df['chest_pain_type'], df['target'], test = "chi-square", expected_freqs = True)
crtb, test, expt = rp.crosstab(df['chest_pain_type'], df['target'], test = "chi-square", expected_freqs = True)
print('\033[1m' + 'CROSSTAB:'+ '\033[0m'+ '\n{}'.format(crtb))
print('\033[1m' + '\nCHI-SQUARE TEST:'+ '\033[0m'+ '\n{}'.format(test))
print('\033[1m' + '\nEXPECTED COUNT:'+ '\033[0m'+ '\n{}'.format(expt))

#df['target'] = df['target'].apply(lambda  x:'Cardiac_Disease' if x==1 else 'Non_Cardiac_Disease')
#d3=df[df['chest_pain_type']=='asymptomatic']
#d3['chest_pain_type'] = d3['chest_pain_type'].apply(lambda  x:1 if x=='asymptomatic' else 0)
df['chest_pain_type'] = df['chest_pain_type'].apply(lambda  x:1 if x=='asymptomatic' else 0)
#d1=df[df['target']=='No_Cardiac_Disease']

df['chest_pain_type'].nunique()

crtb, test, expt = rp.crosstab(df['chest_pain_type'], df['target'], test = "chi-square", expected_freqs = True)
print('\033[1m' + 'CROSSTAB:'+ '\033[0m'+ '\n{}'.format(crtb))
print('\033[1m' + '\nCHI-SQUARE TEST:'+ '\033[0m'+ '\n{}'.format(test))
print('\033[1m' + '\nEXPECTED COUNT:'+ '\033[0m'+ '\n{}'.format(expt))

"""**RESULT**

With regards to chi-square value (1) = 193.8514, 𝑝 < .001, 𝑝ℎ𝑖 =.52. There was a significant association between the asymptomatic chest pain type of a person and the cardiovascular disease

**Target Variable Distribution**
"""

plt.style.use("dark_background")
plt.rcParams['figure.figsize'] = [10, 10]
df['age'].plot.hist(bins = 50, edgecolor = 'deeppink', linewidth = 1.0)
plt.ylabel('Frequency', fontsize = 14) # y-axis label
plt.xlabel('Age', fontsize = 14) # x-axis label
plt.title('Age Distribution', fontsize = 18) # main title
plt.show()

#Explore the distribution of age feature in range
print("Minimum Age:{}".format(min(df['age'])))
print("Maximum Age:{}".format(max(df['age'])))
print("Mean value of Age:{}".format(round(df.age.mean())))

"""Gender Distribution with respect to target variable"""

plt.style.use("seaborn")
#df['target'] = df.target.replace({1: "Cardio_Disease", 0: "No_Cardio_Disease"})
#df['sex'] = df.sex.replace({1: "Male", 0: "Female"})
figure, axis = plt.subplots(figsize=(8,5))
Category = df['sex']
axis = sns.countplot(x='sex', hue='target', data=df, palette='Set3')
axis.set_title("Gender Distribution based on the Target", fontsize = 16, weight = 'bold')
axis.set_xticklabels (Category, rotation = 0)

Aggregated = []
for i in axis.patches:
    Aggregated.append(i.get_height())
total = sum(Aggregated)
for i in axis.patches:
    axis.text(i.get_x()+.05, i.get_height()-15,
            str(round((i.get_height()/total)*100, 2))+'%', fontsize=14,
                color='blue', weight = 'bold')  
plt.tight_layout()
plt.grid(False)

"""Chestpain distribution with respect to target variable"""

plt.style.use("dark_background")
figure, axis = plt.subplots(figsize=(10,5))
Category = df['chest_pain_type']
axis = sns.countplot(x='chest_pain_type', hue='target', data=df, palette='Set1')
axis.set_title("Chest Pain Distribution based on the Target", fontsize = 16, weight = 'bold')
axis.set_xticklabels (Category, rotation = 0)

AGgregated = []
for i in axis.patches:
    Aggregated.append(i.get_height())
total = sum(Aggregated)
for i in axis.patches:
    axis.text(i.get_x()+.03, i.get_height()-5,
            str(round((i.get_height()/total)*100, 2))+'%', fontsize=14,
                color='white', weight = 'bold')  
plt.tight_layout()
plt.grid(False)

"""Fasting Blood Sugar distribution with respect to target variable"""

#df['target'] = df['target'].replace({1: "Cardio_Disease", 0: "No_Cardio_Disease"})
df['fasting_blood_sugar'] = df['fasting_blood_sugar'].replace({1: "True", 0: "False"})
figure, axis = plt.subplots(figsize=(8,5))
Category = df['fasting_blood_sugar']
axis = sns.countplot(x='fasting_blood_sugar', hue='target', data=df, palette='Set1')
axis.set_title("Blood sugar before food Distribution based on the Target", fontsize = 16, weight = 'bold')
axis.set_xticklabels (Category, rotation = 0)

Aggregated = []
for i in axis.patches:
    Aggregated.append(i.get_height())
total = sum(Aggregated)
for i in axis.patches:
    axis.text(i.get_x()+.05, i.get_height()-15,
            str(round((i.get_height()/total)*100, 2))+'%', fontsize=14,
                color='white', weight = 'bold')  
plt.tight_layout()
plt.grid(False)

"""Slope Distribution with respect to Target"""

df.nunique()

#df['fasting_blood_sugar'] = df['fasting_blood_sugar'].replace({1: "True", 0: "False"})
figure, axis = plt.subplots(figsize=(8,5))
Category = df['st_slope']
axis = sns.countplot(x='st_slope', hue='target', data=df, palette='rocket')
axis.set_title("ST-Segment Distribution based on the Target", fontsize = 16, weight = 'bold')
axis.set_xticklabels (Category, rotation = 0)

Aggregated = []
for i in axis.patches:
    Aggregated.append(i.get_height())
total = sum(Aggregated)
for i in axis.patches:
    axis.text(i.get_x()+.05, i.get_height()-15,
            str(round((i.get_height()/total)*100, 2))+'%', fontsize=14,
                color='white', weight = 'bold')  
plt.tight_layout()
plt.grid(False)

"""**Chest Pain Type Distribution**"""

# Non-Cardiac Patients 
fig = plt.figure(figsize=(15,5))
a1 = plt.subplot2grid((1,2),(0,0))
#colors= ['Green','Orange','Purple','Cyan']
a2=sns.countplot(d1['chest_pain_type'],palette="CMRmap")
plt.title('Chest Pain Distribution of Non-Cardiac Patients', fontsize=15, weight='bold')
Aggregated = []
for i in a2.patches:
    Aggregated.append(i.get_height())
total = sum(Aggregated)
for i in a2.patches:
    a2.text(i.get_x()+.05, i.get_height()-15,
            str(round((i.get_height()/total)*100, 2))+'%', fontsize=14,
                color='white', weight = 'bold') 
plt.grid(False)

# Cardiac Patients
ax1 = plt.subplot2grid((1,2),(0,1))
a2=sns.countplot(d2['chest_pain_type'], palette='hsv')
plt.title('Chest Pain Distribution of Cardiac Patients', fontsize=15, weight='bold')
Aggregated = []
for i in a2.patches:
    Aggregated.append(i.get_height())
total = sum(Aggregated)
for i in a2.patches:
    a2.text(i.get_x()+.05, i.get_height()-15,
            str(round((i.get_height()/total)*100, 2))+'%', fontsize=14,
                color='white', weight = 'bold') 
plt.grid(False)
#plt.subplots_adjust(left=0.0, right=1.5)
plt.show()

"""**REST ECG DISTRIBUTION**"""

# Non-Cardiac patients
fig = plt.figure(figsize=(15,5))
a1 = plt.subplot2grid((1,2),(0,0))
a2=sns.countplot(d1['rest_ecg'],palette='Accent_r')
plt.title('Rest ECG Distribution of Non-Cardiac Patients', fontsize=15, weight='bold')
Aggregated = []
for i in a2.patches:
    Aggregated.append(i.get_height())
total = sum(Aggregated)
for i in a2.patches:
    a2.text(i.get_x()+.05, i.get_height()-15,
            str(round((i.get_height()/total)*100, 2))+'%', fontsize=10,
                color='Black', weight = 'bold') 
plt.grid(False)

#Cardiac patients
a1 = plt.subplot2grid((1,2),(0,1))
a2=sns.countplot(d2['rest_ecg'], palette='viridis')
plt.title('Rest ECG Distribution of Cardiac Patients', fontsize=15, weight='bold' )
Aggregated = []
for i in a2.patches:
    Aggregated.append(i.get_height())
total = sum(Aggregated)
for i in a2.patches:
    a2.text(i.get_x()+.05, i.get_height()-15,
            str(round((i.get_height()/total)*100, 2))+'%', fontsize=14,
                color='white', weight = 'bold') 
plt.grid(False)
plt.show()

"""**ST-SLOPE DISTRIBUTION**"""

fig = plt.figure(figsize=(15,5))
a1 = plt.subplot2grid((1,2),(0,0))
a2=sns.countplot(d1['st_slope'],palette='hsv_r')
plt.title('ST SLOPE Distribution of Non-Cardiac Patients', fontsize=15, weight='bold')
Aggregated = []
for i in a2.patches:
    Aggregated.append(i.get_height())
total = sum(Aggregated)
for i in a2.patches:
    a2.text(i.get_x()+.05, i.get_height()-15,
            str(round((i.get_height()/total)*100, 2))+'%', fontsize=14,
                color='deeppink', weight = 'bold') 
plt.grid(False)

#Cardiac patients
a1 = plt.subplot2grid((1,2),(0,1))
a2=sns.countplot(d2['st_slope'], palette='hsv')
plt.title('ST SLOPE Distribution of Cardiac Patients', fontsize=15, weight='bold' )
Aggregated = []
for i in a2.patches:
    Aggregated.append(i.get_height())
total = sum(Aggregated)
for i in a2.patches:
    a2.text(i.get_x()+.05, i.get_height()-15,
            str(round((i.get_height()/total)*100, 2))+'%', fontsize=14,
                color='white', weight = 'bold') 
plt.grid(False)
plt.show()

"""**NUMERICAL VALUES DISTRIBUTION**"""

plt.style.use('seaborn')
colors=['blue','orange']
customPalette = sns.set_palette(sns.color_palette(colors))
sns.pairplot(df, hue = 'target', vars = ['age', 'resting_blood_pressure', 'cholesterol','max_heart_rate','st_depression'],palette= customPalette)
plt.grid(False)

plt.style.use('dark_background')
plt.rcParams['figure.figsize'] = [10, 6]
colors=['blue','white']
customPalette = sns.set_palette(sns.color_palette(colors))
a1 = plt.subplot2grid((1,2),(0,0))
sns.scatterplot(x = 'max_heart_rate', y = 'resting_blood_pressure', hue = 'target', data = df,palette=customPalette)
plt.title("Max_heart_rate Vs Age",weight='bold')
plt.grid(False)

plt.style.use('dark_background')
plt.rcParams['figure.figsize'] = [10, 6]
colors=['deeppink','cyan']
customPalette = sns.set_palette(sns.color_palette(colors))
a1 = plt.subplot2grid((1,2),(0,0))
sns.scatterplot(x = 'cholesterol', y = 'max_heart_rate', hue = 'target', data = df,palette=customPalette)
plt.title("Max_heart_rate Vs Age",weight='bold')
plt.grid(False)

plt.style.use('dark_background')
plt.rcParams['figure.figsize'] = [10, 6]
colors=['yellow','green']
customPalette = sns.set_palette(sns.color_palette(colors))
a1 = plt.subplot2grid((1,2),(0,0))
sns.scatterplot(x = 'max_heart_rate', y = 'age', hue = 'target', data = df,palette=customPalette)
plt.title("Max_heart_rate Vs Age",weight='bold')
plt.grid(False)

colors=['red','white']
customPalette = sns.set_palette(sns.color_palette(colors))
a1 = plt.subplot2grid((1,2),(0,1))
sns.scatterplot(x = 'max_heart_rate', y = 'cholesterol', hue = 'target', data = df, palette=customPalette)
plt.title("Max_heart_rate Vs Cholesterol",weight='bold')
plt.grid(False)

plt.style.use('dark_background')
plt.rcParams['figure.figsize'] = [10, 6]
colors=['red','white']
customPalette = sns.set_palette(sns.color_palette(colors))
a1 = plt.subplot2grid((1,2),(0,0))
sns.scatterplot(x = 'resting_blood_pressure', y = 'age', hue = 'target', data = df,palette=customPalette)
plt.title("Rest_Blood_Pressure Vs Age",weight='bold')
plt.grid(False)

colors=['red','white']
customPalette = sns.set_palette(sns.color_palette(colors))
a1 = plt.subplot2grid((1,2),(0,1))
sns.scatterplot(x = 'resting_blood_pressure', y = 'st_depression', hue = 'target', data = df, palette=customPalette)
plt.title("Rest_Blood_Pressure Vs St_Depression",weight='bold')
plt.grid(False)

plt.style.use('dark_background')
plt.rcParams['figure.figsize'] = [10, 6]
colors=['red','white']
customPalette = sns.set_palette(sns.color_palette(colors))
a1 = plt.subplot2grid((1,2),(0,0))
sns.scatterplot(x = 'resting_blood_pressure', y = 'cholesterol', hue = 'target', data = df,palette=customPalette)
plt.title("Rest_Blood_Pressure Vs Cholesterol",weight='bold')
plt.grid(False)

colors=['red','white']
customPalette = sns.set_palette(sns.color_palette(colors))
a1 = plt.subplot2grid((1,2),(0,1))
sns.scatterplot(x = 'resting_blood_pressure', y = 'age', hue = 'target', data = df, palette=customPalette)
plt.title("Rest_Blood_Pressure Vs Age",weight='bold')
plt.grid(False)

"""**WORKING WITH OUTLIERS**"""

df_numerical = df[['age','resting_blood_pressure','cholesterol','max_heart_rate','st_depression']]

df_numerical.head()

zs = np.abs(stats.zscore(df_numerical))
print(zs)

threshold = 3
print(np.where(zs > 3))

df = df[(zs < 3).all(axis=1)]

"""**CORRELATION BETWEEN FEATURES**"""

df['target'] = df['target'].apply(lambda  x:1 if x=='Cardiac_Disease' else 0)

sns.set(style="white") 
plt.rcParams['figure.figsize'] = (15, 10) 
sns.heatmap(df.corr(), annot = True, linewidths=.5, cmap="YlGnBu")
plt.title('Corelation Between Variables', fontsize = 20)
plt.show()

"""Based on the above visual,
1. There is no multicollinearity between the features.
2. Age,Chest_pain_type and exercise_induced_angina, are having positive correlation with the target feature.
3. Max_heart_rate is having negative correlation with the target feature.
4. Other features are having low correlation with the target feature.
"""

sns.set_style('darkgrid')
sns.set_palette('Blues_r')
plt.figure(figsize = (13,6))
plt.title('Distribution of correlation of features')
abs(df.corr()['target']).sort_values()[:-1].plot.barh()
#abs(df.corr()['target'])
plt.show()

"""The features exerise_induced_angina, chest_pain_type, st_depression, max_heart rate and age are having better correlation with the target feature in total.

**Prediction Model Build**

**Logistic Regression**
"""

df['target'] = df['target'].apply(lambda  x:1 if x=='Cardiac_Disease' else 0)

df['target'].nunique()

# To get key statistics for each of the target groups on selected variables, run:
df[['cholesterol', 'age', 'resting_blood_pressure', 'max_heart_rate']].groupby(df['target']).describe().round(3)

df.shape

#Pairplot
colors=['blue','orange']
customPalette = sns.set_palette(sns.color_palette(colors))
sns.pairplot(df, vars = ['target', 'cholesterol', 'age','resting_blood_pressure','max_heart_rate'], hue = 'target', palette=customPalette)

df.isnull().sum()

# 1. Linearity of independent variables and log odds
# Creating log transformed IVs & 
# Obtain interaction terms between each predictor and the log of itself.
import statsmodels.api as sm
df['cholesterol_int'] = np.log(df['cholesterol'])*df['cholesterol']
df['age_int'] = np.log(df['age'])*df['age']
df['rbs_int'] = np.log(df['resting_blood_pressure'])*df['resting_blood_pressure']
df['mhr_int'] = np.log(df['max_heart_rate'])*df['max_heart_rate']

df['cholesterol_int'].fillna((df['cholesterol_int'].mean()), inplace=True)
df['rbs_int'].fillna((df['rbs_int'].mean()), inplace=True)

x = df[['cholesterol', 'age', 'resting_blood_pressure', 'max_heart_rate','cholesterol_int','age_int','rbs_int','mhr_int']]
x = sm.add_constant(x)
y = df ['target']
# Checking the assumption - met the assumption as p-values for the interaction terms >.05.
logit_assump = sm.Logit(y, x)
print(logit_assump.fit().summary())

#Cholesterol and cholesterol_int P values is 0.0 which is less than 0.05 so, this feature doesn't the linerarity assumption of logistic regression. Due to this we are removing this variable

df[['cholesterol', 'age', 'resting_blood_pressure', 'max_heart_rate']].corr().round(3)
plt.subplots(figsize=(10, 6))
corrMatrix = df[['cholesterol', 'age', 'resting_blood_pressure', 'max_heart_rate']].corr()
sns.heatmap(corrMatrix, annot = True, cmap="OrRd")

#Split the data 30/70
from sklearn.model_selection import train_test_split
x = df[['age', 'resting_blood_pressure', 'max_heart_rate']]
x = sm.add_constant(x)
#x = df[['age', 'max_heart_rate']]
y = df ['target']
log_mdl = sm.Logit(df['target'], x).fit()
print(log_mdl.summary2()) 
#x_train, x_test, y_train, y_test =  train_test_split(x,y, test_size = 0.30, random_state = 8)
print("-2LL:", log_mdl.llr.round(3))
print("p-value:", log_mdl.llr_pvalue.round(3))

"""Coefficients are difficult to interpret in logistic regression models, so we will transform them into odds ratios by calculating the exponent raised to the power of coefficients."""

print("* Odds ratio for AGE:", np.exp(0.0354).round(3))
print("* Odds ratio for RBP:", np.exp(0.0042).round(3))
print("* Odds ratio for MHR:", np.exp(-0.0324).round(3))

#Confusion Matrix
# Calculating predicted y-values for each var by using the ‘predict’ function:
y_pred = log_mdl.predict(x)
from sklearn.metrics import (confusion_matrix, accuracy_score)

# Create a confusion matrix
cm = confusion_matrix(y, y_pred.round()) 
print("Confusion Matrix : \n", cm)

## Calculate the accuracy score of the model
print('Test accuracy = ', accuracy_score(y, y_pred.round()))

print(classification_report(y_train, y_train_pred.round()))

#Splitting the dataset (30/70)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.30, random_state = 8)
x_train = sm.add_constant(x_train) # Add the constant
log_mdl = sm.Logit(y_train, x_train).fit() # Fit a model
print(log_mdl.summary2()) 

from sklearn.metrics import (confusion_matrix, accuracy_score, classification_report)
y_train_pred = log_mdl.predict(x_train)
# confusion matrix
# labels on the test data vs. predicted data
cm = confusion_matrix(y_train, y_train_pred.round())
print ("Confusion Matrix : \n", cm) # introducing a new line
# accuracy score of the model
print('Test accuracy = ', accuracy_score(y_train, y_train_pred.round()))

print(classification_report(y_train, y_train_pred.round()))

"""**Model Evaluation**"""

# performing predictions on the test datdaset
x_test = sm.add_constant(x_test) # Add the constant
y_test_pred = log_mdl.predict(x_test)
# confusion matrix
cm = confusion_matrix(y_test, y_test_pred.round()) 
print ("Confusion Matrix : \n", cm)
# accuracy scores of the model
print('Test accuracy = ', accuracy_score(y_test, y_test_pred.round()))
print(classification_report(y_test, y_test_pred.round()))