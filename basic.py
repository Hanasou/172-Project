import datetime
import os
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = '1'
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = '1'
from project import app, db, file_storage, my_bucket, s3
from flask import render_template, request, Response, session, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from project.forms import SignUpForm, LoginForm
from project.models import User, File

class Card():
    
    def __init__(self, title, uploader = ''):
        self.title = title
        self.uploader = uploader

@app.route('/login', methods = ['GET', 'POST'])
def login():
    pass
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('index')
        
        return redirect(next)
    
    
    return render_template('login.html', form = form)

"""
@app.route('/login/google', methods = ['GET', 'POST'])
def google_login():
    if not google.authorized:
        return render_template(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    email=resp.json()["email"]

    return render_template("index.html",email=email)
"""

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        user = User(username = form.username.data, password = form.password.data, first_name = form.first_name.data, last_name = form.last_name.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html', form = form)

@app.route('/download', methods=['POST'])
def download_file():
    key = request.form['key']
    file_obj = my_bucket.Object(key).get()

    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']

        my_bucket.Object(file.filename).put(Body = file)

        now = datetime.datetime.now()
        f = '%Y-%m-%d %H:%M:%S'
        now = now.strftime(f)
        add_file = File(item = file.filename, user_fn = current_user.first_name, user_ln = current_user.last_name, upload_date = now, update_date = now, 
            description = '', user_id = current_user.id)
        db.session.add(add_file)
        db.session.commit()

        return redirect(url_for('index'))
    except:

        return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update_file():
    pass

@app.route('/delete', methods=['POST'])
def delete_file():
    key = request.form['key']
    my_bucket.Object(key).delete()
    delete_file = File.query.filter_by(item = key)
    db.session.delete(delete_file)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/')
def index():
    card_list = []
    if current_user.is_authenticated:
        if current_user.admin:
            for item in File.query.all():
                card_list.append(Card(item.item, item.user_fn + ' ' + item.user_ln))
        else:
            for item in File.query.filter_by(user_id = current_user.id):
                card_list.append(Card(item.item))

    return render_template('index.html', card_list = card_list)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
    

