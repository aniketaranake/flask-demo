import requests
import datetime
import pandas as pd
import numpy as np

def getstockdata(stock):
    url_prefix = "https://www.quandl.com/api/v3/datasets/WIKI"

    today     = datetime.date.today()    
    startdate = today - datetime.timedelta(30)

    quandl_api_call_string = "%s/%s.json?start_date=%s&end_date=%s"%(url_prefix,stock,startdate,today)
    #quandl_api_call_string = "http://www.stanford.edu/~aniket/GOOG.json"
    print quandl_api_call_string
    
    # Grab the data from Quandl 
    r = requests.get(quandl_api_call_string)

    # Load data into a pandas dataframe
    df0 = pd.read_json(r.text)['dataset']
    df  = pd.DataFrame(df0['data'],columns=df0['column_names'])
    df['Date'] = pd.to_datetime(df['Date'])  # By default, the Date column's type is 'object'

    # Column names:
    # 'Date',
    # 'Open',
    # 'High',
    # 'Low',
    # 'Close',
    # 'Volume',
    # 'Ex-Dividend',
    # 'Split Ratio',
    # 'Adj. Open',
    # 'Adj. High',
    # 'Adj. Low',
    # 'Adj. Close',
    # 'Adj. Volume']
    return df.loc[:,['Date','Close','Adj. Close','Volume']]


if __name__=="__main__":


    stock = "GOOG"
    df = getstockdata(stock)
    import IPython
    IPython.embed()
