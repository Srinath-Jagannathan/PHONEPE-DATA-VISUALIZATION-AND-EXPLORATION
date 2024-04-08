import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
import plotly.express as px
import requests
import json
from PIL import Image


#Data frame creation

#SQL Connection

mydb = mysql.connector.connect( host="localhost",
                                user="root",
                                password="Bharath@36",
                                database="phonepe_data")

cursor = mydb.cursor()


# 1 - Aggre_insurance_df

# Execute the SELECT query
cursor.execute("select * from aggre_insurance")

# Fetch the results
table1 = cursor.fetchall()


# Commit the transaction
mydb.commit()

# Create a DataFrame from the fetched results
Aggre_Insurance = pd.DataFrame(table1,columns= ("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))


# 2 - Aggre_Transactions df

# Execute the SELECT query
cursor.execute("select * from aggre_transactions")


# Fetch the results
table2 = cursor.fetchall()


# Commit the transaction
mydb.commit()

# Create a DataFrame from the fetched results
Aggre_Transactions = pd.DataFrame(table2,columns= ("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))


# 3 - Aggre_user df

# Execute the SELECT query
cursor.execute("select * from aggre_user")


# Fetch the results
table3 = cursor.fetchall()


# Commit the transaction
mydb.commit()

# Create a DataFrame from the fetched results
Aggre_user = pd.DataFrame(table3,columns= ("States","Years","Quarter","Brands","Transaction_count","Percentage"))


# 4 - map_Insurance df

# Execute the SELECT query
cursor.execute("select * from map_insurance")


# Fetch the results
table4 = cursor.fetchall()


# Commit the transaction
mydb.commit()

# Create a DataFrame from the fetched results
Map_insurance = pd.DataFrame(table4,columns= ("States","Years","Quarter","District","Transaction_count","Transaction_amount"))



# 5 - map_transaction df

# Execute the SELECT query
cursor.execute("select * from map_transaction")


# Fetch the results
table5 = cursor.fetchall()


# Commit the transaction
mydb.commit()

# Create a DataFrame from the fetched results
Map_transaction = pd.DataFrame(table5,columns= ("States","Years","Quarter","District","Transaction_count","Transaction_amount"))


# 6 - map_user df

# Execute the SELECT query
cursor.execute("select * from map_user")


# Fetch the results
table6 = cursor.fetchall()


# Commit the transaction
mydb.commit()

# Create a DataFrame from the fetched results
Map_user = pd.DataFrame(table6,columns= ("States","Years","Quarter","District","RegisteredUsers","AppOpens"))


# 7 - top_insurance df

# Execute the SELECT query
cursor.execute("select * from top_insurance")


# Fetch the results
table7 = cursor.fetchall()


# Commit the transaction
mydb.commit()

# Create a DataFrame from the fetched results
Top_insurance = pd.DataFrame(table7,columns= ("States","Years","Quarter","Pincode","Transaction_count","Transaction_amount"))


# 8 - top_transaction df

# Execute the SELECT query
cursor.execute("select * from top_transaction")


# Fetch the results
table8 = cursor.fetchall()


# Commit the transaction
mydb.commit()

# Create a DataFrame from the fetched results
Top_transaction = pd.DataFrame(table8,columns= ("States","Years","Quarter","Pincode","Transaction_count","Transaction_amount"))


# 9 - top_user df

# Execute the SELECT query
cursor.execute("select * from top_user")


# Fetch the results
table9 = cursor.fetchall()


# Commit the transaction
mydb.commit()

# Create a DataFrame from the fetched results
Top_user = pd.DataFrame(table9,columns= ("States","Years","Quarter","Pincode","RegisteredUsers"))


#Trasaction_year_wise

# This function plots transaction amount and count year-wise for a given year.
# It generates bar charts for transaction amount and count, as well as choropleth maps for transaction amount and count distribution across states.

def Transaction_amount_count_year(df,year):
    
    Tran_amount_count_year = df[df["Years"] == year] 

    Tran_amount_count_year.reset_index(drop=True,inplace =True) 

    Tran_amount_count_year_group = Tran_amount_count_year.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    Tran_amount_count_year_group.reset_index(inplace =True)

    col1,col2 = st.columns(2)

    with col1:
        fig_amount = px.bar(Tran_amount_count_year_group,x = "States", y ="Transaction_amount",title= f"{year} TRANSACTION_AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Plasma, height= 650, width= 600)
        
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(Tran_amount_count_year_group,x = "States", y ="Transaction_count",title= f"{year} TRANSACTION_COUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height= 650, width= 600)

        st.plotly_chart(fig_count)

    
    col1,col2 = st.columns(2)

    with col1:

        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        
        fig_india_1 = px.choropleth(Tran_amount_count_year_group,geojson= url, locations= "States",featureidkey= "properties.ST_NM",
                                    color = "Transaction_amount", color_continuous_scale = "Rainbow", 
                                    range_color = (Tran_amount_count_year_group["Transaction_amount"].min(),Tran_amount_count_year_group["Transaction_amount"].max()),
                                    hover_name = "States", title = f"{year} TRANSACTION AMOUNT", fitbounds = "locations",
                                    height= 600, width= 600)
        fig_india_1.update_geos(visible= False)

        st.plotly_chart(fig_india_1)


    with col2:

        fig_india_2 = px.choropleth(Tran_amount_count_year_group,geojson= url, locations= "States",featureidkey= "properties.ST_NM",
                                    color = "Transaction_count", color_continuous_scale = "Rainbow", 
                                    range_color = (Tran_amount_count_year_group["Transaction_count"].min(),Tran_amount_count_year_group["Transaction_count"].max()),
                                    hover_name = "States", title = f"{year} TRANSACTION COUNT", fitbounds = "locations",
                                    height= 600, width= 600)
        fig_india_2.update_geos(visible= False)

        st.plotly_chart(fig_india_2)

    return Tran_amount_count_year


# This function plots transaction amount and count quarter-wise for a given quarter.
# It generates bar charts for transaction amount and count, as well as choropleth maps for transaction amount and count distribution across states.

def Transaction_amount_count_year_Quarter(df, quarter):

    Tran_amount_count_year = df[df["Quarter"] == quarter]

    Tran_amount_count_year.reset_index(drop=True,inplace =True)

    Tran_amount_count_year_group = Tran_amount_count_year.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    Tran_amount_count_year_group.reset_index(inplace =True)


    col1,col2 = st.columns(2)

    with col1:

        fig_amount = px.bar(Tran_amount_count_year_group,x = "States", y ="Transaction_amount",title= f"{Tran_amount_count_year['Years'].min()} YEAR {quarter} QUARTER TRANSACTION_AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Plasma,height= 650, width= 600)

        st.plotly_chart(fig_amount)

    with col2:

        fig_count = px.bar(Tran_amount_count_year_group,x = "States", y ="Transaction_count",title= f"{Tran_amount_count_year['Years'].min()} YEAR {quarter} QUARTER TRANSACTION_COUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height= 650, width= 600)

        st.plotly_chart(fig_count)

    col1,col2 = st.columns(2)

    with col1:

        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

        fig_india_1 = px.choropleth(Tran_amount_count_year_group,geojson= url, locations= "States",featureidkey= "properties.ST_NM",
                                    color = "Transaction_amount", color_continuous_scale = "Rainbow", 
                                    range_color = (Tran_amount_count_year_group["Transaction_amount"].min(),Tran_amount_count_year_group["Transaction_amount"].max()),
                                    hover_name = "States", title = f"{Tran_amount_count_year['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds = "locations",
                                    height= 600, width= 600)
        fig_india_1.update_geos(visible= False)

        st.plotly_chart(fig_india_1)

    with col2:
    
        fig_india_2 = px.choropleth(Tran_amount_count_year_group,geojson= url, locations= "States",featureidkey= "properties.ST_NM",
                                    color = "Transaction_count", color_continuous_scale = "Rainbow", 
                                    range_color = (Tran_amount_count_year_group["Transaction_count"].min(),Tran_amount_count_year_group["Transaction_count"].max()),
                                    hover_name = "States", title = f"{Tran_amount_count_year['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds = "locations",
                                    height= 600, width= 600)
        fig_india_2.update_geos(visible= False)

        st.plotly_chart(fig_india_2)

    return Tran_amount_count_year


# This function plots aggregated transaction amount and count for a given state and transaction type.
# It generates pie charts for transaction amount and count distribution across transaction types.
def Aggre_Tran_Transation_type(df,state):

    Tran_amount_count_year_type = df[df["States"] == state]

    Tran_amount_count_year_type.reset_index(drop = True, inplace= True)


    Tran_amount_count_year_type_group = Tran_amount_count_year_type.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    Tran_amount_count_year_type_group.reset_index(inplace = True)

    col1,col2 = st.columns(2)

    with col1:

        fig_pie_1 = px.pie(data_frame= Tran_amount_count_year_type_group,
                                names = "Transaction_type", 
                                values ="Transaction_amount",
                                title= f"{state.upper()} TRANSACTION_AMOUNT",
                                hole = 0.5,
                                width= 600)

        st.plotly_chart(fig_pie_1)

    with col2:

        fig_pie_2 = px.pie(data_frame= Tran_amount_count_year_type_group,
                                names = "Transaction_type", 
                                values ="Transaction_count",
                                title= f"{state.upper()} TRANSACTION_COUNT",
                                hole = 0.5,
                                width= 600)

        st.plotly_chart(fig_pie_2)



# This function plots transaction counts for different brands in a given year.
# It generates a bar chart showing transaction counts for each brand.

def Aggre_user_plot1_year(df, year):

    aguy = df[df["Years"] == year]

    aguy.reset_index(drop=True,inplace =True)

    aguy_group = pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())

    aguy_group.reset_index(inplace =True)

    fig_count = px.bar(aguy_group, 
                        x = "Brands", 
                        y ="Transaction_count",
                        title= f"{year} BRANDS AND TRANSACTION_COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,
                        hover_name= "Brands",
                        height= 650, width= 1000)

    st.plotly_chart(fig_count)

    return aguy


# This function plots transaction counts for different brands in a given quarter.
# It generates a bar chart showing transaction counts for each brand.

def Aggre_user_plot2_Quarter(df,quarter):

    aguyq = df[df["Quarter"] == quarter]

    aguyq.reset_index(drop=True,inplace =True)

    aguyq_group = pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())

    aguyq_group.reset_index(inplace= True)



    fig_count = px.bar(aguyq_group, 
                x = "Brands", 
                y ="Transaction_count",
                title= f"{quarter} QUARTER, BRANDS AND TRANSACTION_COUNT",
                color_discrete_sequence=px.colors.sequential.Magenta_r,
                hover_name= "Brands",
                height= 650, width= 1000)

    st.plotly_chart(fig_count)

    return aguyq


# This function plots transaction counts for different brands in a given state.
# It generates a line chart showing transaction counts for each brand over time.

def Aggre_user_plot3_state(df,state):

    aguyqs= df[df["States"] == state]

    aguyqs.reset_index(drop=True,inplace =True)

    fig_line_1 = px.line(aguyqs, 
                        x = "Brands",
                        y = "Transaction_count",
                        hover_data= "Percentage",
                        title= f"{state.upper()}'S  BRANDS, TRANSACTION COUNT PERCENTAGE",
                        width= 1000,
                        color_discrete_sequence=px.colors.sequential.Magenta_r,
                        markers= True)

    st.plotly_chart(fig_line_1)



# Map_Insurance_District

# This function generates a comparison of transaction amounts and transaction counts for different districts within a specified state.
# It plots horizontal bar charts for transaction amounts and transaction counts for each district.

def Map_Insurance_district(df,state):

    Tran_amount_count_year_type = df[df["States"] == state]

    Tran_amount_count_year_type.reset_index(drop = True, inplace= True)


    Tran_amount_count_year_type_group = Tran_amount_count_year_type.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
    Tran_amount_count_year_type_group.reset_index(inplace = True)

    col1,col2 = st.columns(2)

    with col1:

        fig_bar_1 = px.bar (Tran_amount_count_year_type_group,
                            x = "Transaction_amount", 
                            y ="District",
                            orientation= "h",
                            height= 600,
                            width= 650,
                            title= f"{state.upper()} DISTRICT AND TRANSACTION_AMOUNT",
                            color_discrete_sequence= px.colors.sequential.Plasma)

        st.plotly_chart(fig_bar_1)
    
    with col2:

        fig_bar_2 = px.bar (Tran_amount_count_year_type_group,
                            x = "Transaction_count", 
                            y ="District",
                            orientation= "h",
                            height= 600,
                            width= 650,
                            title= f"{state.upper()} DISTRICT AND TRANSACTION_COUNT",
                            color_discrete_sequence= px.colors.sequential.Greens_r)


        st.plotly_chart(fig_bar_2)


# Map_User_plot1

# This function generates visualizations of registered users and app opens over a specified year for different states.
# It plots a line chart showing the trend of registered users and app opens across different states.
        
def Map_user_plot1_year(df,year):

    Map_user_year = df[df["Years"] == year]

    Map_user_year.reset_index(drop=True,inplace= True)

    Map_user_year_group = Map_user_year.groupby("States")[["RegisteredUsers","AppOpens"]].sum()

    Map_user_year_group.reset_index(inplace= True)


    fig_line_1 = px.line(Map_user_year_group, 
                        x = "States",
                        y = ["RegisteredUsers", "AppOpens"],
                        title= f"{year} REGISTER USERS AND APPOPENS",
                        width= 1000,
                        height= 800,
                        markers= True)


    st.plotly_chart(fig_line_1)

    return Map_user_year


# This function generates visualizations of registered users and app opens over a specified quarter for different states.
# It plots a line chart showing the trend of registered users and app opens across different states.

def Map_user_plot2_quarter(df,quarter):

    Map_user_year_quarter= df[df["Quarter"] == quarter]

    Map_user_year_quarter.reset_index(drop=True,inplace= True)

    Map_user_year_quarter_group = Map_user_year_quarter.groupby("States")[["RegisteredUsers","AppOpens"]].sum()

    Map_user_year_quarter_group.reset_index(inplace= True)


    fig_line_1 = px.line(Map_user_year_quarter_group, 
                            x = "States",
                            y = ["RegisteredUsers", "AppOpens"],
                            title= f"{df['Years'].min()} YEAR, {quarter} QUARTER REGISTER USERS AND APPOPENS",
                            width= 1000,
                            height= 800,
                            markers= True,
                            color_discrete_sequence=px.colors.sequential.Bluered_r)


    st.plotly_chart(fig_line_1)

    return Map_user_year_quarter


# This function generates visualizations of registered users and app opens for different districts within a specified state.
# It plots horizontal bar charts showing the registered users and app opens for each district.

def Map_user_plot3_state(df,state):

    Map_user_year_quarter_state= df[df["States"] == state]

    Map_user_year_quarter_state.reset_index(drop=True,inplace =True)


    col1,col2 = st.columns(2)

    with col1:

        fig_bar_1 = px.bar(Map_user_year_quarter_state, 
                            x = "RegisteredUsers",
                            y = "District",
                            orientation= "h",
                            title= f"{state.upper()}'s REGISTERED USERS",
                            height=800,
                            color_discrete_sequence=px.colors.sequential.Rainbow_r)


        st.plotly_chart(fig_bar_1)

    with col2:  

        fig_bar_2 = px.bar(Map_user_year_quarter_state, 
                            x = "AppOpens",
                            y = "District",
                            orientation= "h",
                            title= f"{state.upper()}'s APPOPENS",
                            height=800,
                            color_discrete_sequence=px.colors.sequential.Rainbow)


        st.plotly_chart(fig_bar_2)



# TOP_INSURANCE_PLOT1:

# This function generates visualizations of transaction amount and count for the top insurance transactions within a specified state.
# It plots two bar charts side by side, one showing the transaction amount and the other showing the transaction count for each quarter.

def Top_insurance_plot_1(df,state):

    Top_Insur_year_State= df[df["States"] == state]

    Top_Insur_year_State.reset_index(drop=True,inplace= True)

    col1,col2 = st.columns(2)


    with col1:
            
        fig_top_insur_bar_1 = px.bar(Top_Insur_year_State, 
                            x = "Quarter",
                            y = "Transaction_amount",
                            hover_data= "Pincode",
                            title= f"{state}'s  TRANSACTION AMOUNT",
                            height=550,
                            color_discrete_sequence=px.colors.sequential.Agsunset)

        st.plotly_chart(fig_top_insur_bar_1)

    with col2:
            
        fig_top_insur_bar_2 = px.bar(Top_Insur_year_State, 
                            x = "Quarter",
                            y = "Transaction_count",
                            hover_data= "Pincode",
                            title= f"{state}'s  TRANSACTION COUNT",
                            height=550,
                            color_discrete_sequence=px.colors.sequential.BuPu_r)


        st.plotly_chart(fig_top_insur_bar_2)


# This function generates a bar chart showing the total number of registered users for each state, with different quarters represented by colors.
# It plots the data for a specified year.

def Top_user_plot_1(df, year):

    tuy = df[df["Years"] == year]

    tuy.reset_index(drop=True,inplace =True)

    tuy_group = pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUsers"].sum())

    tuy_group.reset_index(inplace =True)

    fig_top_plot_1 = px.bar(tuy_group,
                            x ="States",
                            y = "RegisteredUsers",
                            color = "Quarter",
                            title = f"{year} REGISTER USERS",
                            width = 800,
                            height = 800,
                            hover_name= "States",
                            color_discrete_sequence=px.colors.sequential.Blugrn_r)

    st.plotly_chart(fig_top_plot_1)

    return tuy



# TOP_USER_PLOT_2:
# This function generates a bar chart showing the number of registered users for each quarter within a specified state.

def top_user_plot_2(df, state):

    tuys= df[df["States"] == state]

    tuys.reset_index(drop=True,inplace= True)

    fig_top_plot_2 = px.bar(tuys,
                            x = "Quarter",
                            y  = "RegisteredUsers",
                            title= f"{state}'s  RESISTERED_USER , PINCODE, QUARTER",
                            width = 800,
                            height= 800,
                            color= "RegisteredUsers",
                            hover_data= "Pincode",
                            color_continuous_scale= px.colors.sequential.Magenta)

    st.plotly_chart(fig_top_plot_2)




# Top_chart Analysis

# This function generates three bar charts showing transaction amounts for different states.

# Plot_1: Top 10 states with the highest transaction amounts.
# Plot_2: Bottom 10 states with the lowest transaction amounts.
# Plot_3: Average transaction amount for each state.

    
def top_chart_transaction_amount(table_name):
        
    mydb = mysql.connector.connect( host="localhost",
                                    user="root",
                                    password="Bharath@36",
                                    database="phonepe_data")

    cursor = mydb.cursor()


    # Plot_1

    query1 = f'''SELECT States, SUM(Transaction_amount) as  Transaction_amount
                FROM {table_name}
                GROUP BY States
                ORDER BY Transaction_amount desc
                LIMIT 10;'''

    cursor.execute(query1)

    table_1 = cursor.fetchall()

    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns= ("States","Transaction_amount"))

    col1,col2 = st.columns(2)

    with col1:
            
        fig_amount_1 = px.bar(df_1, 
                            x = "States", 
                            y ="Transaction_amount",
                            title= "TOP 10 OF TRANSACTION_AMOUNT",
                            hover_name= "States",
                            color_discrete_sequence=px.colors.sequential.Plasma,
                            height= 650, 
                            width= 600)

        st.plotly_chart(fig_amount_1)


    # Plot_2

    query2 = f'''SELECT States, SUM( Transaction_amount) as Transaction_amount
                FROM {table_name}
                GROUP BY States
                ORDER BY Transaction_amount
                LIMIT 10;'''

    cursor.execute(query2)

    table_2 = cursor.fetchall()

    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns= ("States","Transaction_amount"))

    with col2:

        fig_amount_2 = px.bar(df_2, 
                            x = "States", 
                            y ="Transaction_amount",
                            title= "LEAST 10 TRANSACTION_AMOUNT",
                            hover_name= "States",
                            color_discrete_sequence=px.colors.sequential.Bluered,
                            height= 650, 
                            width= 600)

        st.plotly_chart(fig_amount_2)


    # Plot_3

    query3=  f'''SELECT States, AVG( Transaction_amount) as Transaction_amount
                FROM {table_name}
                GROUP BY States
                ORDER BY Transaction_amount;'''

    cursor.execute(query3)

    table_3 = cursor.fetchall()

    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns= ("States","Transaction_amount"))

    fig_amount_3 = px.bar(df_3, 
                        y = "States", 
                        x ="Transaction_amount",
                        title= "AVERAGE OF TRANSACTION_AMOUNT",
                        hover_name= "States",
                        orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,
                        height= 800, 
                        width= 1000)

    st.plotly_chart(fig_amount_3)



# This function generates three bar charts showing transaction counts for different states.

# Plot_1: Top 10 states with the highest transaction counts.
# Plot_2: Bottom 10 states with the lowest transaction counts.
# Plot_3: Average transaction count for each state.

def top_chart_transaction_count(table_name):
        
    mydb = mysql.connector.connect(host="localhost",
                                    user="root",
                                    password="Bharath@36",
                                    database="phonepe_data")

    cursor = mydb.cursor()


    # Plot_1

    query1 = f'''SELECT States, SUM(Transaction_count) as  Transaction_count
                FROM {table_name}
                GROUP BY States
                ORDER BY Transaction_count desc
                LIMIT 10;'''

    cursor.execute(query1)

    table_1 = cursor.fetchall()

    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns= ("States","Transaction_count"))

    col1,col2 =st.columns(2)

    with col1:
            
        fig_amount_1 = px.bar(df_1, 
                            x = "States", 
                            y ="Transaction_count",
                            title= " TOP 10 OF TRANSACTION_COUNT",
                            hover_name= "States",
                            color_discrete_sequence=px.colors.sequential.Plasma,
                            height= 650, 
                            width= 600)

        st.plotly_chart(fig_amount_1)


    # Plot_2

    query2 = f'''SELECT States, SUM( Transaction_count) as Transaction_count
                FROM {table_name}
                GROUP BY States
                ORDER BY Transaction_count
                LIMIT 10;'''

    cursor.execute(query2)

    table_2 = cursor.fetchall()

    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns= ("States","Transaction_count"))

    with col2:
            
        fig_amount_2 = px.bar(df_2, 
                            x = "States", 
                            y ="Transaction_count",
                            title= "LEAST 10 OF TRANSACTION_COUNT",
                            hover_name= "States",
                            color_discrete_sequence=px.colors.sequential.Bluered,
                            height= 650, 
                            width= 600)

        st.plotly_chart(fig_amount_2)


    # Plot_3

    query3=  f'''SELECT States, AVG( Transaction_count) as Transaction_count
                FROM {table_name}
                GROUP BY States
                ORDER BY Transaction_count;'''

    cursor.execute(query3)

    table_3 = cursor.fetchall()

    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns= ("States","Transaction_count"))

    fig_amount_3 = px.bar(df_3, 
                        y = "States", 
                        x ="Transaction_count",
                        title= "AVERAGE OF TRANSACTION_COUNT",
                        hover_name= "States",
                        orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,
                        height= 800, 
                        width= 1000)

    st.plotly_chart(fig_amount_3)



