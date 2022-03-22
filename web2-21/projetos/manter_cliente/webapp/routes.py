from flask import (
    Flask, render_template, request, redirect
)
from manter.entities import Produto
from manter.entities import Fornecedor
from manter.database import Database
from manter.entities import Cliente
from manter.dao import DaoCliente
# importando a variavel app do __init__.py
from . import app
from . import db  # ==> SQLAlchemy - vem do __init__.py

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/cliente/add")
def cliente_add():
    return render_template('cadastro_cliente.html', cliente=None)

@app.route("/cliente/edit/<id>")
def cliente_edit(id):
    # buscar na dao o cliente
    # find_by_id(id) - recupera 1 cliente
    dao = DaoCliente()
    cliente = dao.find_by_id(id)
    return render_template(
        'cadastro_cliente.html',
        cliente=cliente
    )

@app.route("/save", methods=["POST"])
def save():
    # recebe os campos do formulario
    # criar o objeto cliente
    # chamar a dao que salva no banco de dados
    id = request.form.get("id")
    nome = request.form.get("nome")
    cpf = request.form.get("cpf")
    email = request.form.get("email")
    cliente = Cliente(nome, cpf, email)
    dao = DaoCliente()
    if id:
        cliente.id = id
        dao.update(cliente)
    else:
        dao.save(cliente)
    return findall()

@app.route("/delete/<id>")
def delete(id):
    dao = DaoCliente()
    dao.delete(id)
    return redirect("/cliente/findall/")


@app.route("/fornecedor/delete/<id>")
def fornecedor_delete(id):
    # Select from fornecedor where id = id
    fn = Fornecedor.query.get(id)
    db.session.delete(fn) # Delete ...
    db.session.commit()
    return f"ok, fornecedor id={id} removido com sucesso!"
    # TODO: redirecionar para fornecedor/findall


@app.route('/restore')
def restore():
    Database.create_db()
    return redirect("/cliente/findall")

@app.route('/fornecedor/list')
def fornecedor_list():
    query = Fornecedor.query.all()  # SELECT * From fornecedor
    print(Fornecedor.query.all())
    return f"{query}"

# TODO: get_fornecedor(id)
# TODO: fornecedor_save()
#
# fn = Fornecedor.query.filter_by(cnpj=19999)
#
# # SELECT from Fornecedor Where nome == "Empresa SA" LIMIT 1
# fn = Fornecedor.query.filter_by(nome='Empresa SA').first()
# # Descobrir os fornecedores com pedido maior que 100
# lista = Fornecedor.query.filter_by(pedidos=100)
#
# lista = Fornecedor.query.filter(
#     Fornecedor.nome.endswith('SA')
# ).all()
#
# lista = Fornecedor.query.filter_by(
#     Fornecedor.nome.endswith('SA')
# ).order_by(Fornecedor.pedidos.desc())


@app.route("/produto/delete/<id>")
def produto_delete(id):
    # Select from produto where id = id
    fn = Produto.query.get(id)
    db.session.delete(fn) # Delete ...
    db.session.commit()
    return f"ok, produto id={id} removido com sucesso!"
    # TODO: redirecionar para produto/findall


@app.route('/restore')
def restore():
    Database.create_db()
    return redirect("/produto/findall")

@app.route('/produto/list')
def produto_list():
    query = Produto.query.all()  # SELECT * From produto
    print(Produto.query.all())
    return f"{query}"



@app.route('/createdb')
def createdb():
    db.drop_all()   # vai apagar todos dados (Cuidado!!!)
    db.create_all() # cria o banco (manter2.db)
    # from manter.entities import Fornecedor

    # cria um objeto Fornecedor
    f1 = Fornecedor(nome="Empresa SA",
                    cnpj=19999,
                    site="www",
                    pedidos=28)
    f2 = Fornecedor(nome="Master SA",
                    cnpj=28888,
                    site="www.org",
                    pedidos=444)

    db.session.add(f1)  # INSERT INTO fornecedor ...
    db.session.add(f2)
    db.session.commit() # realiza essa operacao

    return "ok database criado!"


@app.route("/update")
def update():
    # alem dos atributos eh necessario o ID
    # cliente = Database.find(id)
    # atualiza os campos...
    # Database.update(cliente)
    return "manter.html"

@app.route("/cliente/findall/")
def findall():
    dao = DaoCliente()
    clientes = dao.findall()
    return render_template("manter.html", clientes=clientes)
