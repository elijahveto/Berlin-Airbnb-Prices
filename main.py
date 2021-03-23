import pandas as pd
import streamlit as st
import plotly.express as px


district = 'Charlottenburg, Friedrichshain, Hellersdorf, Hohenschönhausen, Kreuzberg, Köpenick, Lichtenberg, Marzahn, Mitte, Neukölln, Pankow, Prenzlauer Berg, Reinickendorf, Schöneberg, Spandau, Steglitz, Tempelhof, Tiergarten, Treptow, Wedding, Weißensee, Wilmersdorf, Zehlendorf'
district = district.split(', ')

df = pd.read_csv('listings.csv')
df = df[df.host_neighbourhood.isin(district)]

df.price = df.price.astype(str).str.replace("$","")
df.price = df.price.astype(str).str.replace(",","")
df.price = pd.to_numeric(df.price)
data = df.groupby('host_neighbourhood', as_index=False).agg({'price':pd.Series.mean})




st.write('Airbnb listing prices in Berlin per night and district (as of February 2021)')
fig = px.bar(data, x = 'host_neighbourhood',  y = 'price')
fig.update_layout(
        xaxis_title="District",
        yaxis_title="Ø Price in $",
    )
st.write(fig)
st.write('Who would have thought that Marzahn would be so luxurious ;) One has to look at the distribution of Prices in Marzahn, you will see that there are just too few listings.')
hood = st.sidebar.selectbox('Select a District', ('All', data.host_neighbourhood))
max_price = st.sidebar.slider('Price Cutoff', 100, 4000, 1000)

cut_df = df[df.price < max_price]
# Histogram Price
result = cut_df.price if (hood == 'All') else cut_df[cut_df.host_neighbourhood == hood].price
text = f'$ Price in {hood}' if (hood == 'All') else '$ Price across all districts'
fig = px.histogram(
        result
    )
fig.update_layout(
        title= 'Price Distribution',
        xaxis_title=text,
        yaxis_title="Count",
    )

st.write(fig)

# Boxplot Price
fig = px.box(
        result
    )
fig.update_layout(
        title= 'Price Distribution',
        xaxis_title= text,
        yaxis_title="$ Price",
    )

st.write(fig)

# Distribution by room type
result1 = cut_df if (hood == 'All') else cut_df[cut_df.host_neighbourhood == hood]
fig = px.histogram(
        result1, x='price', color='room_type', opacity=0.5
    )
fig.update_layout(
        title= 'Price Distribution per room type (doubleclick on legend to isolate one trace',
        xaxis_title=text,
        yaxis_title="$ Price",
        barmode='overlay'
    )

st.write(fig)

# How would a price distribution for your room look like?
st.sidebar.write('How would a price distribution for your room look like?')
neighbourhood = st.sidebar.selectbox('District', df.host_neighbourhood.unique())
roomtype= st.sidebar.selectbox('Room type', df.room_type.unique())
rooms = st.sidebar.slider('Bedrooms', 1, 10, 1)

# display graph
st.write('$ Price distribution based on your input:')
result = cut_df.loc[(cut_df.host_neighbourhood == neighbourhood) & (cut_df.room_type == roomtype) & (cut_df.bedrooms == rooms)].price
fig = px.histogram(
        result
    )
fig.update_layout(
        title= f'Ø Price of ${round(result.mean(),2)}',
        xaxis_title=f'$ Price',
        yaxis_title="Count",
    )

st.write(fig)