# This function generates three bar charts showing registered user counts for different districts within a specific state.

# Plot_1: Top 10 districts within the specified state with the highest registered user counts.
# Plot_2: Bottom 10 districts within the specified state with the lowest registered user counts.
# Plot_3: Average registered user count for each district within the specified state.

def top_chart_Registered_user(table_name, state):
        
    mydb = mysql.connector.connect(host="localhost",
                                    user="root",
                                    password="Bharath@36",
                                    database="phonepe_data")

    cursor = mydb.cursor()


    # Plot_1

    query1 = f'''SELECT Districts, SUM(RegisteredUsers) AS RegisteredUsers
                 FROM {table_name}
                 WHERE states = '{state}'
                 GROUP BY Districts
                 ORDER BY RegisteredUsers desc
                 LIMIT 10;'''

    cursor.execute(query1)

    table_1 = cursor.fetchall()

    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns= ("districts","RegisteredUsers"))

    col1,col2 = st.columns(2)

    with col1:

        fig_amount_1 = px.bar(df_1, 
                            x = "districts", 
                            y ="RegisteredUsers",
                            title= "TOP 10 OF REGISTERED USER",
                            hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Plasma,
                            height= 650, 
                            width= 600)

        st.plotly_chart(fig_amount_1)



    # Plot_2

    query2 = f'''SELECT Districts, SUM(RegisteredUsers) AS RegisteredUsers
                 FROM {table_name}
                 WHERE states = '{state}'
                 GROUP BY Districts
                 ORDER BY RegisteredUsers 
                 LIMIT 10;'''

    cursor.execute(query2)

    table_2 = cursor.fetchall()

    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns= ("districts","RegisteredUsers"))

    with col2:

        fig_amount_2 = px.bar(df_2, 
                            x = "districts", 
                            y ="RegisteredUsers",
                            title= "LEAST 10 OF REGISTERED USER",
                            hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Bluered,
                            height= 650, 
                            width= 600)

        st.plotly_chart(fig_amount_2)



    # Plot_3

    query3=  f'''SELECT Districts, AVG(RegisteredUsers) AS RegisteredUsers
                 FROM {table_name}
                 WHERE states = '{state}'
                 GROUP BY Districts
                 ORDER BY RegisteredUsers desc;'''

    cursor.execute(query3)

    table_3 = cursor.fetchall()

    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns= ("districts","RegisteredUsers"))

    fig_amount_3 = px.bar(df_3, 
                        y = "districts", 
                        x ="RegisteredUsers",
                        title= "AVERAGE OF REGISTERED USER",
                        hover_name= "districts",
                        orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,
                        height= 800, 
                        width= 1000)

    st.plotly_chart(fig_amount_3)


