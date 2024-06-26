# -*- coding: utf-8 -*-
"""EDA Student performance.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14Oz4wdHQc7YgbMG5zKADRVWHrOeeZE02

Lifecyle of ML Projects:

1. Understand the problem statement
2. Data collection
3. Data check
4. EDA
5. Data preprocessing
6. Model selection and model training
7. Model evaluation

1. Understand the problem statement

How the other factors such as gender, ethnicity are affect the students performance

2. Data Collection
Collect data from the specific site or specific source

3. Data check
Import data and understand the dataset
"""

import pandas as pd

df = pd.read_csv('stud.csv')
df.head()

df.columns

# missing values
df.isna().sum()

"""No null values are available in the dataset"""

# check the duplicates

df.duplicated().sum()

"""No duplicated values are available"""

# check the datatypes

df.info()

# check the unique values

df.nunique()

x = df['gender'].unique()
print("unique categories in Gender: ")
print(x)

x1 = df['race_ethnicity'].unique()
print("unique category in the race enthnicity: ")
print(x1)

## define the numerical  and categorical features

numerical_features = [feature for feature in df.columns if df[feature].dtype != 'O']
print("numerical_features: ")
print(numerical_features)

categorical_features = [feature for feature in df.columns if df[feature].dtype == 'O']
print("categorical_features: ")
print(categorical_features)

## add total score colum

df['total_score'] = df['math_score'] + df['reading_score'] + df['writing_score']
df.head()

## add average score column
df['average'] = df['total_score'] / len(numerical_features)
df.head()

## number of students have a full marks in maths or less than 20 marks in maths

Full_marks = df[df['math_score'] == 100]['gender'].count()
Full_marks
print(f"Full marks: {Full_marks}")

less_than_20 = df[df['math_score'] <= 20]['gender'].count()
print(f'less than 20 marks: {less_than_20}')

"""From above we can get the full marks and worst marks in each category for i.e. maths, writing and reading.

Moreover, we can get the number of students who has a total highest marks and average of it. We can also calculate the percentage of the students from the above details.

EDA
"""

import matplotlib.pyplot as plt
import seaborn as sns

sns.histplot(data = df, x= 'average')

sns.histplot(data = df, x = 'total_score')

"""Model selection and model training"""

## created X and y data based on we are going to evaluate
y = df['math_score']
X = df.drop('math_score', axis = 1)
X.head()

## convert categorical features into the numerical features using the one hot encoding method and
## convert numerical features into standarization using StandardScaler

import numpy as np
num_features = X.select_dtypes(exclude='object').columns
cat_features = X.select_dtypes(include='object').columns

print(num_features)
print(cat_features)

from sklearn.preprocessing import OneHotEncoder, StandardScaler

standard_scaler = StandardScaler()
onehotencoding = OneHotEncoder()

from sklearn.compose import ColumnTransformer

preprocessor = ColumnTransformer(
    [
        ("oneHotEncoder", onehotencoding, cat_features),
        ('StandardScaler', standard_scaler, num_features)
    ]
)

X = preprocessor.fit_transform(X)

X.shape

y.shape

## divide dataset into train and test set

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30)

print(X_train.shape)
print(y_train.shape)

print(X_test.shape)
print(y_test.shape)

## Models

from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor


models = {
    "Linear regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(),
    "KNN": KNeighborsRegressor(),
    'Ridge': Ridge(),
    'Lasso': Lasso()
}

## Evaluate model function

from sklearn.metrics import mean_absolute_error, mean_squared_error


def evaluate_model(true, predicted):
  mae = mean_absolute_error(true, predicted)
  mse = mean_squared_error(true, predicted)
  rmse = np.sqrt(mse)
  return mae, mse, rmse

## train model

for i in range(len(list(models))):
  model = list(models.values())[i]
  model.fit(X_train, y_train)
  print(f"model:: {model}")
  ## predct
  y_train_pred = model.predict(X_train)
  y_test_pred = model.predict(X_test)

  model_train_mae, model_train_mse, model_train_rmse = evaluate_model(y_train, y_train_pred)
  print("train predicted mae: {:.4f}" .format(model_train_mae))
  print("train predicted mse: {:.4f}".format(model_train_mse))
  print("trained predicted rmse: {:.4f}" . format(model_train_rmse))

  model_test_mae, model_test_mse, model_test_rmse = evaluate_model(y_test, y_test_pred)
  print("test model mae: {:.4f}" . format(model_test_mae))
  print("test model mse: {:.4f}" . format(model_test_mse))
  print("test model rmse: {:.4f}" . format(model_test_rmse))

  print("**************************************")

from sklearn.metrics import r2_score
lin_model = LinearRegression(fit_intercept=True)
lin_model = lin_model.fit(X_train, y_train)
y_pred = lin_model.predict(X_test)
score = r2_score(y_test, y_pred)*100
print(" Accuracy of the model is %.2f" %score)

## difference between actual and predicted value

df1 = pd.DataFrame({'actual_value': y_test, 'predicted_value': y_pred, 'diff_value': y_test-y_pred})
#      pd.DataFrame({'Actual Value':y_test,'Predicted Value':y_pred,'Difference':y_test-y_pred})
df1

plt.scatter(y_test, y_pred)
plt.xlabel("y_test")
plt.ylabel("y_pred")

