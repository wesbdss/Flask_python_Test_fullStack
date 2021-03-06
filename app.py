from flask import Flask, request, render_template, jsonify, redirect
import json
app = Flask(__name__)

from flask_mysqldb import MySQL
import time

app.config['MYSQL_HOST'] = 'db4free.net'
app.config['MYSQL_USER'] = 'visie_user'
app.config['MYSQL_PASSWORD'] = 'visie_pass'
app.config['MYSQL_DB'] = 'visie_db'

mysql = MySQL(app)
values = ()

def atualizarValues():
    global values
    cur =  mysql.connection.cursor()
    cur.execute("SELECT * FROM pessoas LIMIT 30")
    values =  cur.fetchall()
    cur.close()
    print(values)

def resto(a,b):
    return a%b

@app.route('/',methods=['GET', 'POST','DELETE'])
def index():
    if request.method == 'GET':
        global values
        try:
            atualizarValues()
            return render_template('index.html',values=values, enumerate = enumerate, resto=resto)
        except Exception as ex:
            return redirect('/')

            
    if request.method == 'POST':
        data = request.form
        id_pessoa = int(request.form['id_pessoa'])
        nome = str(request.form['nome'])
        rg = str(request.form['rg'])
        cpf = str(request.form['cpf'])
        data_nascimento = str(request.form['data_nascimento'])
        data_admissao = str(request.form['data_admissao'])
        funcao = int(request.form['funcao'])
        fields = (id_pessoa,nome,rg,cpf,data_nascimento,data_admissao,funcao)
        try:
            atualizarValues()
        except Exception as ex:
            pass
        try:
            
            sql = '''INSERT INTO pessoas (id_pessoa,nome, rg, cpf, data_nascimento, data_admissao, funcao) VALUES ( %d, "%s", %s, %s, "%s", "%s" ,%d);''' % (id_pessoa,nome,rg,cpf,data_nascimento,data_admissao,funcao)
            cur = mysql.connection.cursor()
            cur.execute(sql)
            mysql.connection.commit()
            return render_template('index.html',values=values, enumerate = enumerate, resto=resto)
        except Exception as ex:
            return redirect('/')

            


        
        
    if request.method == 'DELETE':
        body = json.loads(request.data)
        try:
            atualizarValues()
        except Exception as ex:
            pass
        try:
            sql= '''DELETE FROM pessoas WHERE id_pessoa='''+body['id']+''';'''
            cur = mysql.connection.cursor()
            cur.execute(sql)
            mysql.connection.commit()
            return render_template('index.html',values=values, enumerate = enumerate, resto=resto)
        except Exception as ex:
            return redirect('/')

            





if __name__ == '__main__':
    app.run(debug=True)