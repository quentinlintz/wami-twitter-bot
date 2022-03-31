# WAMI Twitter Bot

## Dependencies

* google-analytics-data: Google Analytics connection to query the daily stats.
* python-dotenv: Processing environment variables
* tweepy: Twitter API to send the tweets.

## Getting Started

Google Analytics has a key.json credential file that should be in the root of this project. The path to this file should be set as an environment variable when testing locally:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/key.json"
```

Create a .env file with the environment variables found in settings.py. Set DEBUG=true to print the tweet rather than tweeting it out with the Twitter API. The WAMI environment variables is from the AWS API endpoint.

## Running

To run the script:

```bash
python3 app.py
```

## Deployment

This bot is deployed on Heroku. The worker is disabled. Instead, a Heroku Scheduler is used to schedule daily runs of this script.

[heroku-google-application-credentials-buildpack](https://github.com/gerywahyunugraha/heroku-google-application-credentials-buildpack) should be installed to populate the key.json on Heroku.