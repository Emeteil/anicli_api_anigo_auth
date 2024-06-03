import logging
import re
from typing import Dict, List

from attrs import define
from httpx import AsyncClient, Client, Response, HTTPStatusError
from parsel import Selector

from anicli_api._http import HTTPAsync, HTTPSync
from anicli_api.base import _HttpExtension, BaseAnime, BaseEpisode, BaseExtractor, BaseLibrary, BaseOngoing, BaseSearch, BaseSource
from anicli_api.source.parsers.animego_parser import (
    AnimeView,
    DubbersView,
    EpisodeView,
    OngoingView,
    SearchView,
    SourceView,
    LibraryView,
)

_logger = logging.getLogger("anicli-api")  # type: ignore

_PHPSESSID = None

def set_PHPSESSID(key: str) -> None:
    """set PHPSESSID cookie"""
    global _PHPSESSID
    _PHPSESSID = key

def _is_authorized() -> bool:
    http_client = HTTPSync(cookies = {"PHPSESSID": _PHPSESSID}, follow_redirects = True)
    return _PHPSESSID and (http_client.get("https://animego.org/profile/").status_code != 500)

class AuthorizationError(Exception):
    def __init__(self, message="PHPSESSID is missing!"):
        super().__init__(message)

class Profile():
    BASE_URL = "https://animego.org"
    
    def __init__(self, nickname: str = None, http: "Client" = HTTPSync(), http_async: "AsyncClient" = HTTPAsync()):
        if not nickname:
            self.http = HTTPSync(cookies = {"PHPSESSID": _PHPSESSID})
            self.http_async = HTTPAsync(cookies = {"PHPSESSID": _PHPSESSID})
            resp = self.http.get(f"{self.BASE_URL}/profile/")
            self.nickname = re.search(r"<title>(.*?)</title>", resp.text)[1].split(" / ")[0]
            return
        self.http = http
        self.http_async = http_async
        self.nickname = nickname
        
    def _get_anime(self, type: str = ""):
        i = 1
        content = ""
        while True:
            resp = self.http.get(f"{self.BASE_URL}/user/{self.nickname}/mylist/anime{('/' if type else '') + type}",
                                 params = {"type": "mylist", "page": i})
            json = resp.json()
            content += json["content"]
            if json["endPage"]: break
            i+=1
        data = LibraryView(content).parse().view()
        return [Library(**d, http = self.http, http_async = self.http_async) for d in data]
        
    async def _a_get_anime(self, type: str = ""):
        i = 1
        content = ""
        while True:
            resp = await self.http_async.get(f"{self.BASE_URL}/user/{self.nickname}/mylist/anime{('/' if type else '') + type}",
                                             params = {"type": "mylist", "page": i})
            json = resp.json()
            content += json["content"]
            if json["endPage"]: break
            print(i)
            i+=1
        data = LibraryView(content).parse().view()
        return [Library(**d, http = self.http, http_async = self.http_async) for d in data]
    
    def get_all_anime(self): return self._get_anime()
    def get_watching_anime(self): return self._get_anime("watching")
    def get_completed_anime(self): return self._get_anime("completed")
    def get_onhold_anime(self): return self._get_anime("onhold")
    def get_dropped_anime(self): return self._get_anime("dropped")
    def get_planned_anime(self): return self._get_anime("planned")
    def get_rewatching_anime(self): return self._get_anime("rewatching")
    
    async def a_get_all_anime(self): return await self._a_get_anime()
    async def a_get_watching_anime(self): return await self._a_get_anime("watching")
    async def a_get_completed_anime(self): return await self._a_get_anime("completed")
    async def a_get_onhold_anime(self): return await self._a_get_anime("onhold")
    async def a_get_dropped_anime(self): return await self._a_get_anime("dropped")
    async def a_get_planned_anime(self): return await self._a_get_anime("planned")
    async def a_get_rewatching_anime(self): return await self._a_get_anime("rewatching")

