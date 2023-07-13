from os import path, listdir

class AudioFileExtractor:

    def __init__(self):
        self._music_directory_list = ('music', 'Music', 'música', 'Música')
        self._allowed_extensions = ('.mp3',)
        self._rute = self._get_music_directory_path

    # To list songs from the selected path
    def list_audio_files(self) -> list:
        data = []

        for filename in listdir(self._rute):
            _, ext = path.splitext(filename)

            if path.isfile(path.join(self._rute, filename)) and ext in self._allowed_extensions:
                data.append(filename)

        return data

    # To list songs with metadata from the selected path
    def list_metadata_audio_files(self) -> list:
        from resources.metadata import MetadataManager # Import

        data = []
        objMetadata = MetadataManager()

        for filename in listdir(self._rute):
            name, ext = path.splitext(filename)
            filepath = path.join(self._rute, filename)

            if path.isfile(filepath) and ext in self._allowed_extensions:
                metadata = objMetadata.get_metadata(filepath)

                data.append([
                    name,
                    metadata['title'][0] if 'title' in metadata else "-",
                    metadata['artist'][0] if 'artist' in metadata else "-",
                    metadata['album'][0] if 'album' in metadata else "-",
                    metadata['albumartist'][0] if 'albumartist' in metadata else "-",
                    metadata['genre'][0] if 'genre' in metadata else "-",
                    metadata['composer'][0] if 'composer' in metadata else "-",
                    metadata['tracknumber'][0] if 'tracknumber' in metadata else "-",
                    metadata['organization'][0] if 'organization' in metadata else "-",
                    metadata['date'][0] if 'date' in metadata else "-",
                    metadata['encodedby'][0] if 'encodedby' in metadata else "-"
                ])

        return data

    @property
    def get_rute(self) -> str:
        return self._rute

    def set_rute(self, rute : str):
        self._rute = rute

    # Find music directory path with the list of possible directory names
    # If found, it returns the directory path; otherwise, return the user directory
    @property
    def _get_music_directory_path(self) -> str:
        main_path = path.expanduser('~')

        for dir_music in self._music_directory_list:
            if dir_music in listdir(main_path):
                main_path = path.join(main_path, dir_music)
                break

        return main_path
