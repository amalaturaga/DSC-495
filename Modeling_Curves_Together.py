import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#The function we use to 
def sigmoid(x, L, x0, k, b):
    y = L / (1 + np.exp(-k*(x-x0))) + b
    return (y)

#This file is in our google drive folder. It gives the shape parameters of each function
curves = pd.read_csv("/Users/amalaturaga/AquaAllstarz/Season_Curve_Parameters.csv")
p_curves = []
h_curves = []

#Inputing the shape parameters, cleaning, and saving the 10 harvesting/planting curves into the lists p_curves and h_curves
for index, line in curves.iterrows():
  params = line["Planting Curve Parameters"]
  params=params[1:-1]
  params=[float(i) for i in params.split()]
  p_curves.append(params)

  params2 = line["Harvesting Curve Parameters"]
  params2=params2[1:-1]
  list1=[float(i) for i in params2.split()]
  h_curves.append(list1)

#Where to plot each curve
planting_dates = np.linspace(20,100,100)
harvesting_dates = np.linspace(160,250,100)

cmap = plt.get_cmap('Grays')

for i in range(0,10,1):
  color = cmap(i / 10)

  #Send x values, and shape parameters back to sigmoid to plot
  planting_results= sigmoid(planting_dates, *p_curves[i])


  plt.plot(planting_dates, planting_results, color=color)
  plt.plot(harvesting_dates, sigmoid(harvesting_dates, *h_curves[i]), color=color)

plt.show()


#This file is also available in the google drive. It includes the each already graphed season curve, as an array of paired x and y values
season_curves = pd.read_csv("/Users/amalaturaga/AquaAllstarz/season_curves.csv")

#2017 Appears to be an outlier year, for now I excluded it while visualizing the data
#season_curves = season_curves.drop(season_curves[season_curves['Year'] == 2017].index)

#inputs the curve, cleans it, then plots each one
#The columns of the csv are Planting_Date_Array, Harvesting_Date_Array and Year. 10 Rows, one for each curve
for index, line in season_curves.iterrows():
  x=line["Planting_Date_Array"]
  x=x[1:-1].split()
  x=[float(i) for i in x]

  y=line["Season_Length_Array"]
  y=y[1:-1].split()
  y=[float(i) for i in y]

  plt.xlabel("Planting Date")
  plt.ylabel("Approximate time to Harvest")
  plt.plot(x,y,label=line["Year"])

plt.legend()
plt.show()

#Dictionary of Growing Degree Days May to November. Should think about dividing each value by 7 to get mean daily GDD

temp = {"2012":	134.1,
"2013":	128,
"2014":	133.9,
"2015":	145.4,
"2016":	151.7,
"2017":	135.1,
"2018":	149,
"2019":	147.7,
"2020":	131.8,
"2021":	135.1,
"2022":	136.3,
"2023":	128.3}

cmap = plt.get_cmap('Reds')
temp_range = 151.7 - 128

#Goes through again and cleans data for each array, then plots it, colored based on the temperature
for index, line in season_curves.iterrows():
  x=line["Planting_Date_Array"]
  x=x[1:-1].split()
  x=[float(i) for i in x]

  y=line["Season_Length_Array"]
  #print(y)
  y=y[1:-1].split()
  y=[float(i) for i in y]
  year_temp=temp[str(line["Year"])]
  #remaps values from 0-1 onto our color scheme
  color=cmap((year_temp-128)/temp_range)

  plt.plot(x,y,label=line["Year"], color = color)
  plt.xlabel("Planting Date (Days since April 1st)")
  plt.ylabel("Approximate time to Harvest")
  plt.title("Season Progress colored based on Temp")

plt.legend()
plt.show()

#Dictionary of total season (May to November) percipiation in inches

prcp = {2012:	25.96,
2013:	30.27,
2014:	35.03,
2015:	36.23,
2016:	35.63,
2017:	27.03,
2018:	38.29,
2019:	22.43,
2020:	33.42,
2021:	28.66,
2022:	27.16,
2023:	21.36}


cmap = plt.get_cmap('Blues')
prcp_range = 38.29 - 21.36

for index, line in season_curves.iterrows():
  x=line["Planting_Date_Array"]
  x=x[1:-1].split()
  x=[float(i) for i in x]

  y=line["Season_Length_Array"]
  #print(y)
  y=y[1:-1].split()
  y=[float(i) for i in y]
  year_prcp=prcp[line["Year"]]
  color=cmap((year_prcp-21.36)/prcp_range)

  plt.xlabel("Planting Date")
  plt.ylabel("Approximate time to Harvest")
  plt.plot(x,y,label=line["Year"], color = color)

plt.legend()
plt.show()