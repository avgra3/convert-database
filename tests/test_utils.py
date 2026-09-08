from convert_database_tool import parse_dict


def test_parse_user_input():
    expected = {
        "user": "admin",
        "password": "admin123",
        "local_infile": True,
        "port": 1111,
    }
    input = str(expected)
    actual = parse_dict(input=input)
    assert expected == actual


def test_invalid_parse_user_input():
    expected = {}
    inputs = [
        "this is invalid",
        "{hello: world}",
        "{'this is valid': True, 'this is not valid': invalid",
    ]
    for input in inputs:
        actual = parse_dict(input=input)
        assert expected == actual
