import pandas as pd
import csv
district = 'Charlottenburg, Friedrichshain, Hellersdorf, Hohenschönhausen, Kreuzberg, Köpenick, Lichtenberg, Marzahn, Mitte, Neukölln, Pankow, Prenzlauer Berg, Reinickendorf, Schöneberg, Spandau, Steglitz, Tempelhof, Tiergarten, Treptow, Wedding, Weißensee, Wilmersdorf, Zehlendorf'
district = district.split(', ')

df = pd.read_csv('listings.csv')
df = df[df.host_neighbourhood.isin(district)]

df.price = df.price.astype(str).str.replace('$','')
df.price = df.price.astype(str).str.replace(',', '')
df.price = pd.to_numeric(df.price)

df.to_csv('altered.csv')