from flask import Flask, redirect, render_template, request, session, url_for
from pathlib import Path
from uuid import uuid4
from werkzeug.utils import secure_filename
app = Flask(__name__)
caminho = Path(__file__).parent / 'cardapio.txt'
pastaPrj = Path(__file__).parent
caminhoSenha = pastaPrj / 'senhas.txt'
pasta = Path(app.static_folder) / 'imagens'
pasta.mkdir(parents=True, exist_ok=True)
app.secret_key = '18fae3aabc11b58eea256223cf850b8cf3ba19d00fe81293ffc798ae2e383608'
senhas = []
with open(caminhoSenha, "r", encoding="utf-8") as arquivo:
    for linha in arquivo:
        senha = linha.strip()
        if senha:
            senhas.append(senha)

@app.route('/')
def inicio():
    return render_template('index.html')
@app.route('/sobre.html')
def sobre():
    return render_template('sobre.html')
@app.route('/contato.html')
def contato():
    return render_template('contato.html')
@app.route('/cardapio.html')
def cardapio():
    listaProdutos = []
    with open(caminho, 'r', encoding='utf-8') as arquivo:
        for i in arquivo:
            frase = i.strip().split(';')
            nome = frase[0]
            preco = frase[1]
            imagem = frase[2]
            valor = float(preco)
            preco_ex = f"{valor:.2f}".replace(".", ",")
            produto = {
                'nome': nome,
                'preco': preco_ex,
                'imagem': imagem
            }

            listaProdutos.append(produto)

    return render_template('cardapio.html', listaProdutos=listaProdutos)
@app.route('/frete.html', methods=['GET', 'POST'])
def frete():
    if request.method == 'GET':
        return render_template('frete.html')
    if request.method == 'POST':
        valorCompra = int(request.form['valorCompra'])
        valorDistancia = int(request.form['valorDistancia'])
        cal = 5 + (2 * valorDistancia)
        cal2 = valorCompra + cal

        return render_template('frete.html', valorCompra=valorCompra, valorDistancia= valorDistancia, cal2=cal2, cal=cal)
@app.route('/cadastro.html', methods=['GET', 'POST'])
def cadastro():
    if not session.get('autenticado'):
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('cadastro.html')
    if request.method == 'POST':
        a = []
        nome = request.form['nome']
        preco = request.form['preco']
        imagem = request.files['imagem']
        extensao = Path(imagem.filename).suffix.lower()
        permitidas = {".jpg", ".jpeg", ".png", ".webp"}
        if extensao not in permitidas:
            return "Use JPG, PNG ou WEBP.", 400
        a.append(nome)
        a.append(preco)
        nomeSafe = secure_filename(imagem.filename)
        if not nomeSafe:
            return "Selecione uma imagem.", 400
        novoNome = uuid4().hex[:8] + "_" + nomeSafe
        a.append(novoNome)
        imagem.save(str(pasta / novoNome))
        with open (caminho, 'a') as arquivo:
            arquivo.write('\n')
            for i in a:
                arquivo.writelines(i + ';')
        return render_template('cadastro.html')
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    erro = ''
    if request.method == "GET":
        return render_template('login.html')
    if request.method == "POST":
        senha = request.form['senha']
        with open(caminhoSenha,'r', encoding='utf-8') as arquivo:
            for i in arquivo:
                if senha == i.strip():
                    session['autenticado'] = True
                    return render_template('cadastro.html')
        erro = 'Senha incorreta'
    return render_template('login.html', erro=erro)
app.run(debug=True)
