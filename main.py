import sqlalchemy
import sqlalchemy
from flask_login import UserMixin
from clasterization import *
from flask import Flask, render_template, request, redirect, url_for, session, make_response
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
import numpy as np
from forms.forms import *
from dao.entities import *
import datetime
import plotly
import plotly.graph_objs as go
import numpy as np
import json
from corellation import pearson
from sqlalchemy import func
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from dao.connection import PostgresDb

app = Flask(__name__)
app.secret_key = 'development key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:134951m@localhost/receipt_webservice'
app.debug = True
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
db = PostgresDb()


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

@login_manager.user_loader
def load_user(user_id):
    return db.sqlalchemy_session.query(User).get(int(user_id))
@app.route('/')
def index():
    allTypes = db.sqlalchemy_session.query(Type).all()
    allDishes = db.sqlalchemy_session.query(Dish).all()
    admin = False

    current_user = session.get('username')
    if (current_user == 'admin'):
        admin = True
    return render_template('index.html', current_user=current_user, admin = admin, allDishes=allDishes, allTypes = allTypes)
@app.route('/all_dishes')
def all_dishes():
    admin = False
    allTypes = db.sqlalchemy_session.query(Type).all()
    allDishes = db.sqlalchemy_session.query(Dish).all()
    current_user = session.get('username')
    if (current_user == 'admin'):
        admin = True
    return render_template('index.html', current_user = current_user, admin = admin,  allDishes = allDishes, allTypes = allTypes)
@app.route('/filtered_dishes')
def filtered_dishes():

    allTypes = db.sqlalchemy_session.query(Type).all()
    allDishes = db.sqlalchemy_session.query(Dish).all()
    filtered_dishes = []
    choosen_type = request.args.get('name')
    current_user = session.get('username')
    if (current_user == 'admin'):
        admin = True
    if (choosen_type == 'all'):
        filtered_dishes = allDishes
    else:
        for dish in allDishes:
            if(dish.type == choosen_type):
                filtered_dishes.append(dish)

    return render_template('index.html', admin = admin, current_user = current_user, allDishes = filtered_dishes, allTypes = allTypes)
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    error = 'User with that data is not exist '
    admin = False
    if form.validate_on_submit():
        user = db.sqlalchemy_session.query(User).filter_by(username = form.username.data).first()
        password = db.sqlalchemy_session.query(User).filter_by(password = form.password.data).first()
        if( user and password):
                login_user(user, remember=form.remember.data)
                session['username'] = user.username
                current_user = session.get('username')
                if (form.username.data == 'admin' and form.password.data == 'adminadmin'):
                    admin = True
                    print('admin')
                    return redirect(url_for('index'))
                    # return render_template('index.html', form=form, error=error, admin=admin, current_user = current_user)
                return redirect(url_for('index'))
                # return render_template('index.html', current_user=current_user, allDishes = allDishes)
                # return redirect(url_for('index'))
        return render_template('login.html', form=form, error = error)
    return render_template('login.html', form = form)
@app.route('/logout')
@login_required
def logout():
    allDishes = db.sqlalchemy_session.query(Dish).all()
    session.pop('username', None)
    current_user = session.get('username')
    return render_template('index.html', current_user = current_user, allDishes = allDishes)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    error = 'User with that data already exist'
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        a = db.sqlalchemy_session.query(User).filter(User.username == form.username.data).all()
        b = db.sqlalchemy_session.query(User).filter(User.email == form.email.data).all()
        if not (a or b):
            db.sqlalchemy_session.add(new_user)
            db.sqlalchemy_session.commit()
            session['username'] = new_user.username
            current_user = session.get('username')
            print('ITS OKAY')
            return render_template('index.html',current_user = current_user)
        return render_template('signup.html', form=form, error=error)
    return render_template('signup.html', form = form)
@app.route('/all_users')
def all_users():
    admin = False
    current_user = session.get('username')
    allUsers = db.sqlalchemy_session.query(User).all()
    return render_template('allusers.html', allUsers = allUsers, current_user = current_user)
