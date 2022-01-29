from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class ProfileForm(FlaskForm):
    pumpCycleLength = StringField('Pump Cycle Length', validators=[DataRequired()])
    lightIntensity = IntegerField('Light Intensity', validators=[DataRequired()])
    overrideActive = BooleanField('Override Active?', validators=[DataRequired()])
    pumpOverride = BooleanField('Pump Override', validators=[DataRequired()])
    submit = SubmitField('Update Profile')