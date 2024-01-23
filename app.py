from flask import Flask, render_template, redirect, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from models import connect_db, db, User, Feedback
from forms import registerUser, loginForm, feedbackForm, deleteForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask_feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "super-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

"note: type createdb flask_feedback in terminal. run app.py in ipython," 
"then db.create_all()"
"to check table: go to sql, type \c flask_feedback, \dt users; \d+ users to see the schema"

connect_db(app)
with app.app_context():
    db.create_all()

@app.route('/')
def root():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = registerUser()
    if form.validate_on_submit():
            username=form.username.data
            password=form.password.data
            email=form.email.data
            first_name=form.first_name.data
            last_name=form.last_name.data
        
            user = User.register(username, password, first_name, last_name, email)

            db.session.commit()
            session['username'] = user.username

            flash ("User created successfully")
            return redirect(url_for('show_user'))
    else:
        return render_template('register.html', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        username = form.username.data 
        password = form.password.data

        user = User.authenticate(username, password) 
        if user:
            session['username'] = user.username
            return redirect("/secret")      
        else:
            form.username.errors = ["Incorrect username or password"]
            return render_template("login.html", form = form)
        
@app.route("/logout")
def logout():
    session.pop("username")

    return redirect("/")

@app.route('/users/<username>')
def show_user(username):

    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    user = User.query.get(username)
    form = deleteForm()
    
    return render_template("users/show_user.html", user = user, form = form)



@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """Remove user and redirect to login."""
    
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback_for_user(username):
   if "username" not in session or username != session['username']:
        raise Unauthorized()
   
   form = feedbackForm()

   if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()

        flash("Feedback added successfully.", "success")
        return redirect(url_for('user_profile', username=username))
   else:
          return render_template('new_feedback.html', form=form, username=username)


@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = feedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("/feedback/edit_feedback.html", form=form, feedback=feedback)

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = deleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")


if __name__ == '__main__':
    app.run(debug=True)