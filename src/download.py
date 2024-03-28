import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib
import yaml
import random
import os


#---------------------------------------------------------------------------------------------#

# This function accepts the year as input and retrieves all the links of the files available in that year
def fetch_links(base_url, year):
    url = f"{base_url}{year}/"

    response = requests.get(url)

    base_url_year = base_url + year + '/'
    list_of_links = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a')
        
        for link in links:
            href = link.get('href')
            if href:
                absolute_url = urljoin(base_url_year, href)
                if ".csv" in absolute_url:
                    list_of_links.append(absolute_url)

        return list_of_links
    
# Function to randomly sample links from the list of all available links
random.seed(8)
def random_links(list_of_links, no_of_links):
    links_to_fetch = random.sample(list_of_links, no_of_links)
    return links_to_fetch

# Function to download all the required files using wget, and place it in the required folder
def download_files(links_to_fetch, folder):
    os.makedirs(folder, exist_ok=True)
        
    for url in links_to_fetch:
        filename = folder + "/" + url.split("/")[-1]
        urllib.request.urlretrieve(url, filename)

def create_folder(folder_path):
    if os.path.exists(folder_path):
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file)) 
            for dir in dirs:
                os.rmdir(os.path.join(root, dir)) 
        os.rmdir(folder_path) 
    os.makedirs(folder_path, exist_ok=True) 

#---------------------------------------------------------------------------------------------#

with open(r"C:\Users\91979\Desktop\Jup_NoteBks\BDL\Asgt_3\example\DVC_repo\params.yaml", 'r') as f:
    params = yaml.safe_load(f)

# Defining the base_url, year which we want to work with, number of files to be fetched and the destination folder for the csv files
base_url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/"
year = str(params['data']['year'])
no_of_links = params['data']['n_locs']
folder = rf"C:\Users\91979\Desktop\Jup_NoteBks\BDL\Asgt_3\example\DVC_repo\data"
create_folder(folder)

list_of_links = fetch_links(base_url, year)
links_to_fetch = random_links(list_of_links, no_of_links)
download_files(links_to_fetch, folder)