import bs4
import bs4 as parser
import faster_than_requests
import requests


class Book:

    @staticmethod
    def request_ajax(*infos):
        a = dict(infos)
        url = "https://www.scribblehub.com/wp-admin/admin-ajax.php"
        print(a)
        return requests.post(url, a)

    def __init__(self, uuid):
        self.uuid = uuid

    def basic_infos(self):
        a = Book.request_ajax(("action","wi_getcache_fp_seriesinfo"), ("intPostID", "173303"), ("isMobile", "173303"))
        print(a)
        parsed = bs4.BeautifulSoup(a.text, "lxml")
        cover = parsed.img['src']
        all_links = parsed.findAll('a')
        permalink = all_links[0]['href']
        title = all_links[0].text
        author_link = all_links[1]['href']
        author = all_links[1].text
        genre_list = [all_links[a].text for a in range(2, len(all_links))]
        genre_string = " ".join(genre_list)
        total_len = 9 + len(title) + len(author) + len(genre_string)
        synopsis = parsed.text.replace('\n', '')[total_len:].replace("more>>","\n").replace("<<less", "\n")
        return {"title": title, "permalink": permalink, "author_link": author_link, "author": author,
                "genre_list": genre_list, "synopsis": synopsis, "cover": cover}

    def name(self):
        return self.content.title.string.split("|")[0].strip()

    def __extract_canonical__(self):
        tag = self.content.find(rel="canonical")
        return tag.attrs['href']

    def __extract_base_stats__(self):
        text = self.content.find(class_="fic_stats")
        attributes = text.contents
        a = {}
        for attr in attributes:
            lst = attr.text.strip().split(" ")
            a[lst[1]] = lst[0].strip()
        return a

    def __extract_synopsis__(self):
        return self.content.find(class_="wi_fic_desc").text

    def __status__(self):
        status = self.content.find(class_="status").find_next()
        return status.text.strip().split(" ")[0]

    def __genre_list__(self):
        fic_genre = self.content.findAll(class_="fic_genre")
        genre = [s.text.strip() for s in fic_genre]
        return genre

    def __tag_list__(self):
        fic_tags = self.content.findAll(class_="stag")
        tags = [s.text.strip() for s in fic_tags]
        return tags

    def __extract_author__(self):
        text = self.content.find(class_='auth_name_fic')
        name = text.text
        url = text.previous.get('href')
        return name, url

    def list_of_chapters(self):
        url = "https://www.scribblehub.com/wp-admin/admin-ajax.php"
        a = {"action": "wi_gettocchp", "strSID": str(self.uuid), "strmypostid": "0", "strFic": "yes"}
        results = requests.post(url, a).text
        parse = parser.BeautifulSoup(results, "html.parser")
        text = parse.contents[0]
        text = text.findAll('li')
        text = [(s.a.attrs['title'], s.a.attrs['href']) for s in text]
        return text

    def top_chapters(self):
        s = self.stat_content.find(class_='top_fav_chp')
        st = [*s.children]
        return [(s.a.text, s.a.attrs['href'], int(s.text.split(" ")[-1][1:-1])) for s in st]

    def __get_cover(self):
        return self.content.img['src']

    def extract_infos(self):
        """Extract informations
            - Author
            - AuthorLink
            - Title
            - Image Link
            - Permalink
            - Synopsis
            - Status
            - Views
            - Favorites
            - Chapters
            - Chapters/Week
            - Readers
            - List of genre
            - List of tags
        """
        author, author_link = self.__extract_author__()
        infos = {'author': author, 'author_link': author_link, 'title': self.name(),
                 'synopsis': self.__extract_synopsis__(), 'cover': self.__get_cover(),
                 'permalink': self.__extract_canonical__(), 'status': self.__status__()}
        infos.update(self.__extract_base_stats__())
        infos['genre_list'] = self.__genre_list__()
        infos['tag_list'] = self.__tag_list__()
        return infos

    def extract_stats(self):
        text = self.stat_content.find(class_="table_pro_overview")
        simple_table = text.contents
        stats = simple_table[1]
        stats = [x.text for x in stats.contents if (not isinstance(x, parser.NavigableString))]
        stats = list(map(lambda g: g.replace('\n', ''), stats))
        stats = list(map(lambda g: tuple(g.split(':')), stats))
        return dict(stats)

    def __extract__(self):
        url = "https://www.scribblehub.com/?p=" + str(self.uuid)
        text = faster_than_requests.get2str(url)
        return parser.BeautifulSoup(text, 'lxml')

    def __extract_stats_page__(self):
        url = self.__extract_canonical__() + "/stats/"
        text = faster_than_requests.get2str(url)
        return parser.BeautifulSoup(text, 'lxml')