# This function generates three bar charts showing the number of app opens for different districts within a specific state.

# Plot_1: Top 10 districts within the specified state with the highest number of app opens.
# Plot_2: Bottom 10 districts within the specified state with the lowest number of app opens.
# Plot_3: Average number of app opens for each district within the specified state.

def top_chart_AppOpens(table_name, state):
        
    mydb = mysql.connector.connect(host="localhost",
                                    user="root",
                                    password="Bharath@36",
                                    database="phonepe_data")

    cursor = mydb.cursor()


    # Plot_1

    query1 = f'''SELECT Districts, SUM(AppOpens) AS AppOpens
                 FROM {table_name}
                 WHERE states = '{state}'
                 GROUP BY Districts
                 ORDER BY AppOpens desc
                 LIMIT 10;'''

    cursor.execute(query1)

    table_1 = cursor.fetchall()

    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns= ("districts","AppOpens"))

    col1,col2 = st.columns(2)
    
    with col1:

        fig_amount_1 = px.bar(df_1, 
                            x = "districts", 
                            y ="AppOpens",
                            title= "TOP 10 OF AppOpens",
                            hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Plasma,
                            height= 650, 
                            width= 600)

        st.plotly_chart(fig_amount_1)



    # Plot_2

    query2 = f'''SELECT Districts, SUM(AppOpens) AS AppOpens
                 FROM {table_name}
                 WHERE states = '{state}'
                 GROUP BY Districts
                 ORDER BY AppOpens 
                 LIMIT 10;'''

    cursor.execute(query2)

    table_2 = cursor.fetchall()

    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns= ("districts","AppOpens"))

    with col2:

        fig_amount_2 = px.bar(df_2, 
                            x = "districts", 
                            y ="AppOpens",
                            title= "LEAST 10 AppOpens",
                            hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Bluered,
                            height= 650, 
                            width= 600)

        st.plotly_chart(fig_amount_2)



    # Plot_3

    query3=  f'''SELECT Districts, AVG(AppOpens) AS AppOpens
                 FROM {table_name}
                 WHERE states = '{state}'
                 GROUP BY Districts
                 ORDER BY AppOpens desc;'''

    cursor.execute(query3)

    table_3 = cursor.fetchall()

    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns= ("districts","AppOpens"))

    fig_amount_3 = px.bar(df_3, 
                        y = "districts", 
                        x ="AppOpens",
                        title= "AVERAGE OF AppOpens",
                        hover_name= "districts",
                        orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,
                        height= 800, 
                        width= 1000)

    st.plotly_chart(fig_amount_3)



