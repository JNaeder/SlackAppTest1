import requests
import os
from dotenv import load_dotenv


class JSM:
    def __init__(self):
        load_dotenv()
        self._base_url = "https://jnaeder.atlassian.net/rest/api/3"
        self._username = os.getenv("JSM_USERNAME")
        self._api_key = os.getenv("JSM_API_KEY")
        self._session = requests.Session()
        self._session.auth = (self._username, self._api_key)

    def create_issue(self, user_info, message):
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
                        "name": user_info.get("real_name", "n/a")
                    },
                    "customfield_10047": message.get("ts"),
                    "description": {
                        "content": [
                            {
                                "content": [
                                    {
                                        "text": message.get("text"),
                                        "type": "text"
                                    }
                                ],
                                "type": "paragraph"
                            }
                        ],
                        "type": "doc",
                        "version": 1
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
                "name": "Me!"
            },
        }
        response = self._session.post(url=f"{self._base_url}/issue/"
                                          f"{issue_id}/comment",
                                      headers=headers,
                                      json=payload)
        return response.json()
