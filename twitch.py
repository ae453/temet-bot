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

class webhook:
    def __init__(self, oauth_token: str) -> None:
        self.headers: dict = {
            "Authorization": oauth_token,
            "Client-Id": client_id,
            "Content-Type": "application/json"
        }
    
    async def post(self) -> None:
        body: dict = {
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

        sub_r = requests.post('https://api.twitch.tv/helix/eventsub/subscriptions', headers=self.headers, data=dumps(body))
        sub_r_data = sub_r.json()

        try:
            if sub_r_data["status"] in [400, 401]:
                print(f'Error Received from Server: {sub_r_data["error"]}. {sub_r_data["message"]}')
        except KeyError as e:
            if not sub_r_data:
                print(f"No Response Received from Server. {e}")

        print(f"Response Received from Server: \n\n{dumps(sub_r_data, sort_keys=True, indent=4)}")


    async def get(self):
        r = requests.get('https://api.twitch.tv/helix/eventsub/subscriptions', headers=self.headers)
        print(dumps(r.json(), sort_keys=True, indent=4))


    async def delete(self):
        del_user_input = input("\nWebhook ID: ")
        r = requests.delete(f'https://api.twitch.tv/helix/eventsub/subscriptions?id={del_user_input}', headers=self.headers)

        try:
            r_data = r.json()
            print(f"Server Responded with Status `{r_data["status"]}`: `{r_data["error"]}`")
        except requests.exceptions.JSONDecodeError:
            print(r)

if __name__ == "__main__":
    while True:
        print("\n\nDelete - Delete a EventSub Subscription (Requires Webhook ID)\nPost - Subscribe to an EventSub Subscription\nGet - Get all Current EventSub Subscriptions")
        user_input = input("[D]elete, [P]ost, [G]et? ")
        
        if user_input.lower() in ["d", "p", "g", "delete", "post", "get"]: break
        
         # Request oAuth Token
    print("\nGetting oAuth Token...")
    r = requests.post('https://id.twitch.tv/oauth2/token', {'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'client_credentials'})
    oauth_token = f"Bearer {r.json()['access_token']}"

    webhook = webhook(oauth_token=oauth_token)
    match user_input.lower():
        case "d" | "delete":
            asyncio.run(webhook.delete())
        case "p" | "post":
            asyncio.run(webhook.post())
        case "g" | "get":
            asyncio.run(webhook.get())