class Extractor(BaseExtractor):
    BASE_URL = "https://animego.org"
    
    def __init__(self, http_client: "Client" = HTTPSync(), http_async_client: "AsyncClient" = HTTPAsync()):
        if not _is_authorized():
            super().__init__(http_client, http_async_client)
            return
        self._http = HTTPSync(cookies = {"PHPSESSID": _PHPSESSID})
        self._http_async = HTTPAsync(cookies = {"PHPSESSID": _PHPSESSID})
    
    def _extract_search(self, resp: str):
        data = SearchView(resp).parse().view()
        return [Search(**d, **self._kwargs_http) for d in data]

    @staticmethod
    def _remove_ongoings_dups(ongoings: List["Ongoing"]):
        # remove duplicates and accumulate by episode and dubber keys
        sorted_ongs: Dict[int, "Ongoing"] = {}
        for ong in ongoings:
            key = hash(ong.url + ong.episode)
            if sorted_ongs.get(key):
                sorted_ongs[key].dub += f", {ong.dub}"
            else:
                sorted_ongs[key] = ong
        return list(sorted_ongs.values())

    def _extract_ongoing(self, resp: str):
        data = OngoingView(resp).parse().view()
        ongs = [Ongoing(**d, **self._kwargs_http) for d in data]
        return self._remove_ongoings_dups(ongs)

    def search(self, query: str):
        resp = self.http.get(f"{self.BASE_URL}/search/anime", params={"q": query})
        return self._extract_search(resp.text)

    async def a_search(self, query: str):
        resp = await self.http_async.get(f"{self.BASE_URL}/search/anime", params={"q": query})
        return self._extract_search(resp.text)

    def ongoing(self):
        resp = self.http.get(self.BASE_URL)
        return self._extract_ongoing(resp.text)

    async def a_ongoing(self):
        resp = await self.http_async.get(self.BASE_URL)
        return self._extract_ongoing(resp.text)


@define(kw_only=True)
class Library(BaseLibrary):
    def _extract(self, resp: str):
        data = AnimeView(resp).parse().view()
        return Anime(**data, **self._kwargs_http)

    @staticmethod
    def _is_valid_page(resp: Response):
        if resp.is_success:
            return True

        title = re.search(r"<title>(.*?)</title>", resp.text)[1]
        _logger.warning(
            "%s returns status code [%s] title='%s' content-length=%s",
            resp.url,
            resp.status_code,
            title,
            len(resp.content),
        )
        return False

    def _create_anime(self):
        return Anime(
            title=self.title,
            thumbnail=self.thumbnail,
            description="",
            id=self.url.split("-")[-1],
            raw_json="",
            **self._kwargs_http,
        )
    
    def get_anime(self):
        resp = self.http.get(self.url)
        if self._is_valid_page(resp):
            return self._extract(resp.text)
        return self._create_anime()

    async def a_get_anime(self):
        resp = await self.http_async.get(self.url)
        if self._is_valid_page(resp):
            return self._extract(resp.text)
        return self._create_anime()

@define(kw_only=True)
class Search(BaseSearch):
    def _extract(self, resp: str):
        data = AnimeView(resp).parse().view()
        return Anime(**data, **self._kwargs_http)

    @staticmethod
    def _is_valid_page(resp: Response):
        # RKN blocks issues eg:
        # https://animego.org/anime/ya-predpochitayu-zlodeyku-2413
        # but API requests MAYBE still works.
        if resp.is_success:
            return True

        title = re.search(r"<title>(.*?)</title>", resp.text)[1]  # type: ignore
        _logger.warning(
            "%s returns status code [%s] title='%s' content-length=%s",
            resp.url,
            resp.status_code,
            title,
            len(resp.content),
        )
        return False

    def _create_anime(self):
        # skip extract metadata and manual create object (API requests maybe still works)
        return Anime(
            title=self.title,
            thumbnail=self.thumbnail,
            description="",
            # id for API requests contains in url
            id=self.url.split("-")[-1],
            raw_json="",
            **self._kwargs_http,
        )
    
    def get_anime(self):
        resp = self.http.get(self.url)
        if self._is_valid_page(resp):
            return self._extract(resp.text)
        return self._create_anime()

    async def a_get_anime(self):
        resp = await self.http_async.get(self.url)
        if self._is_valid_page(resp):
            return self._extract(resp.text)
        return self._create_anime()


