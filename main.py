import json
import os
import sys
import requests
import random

BASE_URL = "https://bonus.ly/api/v1"
BONUS_URL = f"{BASE_URL}/bonuses"
MY_URL = f"{BASE_URL}/users/me"


def _load_recipients():
    recipients = os.getenv("RECIPIENTS")
    return json.loads(recipients)


def _get_giving_amount(access_token: str):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "User-Agent": "python",
    }
    res = requests.get(MY_URL, headers=headers)
    res.raise_for_status()
    return int(res.json()["result"]["giving_balance"])


def main() -> int:
    access_token = os.getenv("ACCESS_TOKEN")
    message = os.getenv("BONUSLY_MESSAGE")
    recipients = _load_recipients()
    giving_amount = _get_giving_amount(access_token)
    amount_per_member = giving_amount // len(recipients)

    recipients = _load_recipients()
    random.shuffle(recipients)

    if amount_per_member == 0 and giving_amount > 0:
        # more people than points to give
        recipients = recipients[:giving_amount]
        # give one of the remaining points to everyone!
        amount_per_member = 1

    for recipient in recipients:
        reason =f"+{amount_per_member} @{recipient} {message}"
        print(reason)
        data = json.dumps({
            "reason": reason,
        })
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "User-Agent": "python",
        }
        res = requests.post(BONUS_URL, data=data, headers=headers)
        if res.status_code != 200:
            print("Error attempting to give bonusly: [{}]: {}".format(res.status_code, res.reason))

    return 0


if __name__ == "__main__":
    sys.exit(main())
