# Hackathon Ponts ENPC

## Install

- when opening VSCode, install the suggested extensions (Python, Black Formatter and Pylance)
(dans le terminal bash: py -m venv .venv) - create your python environment `python3 -m venv .venv`
- copy the `.env.example` file to a `.env` file
- replace the `OPENAI_API_KEY` env variables with the real values
(dans git bash: source .venv/Scripts/activate)- activate your environment with `source .venv/bin/activate`
- install the requirements with `pip install -r requirements.txt`
- download necessary data with `python -m nltk.downloader all`
  (changer la version openai: pip install openai==0.28  )
- run the server with `flask --app main run --debug` (dans le powershell: flask run)


The server should answer on http://localhost:5000

You can deactivate the environment with `deactivate`.

## Adding librairies

if you need to use a new librairies, you can do it with pip
`pip install [library name]` or `pip3 install [library name]`
