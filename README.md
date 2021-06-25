# Rossmann Store Sales Forecast

This is my 1st Data Science project, still in development. It consists of forecasting the sales of +1,000 drug stores from a dataset published @ [Kaggle.](https://www.kaggle.com/c/rossmann-store-sales) 

Its management follows the [CRISP-DM](https://www.datascience-pm.com/crisp-dm-2/) methodology, aiming to work in the problem through successively deeper cycles, while delivering value early, since the first run.  

## Status

Just finished the Hyperparameter Fine Tuning, and currently moving on to the translation and interpretation of the errors in terms of business metrics. 

Four models were implemented (besides the Average Model baseline): Linear Regression, Lasso, Random Forest Regressor and XGBoost. 6-fold cross-validation revealed the Random Forest would be the best choice (under a RMSE criterion), but XGBoost was chosen for continuing the work due to --- in comparison to the Random Forest --- its size (on deployment) being expected to be lower and its performance, rather close. 

Previously, data had already been properly cleaned, engineered, explored and prepared for the modeling. In the preparation phase, the choice to use Boruta as a feature selector was a highlight. 

## Next steps 
	
After evaluating the model performance in terms of business metrics, the model will be deployed to production. Spoiler: a Telegram Bot shall be built in order to have the forecasting at hands. At this point, a new CRISP-DM cycle will be allowed to begin.
