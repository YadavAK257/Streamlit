import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import seaborn as sns

df=pd.read_csv('startup_cleaned.csv')
st.set_page_config(layout='wide',page_title='Startup Analysis')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

#st.dataframe(df)
st.sidebar.title('Startup Funding Analysis')
opt = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

def load_investor_details(investor):
    st.title(investor)
    last5_df = df[df['investors'].str.contains(investor,na=False)].head()[
        ['date','Startup','Vertical','City  Location','round','amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)
    invest_amt = df[df['investors'].str.contains(investor,na=False)].groupby('Startup')['amount'].sum().sort_values(ascending=False).head(1)
    st.subheader('Investors max investment in Company')
    st.dataframe(invest_amt)

    col1,col2,col3=st.columns(3)
    with col1:
        big_series = df[df['investors'].str.contains(investor,na=False)].groupby('Startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig,ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)

    with col2:
        vertical_series = df[df['investors'].str.contains(investor,na=False)].groupby('Vertical')['amount'].sum()
        st.subheader('Sectors Invested')
        fig1,ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f%%")
        st.pyplot(fig1)

    with col3:
        city_invest = df[df['investors'].str.contains(investor,na=False)].groupby('City  Location')['amount'].sum()
        st.subheader('Cities Invested')
        fig2,ax2 = plt.subplots()
        ax2.pie(city_invest,labels=city_invest.index,autopct="%0.01f%%")
        st.pyplot(fig2)

    col1,col2=st.columns(2)
    with col1:
        round_invest = df[df['investors'].str.contains(investor, na=False)].groupby('Vertical')['amount'].sum()
        st.subheader('Round Invested')
        fig,ax = plt.subplots()
        ax.pie(round_invest,labels=round_invest.index,autopct="%0.01f%%")
        st.pyplot(fig)

    with col2:
        subvert_invest = df[df['investors'].str.contains(investor, na=False)].groupby('Vertical')['amount'].sum()
        st.subheader('Subvertical Invested')
        fig1,ax1 = plt.subplots()
        ax1.pie(subvert_invest,labels=subvert_invest.index,autopct="%0.01f%%")
        st.pyplot(fig1)

    col1,col2 = st.columns(2)
    with col1:
        df['year'] = pd.to_datetime(df['date']).dt.year
        yearly = df[df['investors'].str.contains(investor,na=False)].groupby('year')['amount'].sum()
        st.subheader('Yearly Investment')
        fig5,ax5 = plt.subplots()
        ax5.plot(yearly.index, yearly.values)
        st.pyplot(fig5)

    print(df.info())

def overall_analysis():
    st.title('Overall Analysis')

    # Total invested amount
    total = round(df['amount'].sum())
    # Max amount infused in a startup
    max_funding = df.groupby('Startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    # Avg ticket size
    avg_funding = df.groupby('Startup')['amount'].sum().mean()
    # Total funded startups
    num_startups = df['Startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Total',str(total) + ' Cr')
    with col2:
        st.metric('Max',str(max_funding) + ' Cr')
    with col3:
        st.metric('Avg', str(round(avg_funding)) + ' Cr')
    with col4:
        st.metric('Funded Startups',num_startups)

    st.header('MoM Graph')
    select_opt = st.selectbox('Select Type', ['Total', 'Count'])

    if select_opt == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x-axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x-axis'], temp_df['amount'])

    st.pyplot(fig3)

def startup_data(startup):
    st.title('Akshat Yadav --- FS23AI013')
    st.header('Founders:')

    # Filter the DataFrame to select rows where the 'Startup' column
    startup_df = df[df['Startup'] == startup]
    # Print the names of investors in the startup
    investors = pd.DataFrame(startup_df['investors'],columns=['investors']).reset_index()
    # Display the DataFrame
    st.write(investors)

    col1, col2 = st.columns(2)
    with col1:
        st.title('Industry')
        industry_details = df[df['Startup'].str.contains(startup,na=False)]['Vertical'].str.lower().value_counts().head()
        fig,ax = plt.subplots()
        ax.pie(industry_details,labels=industry_details.index,autopct='%1.1f%%',startangle=90)
        ax.set_title('Industry Data Distribution')
        st.pyplot(fig)

    with col2:
        st.title('Sub-Industry')
        sub_industry_details = df[df['Startup'].str.contains(startup,na=False)]['subvertical'].str.lower().value_counts().head()
        fig1,ax1 = plt.subplots()
        ax1.pie(sub_industry_details,labels=sub_industry_details.index,autopct='%1.1f%%',startangle=90)
        ax1.set_title('Sub-Industry Data Distribution')
        st.pyplot(fig1)

    # 'City' section as a pie chart
    st.title('City')
    city_details = startup_df.groupby('City  Location')['investors'].count().sort_values(ascending=False).head()
    fig1,ax1 = plt.subplots()
    ax1.pie(city_details,labels=city_details.index,autopct='%1.1f%%',startangle=90)
    ax1.set_title('City Data Distribution')
    st.pyplot(fig1)

    st.header('Funding Rounds')
    funding_rounds_info = startup_df[['round', 'investors', 'date']].sort_values('date', ascending=False)
    st.dataframe(funding_rounds_info)


if opt == 'Overall Analysis':
    overall_analysis()

elif opt == 'Startup':
    st.title("Startup Analysis")
    select = st.sidebar.selectbox('Select One', sorted(set(df['Startup'].astype(str).str.split(',').sum())))
    btn1 = st.sidebar.button('Find Startup Details')
    if btn1:
        st.title(select)
        startup_data(select)

else:
    st.title('Investor')
    select_investor = st.sidebar.selectbox('Select One', sorted(set(df['investors'].astype(str).str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(select_investor)