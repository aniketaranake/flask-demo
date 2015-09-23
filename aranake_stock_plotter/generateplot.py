from bokeh.plotting import figure
import pandas as pd
from bokeh.charts import Line
from bokeh.embed import components

def generateplot(data ):
    
    note = ""
    # if len(desired_columns)==0:
    #     desired_columns = ['Close']
    #     note = "NOTE: No desired features selected!"

    print "\tSorting data"
    data = data.sort(['OPR_HR'])

    print "\tGenerating plot"
    #plot = figure()
    plot = Line(data['MW'],data['OPR_HR'],xlabel='Hour',ylabel='Locational Marginal Cost ($/MW)')
    script, div = components(plot)  
 
    print "\treturning components"
    return script, div, note
