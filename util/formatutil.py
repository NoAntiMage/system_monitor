

# ParamType text string, width int
# returnType string
def pretty_format(text, width=22):
    assert ":" in text
    s = text.split(":")
    assert len(s) == 2
    remain_length = width - len(s[0]) - len(s[1])
    while remain_length < 0:
        remain_length += 10

    result = s[0] + ":" + remain_length * " " + s[1]
    return result

