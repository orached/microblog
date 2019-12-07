from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _
from guess_language import guess_language
from app import db
from app.posts.forms import PostForm
from app.models import Post
from app.translate import translate
from app.posts import bp


@bp.route('/editpost', methods=['GET', 'POST'])
@login_required
def editpost():
    form = PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body=form.post.data, author=current_user,
                    language=language)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('posts.editpost'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('posts.editpost', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('posts.editpost', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('edit_post.html', title=_('Posts'), form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/translate', methods=['POST'])
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['dest_language'])})