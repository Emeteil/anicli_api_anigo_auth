import re
from typing import List

from anicli_api.player.base import BaseVideoExtractor, Video, url_validator

__all__ = ["SibNet"]
_URL_EQ = re.compile(r"https?://(www\.)?video\.sibnet")
player_validator = url_validator(_URL_EQ)


class SibNet(BaseVideoExtractor):
    URL_RULE = _URL_EQ

    @player_validator
    def parse(self, url: str, **kwargs) -> List[Video]:
        response = self.http.get(url).text
        return self._extract(response)

    @player_validator
    async def a_parse(self, url: str, **kwargs) -> List[Video]:
        async with self.a_http as client:
            response = (await client.get(url)).text
            return self._extract(response)

    def _extract(self, response: str) -> List[Video]:

        if path := re.search(r'"(?P<url>/v/.*?\.mp4)"', response):
            url = f"https://video.sibnet.ru{path[1]}"
            return [Video(type="mp4", quality=480, url=url, headers={"Referer": url})]
        else:
            raise IndexError("Failed parse sibnet")


if __name__ == "__main__":
    SibNet().parse("https://video.sibnet.ru/shell.php?videoid=4779967")
