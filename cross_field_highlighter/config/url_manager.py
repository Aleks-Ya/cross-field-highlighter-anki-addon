import logging
from enum import Enum
from logging import Logger
from typing import NewType

log: Logger = logging.getLogger(__name__)

URL = NewType("URL", str)


class UrlType(Enum):
    ADDON_INFO_PAGE = 1
    GITHUB = 2
    SUPPORT_THREAD = 3
    SONAR_QUBE = 4
    CHANGELOG = 5


class UrlManager:
    __links: dict[UrlType, URL] = {
        UrlType.ADDON_INFO_PAGE: "https://ankiweb.net/shared/info/1312127886",
        UrlType.GITHUB: "https://github.com/Aleks-Ya/cross-field-highlighter-anki-addon",
        UrlType.SUPPORT_THREAD: "https://forums.ankiweb.net/t/cross-field-highlighter-addon-spotlight-word-in-text-support-thread",
        UrlType.SONAR_QUBE: "https://sonarcloud.io/summary/overall?id=Aleks-Ya_cross-field-highlighter-anki-addon&branch=master",
        UrlType.CHANGELOG: "https://github.com/Aleks-Ya/cross-field-highlighter-anki-addon/blob/master/CHANGELOG.md"
    }

    def __init__(self) -> None:
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_url(self, url_type: UrlType) -> URL:
        return URL(self.__links[url_type])

    def get_all_urls(self) -> dict[UrlType, URL]:
        return {url_type: self.get_url(url_type) for url_type in UrlType}
