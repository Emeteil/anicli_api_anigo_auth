from typing import TYPE_CHECKING, Optional, Sequence, Any, Callable, TypeVar
from contextlib import suppress

if TYPE_CHECKING:
    from anicli_api.base import BaseAnime, BaseEpisode, BaseExtractor, BaseOngoing, BaseSearch, BaseSource
    from anicli_api.player.base import Video

__all__ = ["cli"]

T = TypeVar("T")

HELP_ = """h - print help
s <query> - search by query
o - get ongoings
"""


def _pretty_print(items: Sequence[Any]):
    for i, item in enumerate(items):
        print(f"[{i + 1}] {item}")


def _choice(items: Sequence[T]) -> T:
    _pretty_print(items)
    while True:
        ch = input("> ")
        if ch.isdigit() and len(items) > int(ch) - 1:
            return items[int(ch) - 1]


def _generate_mpv_cmd(vid: "Video"):
    def _headers_to_str(headers: dict):
        result = []
        for k, v in headers.items():
            v = v.replace('"', '\\"')
            result.append(f'"{k}: {v}"')
        return ','.join(result)

    if vid.headers:
        return f"mpv {vid.url!r} --http-header-field={_headers_to_str(vid.headers)}"
    return f"mpv {vid.url!r}"


def _search_entry(e: "BaseExtractor", q: str):
    res = e.search(q)
    if not _is_empty(res):
        return
    print("choice title")
    item: "BaseSearch" = _choice(res)
    return _anime_entry(item.get_anime())


def _ongoing_entry(e: "BaseExtractor"):
    res = e.ongoing()
    if not _is_empty(res):
        return
    print("choice title")
    item: "BaseOngoing" = _choice(res)
    return _anime_entry(item.get_anime())


def _is_empty(var: T) -> bool:
    if var:
        return True
    print("not found")
    return False


def _anime_entry(a: "BaseAnime"):
    eps = a.get_episodes()
    if not _is_empty(eps):
        return
    print(a)
    print("choice episode")
    item: "BaseEpisode" = _choice(eps)

    s = item.get_sources()
    if not _is_empty(s):
        return

    print("choice source")
    item: "BaseSource" = _choice(s)
    vids = item.get_videos()
    if not _is_empty(vids):
        return

    print("choice vids")
    vid: "Video" = _choice(vids)
    print("QUALITY, HEADERS, URL")
    print(f"[{vid.quality}]", ", ".join([f"{k}={v}" for k, v in vid.headers.items()]) or None, vid.url)
    print("MPV DEBUG COMMAND:")
    print(_generate_mpv_cmd(vid))


def main(extractor: "BaseExtractor"):
    print("load:", extractor.BASE_URL)
    print("type h for get all commands. PRESS ctrl+c for exit")
    while True:
        try:
            comma = input("> ")
            if not comma:
                continue
            if comma.lower() == "h":
                print(HELP_)
            elif comma.lower().startswith('s '):
                _search_entry(extractor, comma.lstrip('s '))
            elif comma == "o":
                _ongoing_entry(extractor)
        except (KeyboardInterrupt, EOFError):
            exit(0)


def cli(extractor: "BaseExtractor"):
    """minimal dummy cli app for interactive manual tests

    usage:

        >>> from anicli_api.tools import cli
        >>> from anicli_api.source.animego import Extractor
        >>> cli(Extractor())

    """
    main(extractor)
