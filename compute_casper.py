#!/usr/bin/env python
# coding: utf-8
import json
import numpy as np
import pandas as pd
import pickle as pkl
import requests as req

save_as="casper_scores.json"
g_dict=pkl.load(open("g_dict.pkl","rb"))
sp_dict=pkl.load(open("sp_dict.pkl","rb"))
no2_dict=pkl.load(open("dates_dict.pkl","rb"))

CASPER_INDEX={}
w_act_diff_ratio=.6
w_search_pen=.4
w_growth=.8
pop_per=0.00012 # from 0-1, percentage of population that are infected each day

# reduction_in_activity_percentage={} # reduction in activity since g_dict is more than 0.012% of the population
# multiply g_dict by (sp_dict+reduction_in_activity_percentage)
# then scale between 0-10


def ignore_timestamp_zone(stamp):
    return pd.Timestamp("{0}-{1}-{2}".format(stamp.year,stamp.month,stamp.day))
def add_utc_stamp(stamp):
    return pd.Timestamp("{0}-{1}-{2}".format(stamp.year,stamp.month,stamp.day),tz="UTC")

c2pop={'China': 1402870000, 'India': 1363010000, 'United States of America': 331362000, 'Indonesia': 268074600,
'Brazil': 211563000, 'Pakistan': 208857000, 'Nigeria': 200962417, 'Bangladesh': 168698000, 'Guinea': 146793744, 
'Mexico': 126577691, 'Japan': 126200000, 'Philippines': 109483000, 'Egypt': 100605100, 'Ethiopia': 98665000, 
'Viet Nam': 95354000, 'Taiwan, Republic of China': 86727573, 'Germany': 82979100, 'Iraq': 83489300, 'Turkey': 82003882,
'France': 66992000, 'Thailand': 66511080, 'United Kingdom': 66040229, 'Italy': 60375749, 'South Africa': 57725600,
'Albania': 55890747, 'Myanmar': 54339766, 'Kenya': 52214791, 'Colombia': 49849818, 'Spain': 46733038,
'Argentina': 44938712, 'Algeria': 43378027, 'Ukraine': 42101650, 'Sudan': 42528282, 'Uganda': 40006700, 
'Poland': 38413000, 'Canada': 37922800, 'Morocco': 35386900, 'Uzbekistan': 34192718, 'Saudi Arabia': 33413660, 
'Malaysia': 33201700, 'Peru': 32495510, 'Senegal': 32219521, 'Afghanistan': 31575018, 'Ghana': 30280811, 
'Angola': 30175553, 'Nepal': 29609623, 'Yemen': 29579986, 'Mozambique': 27909798, 'Australia': 25799100,
'Madagascar': 25263000, 'Cameroon': 24348251, 'Niger': 22314743, 'Sri Lanka': 21670112, 'Burkina Faso': 20870060, 
'Mali': 19973000, 'Romania': 19523621, 'Chile': 19107216, 'Serbia': 7001444, 'Kazakhstan': 18710200, 'Guatemala': 17679735, 
'Malawi': 17563749, 'Zambia': 17381168, 'Netherlands': 17402000, 'Ecuador': 17495900, 'Cambodia': 16289270, 'Chad': 15692969, 
'Somalia': 15636171, 'Zimbabwe': 15159624, 'South Sudan': 12778250, 'Rwanda': 12374397, 'Benin': 11733059, 'Haiti': 11577779, 
'Tunisia': 11551448, 'Bolivia': 11469896, 'Belgium': 11463692, 'Cuba': 11221060, 'Burundi': 10953317, 'Greece': 10741165,
'Czech Republic': 10649800, 'Jordan': 10691400, 'Dominican Republic': 10358320, 'Portugal': 10291027, 'Sweden': 10255102, 
'Azerbaijan': 9981457, 'Hungary': 9778371, 'United Arab Emirates': 9682088, 'Belarus': 9465300, 'Honduras': 9158345, 
'Israel': 9202530, 'Tajikistan': 8931000, 'Austria': 8859992, 'Papua New Guinea': 8558800, 'Switzerland': 8542323,
'Sierra Leone': 7901454, 'Togo': 7538000, 'Congo (Kinshasa)': 7482500, 'Paraguay': 7152703, 'Gabon': 7123205, 'Bulgaria': 7000039,
'El Salvador': 6704864, 'Libya': 6569864, 'Nicaragua': 6393824, 'Kyrgyzstan': 6389500, 'Lebanon': 6065922, 'Denmark': 5811413, 
'Singapore': 5638700, 'Republic of Kosovo': 5542197, 'Finland': 5518393, 'Central African Republic': 5496011, 'Slovakia': 5450421,
'Norway': 5334762, 'Eritrea': 5309659, 'Costa Rica': 5058007, 'New Zealand': 5068840, 'Ireland': 4857000, 'Oman': 4686829, 
'Liberia': 4475353, 'Kuwait': 4420110, 'Panama': 4218808, 'Croatia': 4105493, 'Mauritania': 4077347, 'Georgia': 3723500, 
'Moldova': 3547539, 'Uruguay': 3518552, 'Bosnia and Herzegovina': 3502550, 'Mongolia': 3320097, 'Equatorial Guinea': 3195153,
'Armenia': 2962100, 'Lithuania': 2790472, 'Qatar': 2772294, 'Jamaica': 2726667, 'Namibia': 2458936, 'Botswana': 2338851,
'Gambia': 2228075, 'Slovenia': 2080908, 'Lesotho': 2007201, 'Latvia': 1915100, 'Comoros': 1798506, 'Guinea-Bissau': 1604528,
'Bahrain': 1543300, 'Estonia': 1324820, 'Trinidad and Tobago': 1359193, 'Mauritius': 1265577, 'Djibouti': 1078373, 'Fiji': 884887,
'Cyprus': 864200, 'Guyana': 786508, 'Bhutan': 741672, 'Montenegro': 622359, 'Luxembourg': 613894, 'Western Sahara': 582478, 'Suriname': 573085,
'Cape Verde': 550483, 'Malta': 475701, 'Belize': 398050, 'Bahamas': 385340, 'Maldives': 378114, 'Iceland': 358780, 'Brunei Darussalam': 421300,
'Barbados': 287010, 'Sao Tome and Principe': 201784, 'Saint Lucia': 180454, 'Saint Vincent and Grenadines': 110520, 'Grenada': 108825, 
'Korea (South)': 51811167, 'Antigua and Barbuda': 104084, 'Seychelles': 96762, 'Andorra': 76177, 'Dominica': 74679,
'Saint Kitts and Nevis': 56345, 'Liechtenstein': 38380, 'Monaco': 38300,'San Marino': 35746, 'Russian Federation': 146793744,
'Iran, Islamic Republic of': 83489300, 'Tanzania, United Republic of': 55890747, 'Venezuela (Bolivarian Republic)': 32219521,
'Syrian Arab Republic (Syria)': 18499181, 'Congo (Brazzaville)': 5542197, 'Swaziland': 8542323, 'Palestinian Territory': 4976684, 'Timor-Leste': 1268000, 
'Holy See (Vatican City State)': 800, 'Lao PDR': 7123205, 'Macedonia, Republic of': 2075301, "Côte d'Ivoire": 25070000}
it_is_srys={} # when was it srys for each country? 
#srys is defined as when the growth rate is more than pop_thresh cases per day
for country in g_dict.keys():
    try:
        pop_thresh=c2pop[country]*pop_per
        
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
        utc_date=add_utc_stamp(date) # change tz to UTC to gain consitancy across all date based dict keys
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
    act_diff_ratio.update({c_name:(b4_turning_point[c_name]-after_turning_point[c_name])/b4_turning_point[c_name]})




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

a=0
CASPER_INDEX_SORTED={}
for k, v in sorted(CASPER_INDEX.items(), key=lambda item: item[1]):
    a+=1
    CASPER_INDEX_SORTED.update({k:a})
    
    
if __name__=="__main__":
    print("Saving CASPER score as ",save_as)
    with open(save_as, 'w+') as handle:
        json.dump(CASPER_INDEX_SORTED, handle)
