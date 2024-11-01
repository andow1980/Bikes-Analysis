import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
st.set_page_config(layout='wide')

data1 = pd.read_csv("data.csv") 

#df = st.dataframe(data1)

def page1(df):  
    tab1, tab2, tab3 = st.tabs(['TAB1', 'TAB2','TAB3'])
    year = st.sidebar.radio('Select year', df['year'].unique())
    df = df[df['year']== year]

    with tab1 :

        col1 , col2 = st.columns(2)
        with col1 :
            st.plotly_chart(px.line(df, x='date', y='rented_bikes_count', title='Bike Rentals') , key = 1 )
            st.plotly_chart(px.bar(df, x='hour', y='rented_bikes_count', title='Bike Rentals by Hour') , key = 2 )   
        with col2 :
            st.plotly_chart(px.box(df, x='day_name', y='rented_bikes_count', title='Bike Rentals by Weekday') , key = 3 )
            st.plotly_chart(px.scatter(df, x='temp', y='rented_bikes_count', title='Temperature vs Bike Rentals') , key = 4 )

# ------------------------------------------------------------------------------

    with tab2 :

        col1 , col2 = st.columns(2)
        with col1 :
            st.plotly_chart(px.scatter(df, x='humidity', y='rented_bikes_count', title='Humidity vs Bike Rentals') , key = 5)
            st.plotly_chart(px.line(df, x='month', y='rented_bikes_count', title='Bike Rentals by Month') , key = 6) 
        with col2 :
            st.plotly_chart(px.violin(df, x='quarter', y='rented_bikes_count', color='season',box=True ,title='Bike Rentals by Day of Week') , key = 7)
            st.plotly_chart(px.scatter(df, x='registered', y='casual', color='Profit' ,title='Casual vs Registered Users') , key = 8)
#--------------------------------------------------------------------------------

    with tab3 :

        col1 , col2 = st.columns(2)
        with col1 :
            st.plotly_chart(px.histogram(df, x='registered', y = 'Profit', color='season', title='Rental Durations by Month') , key = 9)
            st.plotly_chart(px.histogram(df, x='casual', y = 'Profit', color='season', title='Rental Durations by Month'), key = 10) 
        with col2 :
            st.plotly_chart(px.bar(df[df['workingDay'] == False], x='quarter', y="Profit", title="Quarter Profit on Holidays"), key = 11)
            st.plotly_chart(px.bar(df[df['workingDay'] == True], x='quarter', y="Profit", title="Quarter Profit on WorkingDay") , key = 12)

def page2(df):
    month = st.sidebar.selectbox('select month' , df['month'].unique())
    st.plotly_chart(px.bar(df[df['month'] == month], x='hour', y='rented_bikes_count', title='Best Hour for Bike Rentals'))
    
def page3(df):
    day = st.sidebar.selectbox('select day_name' , df['day_name'].unique())
    peak_hours = df[df['hour'].isin([7, 8, 9, 17, 18, 19])]
    peak_hours_day = peak_hours[peak_hours['day_name'] == day]
    st.plotly_chart(px.histogram( peak_hours_day , x='workingDay', y='Profit', color='day_period', title='WorkingDay Profit Per Day Period During Peak Hours'))

def page4(df):
    quarter = st.sidebar.selectbox('select quarter' , df['quarter'].unique())
    st.plotly_chart(px.histogram( df[df['quarter'] == quarter] , x='month_name' ,y='Profit', title="Quarter's Profit"))

def page5(df):
    st.header("Top Profit by Month & Quarter")

    # اعلى شهر  
    top_month = df.groupby('month_name')['Profit'].sum().idxmax()
    top_month_profit = df.groupby('month_name')['Profit'].sum().max()
    top_month_year = df[df['month_name'] == top_month]['year'].unique()[0] 

    # اعلى كوارتر
    top_quarter = df.groupby('quarter')['Profit'].sum().idxmax()
    top_quarter_profit = df.groupby('quarter')['Profit'].sum().max()
    top_quarter_year = df[df['quarter'] == top_quarter]['year'].unique()[0] 

    # اعلى شهر من حيث الربح
    top_year_profit = df.groupby('year')['Profit'].sum().idxmax()
    top_year_profit_by_year_value = df.groupby('year')['Profit'].sum().max()
    #top_month_profit_by_month_year = df[df['month'] == top_month_profit_by_month]['year'].unique()[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Top Month Profit", value=f"{top_month_profit:.2f}", delta=f"{top_month} ({top_month_year})")  

    with col2:
        st.metric(label="Top Quarter Profit", value=f"{top_quarter_profit:.2f}", delta=f"{top_quarter} ({top_quarter_year})")

    with col3:
        st.metric(label="Top Year Profit", value=f"{top_year_profit_by_year_value:.2f}", delta=f"{top_year_profit}")
pgs= {
    'year' : page1,
    'month' : page2,
    'day name' : page3,
    'quarter' : page4,
    'Top Profit' : page5 
}

pg = st.sidebar.radio('Navigate Pages', options= pgs.keys())
pgs[pg](data1) 
