from os import path, rename
import mutagen

class MetadataManager:

    def __init__(self):
        self._tmp_path = ""

    # Get audio file metadata with mutagen
    def get_metadata(self, filepath : str, easy = True):
        return mutagen.File(filepath, easy=easy)

    # Save file metadata
    def save_metadata(self, dirpath, data : dict):
        try:
            # Metadata classes ID3
            from mutagen.id3 import TIT2, TPE1, TPE2, TALB, TRCK, TDRC, TCON, TCOM, TENC, USLT, APIC

            name, ext = path.splitext(data['filename'])
            last_filepath = path.join(dirpath, data['filename'])
            metadata = self.get_metadata(last_filepath, False)

            metadata['TIT2'] = TIT2(encoding=3, text=data['title'])
            metadata['TPE1'] = TPE1(encoding=3, text=data['artist'])
            metadata['TPE2'] = TPE2(encoding=3, text=data['album_artist'])
            metadata['TALB'] = TALB(encoding=3, text=data['album'])
            metadata['TRCK'] = TRCK(encoding=3, text=data['track'])
            metadata['TDRC'] = TDRC(encoding=3, text=data['date'])
            metadata['TCON'] = TCON(encoding=3, text=data['genre'])
            metadata['TCOM'] = TCOM(encoding=3, text=data['compositor'])
            metadata['TENC'] = TENC(encoding=3, text=data['encodedby'])
            metadata.tags.add(USLT(encoding=3, text=data['lyrics'].rstrip()))

            if data['cover']:
                if 'APIC' in metadata:
                    metadata.pop('APIC')

                with open(data['cover'], 'rb') as img:
                    metadata['APIC'] = APIC(encoding=3, mime='image/jpeg', type=3, data=img.read())

            metadata.save()

            if data['new_filename'] != name:
                new_filepath = path.join(dirpath, data['new_filename'] + ext)

                rename(last_filepath, new_filepath) # Change file name

        except Exception as ex:
            raise ValueError(ex)
