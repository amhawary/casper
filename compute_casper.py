#!/usr/bin/env python
# coding: utf-8
import numpy as np
import pandas as pd
import pickle as pkl
import requests as req

save_as="casper_scores.pkl"
g_dict=pkl.load(open("g_dict.pkl","rb"))
sp_dict=pkl.load(open("sp_dict.pkl","rb"))
no2_dict=pkl.load(open("dates_dict.pkl","rb"))

CASPER_INDEX={}
w_act_diff_ratio=.6
w_search_pen=.4
w_growth=.8


# reduction_in_activity_percentage={} # reduction in activity since g_dict is more than 0.012% of the population
# multiply g_dict by (sp_dict+reduction_in_activity_percentage)
# then scale between 0-10


def ignore_timestamp_zone(stamp):
    return pd.Timestamp("{0}-{1}-{2}".format(stamp.year,stamp.month,stamp.day))
def add_utc_stamp(stamp):
    return pd.Timestamp("{0}-{1}-{2}".format(stamp.year,stamp.month,stamp.day),tz="UTC")


it_is_srys={} # when was it srys for each country? 
#srys is defined as when the growth rate is more than 500 cases per day
for country in g_dict.keys():
    try:
        pop_thresh=500#c2pop[country]*0.00012
        
    except KeyError:
        print("skipping",country)
        continue
    for date in g_dict[country].keys():
        if g_dict[country][date]>pop_thresh:
            if country not in it_is_srys.keys():
                    it_is_srys.update({country:date})
                    
for country in g_dict.keys():
    if country not in it_is_srys.keys():
            it_is_srys.update({country:np.nan})
            

new_no2_dict={} #invert the dict so it's name->dates->no2_mean instead of dates->names->no2_mean
for date in no2_dict.keys():
    for c_name in no2_dict[date].keys():
        utc_date=add_utc_stamp(date)
        if c_name in new_no2_dict.keys():
            new_no2_dict[c_name].update({utc_date:no2_dict[date][c_name]})
        else:
            new_no2_dict.update({c_name:{utc_date:no2_dict[date][c_name]}})


b4_turning_point={}
after_turning_point={}

for c_name in new_no2_dict.keys():
    date2meanNo2=new_no2_dict[c_name]
    means_b4=np.zeros(shape=(0,))
    means_after=np.zeros(shape=(0,))
    nd=False
    for date in date2meanNo2.keys():
        try:
            if np.isnan(it_is_srys[c_name]):
                nd=True
                continue
        except:
            pass
        if date>=it_is_srys[c_name]: #if it's after it being srys
            means_b4=np.hstack([means_b4,[date2meanNo2[date]]])
        else:
            means_after=np.hstack([means_after,[date2meanNo2[date]]])
    
    means_b4=means_b4[np.logical_not(np.isnan(means_b4))]
    means_after=means_after[np.logical_not(np.isnan(means_after))]
    
    if nd==False:
        b4_turning_point.update({c_name:np.mean(means_b4)})
        after_turning_point.update({c_name:np.mean(means_after)})
    else:
        b4_turning_point.update({c_name:0})
        after_turning_point.update({c_name:0})
    



act_diff_ratio={} # the lower the score the better
for c_name in b4_turning_point.keys():
    if b4_turning_point[c_name]==0:
        act_diff_ratio.update({c_name:0})
        continue
    act_diff_ratio.update({c_name:(b4_turning_point[c_name]-after_turning_point[c_name])})




def calc_casper(act_diff_ratio,growth,search_pen):
    return (w_growth*sum(growth))*((w_search_pen*search_pen)+(w_act_diff_ratio*act_diff_ratio))
    
for c_name in act_diff_ratio.keys():
    
    growth_over_time=[i[1] for i in g_dict[c_name].items()]
    try:
        search_pen=sp_dict[c_name]
    except KeyError:
        pass
    casper_score=calc_casper(act_diff_ratio[c_name],growth_over_time,search_pen)
    CASPER_INDEX.update({c_name:casper_score})

CASPER_INDEX_scaled={} # the higher the better
casper_array=np.array([[i[0],float(i[1])] for i in CASPER_INDEX.items()])

def rescale_linear(array, new_min, new_max):
    """Rescale an arrary linearly."""
    minimum, maximum = np.min(array), np.max(array)
    m = (new_max - new_min) / (maximum - minimum)
    b = new_min - m * minimum
    return m * array + b

x=np.array([float(i) for i in casper_array[:,1]])
c_idx_keys=[i for i in casper_array[:,0]] #[i for i in CASPER_INDEX.keys()]
for i in range(len(c_idx_keys)):
    CASPER_INDEX_scaled.update({c_idx_keys[i]:rescale_linear(x,0,1000)[i]})


if __name__=="__main__":
    print("Saving CASPER score as ",save_as)
    with open(save_as, 'wb+') as handle:
        pkl.dump(CASPER_INDEX_scaled, handle, protocol=pkl.HIGHEST_PROTOCOL)