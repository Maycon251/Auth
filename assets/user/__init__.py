from flask import request, abort, jsonify, make_response, url_for, redirect
from assets.db import db, md5
from functools import wraps
from uuid import uuid4


User = db.get_collection('users')

def required_login(f):
    """ Define rota que requer login obrigatório """
    
    @wraps(f)
    def check_login():
        token = request.cookies.get('token')
        
        if not token:
            return abort(401, 'Login necessário')
        elif User.find_one({ 'token': token }):
            return f()
        else:
            return abort(401, 'Token inválido ou expirado')
        
    return check_login

def make_login():
    """ Realiza o login do usuário """
    
    data = request.get_json(True)
    
    if (User.find_one({ 'name': data['nickname'], 'password': md5(data['password'].encode()).hexdigest() })):
        token = str(uuid4())
        try:
            User.update_one({ 'name': data['nickname'] }, { '$set': {' token': token } })
        except:
            return abort(500, 'Erro no login, tente novamente mais tarde')
        else:
            return jsonify({ 'acess_token': token })
    else:
        abort(404, 'Usuário não encontrado')
        
def make_register():
    """ Realiza o registro do usuário """
    
    data = request.get_json(True)
    print(data)
    if not (User.find_one({ 'name': data['nickname'] })):
        try:
            User.insert_one({ 'name': data['nickname'], 'key': 'T4Convido' , 'permitiontype': 'convidado', 'password': md5(data['password'].encode() ).hexdigest() })
        except:
            return abort(500, 'Erro no registro, tente novamente mais tarde')
        else:
            return make_login()
    else:
        return abort(401, 'Usuário já existe')
     
def logout():
    """ Realiza o logout do usuário """
        
    response = make_response(redirect(url_for('getLogin')))
    response.delete_cookie('token')
    return response


@required_login
def get_permission():
    """ Retorna o tipo de permissão do usuário """
    
    token = request.cookies.get('token')
    
    if token:
        try:
            return User.find_one({ 'token': token }, { 'permitiontype': 1 })
        except:
            return False
    else:
        return 'convidado'
    

@required_login
def getKey():
    """ Retorna a chave do usuário """
    
    token = request.cookies.get('token')
    
    if token:
        try:
            return User.find_one({ 'token': token }, { 'key': 1 })
        except:
            return False
    