# This function generates three bar charts showing the number of registered users for different states.

# Plot_1: Top 10 states with the highest number of registered users.
# Plot_2: Bottom 10 states with the lowest number of registered users.
# Plot_3: Average number of registered users for each state.

def top_chart_Registered_users(table_name):
        
    mydb = mysql.connector.connect(host="localhost",
                                    user="root",
                                    password="Bharath@36",
                                    database="phonepe_data")

    cursor = mydb.cursor()


    # Plot_1

    query1 = f'''SELECT States, SUM(RegisteredUsers) AS RegisteredUsers
                 FROM {table_name}
                 GROUP BY States
                 ORDER BY RegisteredUsers DESC
                 LIMIT 10;'''

    cursor.execute(query1)

    table_1 = cursor.fetchall()

    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns= ("States","RegisteredUsers"))

    col1,col2 = st.columns(2)

    with col1:

        fig_amount_1 = px.bar(df_1, 
                            x = "States", 
                            y ="RegisteredUsers",
                            title= "TOP 10 OF REGISTERED USERS",
                            hover_name= "States",
                            color_discrete_sequence=px.colors.sequential.Plasma,
                            height= 650, 
                            width= 600)

        st.plotly_chart(fig_amount_1)



    # Plot_2

    query2 = f'''SELECT States, SUM(RegisteredUsers) AS RegisteredUsers
                 FROM {table_name}
                 GROUP BY States
                 ORDER BY RegisteredUsers 
                 LIMIT 10;'''

    cursor.execute(query2)

    table_2 = cursor.fetchall()

    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns= ("States","RegisteredUsers"))

    with col2:

        fig_amount_2 = px.bar(df_2, 
                            x = "States", 
                            y ="RegisteredUsers",
                            title= "LEAST 10 OF REGISTERED USERS",
                            hover_name= "States",
                            color_discrete_sequence=px.colors.sequential.Bluered,
                            height= 650, 
                            width= 600)

        st.plotly_chart(fig_amount_2)



    # Plot_3

    query3=  f'''SELECT States, AVG(RegisteredUsers) AS RegisteredUsers
                 FROM {table_name}
                 GROUP BY States
                 ORDER BY RegisteredUsers;'''

    cursor.execute(query3)

    table_3 = cursor.fetchall()

    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns= ("States","RegisteredUsers"))

    fig_amount_3 = px.bar(df_3, 
                        y = "States", 
                        x ="RegisteredUsers",
                        title= "AVERAGE OF REGISTERED USERS",
                        hover_name= "States",
                        orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,
                        height= 800, 
                        width= 1000)

    st.plotly_chart(fig_amount_3)



