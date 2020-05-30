import os
import sys
import json
import time
import tqdm
import numpy as np
import pandas as pd
import xarray as xr
import pickle as pkl
import requests as req



def load_covid_df():
    st_f_name="covid19API.json"
    dw=False
    print("Loading Covid-19 Data")
    
    if os.path.exists(st_f_name):
        time_in_secs=os.stat(st_f_name).st_mtime
        if (time.time()-time_in_secs)>(60*60*24):
            print("file on disc too old fetching new version")
            dw=True
    else:
        print("couldn't find covid19API.json\nDownloading...")
        dw=True
    
    if dw:
        a=json.loads(req.get("https://api.covid19api.com/all").content)
        json.dump(a,open("covid19API.json","w+"))

    return pd.read_json("covid19API.json")

def get_countries_dict(covid_df):
    d=covid_df[["Country","Lat","Lon"]].copy().drop_duplicates()
    countries_dict={}
    for i in np.array(d):
        lat=i[1]
        lot=i[2]
        country_name=i[0]
        try: 
            countries_dict.update({country_name: countries_dict[country_name]+[(lat,lot)] })
        except KeyError:
            countries_dict.update({country_name:[(lat,lot)] })
    print("Found",sum([len(i) for i in countries_dict.keys()]),"Population Centers in",len(countries_dict.keys()),"Countries")
    return countries_dict

def get_mean_col(df,geo_dist_factor,countries_dict):
    means_list=np.zeros(shape=(0,)) 
    c_dict={}
    idxes_file=np.array([[i[0],i[1]] for i in np.array(df.index)])
    df=np.asarray(df)
    for c_name in countries_dict.keys():
        for c_idx in range(len(countries_dict[c_name])): # some contries have more than one city registred 
            x,y=countries_dict[c_name][c_idx]
            idx_of_xny=np.where (  # numpy black magic search for x,y pairs that are within geo_dist_factor of the x,y pairs
                (np.abs(idxes_file[:,0]-x)<=geo_dist_factor)
                & 
                (np.abs(idxes_file[:,1]-y)<=geo_dist_factor)
            )[0]
            
            no2_amounts=df[idx_of_xny]
            no2_amounts = no2_amounts[np.logical_not(np.isnan(no2_amounts))] # remove all NaNs
            means_list=np.hstack([means_list,no2_amounts])
        
        #after we are done appending NO2 ammounts of population centers to a
        #mean and append and reset means_list
        c_dict.update({c_name:np.mean(means_list)/1000000000000000}) #np.mean result somehow needs to be renormalized into range? why?
        means_list=np.zeros(shape=(0,))
                        
    return c_dict

def compute_dates_no2_mean_dict(geo_dist_factor,data_dir,countries_dict,col_name="ColumnAmountNO2",save_as="dates_dict.pkl"):
    print("Computing Mean NO2 per day per country")
    try:
        dates_dict=pkl.load(open(save_as,"rb"))
        print("loaded dates_dict from file")
    except FileNotFoundError:
        dates_dict={}

    for df_name in tqdm.tqdm([i for i in os.listdir(data_dir) if i.endswith(".nc4")]):
        date=df_name.split("-")[-2].split("_")[-2]
        y,md=date.split("m")
        m=md[:2]
        d=md[2:4]
        date=pd.Timestamp('{0}-{1}-{2}'.format(y,m,d)) #because g_dict uses the same classes Consistancy FTW
        if date in dates_dict.keys():
            continue
        
        df = xr.open_dataset(data_dir+df_name).to_dataframe()[col_name]
        mean_dict=get_mean_col(df,geo_dist_factor,countries_dict)
        dates_dict.update({date:mean_dict})

    print("Saving data as",save_as)

    with open(save_as, 'wb+') as handle:
        pkl.dump(dates_dict, handle, protocol=pkl.HIGHEST_PROTOCOL)
    return dates_dict

def compute_growth_dict(covid_df,save_as="g_dict.pkl"):
    g_dict={} 
    # NOTICE:
    '''
    1-g_dict it offset from the actual case growth by 2 days (good enough I am not fixing it)
    2-g_dict is sometimes negative if recovred cases are more than new cases (used by the weighting algo)
    '''
    ccd=np.asarray(covid_df[["Country","Confirmed","Date"]])
    for idx,row in enumerate(ccd):
        country=row[0]
        confirmed=row[1]
        date=row[2]
        if country not in g_dict.keys():
            g_dict.update({country:{date:ccd[idx+1][1]-confirmed}})
        else:
            try:
                if ccd[idx+1][0]==country:
                    g_dict[country].update({date:ccd[idx+1][1]-confirmed})
                else:
                    pass
            except:
                pass
    print("saving g_dict as",save_as)
    with open(save_as, 'wb+') as handle:
        pkl.dump(g_dict, handle, protocol=pkl.HIGHEST_PROTOCOL)
    return g_dict

if __name__=="__main__":
    geo_dist_factor=2 #in lat/lot degrees what's the range to consider in a city?
    mean_col_name="ColumnAmountNO2" # what column of the data to consider for our operations?
    data_dir="data/"

    covid_df=load_covid_df()
    countries_dict=get_countries_dict(covid_df)
    compute_dates_no2_mean_dict(geo_dist_factor,data_dir,countries_dict,col_name=mean_col_name)
    compute_growth_dict(covid_df)