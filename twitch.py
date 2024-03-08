import asyncio
from json import dumps

import requests
from dotenv import dotenv_values

 # Set Variables
config = dotenv_values(".env")

client_id = config["TWITCH_CLIENT_ID"]
client_secret = config["TWITCH_CLIENT_SECRET"]
broadcaster_name = config["TWITCH_BROADCASTER_NAME"]
broadcaster_id = config["TWITCH_BROADCASTER_ID"]
callback_url = config["TWITCH_CALLBACK_URL"]
webhook_secret = config["TWITCH_WEBHOOK_SECRET"]


 # Make Request, Return oAuth Keys
async def get_oauth() -> dict:
    body = {
        'client_id': client_id,
        'client_secret': client_secret,
        "grant_type": 'client_credentials'
    }
     # Request oAuth Token
    r = requests.post('https://id.twitch.tv/oauth2/token', body)
    return r.json()


async def main() -> None:
    print("Getting oAuth Token...")
    keys = await get_oauth()
    oauth_token = f"Bearer {keys['access_token']}"
        
    sub_headers: dict = {
        "Authorization": oauth_token,
        "Client-Id": client_id,
        "Content-Type": "application/json"
    }
    
    sub_body: dict = {
        "type": "stream.online",
        "version": "1",
        "condition": {
            "broadcaster_user_id": broadcaster_id
        },
        "transport": {
            "method": "webhook",
            "callback": callback_url,
            "secret": webhook_secret
        }
    }
    
    print("Subscribing to EventSub Notifications...")
    
    sub_r = requests.post('https://api.twitch.tv/helix/eventsub/subscriptions', headers=sub_headers, data=dumps(sub_body))
    sub_r_data = sub_r.json()
    
    if sub_r_data["status"] in [400, 401]:
        print(f'Error Received from Server: {sub_r_data["error"]}. {sub_r_data["message"]}')
    
    print(f"\n\n{sub_r_data}")
    
if __name__ == "__main__":
     # Runs all Functions then Subscribes to Websocket
    asyncio.run(main())
