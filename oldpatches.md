# UwU bot
UwU bot (internally NUwU) is my personal discord bot

# v. 0.2.1a
### Additions
- added rematch button to /rock_paper_scissors
- added /leet_speak, t41k 1ik3 th1s
- added an automatic warning for users that repeatedly leave @'s on in replies (will be optional in future updates)
### Changes and Bugfixes
- fixed a crash related to /rock_paper_scissors
- further /patch formatting changes
- fixed potential unnecessary error message during /rock_paper_scissors
### Internals
- added console output for /rock_paper_scissors
- reply_mentions_storage.json used for storing timestamps of reply mentions

# v. 0.2a
### Additions
- added /uwuify, uwuify's a message
- added /say, passes user message through to chat (discord shows the invoker, don't do anything stupid, you're not anonymous)
- added /coinflip, guess what it does?
- added /random_number, generates a number between given min and max values (integers)
- added /rock_paper_scissors, play a game of rock paper scissors with UwU

### Changes and Bugfixes
- /patch and /info messages are now ephemeral (only visible to the user who invoked the command)
- /patch formatting adjustments

### Internals
- non-discord functions were moved to functions.py (ex. console_output() )

# v. 0.1.1a
- added custom status
- changed about me
- commands now give console output for debugging purposes
- added /info, gives information on the bot
- added /patch, reads off the latest patch
- internal seperation of views (buttons) into views.py, keeps main.py cleaner
- removed bananaPuncher

# v. 0.1a
- added vote_kick command