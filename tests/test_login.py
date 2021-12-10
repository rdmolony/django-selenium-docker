from importlib import import_module
from urllib.parse import urlparse

from django.conf import settings
from django.conf import Settings
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.contrib.auth.models import User
from django.test.client import Client
from django.contrib.sessions.backends.db import SessionStore 
import pytest
from pytest_django.live_server_helper import LiveServer
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


@pytest.fixture(autouse=True)
def override_allowed_hosts(settings: Settings) -> None:
    settings.ALLOWED_HOSTS = ["*"]  # Disable ALLOW_HOSTS


@pytest.fixture
def live_server_url() -> str:
    # Set host to externally accessible web server address
    return str(LiveServer(addr="django"))


@pytest.fixture
def browser() -> webdriver.Remote:
    browser_ = webdriver.Remote(
        command_executor='http://selenium:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME,
    )
    yield browser_
    browser_.quit()


@pytest.mark.django_db
def test_manual_admin_user_login(
    live_server_url: str, browser: webdriver.Remote, admin_user: User
) -> None:
    """
    As a superuser with valid credentials, I should gain
    access to the Django admin.
    """
    browser.get(live_server_url)

    username_input = browser.find_element_by_name('username')
    username_input.send_keys('admin')
    password_input = browser.find_element_by_name('password')
    password_input.send_keys('password')
    browser.find_element_by_xpath('//input[@value="Log in"]').click()

    path = urlparse(browser.current_url).path
    assert path == '/'

    body_text = browser.find_element_by_tag_name('body').text
    assert 'WELCOME, ADMIN.' in body_text


@pytest.fixture
def authenticated_browser(
    admin_client: Client, browser: webdriver.Remote, live_server_url: str
) -> webdriver.Remote:
    browser.get(live_server_url)
    sessionid = admin_client.cookies["sessionid"]
    cookie = {
        'name': settings.SESSION_COOKIE_NAME,
        'value': sessionid.value,
        'path': '/'
    }
    browser.add_cookie(cookie)
    browser.refresh()
    return browser


@pytest.mark.django_db
def test_auto_admin_user_login(
    live_server_url: str, authenticated_browser: webdriver.Remote, admin_user: User
) -> None:
    browser = authenticated_browser
    browser.get(live_server_url)

    path = urlparse(browser.current_url).path
    assert path == '/'

    body_text = browser.find_element_by_tag_name('body').text
    assert 'WELCOME, ADMIN.' in body_text


def test_admin_user_is_authenticated(admin_user: User) -> None:
    assert authenticate(username="admin", password="password")