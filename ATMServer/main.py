from flask import Flask, request
from UserHashTable import hash_table

print(hash_table)

app = Flask(__name__)


def checkNip(regnip, nip):
    return regnip == nip


@app.route('/')
def index():
    return 'Server alive and running'


@app.route('/consult')
def consult():
    username = request.args.get('accountid')
    nip = request.args.get('nip')
    balance, regnip = hash_table.get_val(username)
    if (not checkNip(regnip, nip)):
        return '-:Nip incorrecto'
    print(hash_table)
    return f'+:El balance de {username} es {balance}'


@app.route('/withdraw')
def withdraw():
    username = request.args.get('accountid')
    amount = int(request.args.get('amount'))
    nip = request.args.get('nip')
    balance, regnip = hash_table.get_val(username)
    if (not checkNip(regnip, nip)):
        return '-:Nip incorrecto'
    if (balance - amount < 0):
        return '-:No hay fondos suficientes para retirar'
    balance -= amount
    hash_table.set_val(username, [balance, regnip])
    return f'+:El balance de {username} es {balance}'


@app.route('/deposit')
def deposit():
    username = request.args.get('accountid')
    amount = int(request.args.get('amount'))
    nip = request.args.get('nip')
    balance, regnip = hash_table.get_val(username)
    if (nip == "-1"):
        balance += amount
        hash_table.set_val(username, [balance, regnip])
        return f'+:Deposito Anonimo exitoso. {amount} pesos depositados.'
    if (not checkNip(regnip, nip)):
        return '-:Nip incorrecto'
    balance += amount
    hash_table.set_val(username, [balance, regnip])
    print(hash_table)
    return f'+:El balance de {username} es {amount}'


@app.route('/new_account')
def create_account():
    username = request.args.get('accountid')
    nip = request.args.get('nip')
    value = hash_table.get_val(username)
    if (value):
        if (value[1] == nip):
            return f'+:Inicio Sesion Exitoso. {username}'
        else:
            return '-:Nip incorrecto'
    if(nip == "-1"):
      return '+: Inicio Sesion Anonimo Exitoso.'
    hash_table.set_val(username, [0, nip])
    print(hash_table)
    return f'+:Creacion Cuenta Exitosa. {username}'


@app.route('/delete_account')
def delete_account():
    username = request.args.get('accountid')
    nip = request.args.get('nip')
    balance, regnip = hash_table.get_val(username)
    if (not checkNip(regnip, nip)):
        return '-:Nip o usuario incorrecto'
    hash_table.delete_val(username)
    print(hash_table)
    return f'+:Cuenta de {username} borrada con exito'
    print(hash_table)


@app.route('/transfer')
def transfer():
    sender = request.args.get('sender')
    getter = request.args.get('getter')
    nip = request.args.get('nip')
    amount = int(request.args.get('amount'))
    sender_balance, regnip = hash_table.get_val(sender)
    if (not checkNip(regnip, nip)):
        return '-:Nip incorrecto'
    if (sender_balance - amount < 0):
        return '-:No hay fondos suficientes para retirar'
    if (not hash_table.get_val(getter)):
        return f'-:Cuenta recipiente incorrecta. {getter} no existe'

    sender_balance -= amount
    hash_table.set_val(sender, [sender_balance, regnip])
    getter_balance, nipget = hash_table.get_val(getter)
    getter_balance += amount
    hash_table.set_val(getter, [getter_balance, nipget])
    print(hash_table)
    return f'+:Transferencia exitosa. El balance de {sender} es {sender_balance}'


@app.route('/change_nip')
def change_nip():
    username = request.args.get('accountid')
    nip = request.args.get('nip')
    newnip = request.args.get('new_nip')
    if (not hash_table.get_val(username)):
        return f'-:Cuenta incorrecta. {username} no existe'
    value = hash_table.get_val(username)
    if (value[1] != nip):
        return '-:Nip incorrecto'
    hash_table.set_val(username, [value[0], newnip])
    print(hash_table)
    return f'+:Nip de {username} cambiado exitosamenete'


app.run(host='0.0.0.0', port=81)
