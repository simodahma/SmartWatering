# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")





#mintemp,maxtemp,avgtemp,relhumidity data
#https://api.aerisapi.com/forecasts/55415?filter=3hr&limit=40&client_id=hx6HDjGjSsdWBd5ZYZlTE&client_secret=TJI6hvhnOX1ZJXdbcN0JpNtwCJwmgNtoDApVy6FC
#Solar radiation data
#https://api.weatherbit.io/v2.0/forecast/hourly?city=Raleigh,NC&key=1d29b7ef92d14577917e2bcd5340df8d&
import json
import requests
response = requests.get('https://api.aerisapi.com/forecasts/55415?filter=3hr&limit=40&client_id=hx6HDjGjSsdWBd5ZYZlTE&client_secret=TJI6hvhnOX1ZJXdbcN0JpNtwCJwmgNtoDApVy6FC').text

json_data = json.loads(response)
response2 = requests.get('https://api.weatherbit.io/v2.0/forecast/hourly?city=Raleigh,NC&key=1d29b7ef92d14577917e2bcd5340df8d&').text

json_data2 = json.loads(response2)

sr = []
time = []
maxtemp = []
mintemp = []
avgtemp = []
humidity = []

for i in range(0,40):

  for item in json_data['response']:
    vtime = item['periods'][i]['validTime']
    vtime = vtime.replace("-05:00","")
    for item2 in json_data2['data']:
      if vtime == item2['timestamp_utc']:
        sr.append(item2['solar_rad']/2.06)
        time.append(item['periods'][i]['validTime'])
        maxtemp.append(item['periods'][i]['maxTempC'])
        mintemp.append(item['periods'][i]['minTempC'])
        avgtemp.append(item['periods'][i]['avgTempC'])
        humidity.append(item['periods'][i]['humidity'])

        
test = {
    'maxairtemp' : maxtemp,
    'minairtemp' : mintemp,
    'avgairtemp' : avgtemp,
    'relhumidity' : humidity,
    'avgsr' : sr
}
columns = ['maxairtemp','minairtemp','avgairtemp','relhumidity','avgsr']
df = pd.DataFrame(test, columns=columns)
#Soil Moisture Predicted Data
smpd = loaded_model.predict(df)










#Planning Algorithme


#returning the remaining number of hours till the next irrigation schedule
i = 0
h = []
#daily moisture accumilation
dm1 = 0
dm2 = 0
for sm in smpd:
  i=i+1
  if i < 9:
    dm1 = dm1 + sm[0]
  else:
    dm2 = dm2 + sm[0]
  
s = []
#Day 1
#if dm1 > 7*50:
  #Do not irrigate for the day
if dm1 > 4*50 and dm1<7*50:
    #Irrigate once a day
    m1 = []
    for i in range(0,7):
      m1.append(smpd[i])
    h.append(m1.index(min(m1)+1)*3)
elif dm1<4*50:
    #Irrigate twice a day
    h.append(3*3)
    h.append(5*3)

#Day 2
#if dm2 > 7*50:
  #Do not irrigate for the day
if dm2 > 4*50 and dm2<7*50:
  #Irrigate once a day
  m1 = []
  for i in range(8,15):
    m1.append(smpd[i])
  h.append(m1.index(min(m1)+1)*3)
elif dm2<4*50:
    #Irrigate twice a day
  h.append(10*3)
  h.append(13*3)

print(h)






