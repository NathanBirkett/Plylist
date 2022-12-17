class Song:
    def __init__(self, name, path, length) -> None:
        self.name = name
        self.path = "playlists/" + path
        self.length = length
        
    def __str__(self):
        return self.name