##############################################


#Streamlit Part

# Set page configuration and main title

st.set_page_config(layout= 'wide')
st.title ("PHONEPE DATA VISUALIZATION AND EXPLORATION")
st.subheader("INDIA'S LEADING TRANSACTION APP")
st.write("***PhonePe is an Indian digital payments and financial technology company***")

# Sidebar menu
with st.sidebar:
    select = option_menu("Main Menu",["HOME","DATA EXPLORATION","TOP CHARTS"])

# Home section
if select =="HOME":
    
    col1,col2 = st.columns(2)

    # First column
    with col1:
        # Display images and buttons

        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")

        st.image(Image.open(r"D:\Guvi\Python_pratice\Practice_python\Phone_pe\pulse\Phonepe_Image.png"),width= 300)
        st.link_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")

        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")

        st.image(Image.open(r"D:\Guvi\Python_pratice\Practice_python\Phone_pe\pulse\Phonepe _ Image 1.png"),width=300)

        # Options for recharge
        st.subheader("Recharge")
        selected_option = st.radio("Select an option:", ["Mobile Recharge", "FASTag Recharge", "DTH", "Cable TV"])
            
        if selected_option == "Mobile Recharge":
            st.write("You selected 'To Mobile Recharge' option.")
        elif selected_option == "FASTag Recharge":
            st.write("You selected 'FASTag Recharge' option.")
        elif selected_option == "DTH":
            st.write("You selected 'DTH' option.")
        elif selected_option == "Check Bank Balance":
            st.write("You selected 'Cable' option.")

        

    # Second column
    with col2:

        # Display video and transfer options
        st.video(r"D:\Guvi\Python_pratice\Practice_python\Phone_pe\pulse\PhonePe_ video_1.mp4")

        st.subheader("****TRANSFER MONEY****")

        selected_option = st.radio("Select an option:", ["To Mobile Number", "To Bank / UPI ID", "To Self Account", "Check Bank Balance"])

        if selected_option == "To Mobile Number":
             st.write("You selected 'To Mobile Number' option.")
        elif selected_option == "To Bank / UPI ID":
            st.write("You selected 'To Bank / UPI ID' option.")
        elif selected_option == "To Self Account":
            st.write("You selected 'To Self Account' option.")
        elif selected_option == "Check Bank Balance":
            st.write("You selected 'Check Bank Balance' option.")

    # Additional options in two columns
    col3,col4= st.columns(2)

    # Third column
    with col3:

        # Utilities options
        st.subheader("Utilities")

        selected_option = st.radio("Select an option:", ["Rent Payment", "Piped Gas", "Water","Electricity","Postpaid","Broadband/Landline","Education Fees", "Book A Cylinder"])
            
        if selected_option == "Rent Payment":
            st.write("You selected 'Rent Payment' option.")
        elif selected_option == "Piped Gas":
            st.write("You selected 'Piped Gas' option.")
        elif selected_option == "Water":
            st.write("You selected 'Water' option.")       
        elif selected_option == "Electricity":
            st.write("You selected 'Electricity' option.")
        elif selected_option == "Postpaid":
            st.write("You selected 'Postpaid' option.")
        elif selected_option == "Broadband/Landline":
            st.write("You selected 'Broadband/Landline' option.")
        elif selected_option == "Education Fees":
            st.write("You selected 'Education Fees' option.")
        elif selected_option == "Book A Cylinder":
            st.write("You selected 'Book A Cylinder' option.")
    
    # Fourth column
    with col4:

        # Partner with us section

        st.subheader("Partner with us")

        st.image(Image.open(r"D:\Guvi\Python_pratice\Practice_python\Phone_pe\pulse\Phonepe_Image - 2.png"),width=600)


