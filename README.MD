# anicli_api_anigo_auth

A fork of [anicli-api](https://github.com/vypivshiy/anicli-api) with the ability to log in to [animego.org](https://animego.org) accunt.

# Example of use:
```python
from anicli_api.source.animego import Extractor, animego_set_PHPSESSID

set_PHPSESSID("your_PHPSESSID_of_cookies_animego")

if __name__ == '__main__':
    ex = Extractor()
    results = ex.search("Bocchi the Rock!")
    anime = results[0]
    
    anime.set_rate(10)
```

*The code was intentionally not rewritten significantly.*
