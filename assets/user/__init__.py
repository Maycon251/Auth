
from flask import request, abort, jsonify, url_for, redirect
from assets.db import db, md5
from functools import wraps
from uuid import uuid4
from os import getenv


User = db.get_collection('users')

def required_login(f):
    """ Define rota que requer login obrigatório """
    
    @wraps(f)
    def check_login():
        token = request.cookies.get('token')
        
        if not token:
            return abort(401, 'Login necessário')
        
        user = User.find_one({ 'token': token }, {'permitiontype': 1 })
        
        if not user:
            return abort(401, 'Token inválido ou expirado')
        elif user['permitiontype'] == 'blocked':
            return abort(403, 'Usuário bloqueado')
        return f()
        
    return check_login


def required_admin(f):
    """ Define rota que requer permissão de admin """
    
    @wraps(f)
    def check_admin():
        token = request.cookies.get('token')
        
        if not token:
            return abort(401, 'Login necessário')
        elif User.find_one({ 'token': token, 'permitiontype': 'admin' }):
            return f()
        return abort(403, 'Você não tem permissão necessária')
        
    return check_admin


def make_login():
    """ Realiza o login do usuário """
    
    data = request.get_json(True)
    
    if not data.get('nickname') or not data.get('password'):
        return abort(400, 'Dados inválidos')
    
    if (User.find_one({ 'name': data['nickname'], 'password': md5(data['password'].encode()).hexdigest() })):
        token = str(uuid4())
        try:
            User.update_one({ 'name': data['nickname'] }, { '$set': {' token': token } })
        except:
            return abort(500, 'Erro no login, tente novamente mais tarde')
        else:
            return jsonify({ 'acess_token': token })
    else:
        return abort(404, 'Usuário não encontrado')
        
        
def make_register():
    """ Realiza o registro do usuário """
    
    data = request.get_json(True)
   
    if not data.get('nickname') or not data.get('password'):
        return abort(400, 'Dados inválidos')
    
    if not (User.find_one({ 'name': data['nickname'] })):
        try:
            User.insert_one({ 'name': data['nickname'], 'key': getenv('GUEST_KEY') , 'permitiontype': 'bloqued', 'password': md5(data['password'].encode() ).hexdigest() })
        except:
            return abort(500, 'Erro no registro, tente novamente mais tarde')
        else:
            return make_login()
    else:
        return abort(401, 'Usuário já existe')
   

@required_login
def getKey():
    """ Retorna a chave do usuário """
    
    token = request.cookies.get('token')
    
    try:
        return User.find_one({ 'token': token }, { 'key': 1 })
    except:
        return False


def block_permission():
    """ Bloqueia um usuário """
    
    data = request.get_json(True)
    
    if not data.get('nickname'):
        return abort(400, 'Dados inválidos')
    
    try:
        User.update_one({ 'name': data['nickname'] }, { '$set': { 'permitiontype': 'blocked' } })
    except:
        return abort(500, 'Erro ao bloquear permissão, tente novamente mais tarde')
    else:
        return jsonify({ 'status': 'success' })


def unblock_permission():
    """ Desbloqueia um usuário """
    
    data = request.get_json(True)
    
    if not data.get('nickname'):
        return abort(400, 'Dados inválidos')
    
    try:
        User.update_one({ 'name': data['nickname'] }, { '$set': { 'permitiontype': 'guest' } })
    except:
        return abort(500, 'Erro ao desbloquear permissão, tente novamente mais tarde')
    else:
        return jsonify({ 'status': 'success' })
