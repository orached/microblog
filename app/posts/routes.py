from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _
from guess_language import guess_language
from app import db
from app.posts.forms import PostForm, CommentForm
from app.models import Post, Comment, Category
from app.translate import translate
from app.posts import bp


@bp.route('/managepost', methods=['GET', 'POST'])
@login_required
def managepost():
    category_list=[(g.id, g.title) for g in Category.query.all()]
    form = PostForm()
    form.category.choices = category_list
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(title=form.title.data, body_html=form.post.data, author=current_user,
                    language=language, category_id=form.category.data)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('posts.managepost'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('posts.managepost', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('posts.managepost', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('manage_post.html', title=_('Posts'), form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/translate', methods=['POST'])
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['dest_language'])})

@bp.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        language = guess_language(form.comment.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        comment = Comment(body=form.comment.data, post=post, 
                        author=current_user, language=language)
        db.session.add(comment)
        db.session.commit()
        flash(_('Your comment has been published.'))
        return redirect(url_for('posts.post', id=post.id))
    comments = post.comments.order_by(Comment.timestamp.asc())
    return render_template('post.html', post=post, form=form, comments=comments)


@bp.route('/editpost/<int:id>', methods=['GET', 'POST'])
@login_required
def editpost(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        abort(403)
    category_list=[(g.id, g.title) for g in Category.query.all()]
    form = PostForm()
    form.category.choices = category_list
    if form.validate_on_submit():
        post.title = form.title.data
        post.category_id = form.category.data
        post.body_html = form.post.data
        db.session.add(post)
        db.session.commit()
        flash(_('The post has been updated.'))
        return redirect(url_for('posts.post', id=post.id))
    form.title.data = post.title
    form.post.data = post.body_html
    return render_template('edit_post.html', form=form)


@bp.route('/category/<int:id>')
def category(id):
    category = Category.query.get_or_404(id)
    posts = category.posts.order_by(Post.id)
    return render_template('category.html', category=category, posts=posts)