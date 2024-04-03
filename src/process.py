import pandas as pd
import numpy as np
import os

# Function to create folders in the required path
def create_folder(folder_path):
    if os.path.exists(folder_path):
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file)) 
            for dir in dirs:
                os.rmdir(os.path.join(root, dir)) 
        os.rmdir(folder_path) 
    os.makedirs(folder_path)

compute_folder = rf"C:\Users\91979\Desktop\Jup_NoteBks\BDL\Asgt_3\example\DVC_repo\outputs_computed\computed"
create_folder(compute_folder)

list_of_fields_dict = {}

# Reading the list_of_fields.txt file and extracting its contents
with open(rf"C:\Users\91979\Desktop\Jup_NoteBks\BDL\Asgt_3\example\DVC_repo\outputs\list_of_fields.txt", 'r') as file:
    for line in file:
        line = line.strip()

        file_name = line.split(':')[0]
        quantities = line.split(':')[1].split(',')

        list_of_fields_dict[file_name] = quantities

directory = rf'C:\Users\91979\Desktop\Jup_NoteBks\BDL\Asgt_3\example\DVC_repo\data'

# Computing the averages of the fields in list_of_fields.txt file
def compute_averages(file_path, filename, list_of_fields_dict):
    data = pd.read_csv(file_path)
    data['DATE'] = pd.to_datetime(data['DATE'])

    common_q_list = list_of_fields_dict[filename]
    
    computed_df = pd.DataFrame()
    for q in common_q_list:
        monthly_avg_calc = data.groupby(data['DATE'].dt.to_period('M'))[f'Daily{q}'].mean()
        computed_df[f'{q}'] = list(monthly_avg_calc)

    return computed_df

# Storing the computed averages
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)

    computed_df = compute_averages(file_path, filename, list_of_fields_dict)
    computed_df.to_csv(f'{compute_folder}\{filename}', index=False)