import os
import requests
import json

import pandas as pd
from flask import Flask, request, Response, abort

TOKEN = os.environ.get('TOKEN')

def parse_message(message):
    chat_id = message['message']['chat']['id']
    store_id = message['message']['text']
    
    store_id = store_id.replace('/', ' ')
    
    try:
        store_id = int(store_id)
    except ValueError:
        store_id = 'error'
    
    return chat_id, store_id


def send_message(chat_id, text):
    url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}'.format(TOKEN, chat_id)
    r = requests.post(url, json={'text': text})


def load_dataset(store_id):
    df_tester = pd.read_csv('test.csv')
    df_stores_raw = pd.read_csv('store.csv', low_memory=False)
    df_tester = pd.merge(df_tester, df_stores_raw, how='left', on='Store')

    df_tester = df_tester.loc[df_tester.loc[:,'Store'] == store_id,:]
    
    if not df_tester.empty:    
        df_tester = df_tester.loc[df_tester.loc[:,'Open'] != 0,:]

        # Fixing df_tester problems not contemplated by Rossmann.data_cleaning
        df_tester = df_tester.drop(columns='Id', axis=1)
        df_tester = df_tester.loc[~df_tester.loc[:,'Open'].isna(),:]
    
        data = json.dumps(df_tester.to_dict(orient='records'))
    else:
        data = 'error'
    
    return data


def predict(data):
    url = os.environ.get('rossmann-predictor-api')
    header = {'Content-type': 'application/json'}

    r = requests.post(url, data=data, headers=header)
    print('Status code {}'.format(r.status_code))

    df_response = pd.DataFrame(r.json(), columns=r.json()[0].keys())

    return df_response

######################################

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.get_json()
        chat_id, store_id = parse_message(message)

        if store_id != 'error':
            # load data
            data = load_dataset(store_id)
            if data != 'error':
                # predict
                df1 = predict(data)
                # sum up
                df2 = df1.loc[:,['store','prediction']].groupby('store').sum().reset_index()
                msg = 'Store #{} will sell ${:,.2f} in the next 6 weeks.'.format(df2.loc[0,'store'], df2.loc[0,'prediction'])
                # reply
                send_message(chat_id, msg)
                return Response('Ok', status=200)
            else:
                send_message(chat_id, 'Store not available')
                return Response('Ok', status=200)
        else:
            send_message(chat_id, 'Not a valid Store ID')
            return Response('Ok', status=200) 
    else:
        abort(405)


if __name__ == '__main__':
    port = os.environ.get('PORT', 10000)
    app.run(host='0.0.0.0', port=port)