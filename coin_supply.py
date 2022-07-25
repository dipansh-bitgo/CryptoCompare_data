import requests
import pandas as pd
from datetime import datetime
import os 
import csv 



def get_all_responses(top_coins, api_url_prefix, api_url_postfix):
    '''
    Get the responses from the api for the input list of top coins
    '''
    final_list=[]
    other_list=[]
    for id in top_coins:
        response=requests.get(api_url_prefix + id + api_url_postfix)
        responses=response.json() 
        try: 
            for response in responses['Data']['Data']:
                final_list.append([response['time'], response['symbol'], response['current_supply']])
        except:
            other_list.append(id)   
        
    
    return final_list

def get_latest_responses(top_coins, api_url_prefix_latest, api_url_postfix_latest):
  '''
  Get latest data from the api using the input list of top coins
  '''
  final_list=[]
  for id in top_coins:
        response=requests.get(api_url_prefix_latest + id + api_url_postfix_latest)
        responses=response.json() 

        # try:
        if responses['Response']=='Success':
          final_list.append([responses['Data']['time'], responses['Data']['symbol'], responses['Data']['current_supply']])
        # except:
        #     print(id, end=' ')

  return final_list



if __name__=="__main__":
    print("Code running")
    # defining list of top coins
    top_coins=['btc' , 'eth' , 'usdt' , 'usdc', 'bnb', 'busd', 'xrp', 'ada', 'sol', 'doge', 'dot', 'shib', 'dai', 'matic', 'avax', 'trx', 'steth', 'wbtc', 'leo', 'ltc' , 'ftt', 'okb', 'cro', 'link', 'uni', 'etc', 'near', 'atom', 'xlm', 'xmr', 'algo', 'bch', 'xcn', 'tfuel', 'flow', 'vet', 'ape', 'sand', 'icp', 'mana', 'hbar', 'xtz', 'frax', 'qnt', 'fil', 'axs', 'aave', 'egld', 'tusd', 'theta']
    
    
    # api urls to get all the data
    api_url_prefix = 'https://min-api.cryptocompare.com/data/blockchain/histo/day?fsym=' 
    api_url_postfix='&limit=2000&api_key=307a37ebc111052679b5c8629a7712cdabe436c2763667e04c8c304f67f3b3eb'
    
    # api to get the latest data 
    api_url_prefix_latest='https://min-api.cryptocompare.com/data/blockchain/latest?fsym='
    api_url_postfix_latest='&api_key=307a37ebc111052679b5c8629a7712cdabe436c2763667e04c8c304f67f3b3eb'
    
    
    files_cwd=os.listdir()
    if('current_supply_data.csv' not in files_cwd):
        print('CSV file not present in cwd')
        final_list=get_all_responses(top_coins, api_url_prefix, api_url_postfix)
        print('API call made to extract all historical data')
        final_df=pd.DataFrame(final_list, columns=['date', 'coin_type', 'circulation_supply'])
        final_df['date']=pd.to_datetime(final_df['date'], unit='s')
        final_df.to_csv("current_supply_data.csv", index=False)
        print('File saved in csv')
    else: 
        print('CSV file  present in cwd')
        final_list=get_latest_responses(top_coins, api_url_prefix_latest, api_url_postfix_latest)
        latest_df=pd.DataFrame(final_list, columns=['date', 'coin_type', 'circulation_supply'])
        latest_df['date']=pd.to_datetime(latest_df['date'], unit='s').dt.date
        final_list=latest_df.values.tolist()
        with open('current_supply_data.csv','r') as file_object:
          existing_lines  = [line for line in csv.reader(file_object, delimiter=',')]
          file_object.close()
        with open('current_supply_data.csv','a') as file_object:
          writer_object = csv.writer(file_object)
          for value in final_list:
            if value not in existing_lines:
              writer_object.writerow(value)

        file_object.close()


        