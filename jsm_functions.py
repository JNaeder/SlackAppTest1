import requests
import os
from dotenv import load_dotenv


class JSM:
    def __init__(self):
        load_dotenv()
        self._base_url = "https://jnaeder.atlassian.net/rest/api/3"
        self._username = os.getenv("JSM_USERNAME")
        self._customer_username = os.getenv("JSM_CUSTOMER_USERNAME")
        self._api_key = os.getenv("JSM_API_KEY")
        self._session = requests.Session()
        self._session.auth = (self._username, self._api_key)

    def set_session_auth(self, username):
        self._session.auth = (username, self._api_key)

    def create_issue(self, user_info, channel_info, team_info, message):
        self.set_session_auth(self._username)
        slack_info_header = f"{user_info['real_name']}| #{channel_info['name']} | {team_info['name']}"

        headers = {
            "Accept": "application/json",
        }
        payload = {
                "fields": {
                    "project": {
                        "id": 10003
                    },
                    "issuetype": {
                        "id": "10021",
                    },
                    "reporter": {
                        "id":
                            "qm:1c4e7d06-71f1-4f27-8b94-019d840ac81d:4dcf71bd-3b9e-43dc-b1c2-f2ac6b5cc907",
                    },
                    "customfield_10047": message.get("ts"),
                    "description": {
                        "type": "doc",
                        "version": 1,
                        "content": [
                            {
                                "type": "heading",
                                "attrs": {
                                    "level": 1
                                },
                                "content": [
                                    {
                                        "text": slack_info_header,
                                        "type": "text"
                                    }
                                ]
                            },
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "text": message.get("text"),
                                        "type": "text"
                                    }
                                ]
                            }
                        ]
                    },
                    "summary": f"{user_info.get('real_name')} Needs Help"
                },
                "update": {}
            }

        response = self._session.post(url=f"{self._base_url}/issue",
                                      headers=headers,
                                      json=payload)
        return response.json()

    def search_issue(self, thread_ts):
        self.set_session_auth(self._username)
        headers = {
            "Accept": "application/json",
        }
        payload = {
            "jql": f"thread_ts ~ {thread_ts}"
        }
        response = self._session.post(url=f"{self._base_url}/search",
                                      headers=headers,
                                      json=payload)
        return response.json()

    def add_comment(self, issue_id, message):
        self.set_session_auth(self._customer_username)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {
            "body": {
                "content": [
                    {
                        "content": [
                            {
                                "text": message,
                                "type": "text"
                            }
                        ],
                        "type": "paragraph"
                    }
                ],
                "type": "doc",
                "version": 1
            },
            "reporter": {
                "id":
                    "qm:1c4e7d06-71f1-4f27-8b94-019d840ac81d:4dcf71bd-3b9e-43dc-b1c2-f2ac6b5cc907",
            },
        }
        response = self._session.post(url=f"{self._base_url}/issue/"
                                          f"{issue_id}/comment",
                                      headers=headers,
                                      json=payload)
        return response.json()
