from flask import Flask, render_template, redirect, url_for, flash, request 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user


app = Flask(__name__)

# aqui está sendo setada su chave segura, pense bem na sua chave segura, ela é resnsável por fazer com que os forms(formulários) apareçam e transportem dados pelas requisiçoẽs: [GET,POST,PUT,DELETE]
app.config['SECRET_KEY'] = "minha chave segura" 
# aqui a configuracao da instancia da aplicação está recebendo um "caminho" do banco de dados sqlite com o nome site.db
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"

# a variável db está recebendo a classe SQLAlchemy com a instãncia da aplicação
db = SQLAlchemy(app)

# a variável bcrypt está recebendo a Classe Bcrypt com a instãncia da aplicação
bcrypt = Bcrypt(app)

# LoginManager é responsável por gerenciar as sessoẽs de login dos usuários
# caso alguem tente acessar uma rota que é nesscesária a autenticação ou login ela será redirecionada para a rota login 
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# Modelo de Usuario
# está classe está sendo responsável por criar e conectar a aplicação com o banco de dados. Isso se chama ORM (Object-Relational_Mapping)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


# esta função é responsável por carregar o usuário pelo seu id, ajudando a saber quem está logado
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Garante que as tabelas sejam criadas se não existirem 
with app.app_context():
    db.create_all()


# Rota de registro de usuario
@app.route("/register", methods=["GET","POST"]) # a rota /register suporta os métodos "GET" = Pegar, e "POST" = enviar
def register():
    if request.method == "POST": # se a requisição/pedido do tipo/método for igual a "POST"
        username = request.form.get('username') # username recebe = request.form.get ( faça uma requisição em forms para pegar o campo 'usename')
        email = request.form.get('email')# emailrecebe = request.form.get ( faça uma requisição em forms para pegar o campo 'email')
        password = request.form.get('password')# password recebe = request.form.get ( faça uma requisição em forms para pegar o campo 'password')


        # esta variável está recebendo um password criptografado para ser salvo no banco de dados
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password) #  a variável 'user' está recebendo a classe 'User' com os parâmetros passados nos respectivos campos: username, email, password 
        db.session.add(user)
        db.session.commit()

        flash("Sua conta foi criada! Agora você pode fazer login", "success")
        return redirect(url_for("login")) # se tudo ocooreu corretamente retorne o redirecionamento para a url 'login'
    
    return render_template("register.html") # se a requisição for do tipo = "GET" renderize a página. Ela será renderizada inicialmente porque a primeira requesição a ser feita é a requisição po tipo 'GET'


# Rota para login de usuários
@app.route("/login", methods=["GET","POST"])# a rota /login suporta os métodos "GET" = Pegar, e "POST" = enviar
def login():
    if request.method == "POST":# se a requisição/pedido do tipo/método for igual a "POST"
        email = request.form.get("email")# email recebe = request.form.get ( faça uma requisição em forms para pegar o campo 'email')
        password = request.form.get("password")# password recebe = request.form.get ( faça uma requisição em forms para pegar o campo 'password')
        user = User.query.filter_by(email=email).first()# user recebe o parâmetro. User esta pesquisando/consultando e filtrando por email=ao email passado no campo email da rota login. first() se refere ao primeiro parâmetro que for encontrado referente ao campo email que foi passado ma página da rota login

        if user and bcrypt.check_password_hash(user.password, password):# se a variavel user e seu password já descriptografado for igual ao que foi registrado
            login_user(user)# esta função é responsavel por 'logar' o usuario login_user() receberá 'user' como um parâmetro.
            return redirect(url_for('dashboard'))
        else:# senão
            flash("Login falhou. Verifique o e-mail e a senha.", "danger") # frase
    return render_template("login.html")# se a requisição for do tipo = "GET" renderize a página. Ela será renderizada inicialmente porque a primeira requesição a ser feita é a requisição po tipo 'GET'



@app.route("/logout")# a rota /logout somente será acessada se o usuario estiver logado
@login_required# este decorator tem função de verificar se o usuario esta ou não logado
def logout():
    logout_user()# esta função tem como dever "deslogar" o usuario
    return redirect(url_for("login"))# aqui o usuario será redirecionado para a url /login (da linha 68)
    #return redirect(url_for("register"))


@app.route("/dashboard")# a rota /dashboard somente será acessada se o usuario estiver logado
@login_required# este decorator tem função de verificar se o usuario esta ou não logado
def dashboard():
    return render_template("dashboard.html")# renderiza a pagina dashboard.html



# uma simples rota que representa a home ou index
@app.route("/", methods=["GET"])
# @app.route("/home", methods=["GET"])
@app.route("/home/", methods=["GET"])# dica, se deixar a rota com / no inicio e no fim, na url ela se au completara, faca o teste e veja retirando a / do fim da url
def home():
    return render_template("home.html")



# pratica recomendável para que o script rode.
if __name__ == "__main__":
    app.run(debug=True)
