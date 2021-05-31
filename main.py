import json
import os
import sys
import requests


def main() -> int:
    access_token = os.getenv("ACCESS_TOKEN")
    url = "https://bonus.ly/api/v1/bonuses"
    data = json.dumps({
        "reason": "+1 @<user> bonusly api test!"
    })
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "User-Agent": "python",
    }
    res = requests.post(url, data=data, headers=headers)
    res.raise_for_status()
    j = res.json()
    print(json.dumps(j, indent=4))
    return 0


if __name__ == "__main__":
    sys.exit(main())
