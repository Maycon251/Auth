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



@app.post('/admin/listusers')
@user.required_admin
def listUsers():
    data = request.get_json(True)
    
    return user.list_users(data.get('filter') or { 'permitiontype': { '$ne': 'admin' } })

@app.delete('/admin/deleteuser')
@user.required_admin
def deleteUser():
    data = request.get_json(True)
    if not data.get('nickname'):
        return abort(400, 'Dados inválidos')
    
    return user.delete_user(data.get('nickname'))

@app.post('/admin/blockpermission')
@user.required_admin
def blockUserPermission():
    data = request.get_json(True)
    if not data.get('nickname'):
        return abort(400, 'Dados inválidos')
    
    return user.block_permission(data['nickname'])

@app.post('/admin/unblockpermission')
@user.required_admin
def unblockUserPermission():
    data = request.get_json(True)
    if not data.get('nickname'):
        return abort(400, 'Dados inválidos')
    
    return user.unblock_permission(data['nickname'])



@app.get('/error-api')
def getErrorAPI():
    return app.send_static_file('index.html')

@app.errorhandler(Exception)
def error(e):
    if request.method == 'GET':
        return redirect(f'/error-api?status={e.code}')
    return jsonify({ 'status': 'error', 'message': str(e) }), e.code

if __name__ == '__main__':
    app.run(debug=True)