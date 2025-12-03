"""
Example Flask integration - Copy and adapt to your Flask app
"""

from flask import Flask, request, redirect, session, render_template_string
from flow_control.login_hook import resolve_login_redirect

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this!

# Mock user database (replace with your actual user system)
USERS = {
    'admin': {'password': 'admin123', 'id': '1'},
    'user': {'password': 'user123', 'id': '2'}
}

def authenticate_user(username, password):
    """Mock authentication - replace with your actual auth logic"""
    user = USERS.get(username)
    if user and user['password'] == password:
        return user
    return None

@app.route('/')
def index():
    if 'user_id' in session:
        return f'<h1>Welcome! User ID: {session["user_id"]}</h1><a href="/logout">Logout</a>'
    return '<h1>Home</h1><a href="/login">Login</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = authenticate_user(username, password)
        
        if user:
            # Store user in session
            session['user_id'] = user['id']
            
            # INTEGRATION POINT - Single line change
            default_route = '/dashboard'
            redirect_url = resolve_login_redirect(user['id'], default_route)
            
            return redirect(redirect_url)
        else:
            return '<p>Invalid credentials</p><a href="/login">Try again</a>'
    
    # Login form
    login_form = '''
    <form method="POST">
        <h2>Login</h2>
        <p>Username: <input type="text" name="username" required></p>
        <p>Password: <input type="password" name="password" required></p>
        <p><button type="submit">Login</button></p>
    </form>
    <p>Try: admin/admin123 or user/user123</p>
    '''
    return render_template_string(login_form)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    return f'<h1>Dashboard</h1><p>User ID: {session["user_id"]}</p><a href="/logout">Logout</a>'

@app.route('/special-page')
def special_page():
    if 'user_id' not in session:
        return redirect('/login')
    return '<h1>Special Page</h1><p>You were redirected here!</p><a href="/logout">Logout</a>'

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    print("=" * 60)
    print("Flask Integration Example")
    print("=" * 60)
    print("\n1. Start the server:")
    print("   python integration_example_flask.py")
    print("\n2. Visit: http://localhost:5000/login")
    print("\n3. Login with: admin/admin123")
    print("\n4. Set an override:")
    print("   from flow_control.service import force_post_login_route")
    print("   force_post_login_route('1', '/special-page', updated_by='admin')")
    print("\n5. Login again - you'll be redirected to /special-page!")
    print("=" * 60)
    print()
    
    app.run(debug=True, port=5000)

