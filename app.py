from flask import Flask, render_template, request, redirect
from caiso_plotter import getlmpdata
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

@app.route('/plot',methods=['GET'])
def plot():
  print "Arrived in plot()"
  print "request.method: ", request.method
  if request.method=='GET':
    print "Arrived in plot/GET"
#    try:
      # caiso API call to get LMP data
    print "request.data: ", str(request.form)

    for key in request.form:
      for value in request.form.getlist(key):
        print key, " : ", value
    #print "Date data: ", request.form['inputdate']
    #data = getlmpdata(request.form['inputdate'])
#    except:
#      note = "ERROR getting price data! "#+traceback.format_exc()
#      return render_template('layout.html',bokeh_script="",bokeh_div="",note=note)

    # Generate bokeh plot
    # desired_columns = request.form.getlist('features')
    #script,div,note = generateplot(data,desired_columns,request.form['stock'])

    # Render
    #return render_template('plotscreen.html',bokeh_script=script,bokeh_div=div,note=note)
    return render_template('plotscreen.html',bokeh_script="",bokeh_div="",note="")

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=33507,debug=True)
