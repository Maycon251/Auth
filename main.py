from app import *
from assets import user

@app.get('/')
@user.required_login
def getHomePage():
    return app.send_static_file('index.html')

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


@app.post('/admin/blockPermission')
@user.required_admin
def blockUserPermission():
    data = request.get_json(True)
    
    if not data:
        return abort(400, 'Dados inválidos')
    
    return user.block_permission()

@app.post('/admin/unblockPermission')
@user.required_admin
def unblockUserPermission():
    data = request.get_json(True)
    
    if not data:
        return abort(400, 'Dados inválidos')
    return user.unblock_permission()


@app.get('/error-api')
def getErrorAPI():
    return app.send_static_file('index.html')

@app.errorhandler(Exception)
def error(e):
    return redirect(f'/error-api?status={e.code}')

if __name__ == '__main__':
    app.run(debug=True)