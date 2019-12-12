import re

from bs4 import Comment, NavigableString, Tag

from prismriver.plugin.common import Plugin
from prismriver.struct import Song


class LyricalNonsensePlugin(Plugin):
    ID = 'lyricalnonsense'

    def __init__(self, config):
        super(LyricalNonsensePlugin, self).__init__('Lyrical Nonsense', config)

    def search_song(self, artist, title):
        artist_page = self.get_artist_page(artist)
        if artist_page:
            song_page = self.get_song_page(artist_page, title)
            if song_page:
                return self.get_song(artist, title, song_page)

    def get_artist_page(self, artist):
        main_page = self.download_webpage('https://www.lyrical-nonsense.com/lyrics/')
        if main_page:
            soup = self.prepare_soup(main_page)

            artist_infos = []

            artists_pane = soup.find('div', {'class': 'lyricinfoblock'})

            for elem in artists_pane.find_all('a', href=re.compile('https?://www.lyrical-nonsense.com/lyrics/.*/')):
                artist_infos.append([elem['href'], elem.text.split(' | )')])

            artist_link = None
            for info in artist_infos:
                if artist.lower() in map(str.lower, info[1]):
                    artist_link = info[0]

            if artist_link:
                return self.download_webpage(artist_link)

    def get_song_page(self, page, title):
        soup = self.prepare_soup(page)

        song_titles = [title.find('a') for title in soup.findAll('td', {'class': 'song_title'})]
        for song_title in song_titles:
            if title.lower() in song_title.text.lower():
                return self.download_webpage(song_title['href'])

    def get_song(self, artist, title, page):
        soup = self.prepare_soup(page)

        # TODO: get metadata from page I guess

        lyrics = [self.parse_verse_block(l) for l in soup.findAll('div', {'class': 'olyrictext'})]

        return Song(artist, title, self.sanitize_lyrics(lyrics))

    def parse_verse_block(self, verse_block, tags_to_skip=None):
        lyric = ''

        for elem in verse_block.childGenerator():
            if isinstance(elem, Comment):
                pass
            elif isinstance(elem, NavigableString):
                lyric += elem.strip()
            elif isinstance(elem, Tag):
                if elem.name == 'p':
                    lyric += ('\n\n' + super().parse_verse_block(elem))
                else:
                    lyric += '\n'

        return lyric.strip()
