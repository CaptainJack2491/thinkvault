## What this is?
Its a simple python program that uses OPENAI API to generate a obsidian compatible notes from any youtube video.

## How to install?
- clone the repo
    ```bash
    git clone https://github.com/CaptainJack2491/thinkvault
    ```

- install requirements
    ```bash
    pip install -r requirements.txt
    ```

    note: if you are on mac or linux, you might need to download the requirements in a virtual environment, for that run the following commands:

    ```bash
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    ```

- add the openai api key
    - create an api key from (openai)[https://platform.openai.com/api-keys]
    - put that api key in the .env file
    ```.env
    OPENAI_API_KEY = YOUR_OPENAI_API_KEY
    ```

- run the program
    ```bash
    python3 main.py
    ```


The summaries along with your thoughts on it will be stored in a summaries folder in the root directory.
