import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import expit
import pandas as pd
import os
import xarray as xr


def get_subset_of_data(col, df):
    data_y=df[col].to_numpy()
    data_x=df["SEASON_DAYS"].to_numpy()
    for entry in range(0, len(data_y)):
        if not df[col][entry]==0:
            data_x=data_x[entry:]
            data_y=data_y[entry:]
            break

    for entry in range(-1,-1*len(data_y),-1):
        if not data_y[entry]==data_y[entry-1]:
            data_x=data_x[:entry]
            data_y=data_y[:entry]
            break
    return data_x, data_y

def sigmoid(x, L, x0, k, b):
    y = L / (1 + np.exp(-k*(x-x0))) + b
    return (y)

def inverse_sigmoid (y, L, x0, k, b):
    inner = (L/(y-b))-1
    return (np.log(inner)/-k)+x0

# Define the folder containing the datasets
input_folder = '/Users/amalaturaga/AquaAllstarz/Cleaned Datasets'
output_folder = '/Users/amalaturaga/AquaAllstarz/Curve Fit Outcomes'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Function that runs all plots and analysis for each dataset
def run_analysis (df, output_folder, base_filename):

  # Plots for progress in crops planted and harvested
  planting_xdata, planting_ydata = get_subset_of_data("PROGRESS in PCT PLANTED", df)
  harvesting_xdata, harvesting_ydata = get_subset_of_data("PROGRESS in PCT HARVESTED", df)
  plt.plot(planting_xdata, planting_ydata, 'o', label='data')
  plt.plot(harvesting_xdata, harvesting_ydata, 'o', color='red')
  plt.title(f'Progress vs Season Days')
  plt.xlabel('Days Since April 1st')
  plt.ylabel('Percent of Total Planted/Harvested')
  plot_path = os.path.join(output_folder, f"{base_filename}_plot1.png")
  plt.savefig(plot_path)
  plt.show()

  pcurve, pcov = curve_fit(sigmoid, planting_xdata, planting_ydata,[100, 50, 0.09,0])
  planting_xfit = np.linspace(min(planting_xdata), max(planting_xdata), 100)
  planting_yfit = sigmoid(planting_xfit, *pcurve)

  hcurve, pcov1 = curve_fit(sigmoid, harvesting_xdata, harvesting_ydata, [300, 200, 0.09,0])
  harvesting_xfit = np.linspace(min(harvesting_xdata), max(harvesting_xdata), 100)
  harvesting_yfit = sigmoid(harvesting_xfit, *hcurve)

  print(pcurve)
  print(hcurve)

  # Plots for planting and harvesting per year
  plt.plot(planting_xfit, planting_yfit)
  plt.plot(harvesting_xfit, harvesting_yfit)
  plt.plot(planting_xdata, planting_ydata, 'o', label='data')
  plt.plot(harvesting_xdata, harvesting_ydata, 'o', color='red')
  plt.title(f'Progress vs Season Days')
  plt.xlabel('Days Since April 1st')
  plt.ylabel('Percent of Total Planted/Harvested')
  plt.legend(["percent planted", "percent harvested"], loc="upper left")
  plot_path = os.path.join(output_folder, f"{base_filename}_plot2.png")
  plt.savefig(plot_path)
  plt.show()

  harvested_values = np.linspace(10,80,20)
  start_dates=inverse_sigmoid(harvested_values, *pcurve)
  season_lengths=inverse_sigmoid(harvested_values, *hcurve)-start_dates

  #print(start_dates)

  # Plots for season lengths (start date is from April 1st of each year)
  plt.plot(start_dates,season_lengths)
  plt.title(f'Length of Growing Season')
  plt.xlabel('Planting Date (Days since Apri 1st)')
  plt.ylabel('Season Length (Total Days)')
  plot_path = os.path.join(output_folder, f"{base_filename}_plot3.png")
  plt.savefig(plot_path)
  plt.show()

  print("The length of the growing season for the median planting date is:")
  print(inverse_sigmoid(50, *hcurve)   -   inverse_sigmoid(50, *pcurve))


  # Loop through all '.csv' files in the folder
for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):  # Only process CSV files
        file_path = os.path.join(input_folder, filename)  # Construct full file path

        # Read the CSV file
        df = pd.read_csv(file_path)
        print(f"Processing file: {filename}")

        # Use the filename without extension as the base for plot names
        base_filename = os.path.splitext(filename)[0]

        # Run the analysis and generate plots
        run_analysis(df, output_folder, base_filename)

print("All files processed and plots saved.")