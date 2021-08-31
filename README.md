# Rossmann Stores Sales Forecast
## Predicting the income of the units of a chain store

![](cover.png)

## Business Problem
Rossmann is one of the largest chains of drug stores in Europe, with +4k stores as of 2019<sup>[1]</sup>. Its business model is that of a common pharmacy, but with several standardized units spread throughout the continent.

The manager of each store came up with the task of predicting the daily sales of their units for up to 6 weeks in advance. This task was assigned to the Data Science team of the whole chain, who must model the historical database in order to generate the desired forecasting. 

The [database](https://www.kaggle.com/c/rossmann-store-sales) spans around 2.5 years in time (between 2013 and 2015) and 1115 stores in total, containing information for each unit describing factors such as promotions, competition, school and state holidays and seasonality.

## Business Assumptions

## Solution Strategy
In order to solve this challenge, I went along the following steps:
1. Data Description: Understanding of the status of the database and dealing with missing values properly. Basic statistics metrics furnish an overview of the data.  
2. Feature Engineering: Derivation of new attributes based on the original variables aiming to better describe the phenomenon that will be modeled, and to supply interesting attributes for the Exploratory Data Analysis.
3. Data Filtering: Filtering of records and selection of attributes that do not contain information for modeling or that do not match the scope of the business problem.
4. Exploratory Data Analysis (EDA): Exploration of the data searching for insights and seeking to understand the impact of each variable on the upcoming machine learning modeling.
5. Data Preparation: Preprocessing stage required prior to the machine learning modeling step.
6. Feature Selection: Selection of the most significant attributes for training the model.
7. Machine Learning Modeling: Implementation of a few algorithms appropriate to the task at hand. In this case, models befitting the *regression* assignment - *i.e.*, forecasting a continuous value, namely sales.
8. Hyperparameter Fine Tunning: Search for the best values for each of the parameters of the best performing model(s) selected from the previous step.
9. Translation and Interpretation of the Model Performance: Conversion of the performance metrics of the Machine Learning model to a more tangible business result.
10. Deployment of the Model to Production: Publication of the model in a cloud environment so that the interested people can access its results to improve business decisions.

Moreover, the workflow followed the [CRISP-DM](https://www.datascience-pm.com/crisp-dm-2/) methodology, aiming to work in the problem through successively deeper cycles, while delivering value early, since the first run. 

## Top 3 Insights From Exploratory Data Analysis
## Machine Learning Modeling Performance
## Business Results	

## Conclusions
*The deployment scripts are included in the last section of the notebook file, but are better contained in the standalone folders, precisely those deployed to production (in this case, through Heroku).*

[<img alt="Telegram" src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/>](https://t.me/rossmann_sales_forecast_bot)

## Lessons Learned
## Points For Improvement

## References
[1] [Personal Care Retailers in Europe](https://www.retail-index.com/sectors/personalcareretailersineurope.aspx).
