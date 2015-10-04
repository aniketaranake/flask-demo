import pandas as pd
import numpy as np
import scipy, scipy.optimize
from scipy.optimize import minimize, fmin_slsqp
import datetime
import code

def optimize_charge_profile(data, max_charge, max_discharge,capacity):

    def obj(x,costvec):
        return np.sum(x*costvec)

    data = data.sort('OPR_HR')
    hour = np.append(data['OPR_HR'].values,24+data['OPR_HR'].values)

    # Build constraint list
    constraint_list = []
        
    # Make sure energy in our system never negative
    constraint_list.append(lambda x: np.sum(x[:1]))
    constraint_list.append(lambda x: np.sum(x[:2]))
    constraint_list.append(lambda x: np.sum(x[:3]))
    constraint_list.append(lambda x: np.sum(x[:4]))
    constraint_list.append(lambda x: np.sum(x[:5]))
    constraint_list.append(lambda x: np.sum(x[:6]))
    constraint_list.append(lambda x: np.sum(x[:7]))
    constraint_list.append(lambda x: np.sum(x[:8]))
    constraint_list.append(lambda x: np.sum(x[:9]))
    constraint_list.append(lambda x: np.sum(x[:10]))
    constraint_list.append(lambda x: np.sum(x[:11]))
    constraint_list.append(lambda x: np.sum(x[:12]))
    constraint_list.append(lambda x: np.sum(x[:13]))
    constraint_list.append(lambda x: np.sum(x[:14]))
    constraint_list.append(lambda x: np.sum(x[:15]))
    constraint_list.append(lambda x: np.sum(x[:16]))
    constraint_list.append(lambda x: np.sum(x[:17]))
    constraint_list.append(lambda x: np.sum(x[:18]))
    constraint_list.append(lambda x: np.sum(x[:19]))
    constraint_list.append(lambda x: np.sum(x[:20]))
    constraint_list.append(lambda x: np.sum(x[:21]))
    constraint_list.append(lambda x: np.sum(x[:22]))
    constraint_list.append(lambda x: np.sum(x[:23]))
    constraint_list.append(lambda x: np.sum(x[:24]))

    # Make sure we never exceed capacity
    constraint_list.append(lambda x: capacity-np.sum(x[:1]))
    constraint_list.append(lambda x: capacity-np.sum(x[:2]))
    constraint_list.append(lambda x: capacity-np.sum(x[:3]))
    constraint_list.append(lambda x: capacity-np.sum(x[:4]))
    constraint_list.append(lambda x: capacity-np.sum(x[:5]))
    constraint_list.append(lambda x: capacity-np.sum(x[:6]))
    constraint_list.append(lambda x: capacity-np.sum(x[:7]))
    constraint_list.append(lambda x: capacity-np.sum(x[:8]))
    constraint_list.append(lambda x: capacity-np.sum(x[:9]))
    constraint_list.append(lambda x: capacity-np.sum(x[:10]))
    constraint_list.append(lambda x: capacity-np.sum(x[:11]))
    constraint_list.append(lambda x: capacity-np.sum(x[:12]))
    constraint_list.append(lambda x: capacity-np.sum(x[:13]))
    constraint_list.append(lambda x: capacity-np.sum(x[:14]))
    constraint_list.append(lambda x: capacity-np.sum(x[:15]))
    constraint_list.append(lambda x: capacity-np.sum(x[:16]))
    constraint_list.append(lambda x: capacity-np.sum(x[:17]))
    constraint_list.append(lambda x: capacity-np.sum(x[:18]))
    constraint_list.append(lambda x: capacity-np.sum(x[:19]))
    constraint_list.append(lambda x: capacity-np.sum(x[:20]))
    constraint_list.append(lambda x: capacity-np.sum(x[:21]))
    constraint_list.append(lambda x: capacity-np.sum(x[:22]))
    constraint_list.append(lambda x: capacity-np.sum(x[:23]))
    constraint_list.append(lambda x: capacity-np.sum(x[:24]))


    cost_MWh = np.append(data['MW'].values,data['MW'].values)

    max_savings = 0.
    savings = np.zeros([24])

    for start_time in range(24):

        # Initial guess
        x0 = np.append( [max_charge]*12, [-max_discharge]*12)

        # Objective function
        f  = lambda x : obj(x,cost_MWh[start_time:start_time+24])
        f_deriv = lambda x: cost_MWh[start_time:start_time+24]

        # Perform optimization
        out,fx,its,imode,smode = fmin_slsqp(f,x0,bounds=[(-max_discharge,max_charge)]*24,ieqcons=constraint_list,full_output=True,iprint=2)

        savings[start_time] = -fx
        if savings[start_time] > max_savings:
          max_savings    = savings[start_time]
          opt_start_time = start_time
          opt_power_dist = out


    energy = np.zeros(24)
    for j in range(1,25):
      energy[j-1] = sum(opt_power_dist[:j])

    cost_time = np.zeros(24)
    for j in range(24):
        cost_time[j] = opt_power_dist[j]*cost_MWh[start_time+j]

#     print ""
#     print "%15s %15s"%("start time", "savings")
#     for j in range(24):
#         print "%15d %15.2f"%(j, savings[j])
# 
#     print ""
#     print "%15s %15s %15s %15s %15s"%("hour", "LMP", "energy", "cost_time", "charge rate"
#     )
#     for j in range(24):
#         print "%15d %15.2f %15.2f %15.2f %15.2f %15.2f"%(j, cost_MWh[opt_start_time+j], energy[j], cost_time[j], opt_power_dist[j],constraint_list[j](opt_power_dist))

    # import pylab as py
    # py.figure()
    # py.subplot(3,1,1)
    # py.plot(hour,cost_MWh,'-')
    # py.xlabel('Hour of day')
    # py.ylabel('LMP ($/MWh)')
    # py.grid(True)
    # py.xlim([0,48])
    # py.subplot(3,1,2)
    # py.plot(range(start_time,start_time+24),energy)
    # py.grid(True)
    # py.xlim([0,48])
    # py.ylabel('Energy storage (MWh)')
    # py.subplot(3,1,3)
    # py.plot(range(start_time,start_time+24),cost_time)
    # py.grid(True)
    # py.xlim([0,48])
    # py.ylabel('Cost ($)')


    print ""
    print "Savings: $%5.2f"%max_savings
    py.show()


    return opt_power_dist, max_savings, start_time, energy

def compute_opt_dist(fname, date, max_charge, max_discharge,capacity):
        df0 = pd.read_csv(fname)
    
        #code.interact(local=locals())
        use_j = df0['XML_DATA_ITEM']=='LMP_PRC'
        use_j = use_j & (df0['OPR_DT'] == date)
    
        df  = df0[use_j].loc[:,['NODE','OPR_DT','OPR_HR','MW']]
    
        opt_power_dist, max_savings, start_time, energy = optimize_charge_profile(df,max_charge,max_discharge,capacity)

if __name__=="__main__":

    # MW
    max_charge    = 0.002
    max_discharge = 0.002
    # MWh
    capacity      = 0.09


    max_savings = compute_opt_dist(fname='lmp_KERMAN_6_N001_1_2014.csv',date='2014-01-01',max_charge=max_charge,max_discharge=max_discharge,capacity=capacity)
