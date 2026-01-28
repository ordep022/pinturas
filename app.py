from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# CONFIGURAÇÃO DO BANCO (local = SQLite | Render = PostgreSQL)
database_url = os.environ.get('DATABASE_URL')

if database_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# TABELA
class Orcamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    telefone = db.Column(db.String(100))
    servico = db.Column(db.String(100))
    local = db.Column(db.String(200))
    prazo = db.Column(db.String(100))
    data_inicio = db.Column(db.String(50))
    data_fim = db.Column(db.String(50))
    data_pedido = db.Column(db.String(50))

# ROTAS
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    novo = Orcamento(
        nome=request.form['nome'],
        telefone=request.form['telefone'],
        servico=request.form['servico'],
        local=request.form['local'],
        prazo=request.form['prazo'],
        data_inicio=request.form['data_inicio'],
        data_fim=request.form['data_fim'],
        data_pedido=datetime.now().strftime('%Y-%m-%d %H:%M')
    )
    db.session.add(novo)
    db.session.commit()
    return "Orçamento enviado com sucesso!"

# CRIAR BANCO AO INICIAR (Flask 3)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


