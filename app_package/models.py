from app_package import db
from datetime import datetime

class Settings(db.Model):
    __tablename__ = 'settings'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    # time in minutes
    pumpCycleLength = db.Column(db.Integer(), default=15, nullable=False)
    # brightness 0-100
    lightIntensity = db.Column(db.Integer(), default=50, nullable=False)
    overrideActive = db.Column(db.Boolean(), default=False)
    pumpOverride = db.Column(db.Boolean(), default=False)

    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'timestamp': self.timestamp.strftime("%x %X"),
            'pumpCycleLength': self.pumpCycleLength,
            'lightIntensity': self.lightIntensity,
            'overrideActive': self.overrideActive,
            'pumpOverride': self.pumpOverride,
        }

    def serializeNamed(self):
        """Return object data in easily serializable format"""
        overrideActive = "True" if self.overrideActive else "False"
        pumpOverride = "On" if self.pumpOverride else "Off"
        return {
            'Timestamp': self.timestamp.strftime("%x %X"),
            'Pump Cycle Duration': str(self.pumpCycleLength) + " minutes",
            'Light Intensity': str(self.lightIntensity) + "%",
            'Override Active': overrideActive,
            'Pump Override': pumpOverride
        }

class Profile (db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    displayName  = db.Column(db.String(), nullable=False)
    settings_id = db.Column(db.Integer(), db.ForeignKey('settings.id'))
    settings = db.relationship("Settings", backref=db.backref("profile", uselist=False))


    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'id': self.id,
           'name': self.name
       }

class Config (db.Model):
    __tablename__ = 'config'

    id = db.Column(db.Integer(), primary_key=True)
    active_profile_id = db.Column(db.Integer(), db.ForeignKey('profile.id'))
    active_profile = db.relationship("Profile", backref=db.backref("config", uselist=False))


    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'id': self.id,
           'name': self.name
       }

















class Reading(db.Model):
    __tablename__ = 'reading'

    timestamp = db.Column(db.DateTime, default=datetime.utcnow, primary_key=True)
    temperature = db.Column(db.Numeric(precision=2))
    humidity = db.Column(db.Integer())


    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'timestamp': self.timestamp.strftime("%x %X"),
           'temperature': float(self.temperature),
           'humidity': self.humidity,
       }