@app.route('/delete_user')
def delete_user():
    username = request.args.get('name')
    user = db.sqlalchemy_session.query(User).filter(User.username == username).first()
    db.sqlalchemy_session.delete(user)
    db.sqlalchemy_session.commit()

    return redirect(url_for('all_users'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', current_user=current_user.username)


@app.route('/new_dish', methods=['GET', 'POST'])
def new_dish():
    admin = False
    db = PostgresDb()
    allDishes = db.sqlalchemy_session.query(Dish).all()
    # alldeparts = db.sqlalchemy_session.query(Departmanet).all()
    allIngridients = db.sqlalchemy_session.query(Ingridient).all()
    allTypes = db.sqlalchemy_session.query(Type).all()
    form = DishForm()
    choosen_ingridients = request.form.getlist('select_ingridient')
    print('choosen', choosen_ingridients)
    current_user = session.get('username')
    if (current_user == 'admin'):
        admin = True
    if request.method == 'POST':
        if not form.validate():
            return render_template('dish_form.html',
                                   admin = admin,
                                   form=form,
                                   form_name="New dish",
                                   current_user=current_user,
                                   allTypes = allTypes,
                                   allIngridients = allIngridients,
                                   action="new_dish")
        else:
            dish_obj = Dish(
                dishname=form.dishname.data,
                calories_amount=form.calories_amount.data,
                ingridients = choosen_ingridients,
                receipt = form.receipt.data,
                author=current_user,
                type=request.form.get('type_select'),
            )
            db = PostgresDb()
            a = db.sqlalchemy_session.query(Dish).filter(Dish.dishname == form.dishname.data).all()
            if not a:
                db.sqlalchemy_session.add(dish_obj)
                db.sqlalchemy_session.commit()
                allDishes = db.sqlalchemy_session.query(Dish).all()
            return render_template('index.html', current_user=current_user, allDishes=allDishes, admin = admin, allTypes = allTypes, choosen_ingridients = choosen_ingridients)
    return render_template('dish_form.html',
                           allIngridients = allIngridients,
                            form=form,
                            form_name="New dish",
                            current_user=current_user,
                            allTypes=allTypes,
                            admin = admin,
                            action="new_dish")


# MYDISHES
@app.route('/mydishes',  methods = ['GET'])
def mydishes():
    admin = False
    current_user = session.get('username')
    if (current_user == 'admin'):
        admin = True
    allDishes = db.sqlalchemy_session.query(Dish).all()
    current_user = session.get('username')
    return render_template('mydishes.html', admin = admin, allDishes = allDishes, current_user = current_user)
@app.route('/edit_dish', methods=['GET', 'POST'])
def edit_dish():
    allTypes = db.sqlalchemy_session.query(Type).all()
    form = DishForm()
    current_user = session.get('username')
    if request.method == 'GET':
        dishname = request.args.get('name')
        dish = db.sqlalchemy_session.query(Dish).filter(
            Dish.dishname == dishname).one()
        a = db.sqlalchemy_session.query(Dish).filter(Dish.dishname == dish.dishname).all()
        if not a:
            return render_template('dish_form.html',
                                   form=form,
                                   form_name="Edit dish",
                                   current_user = current_user,
                                   allTypes=allTypes,
                                   action="edit_dish")
        form.calories_amount.data = dish.calories_amount
        form.dishname.data = dish.dishname
        form.old_name.data = dish.dishname
        return render_template('dish_form.html',
                               form=form,
                               form_name="Edit dish",
                               current_user=current_user,
                               allTypes=allTypes,
                               action="edit_dish")

    else:
        if not form.validate():
            return render_template('dish_form.html',
                                   form=form,
                                   form_name="Edit dish",
                                   allTypes=allTypes,
                                   action="edit_dish")
        else:
            dish = db.sqlalchemy_session.query(Dish).filter(Dish.dishname == form.old_name.data).one()
            dish.dishname = form.dishname.data
            dish.calories_amount = form.calories_amount.data
            db.sqlalchemy_session.commit()
            return redirect(url_for('mydishes'))
@app.route('/delete_dish')
def delete_dish():
    dishname = request.args.get('name')
    dish = db.sqlalchemy_session.query(Dish).filter(Dish.dishname == dishname).first()
    db.sqlalchemy_session.delete(dish)
    db.sqlalchemy_session.commit()

    return redirect(url_for('mydishes'))
@app.route('/delete_dish_user')
def delete_dish_user():
    dishname = request.args.get('name')
    dish = db.sqlalchemy_session.query(Dish).filter(Dish.dishname == dishname).first()
    db.sqlalchemy_session.delete(dish)
    db.sqlalchemy_session.commit()

    return redirect(url_for('index'))
@app.route('/correllation', methods=['GET', 'POST'])
def corellation():
    array = []
    admin = False

    allData = db.sqlalchemy_session.query(Dish).all()
    current_user = session.get('username')
    choosen_dish = request.form.get('comp_select')
    if(current_user == 'admin'):
        admin = True
    if(choosen_dish == None):
        return render_template('correllation.html', current_user=current_user, allData=allData, selected= choosen_dish, admin = admin )
    else:
        for i in (allData):
            if (i.dishname == choosen_dish):
                index = allData.index(i)
                output_dish = allData[index].__dict__
                return render_template('correllation.html', current_user=current_user, admin = admin,  allData=allData, output_dish = output_dish, array = array)
    return render_template('correllation.html', current_user=current_user, allData=allData, admin = admin)
@app.route('/fill_personal_data', methods = ['GET', 'POST'])
def fill_personal_data():
    current_user = session.get('username')
    allDishes= db.sqlalchemy_session.query(Dish).all()

    form = PersonalDataForm()
    personal_data_obj = {
    }
    if request.method == 'POST':
        if not form.validate():
            return render_template('personal_data.html', form=form, form_name="New personal data", action="fill_personal_data")
        else:
            age = form.age.data
            weight = form.weight.data
            height = form.height.data

            personal_data_obj = {
                "age":age,
                "weight":weight,
                "height":height
            }
            a = []
            a.append(personal_data_obj["age"])
            a.append(personal_data_obj["weight"])
            a.append(personal_data_obj["height"])
            output_result = output(a)
            print('output', output(a))
            return render_template('correllation.html', allDishes = allDishes, output_result = output_result, pearson_res = pearson_res, current_user = current_user,  personal_data_obj = personal_data_obj)
    return render_template('personal_data.html', current_user = current_user, form =form, form_name="New personal data", action="fill_personal_data")


if __name__ == '__main__':
    app.run()
