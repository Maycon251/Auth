from flask import redirect, url_for, request, abort
from assets import user
from functools import wraps
from assets import db
import requests

Controller = db.get_collection('controller')


@user.required_admin
def setIP():
    """ Altera o IP do Controlador """
   
    data = request.get_data()
    try:
        Controller.update_one({ 'name': 'T4 Eletro' }, { '$set': { 'ip': data.get('ip') } })
    except:
        return abort(500, 'Erro ao alterar o IP, tente novamente mais tarde')
    else:
        return 'sucess'
        
        
def send_command():
    """ Envia um comando para o Controlador """
    
    controllerip = Controller.find_one({ "name": "T4 Eletro" }, { 'ip': 1 })
    data = request.get_data()
    user_key = user.getKey()
    
    if controllerip and user_key:
        response = requests.post(f'http://{ controllerip }/{ data.get('command') }?key={ user_key }')
        return response.text 
    else:
        return abort(400, 'Dados insuficientes, tente novamente')
    

def key(action: str['add', 'rm']):
    """ Adiciona ou remove uma chave de convidado no Controlador """
    
    controllerip = Controller.find_one({ "name": "T4 Eletro" }, { 'ip': 1 })
    user_key = user.getKey()
    
    if controllerip and user_key:
        response = requests.post(f'http://{ controllerip }/{ action }guest?key={ user_key }')
        return response.text 
    return abort(400, 'Dados insuficientes, tente novamente')

