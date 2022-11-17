"""Dynamic import extractor form **anicli_api/extractors** directory"""

from abc import ABC, abstractmethod
from typing import cast, Protocol, Type
import importlib
import pathlib
import logging

from anicli_api.base import *

__all__ = (
    'ModuleExtractor',
    'BaseExtractorLoader',
    'ExtractorLoader',
)

# check Extractor signature
VALID_CLASSES = (
    'Extractor',
    'SearchResult',
    'Ongoing',
    'AnimeInfo',
    'Episode',
    'Video',
    'TestCollections'
)


class ModuleExtractor(Protocol):
    """Typehints dyn imported extractor"""
    Extractor: Type[BaseAnimeExtractor]
    SearchResult: Type[BaseSearchResult]
    Ongoing: Type[BaseOngoing]
    AnimeInfo: Type[BaseAnimeInfo]
    Episode: Type[BaseEpisode]
    Video: Type[BaseVideo]
    TestCollections: Type[BaseTestCollections]


class BaseExtractorLoader(ABC):

    @classmethod
    @abstractmethod
    def load(cls, *, module_name: str):
        ...


class ExtractorLoader(BaseExtractorLoader):

    @staticmethod
    def _get_extractor_path() -> pathlib.Path:
        if __name__ == "__main__":
            return pathlib.Path('extractors')
        else:
            return pathlib.Path('anicli_api') / pathlib.Path('extractors')

    @staticmethod
    def _validate(extractor: ModuleExtractor, module_name: str):
        for cls in ModuleExtractor.__dict__["__annotations__"].keys():
            try:
                getattr(extractor, cls)
            except AttributeError as exc:
                raise AttributeError(f"Module '{module_name}' has no class '{cls}'. It is a real Extractor?") from exc

    @staticmethod
    def _import(module_name: str) -> ModuleExtractor:
        try:
            module_name = module_name.replace('/', '.').replace('\\', '.').rstrip('.py')
            extractor = cast(ModuleExtractor, importlib.import_module(module_name, package=None))
        except ModuleNotFoundError as e:
            raise ModuleNotFoundError(f"'{module_name}' not found") from e
        return extractor

    @staticmethod
    def _path_to_import(module_path: str) -> str:
        return module_path.replace('/', '.').replace('\\', '.').rstrip('.py')

    @classmethod
    def load(cls, module_name: str) -> ModuleExtractor:
        if cls._check_module_name(module_name):
            file_import = cls._path_to_import(module_name)
            mdl = cls._import(file_import)
            cls._validate(mdl, file_import)
            return mdl
        cls._import(module_name)  # try import. If error with module_name, throw ModuleNotFoundError
        raise AttributeError(f"'{module_name}' is not Extractor")

    @staticmethod
    def _check_module_name(module: str) -> bool:
        module = module.rstrip(".py").split(".")[-1]
        return not module.startswith("_") and not module.endswith("_") and module != "base.py"

    @classmethod
    def load_all(cls) -> List[ModuleExtractor]:
        modules = []
        for file in cls._get_extractor_path().iterdir():
            if cls._check_module_name(file.name):
                file_import = cls._path_to_import(str(file))
                mdl = cls._import(file_import)
                cls._validate(mdl, file_import)
                modules.append(cls._import(file_import))
        return modules

    @staticmethod
    def _test_module(module: ModuleExtractor, throw_exception: bool = True) -> None:
        # sourcery skip: use-fstring-for-formatting
        test_class = module.TestCollections
        for attr in test_class.__dict__.keys():
            if attr.startswith("test"):
                logging.debug("MODULE {} RUN {}".format(module.__str__().split("/")[-1], attr))
                try:
                    getattr(test_class(), attr)()
                except AssertionError as e:
                    if throw_exception:
                        raise e
                    else:
                        logging.error(e)
                else:
                    logging.debug("[OK] {} {}".format(module.__str__().split("/")[-1], attr))

    @classmethod
    def run_test(cls, module_name: str, *, throw_exception: bool = True):
        module = cls.load(module_name)
        cls._test_module(module, throw_exception)

    @classmethod
    def run_test_all(cls, *, throw_exception: bool = True):
        for module in cls.load_all():
            cls._test_module(module, throw_exception)
