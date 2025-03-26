from app import *
from assets import user

@app.get('/')
@user.required_login
def getHomePage():
    return render_template('index.html')

@app.get('/login')
def getLogin():
    return app.send_static_file('index.html')

@app.get('/register')
def getRegister():
    return app.send_static_file('index.html')


@app.post('/user/login')
def login():
    return user.make_login()

@app.post('/user/register')
def register():
    return user.make_register()


@app.get('/user/logout')
def logout():
    return user.logout()



if __name__ == '__main__':
    app.run(debug=True)