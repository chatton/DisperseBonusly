from typing import List


def generate_reason(total_points: int, message: str, recipients: List[str]) -> str:
    """
    :param total_points: the amount of points that should be distributed
    :param message: the message used when awarding points
    :param recipients: a list of email addressed for users who should receive points
    :return: the reason string that can be used with the bonusly api
    """
    if total_points <= 0:
        raise ValueError("Must enter positive number of points!")

    points_per_member = total_points // len(recipients)

    # give as many people points as possible
    if points_per_member == 0 and total_points > 0:
        recipients = recipients[:total_points]
        points_per_member = 1

    recipients_str = ' @'.join(recipients)
    return f"+{points_per_member} @{recipients_str} {message}"
