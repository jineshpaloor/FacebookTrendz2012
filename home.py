import urllib

#from flask import Flask, , redirect, request
from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauth import OAuth

REDIRECT_URI = 'http://127.0.0.1:5000/accesstoken'
SECRET_KEY = 'development key'
DEBUG = True
FACEBOOK_APP_ID = '453146034732597'
FACEBOOK_APP_SECRET = '83459d1711daff7eaeb6412f635e5abc'

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()


facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/accesstoken')
def use_access_token():
    print 'got response from facebook ::'
    print 'args  :',request.args.__dict__
    return render_template('details.html')


@app.route('/get_accesstoken')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    return 'Logged in as id=%s name=%s redirect=%s' % \
        (me.data['id'], me.data['name'], request.args.get('next'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


@app.route('/get_accesstoken_old')
def get_access_token():

    # Get this value from your Facebook application's settings

    # You could customize which extended permissions are being requested on the login
    # page or by editing the list below. By default, all the ones that make sense for
    # read access as described on http://developers.facebook.com/docs/authentication/
    # are included. (And yes, it would be probably be ridiculous to request this much
    # access if you wanted to launch a successful production application.)

    EXTENDED_PERMS = [
        'user_about_me',
        'friends_about_me',
        'user_activities',
        'friends_activities',
        'user_birthday',
        'friends_birthday',
        'user_education_history',
        'friends_education_history',
        'user_events',
        'friends_events',
        'user_groups',
        'friends_groups',
        'user_hometown',
        'friends_hometown',
        'user_interests',
        'friends_interests',
        'user_likes',
        'friends_likes',
        'user_location',
        'friends_location',
        'user_notes',
        'friends_notes',
        'user_online_presence',
        'friends_online_presence',
        'user_photo_video_tags',
        'friends_photo_video_tags',
        'user_photos',
        'friends_photos',
        'user_relationships',
        'friends_relationships',
        'user_religion_politics',
        'friends_religion_politics',
        'user_status',
        'friends_status',
        'user_videos',
        'friends_videos',
        'user_website',
        'friends_website',
        'user_work_history',
        'friends_work_history',
        'email',
        'read_friendlists',
        'read_requests',
        'read_stream',
        'user_checkins',
        'friends_checkins',
        ]

    args = dict(client_id=FACEBOOK_APP_ID, redirect_uri=REDIRECT_URI,
                scope=','.join(EXTENDED_PERMS), type='user_agent', display='popup')


    return redirect('https://graph.facebook.com/oauth/authorize?'
                    + urllib.urlencode(args))


if __name__ == '__main__':
    app.run(debug=True)
