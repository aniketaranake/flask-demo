from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.io import vplot
import numpy as np
from numpy import pi

def generateplot(data,energy,start_time,savings):

    human_hours = {0: "12 midnight",
                  1: "1 am",
                  2: "2 am",
                  3: "3 am",
                  4: "4 am",
                  5: "5 am",
                  6: "6 am",
                  7: "7 am",
                  8: "8 am",
                  9: "9 am",
                  10: "10 am",
                  11: "11 am",
                  12: "12 noon",
                  13: "1 pm",
                  14: "2 pm",
                  15: "3 pm",
                  16: "4 pm",
                  17: "5 pm",
                  18: "6 pm",
                  19: "7 pm",
                  20: "8 pm",
                  21: "9 pm",
                  22: "10 pm",
                  23: "11 pm"}

    data = data.sort('OPR_HR')

    hours = np.array(range(48))
    cost  = data['MW'].values
    cost_double = np.append(cost,cost)

    print "start_time: ", start_time
    use_j = xrange(start_time,start_time+24)
    hour_axis = [human_hours[i%24] for i in hours[start_time:start_time+24]]

    lmp_plot = figure(title='Cost of electricity', x_range=hour_axis)
    lmp_plot.line(hour_axis,cost_double[use_j])
    lmp_plot.xaxis.axis_label='Time'
    lmp_plot.yaxis.axis_label='LMP ($/MWh)'
    lmp_plot.xaxis.major_label_orientation = pi/4
   
#    hour_axis = [human_hours[i%24] for i in hours[start_time:start_time+25]]
    charge_plot = figure(title='Optimal charge profile',x_range=hour_axis)
    charge_plot.line(hour_axis,np.append([0],energy[:-1]*1000.)) 
    charge_plot.xaxis.axis_label='Time'
    charge_plot.yaxis.axis_label='Charge (kWh)'
    charge_plot.xaxis.major_label_orientation = pi/4

    p = vplot(lmp_plot,charge_plot)
    script, div = components(p)

    note = "Savings: $%5.2f <br>"%savings
    note += "Charge start time: %s"% human_hours[start_time]
    return script, div, note
