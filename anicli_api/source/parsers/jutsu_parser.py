# Auto generated code by ssc_gen
# WARNING: Any manual changes made to this file will be lost when this
# is run again. Do not edit this file unless you know what you are doing.

from __future__ import annotations  # python 3.7, 3.8 comp
import re
from typing import Any, Union

from parsel import Selector, SelectorList

_T_DICT_ITEM = dict[str, Union[str, list[str]]]
_T_LIST_ITEMS = list[dict[str, Union[str, list[str]]]]


class _BaseStructParser:
    def __init__(self, document: str):
        self.__raw__ = document
        self.__selector__ = Selector(document)
        self._cached_result: Union[_T_DICT_ITEM, _T_LIST_ITEMS] = {}

    def _pre_validate(self, document: Selector) -> None:
        # pre validate entrypoint, contain assert expressions
        pass

    def parse(self):
        """run parser"""
        self._pre_validate(self.__selector__)
        self._start_parse()
        return self

    def view(self) -> Union[_T_DICT_ITEM, _T_LIST_ITEMS]:
        """get parsed values"""
        return self._cached_result

    def _start_parse(self):
        """parse logic entrypoint"""
        pass


class OngoingView(_BaseStructParser):
    """usage:

        POST https://jut.su/anime/ongoing/
        ajax_load=yes&start_from_page=1&show_search=&anime_of_user=


        OngoingView view() item signature:

    {
        "url": "String",
        "title": "String",
        "thumbnail": "String",
        "counts": "Array['String']"
    }
    """

    def __init__(self, document: str):
        super().__init__(document)
        self._cached_result: _T_LIST_ITEMS = []

    def _part_document(self) -> SelectorList:
        doc = self.__selector__
        var_0 = doc
        var_1 = var_0.css(".all_anime_global")
        return var_1

    def _start_parse(self):
        self._cached_result.clear()
        for part in self._part_document():
            self._cached_result.append(
                {
                    "url": self._parse_url(part),
                    "title": self._parse_title(part),
                    "thumbnail": self._parse_thumbnail(part),
                    "counts": self._parse_counts(part),
                }
            )

    def view(self) -> _T_LIST_ITEMS:
        return self._cached_result

    def _parse_url(self, doc: Selector):
        var_0 = doc
        var_1 = var_0.css("a")
        var_2 = var_1.attrib["href"]
        var_3 = "https://jut.su{}".format(var_2)
        return var_3

    def _parse_title(self, doc: Selector):
        var_0 = doc
        var_1 = var_0.css(".aaname")
        var_2 = var_1.css("::text").get()
        return var_2

    def _parse_thumbnail(self, doc: Selector):
        """signature:

        background: url('https://gen.jut.su/uploads/animethumbs/aaaa.jpg')  no-repeat;

        """

        var_0 = doc
        var_1 = var_0.css(".all_anime_image")
        var_2 = var_1.attrib["style"]
        var_3 = re.search(r"'(https?://.*?)'", var_2)[1]
        return var_3

    def _parse_counts(self, doc: Selector):
        """signature:

        <div class="aailines">
                1094 серии
                <br>
                14 фильмов
        </div>

        """

        var_0 = doc
        var_1 = var_0.css(".aailines")
        var_2 = var_1.css("::text").getall()
        var_3 = [s.strip("\r\n") for s in var_2]
        var_4 = " ".join(var_3)
        return var_4


class SearchView(_BaseStructParser):
    """
        POST https://jut.su/anime/
        ajax_load=yes&start_from_page=1&show_search=<QUERY>&anime_of_user=

        EXAMPLE:
            POST https://jut.su/anime/
            ajax_load=yes&start_from_page=1&show_search=LA&anime_of_user=

        SearchView view() item signature:

    {
        "url": "String",
        "title": "String",
        "thumbnail": "String",
        "counts": "Array['String']"
    }
    """

    def __init__(self, document: str):
        super().__init__(document)
        self._cached_result: _T_LIST_ITEMS = []

    def _part_document(self) -> SelectorList:
        doc = self.__selector__
        var_0 = doc
        var_1 = var_0.css(".all_anime_global")
        return var_1

    def _start_parse(self):
        self._cached_result.clear()
        for part in self._part_document():
            self._cached_result.append(
                {
                    "url": self._parse_url(part),
                    "title": self._parse_title(part),
                    "thumbnail": self._parse_thumbnail(part),
                    "counts": self._parse_counts(part),
                }
            )

    def view(self) -> _T_LIST_ITEMS:
        return self._cached_result

    def _parse_url(self, doc: Selector):
        var_0 = doc
        var_1 = var_0.css("a")
        var_2 = var_1.attrib["href"]
        var_3 = "https://jut.su{}".format(var_2)
        return var_3

    def _parse_title(self, doc: Selector):
        var_0 = doc
        var_1 = var_0.css(".aaname")
        var_2 = var_1.css("::text").get()
        return var_2

    def _parse_thumbnail(self, doc: Selector):
        """signature:

        background: url('https://gen.jut.su/uploads/animethumbs/aaaa.jpg')  no-repeat;

        """

        var_0 = doc
        var_1 = var_0.css(".all_anime_image")
        var_2 = var_1.attrib["style"]
        var_3 = re.search(r"'(https?://.*?)'", var_2)[1]
        return var_3

    def _parse_counts(self, doc: Selector):
        """signature:

        <div class="aailines">
                1094 серии
                <br>
                14 фильмов
        </div>

        """

        var_0 = doc
        var_1 = var_0.css(".aailines")
        var_2 = var_1.css("::text").getall()
        var_3 = [s.strip("\r\n") for s in var_2]
        var_4 = " ".join(var_3)
        return var_4