@define(kw_only=True)
class Ongoing(BaseOngoing):
    episode: str
    dub: str

    def _extract(self, resp: str):
        data = AnimeView(resp).parse().view()
        return Anime(**data, **self._kwargs_http)

    @staticmethod
    def _is_valid_page(resp: Response):
        # RKN blocks issues eg:
        # https://animego.org/anime/ya-predpochitayu-zlodeyku-2413
        # but API requests MAYBE still works.
        if resp.is_success:
            return True

        title = re.search(r"<title>(.*?)</title>", resp.text)[1]  # type: ignore
        _logger.warning(
            "%s returns status code [%s] title='%s' content-length=%s",
            resp.url,
            resp.status_code,
            title,
            len(resp.content),
        )
        return False

    def _create_anime(self):
        # skip extract metadata, and manual create object (API requests MAYBE still works)
        return Anime(
            title=self.title,
            thumbnail=self.thumbnail,
            description="",
            id=self.url.split("-")[-1],
            raw_json="",
            **self._kwargs_http,
        )

    def get_anime(self):
        resp = self.http.get(self.url)
        if self._is_valid_page(resp):
            return self._extract(resp.text)
        return self._create_anime()

    async def a_get_anime(self):
        resp = await self.http_async.get(self.url)
        if self._is_valid_page(resp):
            return self._extract(resp.text)
        return self._create_anime()

    def __str__(self):
        return f"{self.title} {self.episode} ({self.dub})"


@define(kw_only=True)
class Anime(BaseAnime):
    id: str
    raw_json: str
    
    def __attrs_post_init__(self):
        self.thumbnail = self.thumbnail.strip()
        if _PHPSESSID:
            self._http = HTTPSync(cookies={"PHPSESSID": _PHPSESSID})
            self._http_async = HTTPAsync(cookies={"PHPSESSID": _PHPSESSID})
    
    def _extract(self, resp: str):
        episodes_data = EpisodeView(resp).parse().view()
        
        dubbers = DubbersView(resp).parse().view()
        return [Episode(**d, dubbers=dubbers, **self._kwargs_http) for d in episodes_data]

    @staticmethod
    def _episodes_is_available(response: str):
        sel = Selector(response)
        # RKN issue: maybe title not available in your country
        # eg:
        # https://animego.org/anime/vtorzhenie-gigantov-2-17
        # this title API request don't work in RU ip
        if sel.css("div.player-blocked").get():
            _logger.error("API not available in your country. Element: %s", sel.css("div.h5").get())
            return False
        return True

    def get_episodes(self):
        resp = self.http.get(f"https://animego.org/anime/{self.id}/player?_allow=true").json()["content"]
        return self._extract(resp) if self._episodes_is_available(resp) else []

    def get_json_info(self):
        return Selector(self.raw_json, type="json").getall()[0]
    
    async def a_get_episodes(self):
        resp = await self.http_async.get(f"https://animego.org/anime/{self.id}/player?_allow=true")
        resp = resp.json()["content"]
        return self._extract(resp) if self._episodes_is_available(resp) else []

    def set_rate(self, stars: int) -> bool:
        """rate the anime sync"""
        if not _PHPSESSID: raise AuthorizationError()
        resp = self.http.post(f"https://animego.org/rating/{self.id}/{stars}/anime/vote")
        return (resp.status_code == 200) and (resp.json()['status'] == "success")
    
    async def a_set_rate(self, stars: int) -> bool:
        """rate the anime async"""
        if not _PHPSESSID: raise AuthorizationError()
        resp = await self.http_async.post(f"https://animego.org/rating/{self.id}/{stars}/anime/vote")
        return (resp.status_code == 200) and (resp.json()['status'] == "success")
    
    def get_view_status(self):
        """get all the viewing status for anime sync"""
        if not _PHPSESSID: raise AuthorizationError()
        url: str = self.get_json_info()['url']
        resp = self.http.get(f"https://animego.org{url}")
        return AnimeView.parse_view_status(Selector(resp.text))
        
    async def a_get_view_status(self):
        """get all the viewing status for anime async"""
        if not _PHPSESSID: raise AuthorizationError()
        url: str = self.get_json_info()['url']
        resp = await self.http_async.get(f"https://animego.org{url}")
        return AnimeView.parse_view_status(Selector(resp.text))
    
    def set_view_status(self, status: int = 1):
        """set the viewing status for anime sync"""
        if status not in [1,2,3,4,5,6]: raise ValueError()
        if not _PHPSESSID: raise AuthorizationError()
        resp = self.http.post(f"https://animego.org/animelist/{self.id}/{status}/add")
        return (resp.status_code == 200) and (resp.json()['status'] == "success")
        
    async def a_set_view_status(self, status: int = 1):
        """set the viewing status for anime async"""
        if status not in [1,2,3,4,5,6]: raise ValueError()
        if not _PHPSESSID: raise AuthorizationError()
        resp = await self.http_async.post(f"https://animego.org/animelist/{self.id}/{status}/add")
        return (resp.status_code == 200) and (resp.json()['status'] == "success")

