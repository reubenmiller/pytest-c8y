## pytest-c8y

pytest-c8y is a plugin for `pytest <http://pytest.org>`_ that provides
support for running `Cumulocity IoT <https://www.softwareag.cloud/site/product/cumulocity-iot.html>`_ based tests.

## Getting started

1. Install poetry

    ```sh
    curl -sSL https://install.python-poetry.org | python3 -
    ```

2. Install the dependencies

    ```sh
    poetry install
    ```

3. Activate the virtual env

    ```sh
    poetry env use python3
    ```

    If you are using VSCode then you can set the python interpreter to the virtualenv printed out to the console. This will enable you to run your tests from the editor.

4. Start an interactive shell

    ```sh
    poetry shell
    ```

## Tests

1. Create a .env (use the `.env.template` as a template) and fill

2. Activate the virtualenv shell

    ```sh
    poetry shell
    ```

4. Run the tests

    ```sh
    dotenv run python3 -m pytest testing
    ```
