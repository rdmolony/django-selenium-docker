import socket
from urllib.parse import urlparse

from django.db import connection
import pytest
from pytest_django.live_server_helper import LiveServer
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


@pytest.fixture(autouse=True)
def override_allowed_hosts(settings):
    settings.ALLOWED_HOSTS = ["*"]  # Disable ALLOW_HOSTS


@pytest.fixture
def live_server_at_host():
    # Set host to externally accessible web server address
    host = socket.gethostbyname(socket.gethostname())
    return LiveServer(addr=host)


@pytest.fixture
def driver_init():
    remote_driver = webdriver.Remote(
        command_executor='http://selenium:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME,
    )
    remote_driver.implicitly_wait(5)
    yield remote_driver
    remote_driver.close()


@pytest.mark.django_db(transaction=True)
def test_admin_user_login(live_server_at_host, driver_init, admin_user):
    """
    As a superuser with valid credentials, I should gain
    access to the Django admin.
    """
    driver = driver_init
    live_server_url = str(live_server_at_host)

    driver.get(live_server_url)
    username_input = driver.find_element_by_name('username')
    username_input.send_keys('admin')
    password_input = driver.find_element_by_name('password')
    password_input.send_keys('password')
    driver.find_element_by_xpath('//input[@value="Log in"]').click()

    path = urlparse(driver.current_url).path
    import pdb; pdb.set_trace()
    assert path == '/'

    body_text = driver.find_element_by_tag_name('body').text
    assert 'WELCOME, ADMIN.' in body_text