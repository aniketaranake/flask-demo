import urllib
import datetime
import pandas as pd
import numpy as np
import zipfile

def getlmpdata(date):
    url_prefix = 'http://oasis.caiso.com/oasisapi/SingleZip?queryname=PRC_LMP&version=1&market_run_id=DAM&grp_type=ALL_APNODES&resultformat=6'

    startdatetime = "%sT07:00-0000"%date
    year  = int(date[:4])
    month = int(date[4:6])
    day   = int(date[6:])
    enddate = datetime.date(year,month,day) + datetime.timedelta(days=1)
    enddatetime = "%d%02d%02dT07:00-0000"%(enddate.year,enddate.month,enddate.day)
    print "startdatetime: ", startdatetime
    print "enddatetime: ", enddatetime

    url = url_prefix+"&startdatetime=%s&enddatetime=%s"%(startdatetime,enddatetime)
    print "url: ", url

    urllib.urlretrieve(url,'tmp.zip')

    z = zipfile.ZipFile('tmp.zip')
    fname = z.namelist()[0]
    print fname
    z.extractall()

    df0 = pd.read_csv(fname) 
    df  = df0[df0['XML_DATA_ITEM']=='LMP_PRC'].loc[:,['NODE','OPR_HR','MW']]   # Select only the Locational Marginal Price

    nodelist = (df.groupby('NODE').first())['NODE'].to_list()
    print ""
    print nodelist
    print ""

    return df,nodelist

if __name__=="__main__":

    date = "20140616"
    df = getlmpdata(date)
    import IPython
    IPython.embed()
