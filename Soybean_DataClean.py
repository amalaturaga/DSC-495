import pandas as pd
import os

#df = pd.read_csv(file)
    #this is for getting every column in the data. No usecols
    #col_selection =  ['REFERENCE PERIOD', 'COMMODITY', 'WEEK ENDING', 'PROGRESS in PCT PLANTED', 'PROGRESS in PCT EMERGED','PROGRESS in PCT BLOOMING','PROGRESS in PCT SETTING PODS', 'PROGRESS in PCT DROPPING LEAVES','PROGRESS in PCT HARVESTED']
    #this is for getting every column that records some pct of soybeans in a certain stage of development

# Define input and output folders for cleaning
input_folder = '/Users/amalaturaga/AquaAllstarz/Crop Reports (csv)'  # Folder containing raw CSV files
cleaned_output_folder = '/Users/amalaturaga/AquaAllstarz/Cleaned Datasets'  # Folder to save cleaned files
os.makedirs(cleaned_output_folder, exist_ok=True)  # Ensure the output folder exists

# Function to clean a single dataset
def clean_dataset(file_path):
    try:
        # Step 1: Load the dataset
        print(f"Cleaning {file_path}")
        df = pd.read_csv(file_path)

        # Step 2: Perform cleaning logic
        # This creates a list of the columns that are our key data value, the columns that say progress in percent blank
        progress_cols = [col for col in df.columns if "PROGRESS" in col]
        for col in progress_cols:
            fill_num = 0
            for row in range(len(df[col])):
                if pd.isnull(df[col][row]) or df[col][row] == " ":
                    df.loc[row, col] = fill_num
                else:
                    fill_num = df[col][row]

        # Example: Add a calculated column for season days
        start_day = int(df["WEEK ENDING"][0][-2:])
        days = range(start_day, start_day + 7 * len(df), 7)
        df.insert(2, "SEASON_DAYS", list(days)[:len(df)])

        # Step 3: Save cleaned dataset
        output_file = os.path.join(cleaned_output_folder, os.path.basename(file_path))
        df.to_csv(output_file, index=False)
        print(f"Cleaned data saved to {output_file}")

    except Exception as e:
        print(f"Failed to clean {file_path}: {e}")


#Save the cleaned DataFrame to a new CSV file
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):  # Process only CSV files
        clean_dataset(os.path.join(input_folder, filename))

print("Cleaning complete. Cleaned files saved in the output folder.")