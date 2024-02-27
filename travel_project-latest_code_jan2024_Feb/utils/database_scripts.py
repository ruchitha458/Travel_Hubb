import sqlite3
from datetime import datetime
import os
import csv
import json

global database_nm 
database_nm = os.path.join("database", "travel_data_demo.db") #check this file in sql lite studio to query data

# Function to check if a column exists in a table
def column_exists(table_name, column_name):
    query = f"PRAGMA table_info({table_name})"  
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    cur.execute(query)
    columns = cur.fetchall()
    for column in columns:
        if column[1] == column_name:
            return True
    return False

# def update_locationwithlikes(name):
#     connection = sqlite3.connect(database_nm)
#     cur = connection.cursor()
#     new_column_name = 'num_likes'
#     if not column_exists('locations', new_column_name):
#         print("column cgheck")
#         alter_query = "ALTER TABLE locations ADD COLUMN num_likes INTEGER"
#         cur.execute(alter_query)
#         connection.commit()
#     existing_likes = select_all_from_table('locations', f"name = '{name}'")[0][-1]
#     if not existing_likes:
#         existing_likes = 0
#     new_likes = existing_likes + 1 
#     cur.execute(f"UPDATE locations SET num_likes = {new_likes} where name = '{name}';")
#     connection.commit()
    
def create_table_update_contact(name, email, phone, message):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    createtable_q = "CREATE TABLE IF NOT EXISTS contact_us(contact_id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,email TEXT,phone TEXT, message TEXT, contact_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);"
    cur.execute(createtable_q)
    connection.commit()
    cur.execute("INSERT INTO contact_us (name, email, phone, message) VALUES (?, ?, ?, ?)",
                    (name, email, phone, message))
    connection.commit()
    
def create_table_update_blogpost(title, content, image_url):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    createtable_q = "CREATE TABLE IF NOT EXISTS blog_page(blog_id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL, context TEXT, image_url TEXT, contact_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);"
    cur.execute(createtable_q)
    connection.commit()
    cur.execute("INSERT INTO blog_page (title, context, image_url ) VALUES (?, ?, ?)",
                    (title, content, image_url))
    connection.commit()
    
def update_user_password(username, newpassword):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    sql_query = f" UPDATE users SET password = '{newpassword}' WHERE username = '{username}';"
    cur.execute(sql_query)
    connection.commit()
        
def get_all_states_and_cities():
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    cols = ["state", "city"]
    location_all = {}
    for col in cols:
        query = f"select distinct {col} from locations;"
        result = cur.execute(query).fetchall()
        location_all[col] = [location[0] for location in result]
    return location_all

def get_all_states_cities_cats():
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    cols = ["state", "city", "locationcattype"]
    location_all = {}
    for col in cols:
        query = f"select distinct {col} from locations;"
        result = cur.execute(query).fetchall()
        location_all[col] = [location[0] for location in result]
    return location_all

def find_user_login(username):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    sql_query = f"SELECT distinct password FROM users where username = '{username}';"
    t = cur.execute(sql_query).fetchall()
    return str("".join(t[0]))
    
def select_all_from_table(table_name, where_clause=None):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    if where_clause is not None:
        query = f"select * from {table_name} where " + where_clause
    else:
        query = f"select * from {table_name}"
    print(query)
    all_users = cur.execute(query).fetchall()
    return [user for user in all_users]

def create_table():
   connection = sqlite3.connect(database_nm) 
   with open(os.path.join('database','schema.sql')) as f:
        connection.executescript(f.read())
    
def insert_query_user(username, email, password, fname, lname):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    cur.execute("INSERT INTO users (username, email, password, firstname, lastname) VALUES (?, ?, ?, ?, ?)",
                    (username, email, password, fname, lname))
    connection.commit()
    return "Record Inserted Successfully"

def insert_or_update_location(state, name, city, description, locationcattype, image, map_reflink):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    cur.execute("INSERT INTO locations (state, name, city, description, locationcattype, image, map_reflink) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (state,  name, city, description, locationcattype, image, map_reflink))
    connection.commit()
    return "Record Inserted Successfully" 

def update_user_new_login(username):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    sql_statement = f"INSERT INTO user_sessions(username,logout_time) VALUES('{username}','')";  
    cur.execute(sql_statement)
    connection.commit()

def log_user_session(username, session_id):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    sql_statement = f"UPDATE user_sessions SET logout_time = CURRENT_TIMESTAMP, session_id = '{session_id}' WHERE username='{username}' and session_id is NULL"   
    cur.execute(sql_statement)
    connection.commit()
    connection.close()
    
def get_city_and_cat_state():
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    location_all = {}
    query = f"select distinct state from locations;"
    result = cur.execute(query).fetchall()
    all_states = [location[0] for location in result]
    location_all['state'] = all_states
    location_all['cities'] = {}
    location_all['categories'] = {}
    for state in all_states:
        query = f"select distinct city from locations where state = '{state}';"
        result = cur.execute(query).fetchall()
        location_all['cities'][state] = [location[0] for location in result]
        query = f"select distinct locationcattype from locations where state = '{state}';"
        result = cur.execute(query).fetchall()
        location_all['categories'][state] = [category[0] for category in result]  
    return location_all    

#update_locationwithlikes("kadalivanam caves")