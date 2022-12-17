class Playlist:
    def __init__(self, name, songs) -> None:
        self.name = name
        self.songs = songs
        
    def __str__(self) -> str:
        return self.name
    
    def __iter__(self):
        self.i = 0
        return self
    
    def __next__(self):
        try:
            x = self.songs[self.i]
            self.i += 1
            return x
        except:
            raise StopIteration