@define(kw_only=True)
class Episode(BaseEpisode):
    dubbers: Dict[str, str]
    id: str  # episode id (for extract videos required)

    def __attrs_post_init__(self):
        if _PHPSESSID:
            self._http = HTTPSync(cookies={"PHPSESSID": _PHPSESSID})
            self._http_async = HTTPAsync(cookies={"PHPSESSID": _PHPSESSID})
    
    def _extract(self, resp: str):
        data = SourceView(resp).parse().view()
        data_source = [
            {"title": f'{self.dubbers.get(d["data_provide_dubbing"], "???").strip()}', "url": d["url"]} for d in data
        ]
        return [Source(**d, **self._kwargs_http) for d in data_source]
    
    def _get_series_data(self):
        resp = self.http.get(
            "https://animego.org/anime/series",
            params={"dubbing": 2, "provider": 24, "episode": self.num, "id": self.id},
        ).json()
        return resp
    
    async def _a_get_series_data(self):
        resp = (
            await self.http_async.get(
                "https://animego.org/anime/series",
                params={"dubbing": 2, "provider": 24, "episode": self.num, "id": self.id},
            )
        ).json()
    
    def get_sources(self):
        resp = self._get_series_data()["content"]
        return self._extract(resp)

    async def a_get_sources(self):
        resp = self._a_get_series_data()["content"]
        return self._extract(resp)
    
    def make_viewed(self):
        if not _PHPSESSID: raise AuthorizationError()
        resp = self.http.post(f"https://animego.org/anime/episode/{self.id}/watched")
        if resp.status_code != 200: raise HTTPStatusError()
        return resp.json()['message'] == "create"
    
    async def a_make_viewed(self):
        if not _PHPSESSID: raise AuthorizationError()
        resp = await self.http_async.post(f"https://animego.org/anime/episode/{self.id}/watched")
        if resp.status_code != 200: raise HTTPStatusError()
        return resp.json()['message'] == "create"
    
    def get_viewed(self):
        if not _PHPSESSID: raise AuthorizationError()
        data = self._get_series_data()
        return data["episodeWatched"] is not None
        
    async def a_get_viewed(self):
        if not _PHPSESSID: raise AuthorizationError()
        data = self._a_get_series_data()
        return data["episodeWatched"] is not None

@define(kw_only=True)
class Source(BaseSource):
    pass


if __name__ == "__main__":
    from anicli_api.tools import cli

    cli(Extractor())
