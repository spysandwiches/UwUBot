import os
import time
from pytube import YouTube


def startup_display():
    os.system("cls")
    print("  _    _              _    _ ")
    print(" | |  | |            | |  | |")
    print(" | |  | | __      __ | |  | |")
    print(" | |  | | \\ \\ /\\ / / | |  | |")
    print(" | |__| |  \\ V  V /  | |__| |")
    print("  \\____/    \\_/\\_/    \\____/ ")
    print("                             ")
    print("_____________________________")


def console_output(event, creator, target=None, outcome=None):
    """
    outputs to console for debugging purposes
    :param event: the event, pass an arbitrary string (i.e. "vote_kick" for vote_kick)
    :param creator: the user id of the user that invoked the command, or the user targeted by automatic bot events
    :param target: the user id of the target, if one exists
    :param outcome: arbitrary string of outcome, (i.e. "vote passed" or "vote failed" for vote_kick)
    :return: nothing
    """
    print("event:", event, "| creator:", creator, end=' | ')
    if target is not None:
        print("target:", target, end =' | ')
    if outcome is not None:
        print("result:", outcome, end=' | ')
    print()


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
        ":)": ":3",
        ":(": ">:(",
        "mom": "mommy",
        "dad": "daddy",
        "the": "da",
        "this": "dis",
        "that": "dat",
        "these": "deez",
        "those": "doze",
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
        # special words
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

    new_message = new_message[0:-1]  # removes extra space
    return new_message


# converts input message to 1337 sp34k
def leet_speak(message):
    new_message = ""  # return value
    split_message = message.lower().split(" ")  # lowercases message, splits on space
    letter_dict = {  # stores replacement cases
        "l": "1",
        "e": "3",
        "t": "7",
        "o": "0",
        "a": "4",
        "z": "2",
        "g": "9",
        "s": "5"
    }

    for word in split_message:
        for letter in word:
            if letter in letter_dict:  # checks replacement cases
                new_message += letter_dict[letter]
            else:  # non-replacement case
                new_message += letter
        new_message += " "  # adds space

    new_message = new_message[0: -1]  # removes extra space

    return new_message


async def get_youtube_vid(working_dir, link):
    acceptable_character = "abcdefghijklmnopqrstuvwxyz1234567890"
    save_path = "\\youtubeBuffer"
    video_title = ""
    max_rate_itag = 0
    max_rate = 0
    currtime = time.time()

    try:
        yt = YouTube(link)
    except:
        print("oh fuckles")

    video_title = yt.title
    streams = yt.streams.filter(only_audio=True)

    for audio_track in streams:
        if int(audio_track.abr[:-4]) > max_rate:
            max_rate = int(audio_track.abr[:-4])
            max_rate_itag = audio_track.itag

    final_title = ''.join(filter(str.isalnum, video_title))
    final_title = final_title + str(time.time()).replace(".", "")
    final_stream = yt.streams.get_by_itag(max_rate_itag)
    return final_stream.download(output_path=(working_dir + "/youtubeBuffer"), filename=(final_title + ".mp3")), video_title


async def get_song_name(link):
    try:
        yt = YouTube(link)
    except:
        print("shit")

    return yt.title
