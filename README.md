# Example: Django Selenium Tests on Pytest with Docker

> I've adapted [marcgibbons/django-selenium-docker](https://github.com/marcgibbons/django-selenium-docker) replacing `unittest` with `pytest` with the help of `pytest-django`

## Requirements
- Docker
- Docker-compose
- VNC Viewer (optional for debugging)
  - [NoVNC](https://github.com/novnc/noVNC)
  - or [RealVNC](https://www.realvnc.com/en/connect/download/viewer/)

## Installation

`$ docker-compose build`

## Running the tests

1. Start the selenium container:

   `$ docker-compose start selenium`

2. Open VNC Viewer and connect to `localhost:5900`. Password is `secret`

3. Run the tests

   ```bash
   $ docker-compose run django bash
   $ pytest
   ```
