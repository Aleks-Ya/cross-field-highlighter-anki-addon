from urllib.parse import urlparse, ParseResult

import pytest
import requests
from bs4 import BeautifulSoup
from requests import Response

from cross_field_highlighter.config.url_manager import UrlManager, UrlType, URL


def test_get_all_urls(url_manager: UrlManager):
    urls: dict[UrlType, URL] = url_manager.get_all_urls()
    assert urls == {
        UrlType.ADDON_INFO_PAGE: 'https://ankiweb.net/shared/info/1312127886',
        UrlType.GITHUB: 'https://github.com/Aleks-Ya/cross-field-highlighter-anki-addon',
        UrlType.SUPPORT_THREAD: 'https://forums.ankiweb.net/t/cross-field-highlighter-addon-spotlight-word-in-text-support-thread',
        UrlType.SONAR_QUBE: 'https://sonarcloud.io/summary/overall?id=Aleks-Ya_cross-field-highlighter-anki-addon&branch=master',
        UrlType.CHANGELOG: 'https://github.com/Aleks-Ya/cross-field-highlighter-anki-addon/blob/master/CHANGELOG.md'
    }


@pytest.mark.skip("manually")
def test_ping_all_urls(url_manager: UrlManager):
    urls: dict[UrlType, URL] = url_manager.get_all_urls()
    failed_urls: dict[UrlType, URL] = {}
    for url_type, url in urls.items():
        response: Response = requests.get(url)
        if response.status_code >= 300:
            failed_urls[url_type] = url
            print(f"Unavailable URL {url_type} -> {url}: status code {response.status_code}")
        has_anchor: bool = "#" in url
        if has_anchor:
            soup: BeautifulSoup = BeautifulSoup(response.content, 'html.parser')
            parsed_url: ParseResult = urlparse(url)
            anchor_id: str = f"user-content-{parsed_url.fragment}"
            if anchor_id != '':
                anchor = soup.find(id=anchor_id)
                if not anchor:
                    failed_urls[url_type] = url
                    print(f"Unavailable anchor {url_type} -> {url}: '{anchor_id}'")
    if len(failed_urls) > 0:
        raise AssertionError(f"Unavailable URLS: {len(failed_urls)}")
