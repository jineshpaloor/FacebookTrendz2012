from flask import Flask, url_for, session, request, render_template
from flask_oauth import OAuth

SECRET_KEY = 'development key'
DEBUG = True
FACEBOOK_APP_ID = '453146034732597'
FACEBOOK_APP_SECRET = '83459d1711daff7eaeb6412f635e5abc'

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

EXTENDED_PERMS = [
    'email',
    'publish_actions',
    'user_about_me',
    'user_actions.music',
    'user_actions.news',
    'user_actions.video',
    'user_activities',
    'user_birthday',
    'user_education_history',
    'user_events',
    'user_games_activity',
    'user_groups',
    'user_hometown,',
    'user_interests',
    'user_likes',
    'user_location',
    'user_notes',
    'user_photos',
    'user_questions',
    'user_relationship_details',
    'user_relationships',
    'user_religion_politics',
    'user_status',
    'user_subscriptions',
    'user_videos',
    'user_website',
    'user_work_history',
    'friends_about_me',
    'friends_actions.music',
    'friends_actions.news',
    'friends_actions.video',
    'friends_activities',
    'friends_birthday',
    'friends_education_history',
    'friends_events',
    'friends_games_activity',
    'friends_groups',
    'friends_hometown',
    'friends_interests',
    'friends_likes',
    'friends_location',
    'friends_notes',
    'friends_photos',
    'friends_questions',
    'friends_relationship_details',
    'friends_relationships',
    'friends_religion_politics',
    'friends_status',
    'friends_subscriptions',
    'friends_videos',
    'friends_website',
    'friends_work_history',
    'ads_management',
    'create_event',
    'create_note',
    'export_stream',
    'friends_online_presence',
    'manage_friendlists',
    'manage_notifications',
    'manage_pages',
    'offline_access',
    'publish_checkins',
    'publish_stream',
    'read_friendlists',
    'read_insights',
    'read_mailbox',
    'read_page_mailboxes',
    'read_requests',
    'read_stream',
    'rsvp_event',
    'share_item',
    'sms',
    'status_update',
    'user_online_presence',
    'video_upload',
    'xmpp_login']

scope=','.join(EXTENDED_PERMS)

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': scope},
)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/get_accesstoken')
def get_access_token():
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
    print 'token   :',session['oauth_token']
    me = facebook.get('/me')
    return 'Logged in as id=%s name=%s redirect=%s' % \
        (me.data['id'], me.data['name'], request.args.get('next'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')




if __name__ == '__main__':
    app.run(debug=True)
