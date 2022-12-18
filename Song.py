class Song:
    def __init__(self, name, path, length, url) -> None:
        self.name = name
        self.path = path
        self.length = length
        self.url = url
        
    def __str__(self):
        return self.name