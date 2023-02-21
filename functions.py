def console_output(event, creator, target=None, outcome=None):
    """
    outputs to console for debugging purposes
    :param event: the event, pass an arbitrary string (i.e. "vote_kick" for vote_kick)
    :param creator: the user id of the user that invoked the command
    :param target: the user id of the target, if one exists
    :param outcome: arbitrary string of outcome, (i.e. "vote passed" or "vote failed" for vote_kick)
    :return: nothing
    """
    print("event:", event, "| creator:", creator, end=' | ')
    if target is not None:
        print("target:", target, end =' | ')
    if outcome is not None:
        print("result:", outcome, end=' | ')
    print('\n', end=None)


def uwuify(message):
    """
    turns the input into and "UwUify'd" message (ex. I like oreos -> i wike oweos)
    :param message: the input message
    :return: "UwUify'd" message
    """
    # list of words that are handled uniquely
    special_words = {
        "lol": "LoL",
        "roar": "rawr",
        "xd": "x3",
        "mom": "mommy",
        "dad": "daddy",
        "the": "da",
        "this": "dis",
        "that": "dat",
        "fuck": "fuk",
        "hi": "hai",
        "spy": "spai",
        "bye": "bai"
    }
    new_message = ""  # return value
    temp_word = ""  # holds word while it's being worked on

    split_message = message.lower()
    split_message = split_message.split(" ")

    for word in split_message:
        temp_word = ""
        if word in special_words:
            new_message += special_words[word] + " "
        else:
            # first pass (replacing single letters)
            for letter in word:
                if letter == 'l' or letter == "r":
                    temp_word += "w"
                else:
                    temp_word += letter
            # append finished word to return message
            new_message += temp_word + " "

    new_message = new_message[0:-1]
    return new_message

