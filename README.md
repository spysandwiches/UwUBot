# v. 0.2.2a
### Additions
- /play_song plays a song from youtube
  - parameters:
  - link - the link to the song
  - volume - float betweeen 0.01 and 1.5, volume multiplier
### Changes and Bugfixes
- slight adjustments to leet_speak algorithm
### Internals
- console now has fancy startup 
- functions.get_youtube_vid() makes an mp3 out of a youtube link (slow and synchronous, up for a rewrite)
- functions.get_song_name() gets the title of a youtube video (relies on same library, likely rewrite)
### Known Bugs
- /play_song will freeze the whole bot until it's done downloading that song
  - uses syncronous functions, need to figure out a way to avoid them