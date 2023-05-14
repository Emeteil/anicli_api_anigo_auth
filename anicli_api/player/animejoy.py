import re
from typing import List

from scrape_schema.fields.regex import ReMatchList

from anicli_api.player.base import BaseVideoExtractor, Video, url_validator

__all__ = ["AnimeJoy"]
_URL_EQ = re.compile(r"https://(www\.)?animejoy\.ru/player")
player_validator = url_validator(_URL_EQ)


class AnimeJoy(BaseVideoExtractor):
    URL_RULE = _URL_EQ

    @player_validator
    def parse(self, url: str, **kwargs) -> List[Video]:
        return self._extract(url)

    @player_validator
    async def a_parse(self, url: str, **kwargs) -> List[Video]:
        return self._extract(url)

    def _extract(self, response: str) -> List[Video]:
        # some extract logic
        url_1080, url_360 = ReMatchList(re.compile(r"](https?://(?:www\.)?.*?\.mp4)")).extract(
            response
        )
        return [
            Video(type="mp4", quality=1080, url=url_1080),
            Video(type="mp4", quality=360, url=url_360),
        ]


if __name__ == "__main__":
    U = """https://animejoy.ru/player/playerjs.html?file=[1080p]https://noda3.cdnjoy.site/Tsunlise/KAZOKU/01-1080.mp4,[360p]https://noda3.cdnjoy.site/Tsunlise/KAZOKU/01-360.mp4"""
    print(AnimeJoy().parse(U))