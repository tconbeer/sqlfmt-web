# sqlfmt-web
The code behind sqlfmt.com, a web UI for sqlfmt.

This project uses [pywebio](https://www.pyweb.io/), which makes it very simple.

It is deployed on Heroku.

## Running locally

### Using Heroku (recommended)
1. Install the Heroku CLI: `brew install heroku/brew/heroku`
2. Launch the application: `heroku local web`
3. Open a browser and visit `http://localhost:5000`. Voila

### Using Poetry
1. Install Python and poetry
2. Install dependencies into a venv with `poetry install`
3. Start the server with `poetry run sqlfmt-web`
4. Open a browser and visit `http://localhost:8080`. Voila

## Deploying
1. Create a new branch, make commits to that branch
2. Open a PR to main
3. When the PR to main is merged, Heroku will automatically deploy the new code to prod