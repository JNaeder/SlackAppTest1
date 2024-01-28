block_1 = [
    {
        "type": "section",
        "text": {
            "type": "plain_text",
            "text": "Thanks for messaging Hi! Tech! Someone will be right "
                    "with you.",
            "emoji": True
        }
    },
    {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Resources",
                    "emoji": True
                },
                "value": "click_me_123",
                "action_id": "test_button"
            }
        ]
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Test block with users select"
        },
        "accessory": {
            "type": "users_select",
            "placeholder": {
                "type": "plain_text",
                "text": "Select a user",
                "emoji": True
            },
            "action_id": "users_select-action"
        }
    }
]
