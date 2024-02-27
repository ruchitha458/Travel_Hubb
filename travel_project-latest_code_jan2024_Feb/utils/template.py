from database_scripts import insert_or_update_location, create_table, get_all_states_and_cities
csv_file_path = r"D:\Documents\travel_project-Feb_modified\travel_project-latest_code_jan2024_Feb\database\travel_Hub_locations.xlsx"
import pandas as pd 
create_table()
with open(csv_file_path, 'r') as csv_file:
    print("loading places data")
    df = pd.read_excel(csv_file_path, header=None)
    for index, val in df.iterrows():
        state = val[0]
        name = val[1].strip(" ")
        city = val[2].strip(" ")
        description = val[3].strip(" ")
        locationcattype = val[4].strip(" ")
        image = val[5].strip(" ")
        map_reflink = val[6].strip(" ")
        
        insert_or_update_location(state, name, city, description, locationcattype, image, map_reflink)
print(get_all_states_and_cities())

