import datetime
from flask import Flask, render_template, request, flash, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError

from database import db_session, Funcionario
from sqlalchemy import select, and_, func
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'senaisp'

login_manager = LoginManager(app)
login_manager.login_view ='login'


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@login_manager.user_loader
def load_user(user_id):
    user = select(Funcionario).where(Funcionario.id == int(user_id))
    resultado = db_session.execute(user).scalar_one_or_none()
    return resultado
@app.route('/')
def home():
    return render_template("home.html")


@app.route('/calculos')
def calculos():
    return render_template("calculos.html")

@app.route('/funcionario')
@login_required
def funcionario():
    funcionario_sql = select(Funcionario)
    funcionario_sql = db_session.execute(funcionario_sql).scalars().all()
    return render_template("funcionario.html", lista_funcionario=funcionario_sql)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # pega o campo do formulario
        email = request.form['form_email']
        senha = request.form['form_senha']

        if not email or not senha:
            flash('Preencha todos os campos', 'alert-danger')
            return render_template('login.html')
        else:
            email_sql = select(Funcionario).where(Funcionario.email == email)
            resultado_email = db_session.execute(email_sql).scalar_one_or_none()

            if resultado_email:
                if resultado_email.check_password(senha):
                    # realiza a autentificação
                    login_user(resultado_email)
                    flash('Login realizado com sucesso', 'alert-sucess')
                    return redirect(url_for("home"))
                else:
                    flash('Senha incorreta', 'alert-danger')
                    return render_template('login.html')
            else:
                flash('Email incorreto', 'alert-danger')
                return redirect(url_for("login"))
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))




    return render_template("login.html")

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro_funcionario():
    if request.method == 'POST':
        nome = request.form['form-nome']
        data_nascimento = request.form['form-data_nascimento']
        cpf = request.form['form-cpf']
        email = request.form['form-email']
        senha = request.form['form-senha']
        cargo = request.form['form-cargo']
        salario = float(request.form['form-salario'])

        if not nome or not email or not senha:
            flash('Preencher todos os campos!', 'danger')
            return render_template('funcionario.html')

        verifica_email = select(Funcionario).where(Funcionario.email == email)
        existe_email = db_session.execute(verifica_email).scalar_one_or_none()
        verifica_cpf = select(Funcionario).where(Funcionario.cpf == cpf)
        existe_cpf = db_session.execute(verifica_cpf).scalar_one_or_none()

        if existe_email:
            flash(f'Email {email} já esta cadastrado!', 'danger')
            return render_template('funcionario.html')

        if existe_cpf:
            flash(f'Email {cpf} já esta cadastrado!', 'danger')
            return render_template('funcionario.html')

        try:
            novo_funcionario = Funcionario(nome=nome, data_nascimento=data_nascimento, cpf=cpf, email=email, cargo=cargo, salario=salario)
            novo_funcionario.set_password(senha)
            db_session.add(novo_funcionario)
            db_session.commit()
            flash(f'Funcionario {nome} cadastrado com sucesso!', 'success')
            return redirect(url_for('login'))

        except SQLAlchemyError as e:
            flash(f'Erro na base de dados ao cadastrar funcionario:', 'danger')
            print(f'Erro na base de dados{e}')
            return redirect(url_for('cadastro_funcionario'))

        except Exception as e:
            flash(f'Erro ao cadastrar funcionario:', 'danger')
            print(f'Erro na base de dados{e}')
            return redirect(url_for('cadastro_funcionario'))
    return redirect(url_for('funcionario'))



@app.route('/operacoes')
def operacoes():
    return render_template("operacoes.html")

@app.route('/geometria')
def geometria():
    return render_template("geometria.html")


@app.route('/somar', methods=['GET', 'POST'])
def somar():
    if request.method == 'POST':
        if request.form['form-n1'] and request.form['form-n2']:
            n1 = int(request.form['form-n1'])
            n2 = int(request.form['form-n2'])
            soma = n1 + n2
            flash("Soma realizada", 'alert-success')
            return render_template("operacoes.html", n1=n1, n2=n2, soma=soma)
        else:
            # Passo 1: Emitir a mensagem e a categoria do flash
            flash("Preencha o campo para realizar a soma", 'alert-danger')
    return render_template("operacoes.html")


@app.route('/subtrair', methods=['GET', 'POST'])
def subtrair():
    if request.method == 'POST':
        if request.form['form-n1'] and request.form['form-n2']:
            n1 = int(request.form['form-n1'])
            n2 = int(request.form['form-n2'])
            subtrair = n1 - n2
            return render_template("operacoes.html", n1=n1, n2=n2, subtrair=subtrair)
    return render_template("operacoes.html")


@app.route('/multiplicar', methods=['GET', 'POST'])
def multiplicar():
    if request.method == 'POST':
        if request.form['form-n1'] and request.form['form-n2']:
            n1 = int(request.form['form-n1'])
            n2 = int(request.form['form-n2'])
            multiplicar = n1 * n2
            return render_template("operacoes.html", n1=n1, n2=n2, multiplicar=multiplicar)
    return render_template("operacoes.html")


