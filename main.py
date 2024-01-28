import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_sdk.web import SlackResponse
from jsm_functions import JSM
from fastapi import FastAPI, Request
from slack_bolt.adapter.fastapi import SlackRequestHandler

load_dotenv()
jsm = JSM()

api = FastAPI()

app = App(token=os.getenv("SLACK_BOT_TOKEN"),
          signing_secret=os.getenv("SLACK_SIGNING_SECRET"))

handler = SlackRequestHandler(app)


@app.message()
def say_something(message, say, client):
    thread_ts = message.get("ts")
    user_id = message.get("user")
    user_response: SlackResponse = client.users_info(user=user_id)
    user_info = user_response.data["user"]
    new_issue = jsm.create_issue(user_info=user_info, message=message)
    new_text = (f"Thank you for your message. An issue has been created for "
                f"you: {new_issue.get('self')}")
    say(text=new_text, thread_ts=thread_ts)


@api.post("/slack/events")
async def slack_events(request: Request):
    return await handler.handle(request)


@api.get("/")
def test():
    return {"message": "Hello world!"}


@api.post("/slack_response")
async def slack_response(request: Request):
    req_body = await request.json()
    print(req_body)
    app.client.chat_postMessage(channel="#general", text="Hello world!")
