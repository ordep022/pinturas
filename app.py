from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# ===== CORREÇÃO SUPABASE / RENDER =====
database_url = os.getenv("DATABASE_URL")

if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ===== MODELO DA TABELA =====
class Orcamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(200))
    descricao = db.Column(db.Text)
    prazo = db.Column(db.String(50))
    data_inicio = db.Column(db.String(50))
    data_fim = db.Column(db.String(50))
    valor = db.Column(db.String(50))

# ===== CRIA TABELA AUTOMATICAMENTE =====
with app.app_context():
    db.create_all()

# ===== ROTAS =====
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    novo = Orcamento(
        nome=request.form['nome'],
        telefone=request.form['telefone'],
        endereco=request.form['endereco'],
        descricao=request.form['descricao'],
        prazo=request.form['prazo'],
        data_inicio=request.form['data_inicio'],
        data_fim=request.form['data_fim'],
        valor=request.form['valor']
    )
    db.session.add(novo)
    db.session.commit()
    return redirect('/')

# ===== INICIAR SERVIDOR =====
if __name__ == '__main__':
    app.run(debug=True)





