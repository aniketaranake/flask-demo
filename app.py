from flask import Flask, render_template, request, redirect
<<<<<<< Updated upstream
from aranake_stock_plotter import getstockdata,generateplot
=======
from caiso_plotter import getlmpdata, getselectorcode, generateplot
>>>>>>> Stashed changes
import traceback

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def main():
  print "Arrived in main()"
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():

  print "Arrived in index()"
  print "request.method: ", request.method
  # Show the initial question sheet
  if request.method=='GET':
    print "Arrived in GET"
    return render_template('layout.html',bokeh_script="",bokeh_div="",note="")

<<<<<<< Updated upstream
  # Form was filled out, time to draw the plot
  else:
    print "Arrived in POST"

    try:
        # Call quandl API to get stock data
        data = getstockdata(request.form['stock'])
    except:
        note = "ERROR getting stock data! Faulty ticker symbol?"#+traceback.format_exc()
        return render_template('layout.html',bokeh_script="",bokeh_div="",note=note)
=======
@app.route('/plot',methods=['GET','POST'])
def plot():
  print "Arrived in plot()"
  print "request.method: ", request.method
  if request.method=='POST':

    print "Arrived in plot/POST"
    print "request.data: ", str(request.form)

    if(True):
#    try:
      data,nodelist = getlmpdata(request.form['inputdate'])
#    except:
#      return render_template('layout.html',bokeh_script="",bokeh_div="",note="ERROR getting LMP data")

    try:
      apnode = request.form['apnode']
    except KeyError:
      print "Key error, must not have an APnode: "
      selector_code = getselectorcode(nodelist)
      return render_template('plotscreen.html',selector_code=selector_code,bokeh_script="",bokeh_div="",note="",previous_date=request.form['inputdate'])
  
    selector_code = getselectorcode(nodelist)
    print "No key error, time to render the plot!"
    script,div,note = generateplot(data[data['NODE']==apnode])
    return render_template('plotscreen.html',selector_code=selector_code,bokeh_script=script,bokeh_div=div,note=note)

#    except:
#      note = "ERROR getting price data! "#+traceback.format_exc()
#      return render_template('layout.html',bokeh_script="",bokeh_div="",note=note)
>>>>>>> Stashed changes

    # Generate bokeh plot
    desired_columns = request.form.getlist('features')
    script,div,note = generateplot(data,desired_columns,request.form['stock'])

    # Render
<<<<<<< Updated upstream
    return render_template('layout.html',bokeh_script=script,bokeh_div=div,note=note)
=======
    #return render_template('plotscreen.html',bokeh_script=script,bokeh_div=div,note=note)
>>>>>>> Stashed changes

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=33507,debug=True)
