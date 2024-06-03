# anicli_api_anigo_auth

A fork of [anicli-api](https://github.com/vypivshiy/anicli-api) with the ability to log in to [animego.org](https://animego.org) accunt.

# Example of use:

```python
from anicli_api.source.animego import Profile, set_PHPSESSID

set_PHPSESSID("your_PHPSESSID_of_cookies_animego")

if __name__ == '__main__':
    pf = Profile() # nickname = None -> current user

    results = pf.get_all_anime()
    anime = results[0].get_anime()

    print(anime.title) # 5 сантиметров в секунду
 
    anime.set_rate(10)

    status = anime.get_view_status()
    print(status) # {'my_status': 'Просмотрено', 'other_status': {'Отложено': 3, 'Брошено': 4, 'Запланировано': 5, 'Пересматриваю': 6}}

    anime.set_view_status(status["other_status"]["Пересматриваю"])

    episodes = anime.get_episodes()
    episode = episodes[0]

    print(episode.get_viewed()) # True
    episode.make_viewed()
```

*The code was intentionally not rewritten significantly.*
