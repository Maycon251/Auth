
from flask import request, abort, jsonify, url_for, redirect, make_response
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
    
    user = User.find_one({ 'name': data['nickname'], 'password': md5(data['password'].encode()).hexdigest() }, {'permitiontype': 1})
    if (user):
        token = str(uuid4())
        try:
            User.update_one({ 'name': data['nickname'] }, { '$set': {'token': token } })
        except:
            return abort(500, 'Erro no login, tente novamente mais tarde')
        else:
            response = jsonify({ 'status': 'success', 'permisionType': user['permitiontype'] })
            response.set_cookie('token', token, samesite='Lax', httponly=True, secure=True)
            response.status_code = 200 if user['permitiontype'] != 'blocked' else 403
            return response
    else:
        return abort(401, 'Login e/ou senha inválidos')
        
def make_register():
    """ Realiza o registro do usuário """
    
    data = request.get_json(True)
   
    if not data.get('nickname') or not data.get('password'):
        return abort(400, 'Dados inválidos')
    
    if not (User.find_one({ 'name': data['nickname'] })):
        try:
            User.insert_one({ 'name': data['nickname'], 'key': getenv('GUEST_KEY') , 'permitiontype': 'blocked', 'password': md5(data['password'].encode() ).hexdigest() })
        except:
            return abort(500, 'Erro no registro, tente novamente mais tarde')
        else:
            return jsonify({ 'status': 'success' })
    else:
        return abort(401, 'Usuário já existe')

def logout():
    """ Realiza o logout do usuário """
    
    response = make_response(redirect(url_for('getLogin')))
    response.delete_cookie('token', samesite='Lax', httponly=True, secure=True)
    return response


def list_users(filter):
    """ Lista os usuários com base no filtro """
    
    users = User.find(filter, { '_id': 0, 'name': 1, 'permitiontype': 1 }).limit(50)
    
    if not users:
        return abort(404, 'Nenhum usuário encontrado')
    
    return jsonify([ { 'nickname': user['name'], 'permitiontype': user['permitiontype'] } for user in users ])

def block_permission(nickname):
    """ Bloqueia um usuário """
    
    try:
        User.update_one({ 'name': nickname }, { '$set': { 'permitiontype': 'blocked' } })
    except:
        return abort(500, 'Erro ao bloquear usuário')
    else:
        return jsonify({ 'status': 'success' })

def unblock_permission(nickname):
    """ Desbloqueia um usuário """
    
    try:
        User.update_one({ 'name': nickname }, { '$set': { 'permitiontype': 'guest' } })
    except:
        return abort(500, 'Erro ao desbloquear usuário')
    else:
        return jsonify({ 'status': 'success' })

def delete_user(nickname):
    try:
        User.delete_one({ 'name': nickname })
    except:
        return abort(500, 'Erro ao deletar usuário, tente novamente mais tarde')
    else:
        return jsonify({ 'status': 'success' })
