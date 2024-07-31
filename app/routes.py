from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user
from app import db
from app.forms import RegisterForm, AuthorizationForm
from app.models import User, Recepts
from urllib.parse import urlsplit
from app.logic import search_recipes_by_category, search_recipes_by_keyword

from app import app


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/profile')
def profile():

    recipes = Recepts.query.filter_by(id_user=current_user.id).all()

    return render_template('profile.html', recipes=recipes)


@app.route('/register', methods=["POST", "GET"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        name = request.form['name']
        email = request.form['email']

        user = User(username=name, email=email)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('authorization'))

    return render_template('register.html', form=form)


@app.route('/authorization', methods=["POST", "GET"])
def authorization():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = AuthorizationForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):

            return redirect(url_for('authorization'))

        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')

        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('profile')
        return redirect(next_page)

    return render_template('authorization.html', form=form)


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':

        name = request.form['name']
        category = request.form['category']
        ingredients = request.form['Ingredients']
        recept = request.form['steps']
        time = request.form['time']

        recipe = Recepts(id_user=current_user.id, name=name, category=category, ingredients=ingredients, recept=recept, time=time)

        db.session.add(recipe)
        db.session.commit()

        return redirect(url_for('profile'))

    return render_template('new.html')


@app.route('/profile/<int:id_recipe>/delite')
def delite(id_recipe):

    recipe = Recepts.query.get_or_404(id_recipe)

    db.session.delete(recipe)
    db.session.commit()

    return redirect('/profile')


@app.route('/profile/<int:id_recipe>/change', methods=['GET', 'POST'])
def change(id_recipe):

    recept = Recepts.query.get(id_recipe)

    if request.method == 'POST':

        recept.name = request.form['name']
        recept.category = request.form['category']
        recept.ingredients = request.form['Ingredients']
        recept.recept = request.form['steps']
        recept.time = request.form['time']

        db.session.commit()

        return redirect(url_for('profile'))

    else:
        return render_template('update.html', recept=recept)


@app.route('/profile/<int:id_recipe>/info')
def recipe(id_recipe):

    recept = Recepts.query.get(id_recipe)

    return render_template('recipe.html', recept=recept)


@app.route('/select', methods=['GET', 'POST'])
def recipe_select():

    if request.method == 'POST':

        if 'category' in request.form.keys():

            return redirect(url_for('sort_recipe_by_category', category=request.form['category']))

        if 'name' in request.form.keys():

            return redirect(url_for('search_by_keyword', keyword=request.form['name']))

    else:
        return render_template('select.html')


@app.route('/sortrecipe/<category>')
def sort_recipe_by_category(category):

    all_recipes = Recepts.query.filter_by(id_user=current_user.id).all()

    recipes = search_recipes_by_category(all_recipes, category)

    return render_template('sortresipe.html', recipes=recipes)


@app.route('/search_by_keyword/<keyword>')
def search_by_keyword(keyword):

    all_recipes = Recepts.query.filter_by(id_user=current_user.id).all()

    recipes = search_recipes_by_keyword(all_recipes, keyword)

    return render_template('sortresipe.html', recipes=recipes)

