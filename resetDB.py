from app_package import db
from app_package import models

db.drop_all()

db.create_all()

defaultSettings = models.Settings(pumpCycleLength = 15, lightIntensity = 100)
defaultProfile = models.Profile(name = "Default Profile", settings = defaultSettings)

db.session.add(defaultSettings)
db.session.add(defaultProfile)

profileOneSettings = models.Settings(pumpCycleLength = 20, lightIntensity = 50)
profileOne = models.Profile(name = "Profile One", settings = profileOneSettings)

db.session.add(profileOneSettings)
db.session.add(profileOne)

lettuceProfileSettings = models.Settings(pumpCycleLength = 5, lightIntensity = 75, overrideActive = True)
lettuceProfile = models.Profile(name = "Lettuce", settings = lettuceProfileSettings)

db.session.add(lettuceProfileSettings)
db.session.add(lettuceProfile)

config = models.Config(id = 1, active_profile = defaultProfile)

db.session.add(config)


db.session.commit()