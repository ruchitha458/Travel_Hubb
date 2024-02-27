from flask import Flask, url_for, render_template, request, redirect, flash, session
from utils.database_scripts import insert_query_user, create_table_update_contact, find_user_login, log_user_session, \
    update_user_new_login, select_all_from_table, update_user_password, get_all_states_and_cities, \
    get_city_and_cat_state, get_all_states_cities_cats, create_table_update_blogpost #update_locationwithlikes
from flask_session import Session
import os
from PIL import Image


app = Flask(__name__)

PERMANENT_SESSION_LIFETIME = 10
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True 
app.config['SESSION_REFRESH_EACH_REQUEST'] = True 
UPLOAD_FOLDER = 'static/images_blogs/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.update(SECRET_KEY=os.urandom(24))

app.config.from_object(__name__)
Session(app)

@app.route('/travelblog/about')
def about():
    username = session.get('username')
    return render_template('about.html', username1=username)

@app.route('/travelblog/home')
def site_home():
    locations = get_all_states_and_cities()['state']
    print(locations)
    return render_template('index.html', msg='', login=url_for("login"), locations=locations, selected_state="selected_state")

# Define aliases for other URL endpoints
app.add_url_rule("/home", "home_alias", site_home)
app.add_url_rule("/welcome", "welcome_alias", site_home)
app.add_url_rule("/", "initial_alias", site_home)

def get_locationdata(selected_state, selected_city, selected_category):
 #   where_clause = "state = '" + selected_state + "' and locationcategorytype ='" + locationcat + "'" and "description not like" + "'" +"%Kapu is a beach village in coastal Karnataka%" + "';"
    print("selecteddetails", selected_state, selected_city, selected_category)
    where_clause = "state = '" + selected_state + "'"
    if selected_city and selected_city != 'All':
        where_clause = "city = '" + selected_city + "'"
    if selected_category and selected_category != 'All':
        where_clause = where_clause +  "and locationcattype ='" + selected_category + "'" 
    where_clause = where_clause + ";"
    print(where_clause) 
    data = select_all_from_table('locations', where_clause)
    card_data = []
    for i, each in enumerate(data):
        location = {}
        location['state'] = each[1]
        location['name'] = each[2]
        location['city'] = each[3]
        location['description'] = each[4]
        location['locationcattype'] = each[5]
        location['image'] = each[6]
        location['map_reflink'] = each[7]
        # if each[9]:
        #     location['likes'] = each[9]
        location['class'] = each[1] + str(i)
        card_data.append(location)
    return card_data 

from flask import Flask, render_template, jsonify

@app.route('/get_cities_and_categories/<selected_state>')
def get_cities_and_categories(selected_state):
    datalocation = get_city_and_cat_state()
    cities = datalocation['cities'].get(selected_state, [])
    categories = datalocation['categories'].get(selected_state, [])
    return jsonify({'cities': cities, 'categories': categories})


@app.route('/get_filtered_data', methods=['GET', 'POST'])
def get_filtered_data():
    selected_state = request.form.get('stateselector')
    selected_city = request.form.get('cityselector')
    selected_category = request.form.get('categoryselector')
    if 'username' in session:
        username = session["username"]
    else:
        username = None
    data_location  = get_city_and_cat_state()
    print(selected_city, selected_category, selected_state)
    if selected_state in data_location['state']:
        session['state'] = selected_state
    else:
        selected_state = "Karnataka"
    card_data = get_locationdata(selected_state)
    print(request.form)
    # print(selected_city,selected_state, selected_category)
    # Render the filtered data in a template (replace with your actual template)
    return render_template('location_select.html', username1= username, 
                           state = selected_state, 
                           data_location = data_location,
                           stateselector=selected_state, 
                           cityselector=selected_city,
                           selected_category=selected_category, 
                           card_data=card_data)
   
@app.route('/travelblog/profile/location/', methods=['GET', 'POST'])
def locationdetails():
    if 'username' in session:
        username = session["username"]
    else:
        username = None
    selected_state = request.form.get('selected_state')
    data_location  = get_city_and_cat_state()
    # if selected_state in data_location['state']:
    #     session['state'] = selected_state
    # else:
    #     selecthsiudgcfoaibded_state = "Karnataka"
    selectedstate = request.form.get('stateselector')
    selected_city = request.form.get('cityselector')
    selected_category = request.form.get('categoryselector')
    print(selected_city, selected_category, selectedstate)
    if selectedstate:
        html_tag = selectedstate
    elif selected_state:
        html_tag = selected_state
    else:
        html_tag = 'Andhrapradesh'
    print(html_tag)
    if selectedstate:
        selected_state = selectedstate
    selected_location= {}
    selected_location['state'] = data_location['state']
    selected_location['cities'] = ["All"] + data_location['cities'][html_tag]
    selected_location['categories'] = ["All"] + data_location['categories'][html_tag] 
    data_location = selected_location
    print(selected_state)
    print("details", request.form)
    print(data_location)
    card_data = get_locationdata(html_tag, selected_city, selected_category) 
    return render_template('test.html', username1= username, 
                           state = html_tag, 
                           data_location = data_location,
                           stateselector=selectedstate, 
                           cityselector=selected_city,
                           selected_category=selected_category, 
                           card_data=card_data)
