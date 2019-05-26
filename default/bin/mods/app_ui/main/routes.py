import os

from flask import render_template, request, Blueprint, redirect, url_for
from flask_login import current_user
from core.utils.app_utils import get_theme
# rom flask_breadcrumbs import Breadcrumbs, register_breadcrumb
from mods.app_ui.models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
#@register_breadcrumb(main, '.', 'Home')
def home():
    return render_template('home.html', title='Home', theme=get_theme(type='path'))


@main.route("/blogs")
def blog():
    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
        return render_template('blogs.html', posts=posts, title='Blogs', theme=get_theme(type='path'))
    else:
        return redirect(url_for('users.login'))


@main.route("/datatables")
def datatables():
    if current_user.is_authenticated:
        return render_template('datatable.html', title='Datatables', theme=get_theme(type='path'))
    else:
        return redirect(url_for('users.login'))


@main.route("/theme")
def themes():
    os.environ['THEME'] = request.args.get('theme')
    return render_template('theme.html', title='Theme', theme='themes/' + request.args.get('theme'))


@main.route("/about")
def about():
    return render_template('about.html', title='About', theme=get_theme(type='path'))



