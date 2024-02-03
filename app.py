from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

# Use Heroku environment variables for database configuration
db_config = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'Qunta729'),
    'database': os.environ.get('DB_DATABASE', 'Blog'),
}

# Establish the MySQL database connection
db = mysql.connector.connect(**db_config)
cursor = db.cursor()

# Adjust the authentication method for the MySQL user
cursor.execute("ALTER USER '{}'@'{}' IDENTIFIED WITH mysql_native_password BY '{}';".format(
    db_config['user'], db_config['host'], db_config['password']))

def get_current_user_id():
    # Replace this with your authentication logic to get the current user ID
    return 1  # Placeholder value

# Adjust the authentication method for MySQL user
cursor.execute("ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Qunta729';")

def get_current_user_id():
    # Replace this with your authentication logic to get the current user ID
    return 1  # Placeholder value

@app.route('/')
def index():
    # Display a list of blog posts
    cursor.execute("SELECT * FROM blog_posts")
    posts = cursor.fetchall()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    if request.method == 'POST':
        content = request.form['content']
        author_id = get_current_user_id()  # Implement a function to get the current user ID
        cursor.execute("INSERT INTO comments (post_id, author_id, content) VALUES (%s, %s, %s)",
                       (post_id, author_id, content))
        db.commit()

    cursor.execute("SELECT * FROM blog_posts WHERE id = %s", (post_id,))
    post = cursor.fetchone()
    cursor.execute("SELECT * FROM comments WHERE post_id = %s", (post_id,))
    comments = cursor.fetchall()
    return render_template('view_post.html', post=post, comments=comments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Implement user authentication logic here
    # You may use Flask-Login or other authentication libraries
    # Placeholder, replace with your code
    return render_template('login.html')  # Example: render a login form

@app.route('/logout')
def logout():
    # Implement logout logic here
    # Placeholder, replace with your code
    return redirect(url_for('index'))  # Redirect to the home page after logout

@app.route('/profile/<username>')
def profile(username):
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user:
        cursor.execute("SELECT * FROM blog_posts WHERE author_id = %s", (user[0],))
        posts = cursor.fetchall()
        return render_template('profile.html', user=user, posts=posts)
    else:
        return render_template('profile_not_found.html', username=username)

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        # Get form data
        title = request.form['title']
        content = request.form['content']
        author_id = get_current_user_id()  # Implement a function to get the current user ID

        # Insert new blog post into the database
        cursor.execute("INSERT INTO blog_posts (title, content, author_id) VALUES (%s, %s, %s)",
                       (title, content, author_id))
        db.commit()

        # Redirect to the home page after creating a post
        return redirect(url_for('index'))

    return render_template('create_post.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']

        # Insert new user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()

        # Redirect to login page after registration
        return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)