@app.route('/dividir', methods=['GET', 'POST'])
def dividir():
    if request.method == 'POST':
        if request.form['form-n1'] and request.form['form-n2']:
            n1 = int(request.form['form-n1'])
            n2 = int(request.form['form-n2'])
            dividir = n1 / n2
            return render_template("operacoes.html", n1=n1, n2=n2, dividir=dividir)
    return render_template("operacoes.html")

@app.route('/triangulo_perimetro', methods=['GET', 'POST'])
def triangulo_perimetro():
    if request.method == 'POST':
        if request.form['form-n1']:
            n1 = int(request.form['form-n1'])
            perimetro = n1 + n1 + n1
            flash("Perímetro realizado", 'alert-success')
            return render_template("geometria.html", n1=n1, perimetro=perimetro)
        else:
            # Passo 1: Emitir a mensagem e a categoria do flash
            flash("Preencha o campo para realizar o perímetro", 'alert-danger')
    return render_template("geometria.html")

@app.route('/triangulo_area', methods=['GET', 'POST'])
def triangulo_area():
    if request.method == 'POST':
        if request.form['form-n1']:
            n1 = int(request.form['form-n1'])
            area = (n1 * n1) / 2
            flash("Área realizada", 'alert-success')
            return render_template("geometria.html", n1=n1, area=area)
        else:
            # Passo 1: Emitir a mensagem e a categoria do flash
            flash("Preencha o campo para realizar a área", 'alert-danger')
    return render_template("geometria.html")


@app.route('/circulo_perimetro', methods=['GET', 'POST'])
def circulo_perimetro():
    if request.method == 'POST':
        if request.form['form-n1']:
            n1 = int(request.form['form-n1'])
            perimetro2 = 2 * 3,14 * n1
            flash("Perímetro realizado", 'alert-success')
            return render_template("geometria.html", n1=n1, perimetro2=perimetro2)
        else:
            # Passo 1: Emitir a mensagem e a categoria do flash
            flash("Preencha o campo para realizar o perímetro", 'alert-danger')
    return render_template("geometria.html")

@app.route('/circulo_area', methods=['GET', 'POST'])
def circulo_area():
    if request.method == 'POST':
        if request.form['form-n1']:
            n1 = int(request.form['form-n1'])
            area2 = 3,14 * n1 ** 2
            flash("Área realizada", 'alert-success')
            return render_template("geometria.html", n1=n1, area2=area2)
        else:
            # Passo 1: Emitir a mensagem e a categoria do flash
            flash("Preencha o campo para realizar a área", 'alert-danger')
    return render_template("geometria.html")

@app.route('/quadrado_perimetro', methods=['GET', 'POST'])
def quadrado_perimetro():
    if request.method == 'POST':
        if request.form['form-n1']:
            n1 = int(request.form['form-n1'])
            perimetro3 = n1 + n1 + n1 + n1
            flash("Perímetro realizado", 'alert-success')
            return render_template("geometria.html", n1=n1, perimetro3=perimetro3)
        else:
            # Passo 1: Emitir a mensagem e a categoria do flash
            flash("Preencha o campo para realizar o perímetro", 'alert-danger')
    return render_template("geometria.html")

@app.route('/quadrado_area', methods=['GET', 'POST'])
def quadrado_area():
    if request.method == 'POST':
        if request.form['form-n1']:
            n1 = int(request.form['form-n1'])
            area3 = n1 * n1
            flash("Área realizada", 'alert-success')
            return render_template("geometria.html", n1=n1, area3=area3)
        else:
            # Passo 1: Emitir a mensagem e a categoria do flash
            flash("Preencha o campo para realizar a área", 'alert-danger')
    return render_template("geometria.html")

@app.route('/hexagono_perimetro', methods=['GET', 'POST'])
def hexagono_perimetro():
    if request.method == 'POST':
        if request.form['form-n1']:
            n1 = int(request.form['form-n1'])
            perimetro4 = n1 + n1 + n1 + n1 + n1 + n1
            flash("Perímetro realizado", 'alert-success')
            return render_template("geometria.html", n1=n1, perimetro4=perimetro4)
        else:
            # Passo 1: Emitir a mensagem e a categoria do flash
            flash("Preencha o campo para realizar o perímetro", 'alert-danger')

    return render_template("geometria.html")

@app.route('/hexagono_area', methods=['GET', 'POST'])
def hexagono_area():
    if request.method == 'POST':
        if request.form['form-n1']:
            n1 = int(request.form['form-n1'])
            area4 = ((n1 * n1) / 2) * 6
            flash("Área realizada", 'alert-success')
            return render_template("geometria.html", n1=n1, area4=area4)
        else:
            # Passo 1: Emitir a mensagem e a categoria do flash
            flash("Preencha o campo para realizar a área", 'alert-danger')

    return render_template("geometria.html")

# TODO Final do código

if __name__ == '__main__':
    app.run(debug=True)


