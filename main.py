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

app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET")
)

handler = SlackRequestHandler(app)


@app.message()
def say_something(message, client):
    if "thread_ts" not in message:
        # Create a new issue in JSM

        thread_ts = message.get("ts")

        user_id = message.get("user")
        user_response: SlackResponse = client.users_info(user=user_id)
        user_info = user_response.data["user"]

        channel_id = message.get("channel")
        channel_response: SlackResponse = client.conversations_info(
            channel=channel_id)
        channel_info = channel_response.data["channel"]

        team_id = message.get("team")
        team_response: SlackResponse = client.team_info(team=team_id)
        team_info = team_response.data["team"]

        new_ticket = jsm.create_issue(
            user_info=user_info,
            channel_info=channel_info,
            team_info=team_info,
            message=message
        )

        if "errorMessages" in new_ticket:
            emoji = "x"
        else:
            emoji = "envelope"

        client.reactions_add(channel=message.get("channel"),
                             name=emoji,
                             timestamp=thread_ts)
    else:
        # Add a comment to an existing issue in JSM
        thread_ts = message.get("thread_ts")
        search_results = jsm.search_issue(thread_ts=thread_ts)
        current_issue = search_results.get("issues")[0]
        issue_id = current_issue.get("id")
        comment_response = jsm.add_comment(issue_id=issue_id,
                                          message=message.get("text"))

        print(comment_response)
@api.post("/slack/events")
async def slack_events(request: Request):
    return await handler.handle(request)


@api.post("/slack_response")
async def slack_response(request: Request):
    req_body = await request.json()
    thread_ts = req_body.get("issue").get("fields").get("customfield_10047")
    message = req_body.get("comment").get("body") + (f" "
                                                     f"~{req_body.get('comment').get('author').get('displayName')}")
    message_response = app.client.chat_postMessage(
        channel="#general",
        text=message,
        thread_ts=thread_ts
    )
