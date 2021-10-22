import streamlit as st
import pyowm
from datetime import datetime
from collections import defaultdict
import pandas as pd      
owm=pyowm.OWM('e2acae24364ca45b1b65c43c8e770355')
mgr=owm.weather_manager()
st.title('5-Days Temperature Graph')
st.subheader("Give the Place's Name and Temperture Unit")
place=st.text_input('NAME OF PLACE')


unit=st.selectbox("SELECT TEMPERATURE UNIT",('Celsius','Fahrenheit','Kelvin'))
graph_type=st.selectbox("SELECT GRAPH TYPE",('Line Graph','Bar Graph'))
if unit=='Celsius':
    unit='celsius'
elif unit == 'Fahrenheit':
    unit='fahrenheit'
else:
    unit='kelvin'
def get_data():
    temp=[]
    dates=[]
    forcast=mgr.forecast_at_place(place,'3h')
    data=forcast.forecast.weathers
    for weather in data:
        d=datetime.utcfromtimestamp(weather.reference_time()).strftime("%d/%m/%y")
        dates.append(d)
        temp.append(weather.temperature(unit)['temp'])
    data=defaultdict(list)
    for d, t in zip(dates,temp):
        data[d].append(t)
    return data
def dataFrame():
    data=get_data()
    datas=[]
    dates=[]
    for d,t in data.items():
        datas.append((min(t),max(t)))
        dates.append(d)
    return (datas,dates)
def line_graph():
    datas,dates=dataFrame()
    df=pd.DataFrame(datas,columns=['Temp_min','Temp_max'],index=dates)
    st.line_chart(df)
    

def bar_graph():
    datas,dates=dataFrame()
    df=pd.DataFrame(datas,columns=['Temp_min','Temp_max'],index=dates)
    st.bar_chart(df)
    
if st.button("SUBMIT"):
    try:
        if graph_type=='Line Graph':
            line_graph()
            st.balloons()
        else:
            bar_graph()
            st.balloons()
    except:
        st.warning('Input valid  place name')
        