from lib.oauth_dancer import OauthDancer
from lib.strava_client import StravaClient

dancer = OauthDancer()
dancer.dance()

client = StravaClient(dancer.token)
client.refresh()
