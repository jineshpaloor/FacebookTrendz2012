import os
import urllib, urllib2
#import requests
import json

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


@app.route('/get_photos')
def get_photos():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@app.route('/fb/photos')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    access_token = resp['access_token']

#    current_dir = os.path.realpath(__file__)
    current_dir = os.getcwd()
    filepath = str(current_dir)+'/cache/'+str(access_token)+'.txt'
    if os.path.exists(filepath):
        with open(filepath, 'r') as fp:
            fb_liked_photos = fp.read()
            fb_liked_photos = json.loads(fb_liked_photos)
    else:
        #query to get liked photos of user and his friends
        liked_photos_query = "SELECT pid, caption, aid, owner, link, src_big, src_small, created, modified, like_info FROM photo WHERE created > 1325356200 and aid IN \
            (SELECT aid FROM album WHERE owner IN \
            (SELECT uid2 FROM friend WHERE uid1=me()))ORDER BY like_info.like_count DESC LIMIT 30"

        data = {'q':liked_photos_query, 'access_token':access_token}
        encode_data = urllib.urlencode(data)
        query_url = 'https://graph.facebook.com/fql?%s' % encode_data
        fetch_data = urllib2.urlopen(query_url)
        fb_liked_photos = json.load(fetch_data)
        fetch_data.close()

        with open('cache/'+access_token+'.txt', 'w') as f:
            f.write(json.dumps(fb_liked_photos))

    return render_template('details.html', fb_liked_photos=fb_liked_photos['data'])


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


if __name__ == '__main__':
    app.run(debug=True)