# Data exploration section

elif select == "DATA EXPLORATION":

    # Tabs for different analysis methods
    tab1,tab2,tab3 = st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])

    with tab1:
        
        # Aggregated analysis tab
        method = st.radio("Select the Method",["Aggregated Insurance Analysis","Aggregated Transaction Analysis","Aggregated User Analysis"])

        
        if method == "Aggregated Insurance Analysis":

            # Select year and quarter for aggregated insurance analysis
            col1,col2 = st.columns(2)
            with col1: 
                
                years = st.slider("Select the year_Aggre_Insurance",Aggre_Insurance["Years"].min(),Aggre_Insurance["Years"].max(),Aggre_Insurance["Years"].min())
            Aggre_Insur_tac_Y = Transaction_amount_count_year(Aggre_Insurance, years)

            col1,col2 = st.columns(2)

            with col1:

                quarter = st.slider("Select the Quarter_Aggre_Insurance",Aggre_Insur_tac_Y["Quarter"].min(),Aggre_Insur_tac_Y["Quarter"].max(),Aggre_Insur_tac_Y["Quarter"].min())
            
            Transaction_amount_count_year_Quarter(Aggre_Insur_tac_Y,quarter)

        
        
        elif method == "Aggregated Transaction Analysis":
            
            # Select year, state, and quarter for aggregated transaction analysis

            col1,col2 = st.columns(2)

            with col1: 
                
                years = st.slider("Select the year_Aggre_Transactions",Aggre_Transactions["Years"].min(),Aggre_Transactions["Years"].max(),Aggre_Transactions["Years"].min())
            Aggre_trans_tac_Y = Transaction_amount_count_year(Aggre_Transactions, years)

            col1,col2 = st.columns(2)

            with col1:

                states = st.selectbox("Select the state_Aggre_Transactions", Aggre_trans_tac_Y["States"].unique())

            Aggre_Tran_Transation_type(Aggre_trans_tac_Y,states)

            col1,col2 = st.columns(2)
            
            with col1:

                quarter = st.slider("Select the Quarter_Aggre_Transactions",Aggre_trans_tac_Y["Quarter"].min(),Aggre_trans_tac_Y["Quarter"].max(),Aggre_trans_tac_Y["Quarter"].min())
            
            Aggre_trans_tac_Y_Q = Transaction_amount_count_year_Quarter(Aggre_trans_tac_Y,quarter)

            col1,col2 = st.columns(2)

            with col1:

                states = st.selectbox("Select the state_type_Aggre_Transactions", Aggre_trans_tac_Y_Q["States"].unique())

            Aggre_Tran_Transation_type(Aggre_trans_tac_Y_Q,states)

        
        elif method =="Aggregated User Analysis":

            # Select year, quarter, and state for aggregated user analysis
            col1,col2 = st.columns(2)

            with col1: 
                
                years = st.slider("Select the year_Aggre_user",Aggre_user["Years"].min(),Aggre_user["Years"].max(),Aggre_user["Years"].min())
            Aggre_user_Year = Aggre_user_plot1_year (Aggre_user, years)

            col1,col2 = st.columns(2)
            
            with col1:

                if years!= 2022:
                    quarter = st.slider("Select the Quarter_Aggre_user",Aggre_user_Year["Quarter"].min(),Aggre_user_Year["Quarter"].max(),Aggre_user_Year["Quarter"].min())
                else:
                    quarter =int( st.radio("Quarter Aggregate_user","1"))


            Aggre_user_year_Quarter = Aggre_user_plot2_Quarter(Aggre_user_Year,quarter)

            col1,col2 = st.columns(2)
            
            with col1:

                states = st.selectbox("Select the state_Aggre_user", Aggre_user_year_Quarter["States"].unique())

            Aggre_user_plot3_state (Aggre_user_year_Quarter,states)

        

    with tab2:
        
        # Map analysis tab
        method_2 = st.radio("Select the Method",["Map Insurance","Map Transaction","Map User"])

        if method_2 == "Map Insurance":
            
            # Select year, state, and quarter for map insurance analysis
            col1,col2 = st.columns(2)

            with col1: 
                
                years = st.slider("Select the year_map_insurance",Map_insurance["Years"].min(),Map_insurance["Years"].max(),Map_insurance["Years"].min())
            Map_insurance_tac_Y = Transaction_amount_count_year(Map_insurance, years)


            col1,col2 = st.columns(2)

            with col1:

                states = st.selectbox("Select the state_map_insurance", Map_insurance_tac_Y["States"].unique())

            Map_Insurance_district(Map_insurance_tac_Y, states) 

            col1,col2 = st.columns(2)
            
            with col1:

                quarter = st.slider("Select the Quarter_Map_Insurance",Map_insurance_tac_Y["Quarter"].min(),Map_insurance_tac_Y["Quarter"].max(),Map_insurance_tac_Y["Quarter"].min())
            
            Map_insurance_tac_Y_Q = Transaction_amount_count_year_Quarter(Map_insurance_tac_Y,quarter)

            col1,col2 = st.columns(2)

            with col1:

                states = st.selectbox("Select the state", Map_insurance_tac_Y_Q["States"].unique())

            Map_Insurance_district(Map_insurance_tac_Y_Q,states)


            
        elif method_2 == "Map Transaction":
            
            # Select year, state, and quarter for map transaction analysis
            col1,col2 = st.columns(2)

            with col1: 
                
                years = st.slider("Select the   ",Map_transaction["Years"].min(),Map_transaction["Years"].max(),Map_transaction["Years"].min())
            Map_Transactions_tac_Y = Transaction_amount_count_year(Map_transaction, years)


            col1,col2 = st.columns(2)

            with col1:

                states = st.selectbox("Select the state_Map_Transaction", Map_Transactions_tac_Y["States"].unique())

            Map_Insurance_district(Map_Transactions_tac_Y, states) 

            col1,col2 = st.columns(2)
            
            with col1:

                quarter = st.slider("Select the Quarter_state_Map_Transaction",Map_Transactions_tac_Y["Quarter"].min(),Map_Transactions_tac_Y["Quarter"].max(),Map_Transactions_tac_Y["Quarter"].min())
            
            Map_Transactions_tac_Y_Q = Transaction_amount_count_year_Quarter(Map_Transactions_tac_Y,quarter)

            col1,col2 = st.columns(2)

            with col1:

                states = st.selectbox("Select the state", Map_Transactions_tac_Y_Q["States"].unique())

            Map_Insurance_district(Map_Transactions_tac_Y_Q,states)



        elif method_2 =="Map User":

            # Select year, quarter, and state for map user analysis
            col1,col2 = st.columns(2)

            with col1: 
                
                years = st.slider("Select the year_Map_user",Map_user["Years"].min(),Map_user["Years"].max(),Map_user["Years"].min())
            Map_user_Year = Map_user_plot1_year (Map_user, years)

            col1,col2 = st.columns(2)

            with col1:

                quarter = st.slider("Select the Quarter_Map_user",Map_user_Year["Quarter"].min(),Map_user_Year["Quarter"].max(),Map_user_Year["Quarter"].min())
            
            Map_user_year_Quarter = Map_user_plot2_quarter(Map_user_Year,quarter)

            col1,col2 = st.columns(2)
            
            with col1:

                states = st.selectbox("Select the state", Map_user_year_Quarter["States"].unique())

            Map_user_plot3_state (Map_user_year_Quarter,states)

            
    
    with tab3:
        # Top analysis tab

        method_3 = st.radio("Select the Method",["Top Insurance","Top Transaction","Top User"])

        if method_3 == "Top Insurance":

            # Select year, state, and quarter for top insurance analysis

            col1,col2 = st.columns(2)
           
            with col1: 
                
                years = st.slider("Select the year_top_insurance",Top_insurance["Years"].min(),Top_insurance["Years"].max(),Top_insurance["Years"].min())
            Top_Insurance_tac_Y = Transaction_amount_count_year(Top_insurance, years)

            col1,col2 = st.columns(2)

            with col1:

                states = st.selectbox("Select the state_top_insurance", Top_Insurance_tac_Y["States"].unique())

            Top_insurance_plot_1(Top_Insurance_tac_Y, states) 

            col1,col2 = st.columns(2)

            with col1:

                quarter = st.slider("Select the Quarter_top_insurance",Top_Insurance_tac_Y["Quarter"].min(),Top_Insurance_tac_Y["Quarter"].max(),Top_Insurance_tac_Y["Quarter"].min())
            
            Top_Insurance_tac_Y_Q = Transaction_amount_count_year_Quarter(Top_Insurance_tac_Y,quarter)



        elif method_3 == "Top Transaction":
            
            # Select year, state, and quarter for top transaction analysis
            col1,col2 = st.columns(2)
           
            with col1: 
                
                years = st.slider("Select the year_top_transaction",Top_transaction["Years"].min(),Top_transaction["Years"].max(),Top_transaction["Years"].min())
            Top_Transaction_tac_Y = Transaction_amount_count_year(Top_transaction, years)

            col1,col2 = st.columns(2)

            with col1:

                states = st.selectbox("Select the state_top_transaction", Top_Transaction_tac_Y["States"].unique())

            Top_insurance_plot_1(Top_Transaction_tac_Y, states) 

            col1,col2 = st.columns(2)

            with col1:

                quarter = st.slider("Select the Quarter_top_transaction",Top_Transaction_tac_Y["Quarter"].min(),Top_Transaction_tac_Y["Quarter"].max(),Top_Transaction_tac_Y["Quarter"].min())
            
            Top_Transaction_tac_Y_Q = Transaction_amount_count_year_Quarter(Top_Transaction_tac_Y,quarter)

        elif method_3 =="Top User":
            
            # Select year and state for top user analysis
            col1,col2 = st.columns(2)
           
            with col1: 
                
                years = st.slider("Select the year_top_user",Top_user["Years"].min(),Top_user["Years"].max(),Top_user["Years"].min())
            Top_user_year = Top_user_plot_1(Top_user, years)


            col1,col2 = st.columns(2)
            
            with col1:

                states = st.selectbox("Select the state_top_user", Top_user_year["States"].unique())

            top_user_plot_2 (Top_user_year,states)



