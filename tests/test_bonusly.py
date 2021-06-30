import pytest
from disperse_bonsuly.reason import generate_reason


def test_generate_reason_with_a_single_recipient_gets_all_points():
    reason = generate_reason(100, "here you go!", ["user0"])
    assert reason == "+100 @user0 here you go!"


def test_generate_reason_with_a_multiple_recipients_have_points_divided_evenly():
    reason = generate_reason(300, "here you go!", ["user0", "user1", "user2"])
    assert reason == "+100 @user0 @user1 @user2 here you go!"


def test_uneven_points_are_split_correctly():
    reason = generate_reason(350, "a different message!", ["user0", "user1", "user2", "user4"])
    assert reason == "+87 @user0 @user1 @user2 @user4 a different message!"


def test_points_are_fewer_than_recipients_give_out_as_much_as_possible():
    reason = generate_reason(4, "here you go!", ["user0", "user1", "user2", "user3", "user4", "user5"])
    assert reason == "+1 @user0 @user1 @user2 @user3 here you go!"


def test_negative_points_raises_exception():
    with pytest.raises(ValueError):
        generate_reason(-100, "bad points!", ["user0"])


def test_zero_points_raises_exception():
    with pytest.raises(ValueError):
        generate_reason(0, "bad points!", ["user0"])
