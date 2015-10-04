from flask import Flask, render_template, request, redirect
from caiso_plotter import getlmpdata, getselectorcode, generateplot
import traceback
import dill
import pandas as pd

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def main():
  print "Arrived in main()"
  return redirect('/index')

@app.route('/map_plotter',methods=['GET','POST'])
def map_plotter():

    fname = request.args.get('plot_id')
    if fname:
        with open('csv_data/%s.csv'%fname,'r') as f:
            f.readline()
            nodename = []
            longitude = []
            latitude = []
            data_val = []
            for line in f.readlines():
                splt = line.split(',')
                nodename.append(splt[1])
                longitude.append(splt[2])
                latitude.append(splt[3])
                data_val.append(splt[4].strip())
    
            str_out = "nodename = ["
            for nn in nodename[:-1]:
                str_out += '"' + nn + '", '
            str_out += '"' + nodename[-1] + '"]; \n'
    
            str_out += "latitude = ["
            for lat in latitude[:-1]:
                str_out += lat + ', '
            str_out += latitude[-1] + "]; \n"
    
            str_out += "longitude = ["
            for lon in longitude[:-1]:
                str_out += lon + ', '
            str_out += longitude[-1] + "]; \n"
    
            str_out += "data_val = ["
            for dv in data_val[:-1]:
                str_out += dv + ', '
            str_out += data_val[-1] + "]; \n"
    
        return render_template('map_layout.html',plotting_data=str_out)

@app.route('/index',methods=['GET','POST'])
def index():

  print "Arrived in index()"
  print "request.method: ", request.method

  nodelist = []
  with open('csv_data/opt_savings.csv','r') as f:
      f.readline()
      for line in f.readlines():
          nodelist.append(line.split()[0])
  selector_code = getselectorcode(nodelist)

  if request.method=='POST':

    print "Arrived in plot/POST"
    print "request.data: ", str(request.form)

    try:
      apnode = request.form['apnode']
    except KeyError:
      print "Key error, must not have an APnode: "
      return render_template('plotscreen.html',selector_code=selector_code,bokeh_script="",bokeh_div="",note="",previous_date=request.form['inputdate'])
  
    print "No key error, time to render the plot!"

    date = request.form['inputdate'] 
    print date
    data,_ = getlmpdata(date,apnode)

    script,div,note = generateplot(data)
    return render_template('plotscreen.html',selector_code=selector_code,bokeh_script=script,bokeh_div=div,note=note)

#    except:
#      note = "ERROR getting price data! "#+traceback.format_exc()
#      return render_template('layout.html',bokeh_script="",bokeh_div="",note=note)

    # Generate bokeh plot
    desired_columns = request.form.getlist('features')
    script,div,note = generateplot(data,desired_columns,request.form['stock'])

    # Render
    return render_template('plotscreen.html',bokeh_script=script,bokeh_div=div,note=note)
  
  else:

    return render_template('plotscreen.html',selector_code=selector_code,bokeh_script="",bokeh_div="",note="")

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=33507,debug=True)
