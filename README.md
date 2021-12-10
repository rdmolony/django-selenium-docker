# Example: Django Selenium Tests on Pytest with Docker

> I've adapted [marcgibbons/django-selenium-docker](https://github.com/marcgibbons/django-selenium-docker) replacing `unittest` with `pytest` with the help of `pytest-django`

1. Install [`docker`](https://docs.docker.com/get-docker/)

2. Launch selenium & django

   ```bash
   docker-compose up
   ```

3. Open `localhost:7900` in your browser to view `Selenium` in action. Password is `secret`

   > `selenium/standalone-chrome` uses [`NoVNC`](https://github.com/novnc/noVNC) to hook into the running `selenium` browser

4. Hook in to the running Django container and run the tests

   ```bash
   docker exec django bash
   pytest
   ```