class SourceView(_BaseStructParser):
    """
        GET https://jut.su/<ANIME PATH>/<SEASON?>/episode-<NUM>.html

        NOTE: VIDEO REQUEST SHOULD HAVE SAME USER-AGENT AS CLIENT

        need set user-agent same as send HTTP request in API

        eg:

        cl = Client(headers={"user-agent": "X"})

        s = SourceView(doc).parse().view()

        mpv s["url_1080"]  # 403, FORBIDDEN

        mpv s["url_1080"] --user-agent="Y"  # 403, FORBIDDEN

        mpv s["url_1080"] --user-agent="X"  # 200, OK

        EXAMPLE:
            GET https://jut.su/kime-no-yaiba/season-1/episode-1.html

        SourceView view() item signature:

    {
        "url_1080": "String",
        "url_720": "String",
        "url_480": "String",
        "url_360": "String"
    }
    """

    def __init__(self, document: str):
        super().__init__(document)
        self._cached_result: _T_DICT_ITEM = {}

    def _start_parse(self):
        self._cached_result.clear()
        self._cached_result["url_1080"] = self._parse_url_1080(self.__selector__)
        self._cached_result["url_720"] = self._parse_url_720(self.__selector__)
        self._cached_result["url_480"] = self._parse_url_480(self.__selector__)
        self._cached_result["url_360"] = self._parse_url_360(self.__selector__)

    def view(self) -> _T_DICT_ITEM:
        return self._cached_result

    def _parse_url_1080(self, doc: Selector):
        var_0 = doc
        try:
            var_2 = var_0.css(".watch_additional_players .wap_player")
            var_3 = var_2.attrib["data-player-1080"]
            return var_3
        except Exception as e:
            return None

    def _parse_url_720(self, doc: Selector):
        var_0 = doc
        try:
            var_2 = var_0.css(".watch_additional_players .wap_player")
            var_3 = var_2.attrib["data-player-720"]
            return var_3
        except Exception as e:
            return None

    def _parse_url_480(self, doc: Selector):
        var_0 = doc
        try:
            var_2 = var_0.css(".watch_additional_players .wap_player")
            var_3 = var_2.attrib["data-player-480"]
            return var_3
        except Exception as e:
            return None

    def _parse_url_360(self, doc: Selector):
        var_0 = doc
        try:
            var_2 = var_0.css(".watch_additional_players .wap_player")
            var_3 = var_2.attrib["data-player-360"]
            return var_3
        except Exception as e:
            return None


class AnimeView(_BaseStructParser):
    """
        GET https://jut.su/<ANIME PATH>

        EXAMPLE:
            GET https://jut.su/kime-no-yaiba/

        AnimeView view() item signature:

    {
        "title": "String",
        "description": "Array['String']",
        "thumbnail": "String"
    }
    """

    def __init__(self, document: str):
        super().__init__(document)
        self._cached_result: _T_DICT_ITEM = {}

    def _start_parse(self):
        self._cached_result.clear()
        self._cached_result["title"] = self._parse_title(self.__selector__)
        self._cached_result["description"] = self._parse_description(self.__selector__)
        self._cached_result["thumbnail"] = self._parse_thumbnail(self.__selector__)

    def view(self) -> _T_DICT_ITEM:
        return self._cached_result

    def _parse_title(self, doc: Selector):
        var_0 = doc
        var_1 = var_0.css(".anime_padding_for_title")
        var_2 = var_1.css("::text").get()
        var_3 = re.search(r"Смотреть (.*?) все", var_2)[1]
        return var_3

    def _parse_description(self, doc: Selector):
        var_0 = doc
        var_1 = var_0.css(".uv_rounded_bottom span")
        var_2 = var_1.css("::text").getall()
        var_3 = " ".join(var_2)
        return var_3

    def _parse_thumbnail(self, doc: Selector):
        var_0 = doc
        var_1 = var_0.css(".all_anime_title")
        var_2 = var_1.attrib["style"]
        var_3 = re.search(r"'(https?://.*?)'", var_2)[1]
        return var_3


class EpisodeView(_BaseStructParser):
    """
        GET https://jut.su/<ANIME PATH>

        EXAMPLE:
            GET https://jut.su/kime-no-yaiba/

        EpisodeView view() item signature:

    {
        "title": "String",
        "url": "String"
    }
    """

    def __init__(self, document: str):
        super().__init__(document)
        self._cached_result: _T_LIST_ITEMS = []

    def _part_document(self) -> SelectorList:
        doc = self.__selector__
        var_0 = doc
        var_1 = var_0.css(".video")
        return var_1

    def _start_parse(self):
        self._cached_result.clear()
        for part in self._part_document():
            self._cached_result.append(
                {
                    "title": self._parse_title(part),
                    "url": self._parse_url(part),
                }
            )

    def view(self) -> _T_LIST_ITEMS:
        return self._cached_result

    def _parse_title(self, doc: Selector):
        var_0 = doc
        var_1 = var_0.css("::text").get()
        var_2 = var_1.strip(" ")
        return var_2

    def _parse_url(self, doc: Selector):
        var_0 = doc
        var_1 = var_0.attrib["href"]
        var_2 = "https://jut.su{}".format(var_1)
        return var_2
