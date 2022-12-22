from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class ProfileForm(FlaskForm):
    profileName = StringField('Profile Name')
    pumpCycleLength = StringField('Pump Cycle Length', validators=[DataRequired()])
    lightIntensity = IntegerField('Light Intensity', validators=[DataRequired()])
    overrideActive = BooleanField('Override Active?')
    pumpOverride = BooleanField('Pump Override')
    isActive = BooleanField('Set to active profile')
    submit = SubmitField('Update Profile')