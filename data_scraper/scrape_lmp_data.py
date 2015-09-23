import pandas as pd
import datetime, time
import urllib
import zipfile
import shutil
import os, os.path
import sys

def get_node_locations():

    fname = 'LMPLocations.csv'
    if os.path.isfile(fname):
        df = pd.read_csv(fname)
    else:
        df = pd.read_csv('https://raw.githubusercontent.com/emunsing/CAISO-Scrapers/master/LMP%20Location%20Scraper/LMPLocations.csv')
    return df

class NodeDataHandler:

    def __init__(self,nodelist='all',months=range(1,13),years=[2014]):
        if type(nodelist)==type([]):
            self.nodelist = nodelist
        else:
            self.nodelist = ['all']

        self.months   = months
        self.years    = years

    def check_existing_files(self):

        existing_files = []
        missing_files  = []
        for node in self.nodelist:
            for month in self.months:
                for year in self.years:
                    fname = self.get_fname(node,month,year)
                    if os.path.isfile(fname):
                        existing_files.append((node,month,year))
                    else:
                        missing_files.append((node,month,year))
        return existing_files, missing_files


    def get_fname(self,node,month,year):
        return 'data/lmp_'+node+'_%d_%d'%(month,year)+'.csv'

    def dl_all(self):
        for node in self.nodelist:
            for month in self.months:
                for year in self.years:
                    self.get_lmp_data(node, month, year)

    def dl_missing(self):
        _,missing_files = self.check_existing_files()
        for missing_file in missing_files:
            (node,month,year) = missing_file
            self.get_lmp_data(node,month,year)
            

    def dlprogress(self,count, blockSize, totalSize):
        if count==0:
            sys.stdout.write("...done!\n")

        if totalSize > -1:
            percent = int(count*blockSize*100/totalSize)
            sys.stdout.write("\r[%5.2fMB/%5.2fMB] %d%%" % (count*blockSize/1024./1024.,totalSize/1024./1024.,percent))
        else:
            sys.stdout.write("\rDownloading: [%5.2fMB]" % (count*blockSize/1024./1024.))
        sys.stdout.flush()

    def get_lmp_data(self,node, month, year):
        
        url_prefix = 'http://oasis.caiso.com/oasisapi/SingleZip?queryname=PRC_LMP&version=1&market_run_id=DAM&resultformat=6'
    
        # Start and end date parameters for a year's worth of data
        startdate = datetime.date(year,month,1)
        if month<12:
            enddate   = datetime.date(year,month+1,1) - datetime.timedelta(days=1)
        elif month==12:
            enddate   = datetime.date(year+1,1,1) - datetime.timedelta(days=1)
        startdate_str = "%d%02d%02dT07:00-0000"%(startdate.year,startdate.month,startdate.day)
        enddate_str   = "%d%02d%02dT07:00-0000"%(enddate.year,enddate.month,enddate.day)
    
        url = url_prefix+"&startdatetime=%s&enddatetime=%s"%(startdate_str,enddate_str)

        if node=='all':
            url = url + '&grp_type=ALL_APNODES'
        else:
            url = url + '&node='+node
    
        # Make the URL request, save result as tmp.zip
        print ""
        print "Sent request for node: %s, month: %d, year: %d"%(node, month, year)
        sys.stdout.write("Waiting for response...")
        sys.stdout.flush()
        request_starttime = time.time()
        urllib.urlretrieve(url,'tmp.zip',reporthook=self.dlprogress)
        print ""

        sys.stdout.write("Inflating...")
        sys.stdout.flush()

        try:
            z = zipfile.ZipFile('tmp.zip')
        except zipfile.BadZipfile:
            print sys.exc_info()[0], ': ', sys.exc_info()[1]    
            print "Error in archive: Bad data recieved from CAISO."
        else:
            caiso_fname = z.namelist()[0]
            z.extractall()
            shutil.move(caiso_fname,self.get_fname(node,month,year))
            sys.stdout.write('done!\n')
            sys.stdout.flush()

        # Make sure 5 seconds have passed since request was sent
        time_elapsed = time.time()-request_starttime
        sys.stdout.write('Time Elapsed: %d seconds'%time_elapsed)
        sys.stdout.flush()
        threshold_time = 5.1
        if time_elapsed < threshold_time:
            sys.stdout.write('...sleeping for %d seconds'%(threshold_time-time_elapsed))
            sys.stdout.flush()
            time.sleep(threshold_time-time_elapsed)
        sys.stdout.write('\n')

        return

    def save_db(self):

        files = []
        for node in self.nodelist:
            for month in self.months:
                for year in self.years:
                    files.append(self.get_fname(node,month,year))
        frames = [ pd.read_csv(f) for f in files ]
        result = pd.concat(frames)

        result.to_pickle('caiso_data.pkl')


if __name__=="__main__":

    node_locations = get_node_locations()
    # print node_locations.head()


    testnodes  = ['KERMAN_6_N001']
    testnodes = 'all'
    testmonths = [1,2,3,4,5,6,7,8,9,10,11,12]
    testyears  = [2014,2013] 

    node_data_handler = NodeDataHandler(testnodes,testmonths,testyears)

    _, missing = node_data_handler.check_existing_files()

    while missing:
        node_data_handler.dl_missing()
        _, missing = node_data_handler.check_existing_files()


    node_data_handler.save_db()
