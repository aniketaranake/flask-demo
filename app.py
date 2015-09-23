from flask import Flask, render_template, request, redirect
from aranake_stock_plotter import getstockdata,generateplot
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

  # Form was filled out, time to draw the plot
  else:
    print "Arrived in POST"

    try:
        # Call quandl API to get stock data
        data = getstockdata(request.form['stock'])
    except:
        note = "ERROR getting stock data! Faulty ticker symbol?"#+traceback.format_exc()
        return render_template('layout.html',bokeh_script="",bokeh_div="",note=note)

    # Generate bokeh plot
    desired_columns = request.form.getlist('features')
    script,div,note = generateplot(data,desired_columns,request.form['stock'])

    # Render
    return render_template('layout.html',bokeh_script=script,bokeh_div=div,note=note)

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=33507,debug=True)
