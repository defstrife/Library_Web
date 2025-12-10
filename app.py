from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from models import db, User, Author, Book, Order, Issuance
from forms import LoginForm, BookForm, OrderForm, IssueForm
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = '!!!&&&%%%64r147812648930**&^^'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager(app)

migrate = Migrate(app, db)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('index'))
        flash('Неверное имя пользователя или пароль')
    return render_template('login.html', form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/add_book', methods = ['GET', 'POST'])
@login_required
def add_book():
    form = BookForm()
    form.author.choices = [(author.id, author.name)for author in Author.query.all()]
    if form.validate_on_submit():
        book = Book(title = form.title.data, author_id = form.author.data, genre = form.genre.data)
        db.session.add(book)
        db.session.commit()
        flash('Книга добавлена')
        return redirect(url_for('index'))
    return render_template('books/add_book.html', form = form)

@app.route('/order', methods=['GET', 'POST'])
@login_required
def order():
    form = OrderForm()
    form.book_id.choices = [(book.id, book.title) for book in Book.query.filter_by(available=True).all()]
    if form.validate_on_submit():
        order = Order(user_id=current_user.id, book_id=form.book_id.data)
        db.session.add(order)
        db.session.commit()
        flash('Книга заказана!')
        return redirect(url_for('index'))
    return render_template('orders/order.html', form=form)

@app.route('/issue', methods=['GET', 'POST'])
@login_required
def issue():
    if current_user.role not in ['librarian', 'admin']:
        flash('У вас нет прав для выдачи книг!')
        return redirect(url_for('index'))

    form = IssueForm()
    form.user_id.choices = [(user.id, user.username) for user in User.query.filter_by(role='reader').all()]
    form.book_id.choices = [(book.id, book.title) for book in Book.query.filter_by(available=True).all()]
    if form.validate_on_submit():
        book = Book.query.get(form.book_id.data)
        book.available = False
        issuance = Issuance(user_id=form.user_id.data, book_id=form.book_id.data)
        db.session.add(issuance)
        db.session.commit()
        flash('Книга выдана!')
        return redirect(url_for('index'))
    return render_template('issuances/issue.html', form=form)

@app.route('/track')
@login_required
def track():
    if current_user.role not in ['librarian', 'admin']:
        flash('У вас нет прав для просмотра выдач!')
        return redirect(url_for('index'))

    issuances = Issuance.query.filter_by(status='выдано').all()
    return render_template('issuances/track.html', issuances=issuances)

# Create tables after all models are defined
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)