# Top charts section
elif select == "TOP CHARTS":
    
    # Selecting the question from the dropdown
    question = st.selectbox("Select the question", ["1. Transaction Amount and Count of Aggregated Insurance",
                                                   "2. Transaction Amount and Count of Map Insurance",
                                                   "3. Transaction Amount and Count of Top Insurance",
                                                   "4. Transaction Amount and Count of Aggregated Transactions",
                                                   "5. Transaction Amount and Count of Map Transactions",
                                                   "6. Transaction Amount and Count of Top Transactions",
                                                   "7. Transaction Count of Aggregated User",
                                                   "8. Registered users of Map User",
                                                   "9. App Opens of Map User",
                                                   "10. Registered users of Top User"])
    
    if question == "1. Transaction Amount and Count of Aggregated Insurance":

        st.subheader("TRANSACTION AMOUNT")

        top_chart_transaction_amount("aggre_insurance")

        st.subheader("TRANSACTION COUNT")

        top_chart_transaction_count("aggre_insurance")


    elif question == "2. Transaction Amount and Count of Map Insurance":

        st.subheader("TRANSACTION AMOUNT")

        top_chart_transaction_amount("map_insurance")

        st.subheader("TRANSACTION COUNT")

        top_chart_transaction_count("map_insurance")


    elif question == "3. Transaction Amount and Count of Top Insurance":

        st.subheader("TRANSACTION AMOUNT")

        top_chart_transaction_amount("top_insurance")

        st.subheader("TRANSACTION COUNT")

        top_chart_transaction_count("top_insurance")

    
    elif question == "4. Transaction Amount and Count of Aggregated Transactions":

        st.subheader("TRANSACTION AMOUNT")

        top_chart_transaction_amount("aggre_transactions")

        st.subheader("TRANSACTION COUNT")

        top_chart_transaction_count("aggre_transactions")


    elif question == "5. Transaction Amount and Count of Map Transactions":

        st.subheader("TRANSACTION AMOUNT")

        top_chart_transaction_amount("map_transaction")

        st.subheader("TRANSACTION COUNT")

        top_chart_transaction_count("map_transaction")


    elif question == "6. Transaction Amount and Count of Top Transactions":

        st.subheader("TRANSACTION AMOUNT")

        top_chart_transaction_amount("top_transaction")

        st.subheader("TRANSACTION COUNT")

        top_chart_transaction_count("top_transaction")


    elif question == "7. Transaction Count of Aggregated User":

        st.subheader("TRANSACTION COUNT")

        top_chart_transaction_count("aggre_user")


 
    elif question == "8. Registered users of Map User":

        states =st.selectbox("Select the state", Map_user["States"].unique()) 

        st.subheader("REGISTERED USERS")

        top_chart_Registered_user("map_user",states)  


    elif question == "9. App Opens of Map User":

        states =st.selectbox("Select the state", Map_user["States"].unique()) 

        st.subheader("APPOPENS")

        top_chart_AppOpens("map_user",states)
    

    elif question == "10. Registered users of Top User":

        st.subheader("REGISTERED USERS")

        top_chart_Registered_users("top_user")   

