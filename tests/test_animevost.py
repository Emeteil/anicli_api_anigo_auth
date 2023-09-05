import pytest

from anicli_api.source.animevost import Extractor

STATUS = Extractor().HTTP().get(Extractor().BASE_URL + "last").status_code


@pytest.fixture()
def extractor():
    return Extractor()


@pytest.mark.skipif(STATUS != 200, reason=f"RETURN CODE [{STATUS}]")
def test_search(extractor):
    result = extractor.search("chainsaw")
    assert result[0].dict() == {
        "id": 2872,
        "title": "Человек-бензопила / Chainsaw Man [1-12 из 12]",
        "description": "Шестнадцатилетний Дэндзи имеет далеко не подростковые проблемы, и они связаны с финансами, причем долги, не дающие спокойствия парню, наделал его отец. Родитель умер, не погасив долг, а парню придется искать способ, чтобы решить проблему. Таковой подворачивается, хоть и весьма сомнительный, и самое страшное, что грозящий опасностью. Должник заключает контракт с демоном-бензопилой, согласно которого он будет охотиться на его собратьев по виду. Помогать ему будет в этом сила Почиты, но Дэндзи должен будет кормить его своей кровью. Но за убийство демонов будут платить, что куда важнее для Дэндзи.<br>\n<br>\nПока долг все ещё не закрыт, Дэндзи вынужден заниматься не тем, чем бы хотелось. И уж явно молодой парень такую жизнь не заслуживает. Он тешит надежду, что как только погасит долг, сможет закончить с охотой на демонов. Кроме того, парень рассчитывал на то, что встретит девушку, в которую влюбится и будет себе счастливо жить. Но такие планы он не сможет принять без оглядки на желание Почиты. А пока Дэндзи трудится бензопилой и ему нравится то, чем он занимается. А демонов оказывается невероятно много, и работа Дэндзи весьма актуальна, и Почита может успокоиться за свою судьбу.",
        "genre": "приключения, сёнэн",
        "year": "2022",
        "urlImagePreview": "https://static.openni.ru/uploads/posts/2022-10/1665487278_1.jpg",
        "screenImage": [
            "/uploads/posts/2022-10/1665487366_4.jpg",
            "/uploads/posts/2022-10/1665487345_3.jpg",
            "/uploads/posts/2022-10/1665487316_2.jpg",
        ],
        "isFavorite": 0,
        "isLikes": 0,
        "rating": 27665,
        "votes": 5883,
        "timer": 0,
        "type": "ТВ",
        "director": "Накаяма Рю",
        "series": "{'1 серия':'2147422737','2 серия':'2147422797','3 серия':'2147422858','4 серия':'2147422909','5 серия':'2147422957','6 серия':'2147423004','7 серия':'2147423057','8 серия':'2147423098','9 серия':'2147423144','10 серия':'2147423205','11 серия':'2147423249','12 серия':'2147423289'}",
    }
    anime = result[0].get_anime()
    assert anime.dict() == {
        "id": 2872,
        "title": "Человек-бензопила / Chainsaw Man [1-12 из 12]",
        "description": "Шестнадцатилетний Дэндзи имеет далеко не подростковые проблемы, и они связаны с финансами, причем долги, не дающие спокойствия парню, наделал его отец. Родитель умер, не погасив долг, а парню придется искать способ, чтобы решить проблему. Таковой подворачивается, хоть и весьма сомнительный, и самое страшное, что грозящий опасностью. Должник заключает контракт с демоном-бензопилой, согласно которого он будет охотиться на его собратьев по виду. Помогать ему будет в этом сила Почиты, но Дэндзи должен будет кормить его своей кровью. Но за убийство демонов будут платить, что куда важнее для Дэндзи.<br>\n<br>\nПока долг все ещё не закрыт, Дэндзи вынужден заниматься не тем, чем бы хотелось. И уж явно молодой парень такую жизнь не заслуживает. Он тешит надежду, что как только погасит долг, сможет закончить с охотой на демонов. Кроме того, парень рассчитывал на то, что встретит девушку, в которую влюбится и будет себе счастливо жить. Но такие планы он не сможет принять без оглядки на желание Почиты. А пока Дэндзи трудится бензопилой и ему нравится то, чем он занимается. А демонов оказывается невероятно много, и работа Дэндзи весьма актуальна, и Почита может успокоиться за свою судьбу.",
        "genre": "приключения, сёнэн",
        "year": "2022",
        "urlImagePreview": "https://static.openni.ru/uploads/posts/2022-10/1665487278_1.jpg",
        "screenImage": [
            "/uploads/posts/2022-10/1665487366_4.jpg",
            "/uploads/posts/2022-10/1665487345_3.jpg",
            "/uploads/posts/2022-10/1665487316_2.jpg",
        ],
        "isFavorite": 0,
        "isLikes": 0,
        "rating": 27665,
        "votes": 5883,
        "timer": 0,
        "type": "ТВ",
        "director": "Накаяма Рю",
        "series": "{'1 серия':'2147422737','2 серия':'2147422797','3 серия':'2147422858','4 серия':'2147422909','5 серия':'2147422957','6 серия':'2147423004','7 серия':'2147423057','8 серия':'2147423098','9 серия':'2147423144','10 серия':'2147423205','11 серия':'2147423249','12 серия':'2147423289'}",
        "playlist": [
            {
                "name": "1 серия",
                "hd": "http://video.aniland.org/720/2147422737.mp4",
                "std": "http://video.aniland.org/2147422737.mp4",
                "preview": "http://media.aniland.org/img/2147422737.jpg",
            },
            {
                "name": "2 серия",
                "hd": "http://video.aniland.org/720/2147422797.mp4",
                "std": "http://video.aniland.org/2147422797.mp4",
                "preview": "http://media.aniland.org/img/2147422797.jpg",
            },
            {
                "name": "3 серия",
                "hd": "http://video.aniland.org/720/2147422858.mp4",
                "std": "http://video.aniland.org/2147422858.mp4",
                "preview": "http://media.aniland.org/img/2147422858.jpg",
            },
            {
                "name": "4 серия",
                "hd": "http://video.aniland.org/720/2147422909.mp4",
                "std": "http://video.aniland.org/2147422909.mp4",
                "preview": "http://media.aniland.org/img/2147422909.jpg",
            },
            {
                "name": "5 серия",
                "hd": "http://video.aniland.org/720/2147422957.mp4",
                "std": "http://video.aniland.org/2147422957.mp4",
                "preview": "http://media.aniland.org/img/2147422957.jpg",
            },
            {
                "name": "6 серия",
                "hd": "http://video.aniland.org/720/2147423004.mp4",
                "std": "http://video.aniland.org/2147423004.mp4",
                "preview": "http://media.aniland.org/img/2147423004.jpg",
            },
            {
                "name": "7 серия",
                "hd": "http://video.aniland.org/720/2147423057.mp4",
                "std": "http://video.aniland.org/2147423057.mp4",
                "preview": "http://media.aniland.org/img/2147423057.jpg",
            },
            {
                "name": "8 серия",
                "hd": "http://video.aniland.org/720/2147423098.mp4",
                "std": "http://video.aniland.org/2147423098.mp4",
                "preview": "http://media.aniland.org/img/2147423098.jpg",
            },
            {
                "name": "9 серия",
                "hd": "http://video.aniland.org/720/2147423144.mp4",
                "std": "http://video.aniland.org/2147423144.mp4",
                "preview": "http://media.aniland.org/img/2147423144.jpg",
            },
            {
                "name": "10 серия",
                "hd": "http://video.aniland.org/720/2147423205.mp4",
                "std": "http://video.aniland.org/2147423205.mp4",
                "preview": "http://media.aniland.org/img/2147423205.jpg",
            },
            {
                "name": "11 серия",
                "hd": "http://video.aniland.org/720/2147423249.mp4",
                "std": "http://video.aniland.org/2147423249.mp4",
                "preview": "http://media.aniland.org/img/2147423249.jpg",
            },
            {
                "name": "12 серия",
                "hd": "http://video.aniland.org/720/2147423289.mp4",
                "std": "http://video.aniland.org/2147423289.mp4",
                "preview": "http://media.aniland.org/img/2147423289.jpg",
            },
        ],
    }
    episodes = anime.get_episodes()
    assert len(episodes) == 12
    sources = episodes[0].get_sources()
    assert len(sources) == 1


@pytest.mark.skipif(STATUS != 200, reason=f"RETURN CODE [{STATUS}]")
def test_ongoing(extractor):
    result = extractor.ongoing()
    assert len(result) > 2
