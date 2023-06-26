from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import ScoreForm, WeightLossForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    score = db.Column(db.Integer, default=0, nullable=False)
    weight_loss = db.Column(db.Float, default=0.0, nullable=False)
    button_states = db.Column(db.String(75), default='0'*75, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ScoreForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if not user:
            user = User(name=form.name.data)
            db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    users = User.query.all()
    weight_forms = {user.id: WeightLossForm() for user in users}
    return render_template('index.html', form=form, users=users, weight_forms=weight_forms)

@app.route('/update_score/<int:user_id>/<int:button_id>')
def update_score(user_id, button_id):
    user = User.query.get(user_id)
    button_states = list(user.button_states)
    button_states[button_id - 1] = '1' if button_states[button_id - 1] == '0' else '0'
    user.button_states = ''.join(button_states)
    user.score = user.button_states.count('1')
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_weight/<int:user_id>', methods=['GET', 'POST'])
def update_weight(user_id):
    form = WeightLossForm()
    user = User.query.get(user_id)
    if form.validate_on_submit():
        if user:
            user.weight_loss = form.weight_loss.data
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', form=form, users=User.query.all())

if __name__ == '__main__':
    app.run(debug=True)
