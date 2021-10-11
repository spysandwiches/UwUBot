def makeuwu(message):

    msg = message.split(" ")
    newmsg = ""

    wordreplaces = {
        "the": "da",
        "you": "u",
        "do": "dew",
        "guys": "gais",
        "fuck": "fuk",
        "what": "wat",
        "some": "sum",
        "why": "y",
        "gay": "GAY",
        "bye": "bai",
        "by": "bai"
    }

    for word in msg:
        newword = ""

        # uses above dict for hardcoded word swaps
        if word in wordreplaces:
            newmsg = newmsg + wordreplaces[word.lower()] + " "

        # dynamic UwU generation
        else:
            for letter in word:
                if letter.lower() == "r" or letter.lower() == "l":
                    newword = newword + "w"
                elif letter.lower() == "y":
                    newword = newword + "i"
                else:
                    newword = newword + letter

            newmsg += newword + " "

    # removes extra space
    newmsg = newmsg[0:-1]

    return newmsg
