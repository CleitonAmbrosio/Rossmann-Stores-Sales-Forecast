import pickle
import inflection
import numpy as np
import pandas as pd
import datetime
import math

class Rossmann(object):
    def __init__(self):
        self.home_path = ''
        self.competition_distance_scaler = pickle.load(
            open(self.home_path + 'parameters/competition_distance_scaler.pkl', 'rb')
        )
        self.competition_time_month_scaler = pickle.load(
            open(self.home_path + 'parameters/competition_time_month_scaler.pkl', 'rb')
        )
        self.promo2_time_week_scaler = pickle.load(
            open(self.home_path + 'parameters/promo2_time_week_scaler.pkl', 'rb')
        )
        self.year_scaler = pickle.load(
            open(self.home_path + 'parameters/year_scaler.pkl', 'rb')
        )
        self.store_scaler = pickle.load(
            open(self.home_path + 'parameters/store_scaler.pkl', 'rb')
        )
        self.competition_open_since_year_scaler = pickle.load(
            open(self.home_path + 'parameters/competition_open_since_year_scaler.pkl', 'rb')
        )
        self.promo2_since_year_scaler = pickle.load(
            open(self.home_path + 'parameters/promo2_since_year_scaler.pkl', 'rb')
        )
        self.store_type_encoder = pickle.load(
            open(self.home_path + 'parameters/store_type_encoder.pkl', 'rb')
        )
    
    def data_cleaning(self, df2):
        ## Renaming columns
        cols_old = [
            'Store', 'DayOfWeek', 'Date', 'Open', 'Promo', 
            'StateHoliday', 'SchoolHoliday', 'StoreType', 'Assortment', 
            'CompetitionDistance', 'CompetitionOpenSinceMonth', 'CompetitionOpenSinceYear', 
            'Promo2', 'Promo2SinceWeek', 'Promo2SinceYear', 'PromoInterval'
        ]
        snakecase = lambda x: inflection.underscore(x)
        cols_new = list(map(snakecase, cols_old))
        df2.columns = cols_new

        ## Fixing types 
        df2.loc[:,'date'] = pd.to_datetime(df2.loc[:,'date'])
        
        ## Filling out NAs
        # competition_distance
        df2.loc[:,'competition_distance'] = df2.loc[:,'competition_distance'].apply(
            lambda x: 300000 if math.isnan(x) else x
        )

        # competition_open_since_month
        df2.loc[:,'competition_open_since_month'] = df2.apply(
            lambda x: x['date'].month if math.isnan(x['competition_open_since_month'])
            else x['competition_open_since_month'],
            axis = 1
        )

        # competition_open_since_year
        df2.loc[:,'competition_open_since_year'] = df2.apply(
            lambda x: x['date'].year if math.isnan(x['competition_open_since_year'])
            else x['competition_open_since_year'],
            axis = 1
        )

        # promo2_since_week
        df2.loc[:,'promo2_since_week'] = df2.apply(
            lambda x: x['date'].week if math.isnan(x['promo2_since_week'])
            else x['promo2_since_week'], axis = 1)

        # promo2_since_year
        df2.loc[:,'promo2_since_year'] = df2.apply(
            lambda x: x['date'].year if math.isnan(x['promo2_since_year'])
            else x['promo2_since_year'],
            axis = 1
        )
              
        # promo_interval
        month_map = {
            1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
            7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
        }
        df2.loc[:,'month_map'] = df2.loc[:,'date'].dt.month.map(month_map)
        df2.loc[:,'promo_interval'].fillna(0, inplace=True)
        df2.loc[:,'is_start_promo2'] =  df2.loc[:,['promo_interval','month_map']].apply(
            lambda x: 0 if x['promo_interval'] == 0 
            else 1 if x['month_map'] in x['promo_interval'] 
            else 0,
            axis=1
        )

        ## Changing types 
        df2.loc[:,'competition_open_since_month'] = df2.loc[:,'competition_open_since_month'].astype(np.int64)
        df2.loc[:,'competition_open_since_year'] = df2.loc[:,'competition_open_since_year'].astype(np.int64)
        df2.loc[:,'promo2_since_week'] = df2.loc[:,'promo2_since_week'].astype(np.int64)
        df2.loc[:,'promo2_since_year'] = df2.loc[:,'promo2_since_year'].astype(np.int64)
        
        return df2 
    
    
    def feature_engineering(self, df3):
        # year
        df3.loc[:,'year'] = df3.loc[:,'date'].dt.year

        # month
        df3.loc[:,'month'] = df3.loc[:,'date'].dt.month

        # day
        df3.loc[:,'day'] = df3.loc[:,'date'].dt.day

        # week of year
        df3['week_of_year'] = df3['date'].dt.isocalendar().week - 1 # Minus 1 since ISO count starts from 1
        df3['week_of_year'] = df3['week_of_year'].astype(np.int64) #UInt32 to int64

        # year week
        df3.loc[:,'year_week'] = df3.loc[:,'date'].dt.strftime('%Y-%W')

        # competition since
        df3.loc[:,'competition_since'] = df3.apply(
            lambda x: datetime.datetime(year=x['competition_open_since_year'], month=x['competition_open_since_month'], day=1),
            axis=1
        )
        # competition time (months)
        df3.loc[:,'competition_time_month'] = ((df3.loc[:,'date'] - df3.loc[:,'competition_since'])/30).dt.days
        
        # promo2 since
        df3.loc[:,'promo2_since'] = df3.loc[:,'promo2_since_year'].astype(str) + '-' + df3.loc[:,'promo2_since_week'].astype(str)
        df3.loc[:,'promo2_since'] = df3.loc[:,'promo2_since'].apply(lambda x: datetime.datetime.strptime(x + '-1', '%Y-%W-%w'))
        # promo2 time (weeks)
        df3.loc[:,'promo2_time_week'] = ((df3.loc[:,'date'] - df3.loc[:,'promo2_since'])/7).dt.days
        
        # assortment
        df3.loc[:,'assortment'] = df3.loc[:,'assortment'].apply(
            lambda x: 'basic' if x == 'a' 
            else 'extra' if x =='b' 
            else 'extended'
        )

        # state holiday
        df3.loc[:,'state_holiday'] = df3.loc[:,'state_holiday'].apply(
            lambda x: 'public_holiday' if x == 'a'
            else 'easter_holiday' if x == 'b'
            else 'christmas' if x == 'c'
            else 'regular_day'
        )

        ## Filtering rows
        df3 = df3.loc[df3.loc[:,'open'] != 0, :]

        ## Selecting columns
        cols_drop = ['open', 'promo_interval', 'month_map']
        df3.drop(columns=cols_drop, inplace=True)

        return df3
    
    
    def data_preparation(self, df6):
        ## Rescaling
        df6.loc[:,'competition_distance'] = self.competition_distance_scaler.fit_transform(df6.loc[:,['competition_distance']])

        df6.loc[:,'competition_time_month'] = self.competition_time_month_scaler.fit_transform(df6.loc[:,['competition_time_month']])

        df6.loc[:,'promo2_time_week'] = self.promo2_time_week_scaler.fit_transform(df6.loc[:,['promo2_time_week']])

        df6.loc[:,'year'] = self.year_scaler.fit_transform(df6.loc[:,['year']])
        
        df6.loc[:,'store'] = self.store_scaler.fit_transform(df6.loc[:,['store']])

        df6.loc[:,'competition_open_since_year'] = self.competition_open_since_year_scaler.fit_transform(df6.loc[:,['competition_open_since_year']])

        df6.loc[:,'promo2_since_year'] = self.promo2_since_year_scaler.fit_transform(df6.loc[:,['promo2_since_year']])

        ## Transformation
        ### Categorical variables encoding
        # state_holiday - One Hot Encoding
        df6 = pd.get_dummies(df6, prefix=['state_holiday'], columns=['state_holiday'])

        # store_type - Label Encoding
        df6.loc[:,'store_type'] = self.store_type_encoder.fit_transform(df6.loc[:,'store_type'])

        # assortment - Ordinal Encoding
        assortment_dict = {'basic': 0, 'extra': 1, 'extended': 2}
        df6.loc[:,'assortment'] = df6.loc[:,'assortment'].map(assortment_dict)

        ### Nature transformation
        # day_of_week
        df6.loc[:,'day_of_week_sin'] = df6.loc[:,'day_of_week'].apply(lambda x: np.sin(x*2*np.pi/7))
        df6.loc[:,'day_of_week_cos'] = df6.loc[:,'day_of_week'].apply(lambda x: np.cos(x*2*np.pi/7))

        # month
        df6.loc[:,'month_sin'] = df6.loc[:,'month'].apply(lambda x: np.sin(x*2*np.pi/12))
        df6.loc[:,'month_cos'] = df6.loc[:,'month'].apply(lambda x: np.cos(x*2*np.pi/12))

        # day
        df6.loc[:,'day_sin'] = df6.loc[:,'day'].apply(lambda x: np.sin(x*2*np.pi/30))
        df6.loc[:,'day_cos'] = df6.loc[:,'day'].apply(lambda x: np.cos(x*2*np.pi/30))

        # week_of_year
        df6.loc[:,'week_of_year_sin'] = df6.loc[:,'week_of_year'].apply(lambda x: np.sin(x*2*np.pi/52))
        df6.loc[:,'week_of_year_cos'] = df6.loc[:,'week_of_year'].apply(lambda x: np.cos(x*2*np.pi/52))
        
        # competition_open_since_month
        df6.loc[:,'competition_open_since_month_sin'] = df6.loc[:,'competition_open_since_month'].apply(lambda x: np.sin(x*2*np.pi/12))
        df6.loc[:,'competition_open_since_month_cos'] = df6.loc[:,'competition_open_since_month'].apply(lambda x: np.cos(x*2*np.pi/12))

        # promo2_since_week
        df6.loc[:,'promo2_since_week_sin'] = df6.loc[:,'promo2_since_week'].apply(lambda x: np.sin(x*2*np.pi/52))
        df6.loc[:,'promo2_since_week_cos'] = df6.loc[:,'promo2_since_week'].apply(lambda x: np.cos(x*2*np.pi/52))
        
        cols_selected = [
        'store',
        'promo',
        'store_type',
        'assortment',
        'competition_distance',
        'competition_open_since_year',
        'promo2',
        'promo2_since_year',
        'competition_time_month',
        'promo2_time_week',
        'day_of_week_sin',
        'day_of_week_cos',
        'month_sin',
        'month_cos',
        'day_sin',
        'day_cos',
        'competition_open_since_month_sin',
        'competition_open_since_month_cos',
        'promo2_since_week_sin',
        'promo2_since_week_cos']
        
        return df6.loc[:,cols_selected]
    
    
    def get_prediction(self, model, tester, tester_pipelined):
        # Prediction
        pred = model.predict(tester_pipelined)
        
        # Add to the original
        tester['prediction'] = np.expm1(pred)
        
        return tester.to_json(orient='records', date_format='iso')