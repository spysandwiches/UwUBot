# used to store the link and name of a song inside client.music_queue
class QueuedSong:
    def __init__(self, file_path, real_name):
        self.file_path = file_path
        self.real_name = real_name