@app.route('/login')
def site_login():
    return redirect(url_for("login"))

@app.route('/travelblog/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        session['logged_in'] = True
        session['username'] = username
        password = request.form['password']
        password_db = ""
        try:
            password_db = find_user_login(username)
        except IndexError as e:    
            error = 'Invalid User! Please Register' 
        if password_db != "" and password_db.strip() != password.strip():
            print("after validation", password_db)
            error = 'Invalid User Credentials! Please try Again'
        elif password_db == "":
            print("check none", password_db)
            redirect(url_for("register"))
        else:
            print(password_db)
            update_user_new_login(username)
            return redirect(url_for("profile", username=username))
        
    return render_template('login.html', msg=error)


@app.route('/travelblog/register', methods=['GET', 'POST'])
def register():
    error = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        session['username'] = username
        password = request.form['password']
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form['email']
        try:
            password_db = find_user_login(username)
        except Exception:
            password_db = None
            insert_query_user(username=username, email=email, password=password, fname=fname, lname=lname)
        if not password_db:
            return redirect(url_for("profile", username=username))
        else:
            error = 'user already exists! please try to login!'
            return render_template('login.html', msg=error)
    elif request.method == 'post':
        error = 'please fill out the form!'
    return render_template('register.html', msg=error)


@app.route('/travelblog/forgotpassword', methods=['GET', 'POST'])
def reset_password():
    error = ''
    if request.method == 'POST' and 'username' in request.form and 'oldpassword' in request.form:
        username = request.form['username']
        session['username'] = username
        oldpassword = request.form['oldpassword']
        newpassword = request.form['newpassword']
        update_user_password(username=username, newpassword=newpassword)
        return redirect(url_for("login", username=username)) 
    return render_template('forgotpassword.html', msg = "")
    
    
@app.route('/travelblog/profile/<username>')
def profile(username):
    print(session)
    locations = get_all_states_and_cities()['state']
    print(locations)
    return render_template('profile.html', username1=username, locations=locations)
   
@app.route('/travelblog/contactus', methods=['GET', 'POST'])
def contactus():
    username = session.get('username')
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        create_table_update_contact(name, email, phone, message)
        return redirect(url_for("site_home", username=name)) 
    return render_template('contact.html', username1=username)

@app.route('/travelblog/logout')
def logout():
    if 'username' in session: 
        username = session['username']
        session_id = str(session.sid)
        session.pop('username', None)
        session.pop('sid', None)
        log_user_session(username, session_id)
    locations = get_all_states_and_cities()['state']
    return render_template('index.html', msg='', login=url_for("login"), locations=locations)

from PIL import Image
import mimetypes

def convert_to_jpg(input_path, output_path):
    try:
        with open(input_path, 'rb') as file:
            mime_type, _ = mimetypes.guess_type(input_path)
            if mime_type and mime_type.startswith('image'):
                with Image.open(file) as img:
                    img.convert('RGB').save(output_path, 'JPEG')
                return True 
            else:
                print("Not an image file.")
                return False  
    except Exception as e:
        print(f"Error converting file: {e}")
        return False  

@app.route('/travelblog/blog/create_blog', methods=['GET', 'POST'])
def create_blog():
    print("posted blob before", request.method, request.form)
    if request.method == 'POST':
        print("posted blob")
        title = request.form['post_title']
        content = request.form['post_content']
        #print(title, content)
        file = request.files['file_input']  
        if file:
            image_path = file.filename
            #print(os.getcwd(), app.config['UPLOAD_FOLDER'], image_path)
            file.save(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'], image_path))
            image_url = f"images_blogs/{image_path}"
        else:
            image_url= ""
        create_table_update_blogpost(title, content, image_url)
        return render_template('blog.html')
    return render_template('blog.html')

def get_blogdetails(blogPosts):
    blogdetails = []
    for post in blogPosts:
        print(post)
        post_d = {}
        post_d['title'] = post[1]
        post_d['content'] = post[2]
        post_d['media'] = post[3]
        blogdetails.append(post_d)
        #print(blogdetails)
    #print([file for file in os.listdir(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']))])
    return blogdetails

# Function to read the current like count from the file
def read_like_count(name):
    try:
        likes = select_all_from_table('locations', f"name = '{name}'")[0][-1]
    except FileNotFoundError:
        return 0
    return likes

# Function to write the updated like count to the file
# def write_like_count(name):
#     update_locationwithlikes(name)

# @app.route('/like')
# def increment_like():
#     name = request.form.get('card.name')
#     write_like_count(name)
#     return redirect(url_for("locationdetails")) 

        
@app.route('/travelblog/blog/viewblog', methods=['GET'])
def viewblog():
    blogPosts = select_all_from_table("blog_page")
    blogdetails = get_blogdetails(blogPosts)
    print("final html")
    print(blogdetails)
    return render_template('view_blog.html', blogPosts=blogdetails)
    
if __name__ == "__main__":
    with app.test_request_context("/"):
        session["key"] = "value"
    app.run(debug=True)