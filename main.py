import json
import os
import sys
import requests

from disperse_bonsuly.reason import generate_reason

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

    reason = generate_reason(giving_amount, message, recipients)

    data = json.dumps({
        "reason": reason,
    })
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "User-Agent": "python",
    }
    res = requests.post(BONUS_URL, data=data, headers=headers)
    res.raise_for_status()
    return 0


if __name__ == "__main__":
    sys.exit(main())
