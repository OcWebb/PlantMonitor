from flask import render_template, url_for, jsonify, request, abort, redirect
import json

from app_package import app, db
from app_package.models import Reading, Settings, Profile, Config
from app_package.forms import ProfileForm


@app.route('/', methods= ['GET', 'POST'])
def home():
    config = Config.query.filter_by(id = 1).first()
    ActiveProfileName = config.active_profile.displayName

    return redirect(url_for('getProfile', id = config.active_profile.id))

@app.route('/profiles', methods= ['GET', 'POST'])
def profiles():
    config = Config.query.filter_by(id = 1).first()
    ActiveProfileName = config.active_profile.displayName

    resp = getAllProfiles()
    allProfilesNames = json.loads(resp.data)

    return render_template('profiles.html', profileNames = allProfilesNames, activeProfile=ActiveProfileName)

@app.route('/profile/new', methods= ['GET', 'POST'])
def newProfile():
    newSettings = Settings()
    newProfile = Profile(displayName="NEW PROFILE", settings=newSettings)
    db.session.add(newProfile)
    db.session.add(newSettings)
    db.session.commit()

    return redirect(url_for('getProfile', id=newProfile.id))


@app.route('/profile/<int:id>', methods= ['GET', 'POST'])
def getProfile(id):
    allProfilesResponse = getAllProfiles()
    allProfiles = Profile.query.order_by(Profile.displayName)

    config = Config.query.filter_by(id = 1).first()
    activeProfile = config.active_profile.displayName

    profile = Profile.query.filter_by(id = id).first()
    profileSettings = profile.settings
    form = ProfileForm()
    
    if form.validate_on_submit():
        form.populate_obj(profile.settings)

        setToActive = form.isActive.data
        newProfileName = form.profileName.data
        print(newProfileName)

        if (newProfileName):
            profile.displayName = newProfileName
        
        if (setToActive):
            config.active_profile = profile
            config.active_profile_id = profile.displayName

        db.session.commit()

        return redirect(url_for('getProfile', id=profile.id))
    
    return render_template('home.html', id = profile.id, profileName=profile.displayName, currentSettings=profileSettings, allProfiles=allProfiles, form=form, activeProfile = activeProfile)


@app.route('/api/<int:id>/settings', methods= ['GET'])
def getProfileSettings(id):
    """
        Gets settings for profile by name
    """

    try:
        profile = Profile.query.filter_by(id = id).first()
        return jsonify(profile.settings.serialize())
    except Exception:
        return jsonify({ 'error': 'failed to fetch profile, ID: ' + str(id) }), 400


@app.route('/api/<int:id>/settings', methods= ['PUT'])
def updateProfileSettings(id):
    profile = Profile.query.filter_by(id = id).first()
    currentSettings = profile.settings
    
    if not request.json:
        abort(400)

    if 'pumpCycleLength' in request.json:
        currentSettings.pumpCycleLength = request.json['pumpCycleLength']

    if 'lightIntensity' in request.json:
        currentSettings.lightIntensity = request.json['lightIntensity']

    if 'overrideActive' in request.json:
        currentSettings.overrideActive = request.json['overrideActive']
    
    if 'pumpOverride' in request.json:
        currentSettings.pumpOverride = request.json['pumpOverride']

    db.session.commit()

    return jsonify({'updatedSettings': currentSettings.serialize()}), 201


@app.route('/api/profiles', methods= ['GET'])
def getAllProfiles():
    """
        Gets all profiles
    """

    profiles = Profile.query.order_by(Profile.displayName)
    
    if profiles is not None:
        profileNames = [profile.displayName for profile in profiles]
        return jsonify(profileNames)
    else:
        return jsonify({ 'error': 'failed to fetch profile list ' }), 400






@app.route('/table', methods=['GET'])
def table():
    """
        Querys database and displays metrics collected 
        in a tabular format
    """
    # readings = Reading.query.all()
    readings = Reading.query.order_by(db.desc(Reading.timestamp)).limit(1000).all()

    return render_template('table.html', readings=readings)

@app.route('/graphs', methods=['GET'])
def index():
    """
        Querys database and displays metrics collected
    """
    readings = Reading.query.order_by(db.desc(Reading.timestamp)).all()
    temperatures = [float(x.temperature) for x in readings]
    humidity = [float(x.humidity) for x in readings]
    dates = [x.timestamp.strftime("%x %X") for x in readings]

    # print(dates)
    temp = zip(temperatures, dates)
    
    return render_template('graphs.html', readings=readings, temperatures=temperatures, dates=dates, temp=temp, humidity=humidity)
