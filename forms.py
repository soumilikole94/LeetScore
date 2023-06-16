from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired

class ScoreForm(FlaskForm):
    name = StringField('Add New User', validators=[DataRequired()])
    submit = SubmitField('Add User')

class WeightLossForm(FlaskForm):
    weight_loss = FloatField('Weight Lost in lbs since June 15', validators=[DataRequired()])
    submit = SubmitField('Update')
