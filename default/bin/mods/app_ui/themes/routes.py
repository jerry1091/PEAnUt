from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, current_app)
from flask_login import current_user, login_required
from core import db
from mods.app_ui.models import Post
from mods.app_ui.themes.forms import PostForm

themes = Blueprint('themes', __name__)


@themes.route("/theme/new", methods=['GET', 'POST'])
@login_required
def new_theme():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your theme has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('/create_theme.html', title='New Theme',
                           form=form, legend='New Theme', theme=current_app.config['THEME'])


@themes.route("/theme/<int:post_id>")
def post(post_id):
    theme = Post.query.get_or_404(post_id)
    return render_template('/theme.html', title=theme.title, theme=current_app.config['THEME'])


@themes.route("/theme/<int:theme_id>/update", methods=['GET', 'POST'])
@login_required
def update_theme(theme_id):
    theme = Post.query.get_or_404(theme_id)
    if theme.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        theme.title = form.title.data
        theme.content = form.content.data
        db.session.commit()
        flash('Your theme has been updated!', 'success')
        return redirect(url_for('themes.post', theme_id=theme.id))
    elif request.method == 'GET':
        form.title.data = theme.title
        form.content.data = theme.content
    return render_template('/create_theme.html', title='Update Theme',
                           form=form, legend='Update Theme', theme=current_app.config['THEME'])


@themes.route("/theme/<int:theme_id>/delete", methods=['POST'])
@login_required
def delete_theme(theme_id):
    theme = Post.query.get_or_404(theme_id)
    if theme.author != current_user:
        abort(403)
    db.session.delete(theme)
    db.session.commit()
    flash('Your theme has been deleted!', 'success')
    return redirect(url_for('main.home'))
