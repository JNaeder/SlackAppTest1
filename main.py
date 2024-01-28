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

    if "thread_ts" not in message:
        # Create a new issue in JSM
        thread_ts = message.get("ts")
        user_id = message.get("user")
        user_response: SlackResponse = client.users_info(user=user_id)
        user_info = user_response.data["user"]
        jsm.create_issue(user_info=user_info, message=message)
        client.reactions_add(channel=message.get("channel"),
                             name="brian-party",
                             timestamp=thread_ts)
    else:
        # Add a comment to an existing issue in JSM
        thread_ts = message.get("thread_ts")
        search_results = jsm.search_issue(thread_ts=thread_ts)
        current_issue = search_results.get("issues")[0]
        issue_id = current_issue.get("id")
        jsm.add_comment(issue_id=issue_id, message=message.get("text"))


@api.post("/slack/events")
async def slack_events(request: Request):
    return await handler.handle(request)


@api.post("/slack_response")
async def slack_response(request: Request):
    req_body = await request.json()
    thread_ts = req_body.get("issue").get("fields").get("customfield_10047")
    message = req_body.get("comment").get("body")
    app.client.chat_postMessage(
        channel="#general",
        text=message,
        thread_ts=thread_ts
    )
