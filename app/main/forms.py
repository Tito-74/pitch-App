from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required

class PitchForm(FlaskForm):
  title = StringField('Pitch title',validators=[Required()])
  category = SelectField("Choose Category",choices=[('business','business'),('sports','sports'),('politics','politics')])
  pitch_info = TextAreaField('Your Pitch',validators=[Required()])
  submit = SubmitField('Submit')
class CommentForm(FlaskForm):
  comment = TextAreaField('Your Comment',validators=[Required()])
  submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')