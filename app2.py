from flask import Flask, render_template, request

app = Flask(__name__)


# Декоратор @app.route регистрирует функцию как обработчик URL.
# Когда пользователь заходит на главную страницу "/", вызывается функция home().
# @app.route("/")
# def home():
#     return """
#     <h1>MS</h1>
#     <a href="/about">
#         <button>Нажми меня</button>
#     </a>
#     """

@app.route("/")
def home():
    return """
    <a href="/creators">
        <button>Создатели</button>
    </a>

    """

@app.route("/creators")
def about():
    return """
    <h1>MS | Создатели</h1>
    <p>Главный программист - <b>tigran Newtonioapple gevorkyan</b></p>
    <p>Главный дизайнер - <b>gleb Pappet zdorov</b></p>
    <a href="/">
        <button>MS</button>
    </a>
    """

@app.route('/login', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        username = request.form.get('username')
        # Добавлена буква 'f' перед строкой для форматирования
        return f"""
        <h1>Привет, {username}</h1>
        <a href="/">
            <button>Главная</button>
        </a>
        """
    
    # Если пользователь просто зашел на /login (GET), показываем саму форму
    return """
    <form method="POST">
        <input type="text" name="username" placeholder="Введите имя">
        <button type="submit">Войти</button>
    </form>
    """



    
if __name__ == "__main__":
    app.run(debug=True)