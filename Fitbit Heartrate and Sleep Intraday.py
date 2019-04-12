#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import fitbit
import Oauth2
import pandas as pd 
import datetime
CLIENT_ID = '22DKWR'
CLIENT_SECRET = 'da454d65f2795e5784e9d682f46a2089'

server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['https://api.fitbit.com/oauth2/token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['https://api.fitbit.com/oauth2/token'])
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)


# In[ ]:


yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d"))
yesterday2 = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
today = str(datetime.datetime.now().strftime("%Y%m%d"))


# In[ ]:


fit_statsHR = auth2_client.intraday_time_series('activities/heart', base_date=yesterday2, detail_level='1sec')


# In[ ]:


time_list = []
val_list = []
for i in fit_statsHR['activities-heart-intraday']['dataset']:
    val_list.append(i['value'])
    time_list.append(i['time'])
heartdf = pd.DataFrame({'Heart Rate':val_list,'Time':time_list})


# In[ ]:


heartdf = pd.Dataframe({'Heart Rate':val_list,'Time':time_list})


# In[ ]:


heartratedf


# In[ ]:


heartdf.to_csv('/Users/shsu/Downloads/python-fitbit-master/Heart/heart'+                yesterday+'.csv',                columns=['Time','Heart Rate'], header=True,                index = False)


# In[ ]:


fit_statsSl = auth2_client.sleep(date='today')
stime_list = []
sval_list = []
for i in fit_statsSl['sleep'][0]['minuteData']:
    stime_list.append(i['dateTime'])
    sval_list.append(i['value'])
sleepdf = pd.DataFrame({'State':sval_list,
                     'Time':stime_list})
sleepdf['Interpreted'] = sleepdf['State'].map({'2':'Awake','3':'Very Awake','1':'Asleep'})
sleepdf.to_csv('/Users/shsu/Downloads/python-fitbit-master/Sleep/sleep' +                today+'.csv',                columns = ['Time','State','Interpreted'],header=True, 
               index = False)


# In[ ]:


fit_statsSum = auth2_client.sleep(date='today')['sleep'][0]
ssummarydf = pd.DataFrame({'Date':fit_statsSum['dateOfSleep'],
                'MainSleep':fit_statsSum['isMainSleep'],
               'Efficiency':fit_statsSum['efficiency'],
               'Duration':fit_statsSum['duration'],
               'Minutes Asleep':fit_statsSum['minutesAsleep'],
               'Minutes Awake':fit_statsSum['minutesAwake'],
               'Awakenings':fit_statsSum['awakeCount'],
               'Restless Count':fit_statsSum['restlessCount'],
               'Restless Duration':fit_statsSum['restlessDuration'],
               'Time in Bed':fit_statsSum['timeInBed']
                        } ,index=[0])

