# UwU bot
UwU bot (internally NUwU) is my personal discord bot

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
