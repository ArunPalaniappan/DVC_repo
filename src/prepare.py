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

GT_folder = rf"C:\Users\91979\Desktop\Jup_NoteBks\BDL\Asgt_3\example\DVC_repo\outputs\GT"
create_folder(GT_folder)

directory = rf'C:\Users\91979\Desktop\Jup_NoteBks\BDL\Asgt_3\example\DVC_repo\data'

# Function to extract the list_of_fields which contain both daily and monthly values
def extract_fields(file_path, filename):
    data = pd.read_csv(file_path)
    data['DATE'] = pd.to_datetime(data['DATE'])

    quantities = list(data)

    daily_q = []
    monthly_q = []

    for quantity in quantities:
        if "Daily" in quantity:
            daily_q.append(quantity[5:])

        elif "Monthly" in quantity:
            monthly_q.append(quantity[7:])

    common_q = set(daily_q).intersection(set(monthly_q))

    common_q_list = list(common_q)

    quantity_string_data = str(filename) + ":"

    GT_df = pd.DataFrame()

    for index, quantity in enumerate(common_q_list):
        if index!= len(common_q_list) - 1:
            quantity_string_data = quantity_string_data + quantity + ","
        else:
            quantity_string_data = quantity_string_data + quantity + "\n"
        #----------------------------------------------------------------         
        monthly_avg_obs_from_data = data.groupby(data['DATE'].dt.to_period('M'))[f'Monthly{quantity}'].sum()

        GT_df[f'{quantity}'] = list(monthly_avg_obs_from_data)

    return quantity_string_data, GT_df

final_string_data = ''

# Extracting the monthly averages and storing them
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)

    quantity_string_data, GT_df = extract_fields(file_path, filename)
    final_string_data = final_string_data + quantity_string_data
    GT_df.to_csv(f'{GT_folder}\{filename}', index=False)

# Creating and populating the list_of_fields.txt text file
with open(rf'C:\Users\91979\Desktop\Jup_NoteBks\BDL\Asgt_3\example\DVC_repo\outputs\list_of_fields.txt', 'w') as f:
    f.write(final_string_data)