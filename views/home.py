import datetime

from . import auth, db, createLoginSession, createCookieSession, isFirebaseCookieSessionValid, verifyFirebaseCookieCreateSession
from flask import Blueprint, redirect, render_template, request, url_for, jsonify, make_response
from flask import current_app as app
from flask_login import logout_user, current_user, login_required
from models.models import UserInfo, UserRole, UserXRole

home = Blueprint('home', __name__, template_folder='templates', static_folder='static')

@home.route('/')
def _index():
    app.logger.debug('** SWING_CMS ** - Index')
    return redirect(url_for('home._welcome'))


@home.route('/welcome/')
def _welcome():
    app.logger.debug('** SWING_CMS ** - Welcome')
    return render_template('welcome.html')


@home.route('/loginuser/', methods=['POST'])
def _loginuser():
    app.logger.debug('** SWING_CMS ** - Login')
    try:
        # Validate if the user has a Valid Session
        if current_user.is_authenticated:
            # If it has a valid Session, verifies the Firebase Cookie Session
            if isFirebaseCookieSessionValid():
                return redirect(url_for('home._index'))
            else:
                # If the Firebase Cookie Session is invalid, user is logged out and Login Process continues
                logout_user()
        else:
            # If user doesnt have a Valid Session, validate if it has a Firebase Cookie Session
            if verifyFirebaseCookieCreateSession():
                return redirect(url_for('home._index'))
        
        # Login Process
        # Retrieve the uid from the JWT idToken
        idToken = request.json['idToken']
        decoded_token = auth.verify_id_token(idToken)
        uid = decoded_token['uid']

        # Search for the user in the DB.
        user = UserInfo.query.filter_by(uid = uid).first()
        if user is None:
            # Retrieve Firebase's User info
            fbUser = auth.get_user(uid)

            # User is not registered on DB. Insert user in DB.
            user = UserInfo()
            user.uid = uid
            user.email = fbUser.email
            user.name = fbUser.display_name
            user.datecreated = datetime.datetime.utcnow()
            user.cmsvuserid = 'CMSV-' + user.name.strip().upper()[0:1] + user.datecreated.strftime('-%y%m%d-%H%M%S')
            
            db.session.add(user)
            db.session.commit()
            app.logger.info('** SWING_CMS ** - LoginUser added: {}'.format(user.id))
        
        # Create User Session
        createLoginSession(user)
        
        # Return Session Cookie
        response = createCookieSession(idToken, 'redirectURL', '/terminosdelservicio/')
        return response

    except Exception as e:
        app.logger.error('** SWING_CMS ** - LoginUser Error: {}'.format(e))
        return jsonify({ 'status': 'error' })


@home.route('/logoutuser/')
@login_required
def _logoutuser():
    app.logger.debug('** SWING_CMS ** - Logout')
    try:
        # First, user is logged out from Flask Login Session
        logout_user()

        response = make_response(redirect(url_for('home._welcome')))

        # Second, user is logged out from Firebase Cookie Session
        # The Firebase Cookie is cleared
        response.set_cookie(app.config['FIREBASE_COOKIE_NAME'], expires=0)

        return response
    except Exception as e:
        app.logger.error('** SWING_CMS ** - LogoutUser Error: {}'.format(e))
        return jsonify({ 'status': 'error' })


@home.route('/chooseavatar/')
@login_required
def _chooseavatar():
    app.logger.debug('** SWING_CMS ** - ChooseAvatar')
    return render_template('acercade.html')


@home.route('/home/')
@login_required
def _home():
    app.logger.debug('** SWING_CMS ** - Home')
    return render_template('acercade.html')


@home.route('/acercade/')
def _acercade():
    app.logger.debug('** SWING_CMS ** - AcercaDe')
    return render_template('acercade.html')


@home.route('/politicaprivacidad/')
def _politicaprivacidad():
    app.logger.debug('** SWING_CMS ** - PoliticaPrivacidad')
    return render_template('politicaprivacidad.html')


@home.route('/terminosdelservicio/')
def _terminosdelservicio():
    app.logger.debug('** SWING_CMS ** - TerminosDelServicio')
    return render_template('terminosdelservicio.html')