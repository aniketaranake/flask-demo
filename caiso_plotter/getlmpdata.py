import urllib
import datetime
import pandas as pd
import numpy as np
import zipfile

def getlmpdata(date,node):
    url_prefix = 'http://oasis.caiso.com/oasisapi/SingleZip?queryname=PRC_LMP&version=1&market_run_id=DAM&resultformat=6'

    year  = int(date[:4])
    month = int(date[5:7])
    day   = int(date[8:])
    startdatetime = "%d%02d%02dT07:00-0000"%(year,month,day)
    enddate = datetime.date(year,month,day) + datetime.timedelta(days=1)
    enddatetime = "%d%02d%02dT07:00-0000"%(enddate.year,enddate.month,enddate.day)
    print "startdatetime: ", startdatetime
    print "enddatetime: ", enddatetime

    url = url_prefix+"&startdatetime=%s&enddatetime=%s"%(startdatetime,enddatetime)
    url = url+'&node='+node
    print "url: ", url

    urllib.urlretrieve(url,'tmp.zip')

    z = zipfile.ZipFile('tmp.zip')
    fname = z.namelist()[0]
    print fname
    z.extractall()

    df0 = pd.read_csv(fname) 
    df  = df0.loc[df0['XML_DATA_ITEM']=='LMP_PRC',['NODE','OPR_HR','MW']]   # Select only the Locational Marginal Price

    nodelist = (df.groupby('NODE').first()).index.values

    return df,nodelist

def getselectorcode(nodelist,prev_node=None):
  
  code = ''
  for node in nodelist:
    if node==prev_node:
        code += '<option value="%s" selected="selected">%s</option>\n'%(node,node)
    else:
        code += '<option value="%s">%s</option>\n'%(node,node)

  return code
if __name__=="__main__":

    date = "20140616"
    df = getlmpdata(date)
    import IPython
    IPython.embed()
