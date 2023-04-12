# Inverse Finance Twitter Bot

This project is a Twitter bot that interacts with the Inverse Finance API to fetch and process data, then posts tweets containing the processed data. The bot posts information about top APY pools (both stable and volatile), DOLA liquidity, protocol-owned liquidity, and average APY.

## Getting Started

These instructions will help you set up and run the project on your local machine.

### Prerequisites

You need Python 3.10.10 to run this project. Install the required packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```


## Setting up environment variables

Create a .env file in the root directory of the project with the following variables:

```
TWITTER_CONSUMER_KEY=<your_consumer_key>
TWITTER_CONSUMER_SECRET=<your_consumer_secret>
TWITTER_ACCESS_TOKEN=<your_access_token>
TWITTER_ACCESS_TOKEN_SECRET=<your_access_token_secret>
TWITTER_BEARER_TOKEN=<your_bearer_token>
```

Replace <your_consumer_key>, <your_consumer_secret>, <your_access_token>, <your_access_token_secret>, and <your_bearer_token> with your actual Twitter API keys and tokens.

## Running the project

Import and use the functions from helpers.py to interact with the Inverse Finance API and post tweets.

For example, you can use the following commands in your main script:


```
from helpers import post_stable, post_volatile, post_liquidity

post_stable()
post_volatile()
post_liquidity()
```

These commands will fetch data from the Inverse Finance API, process it, and post tweets with the relevant information.

## Scheduler and Server

The scheduler and server are already set up in the main.py file. The scheduler uses APScheduler to run the tweet posting process periodically, and the Flask application serves as the server.

No additional configuration is needed for the scheduler and server. To run the application, simply execute:


```
python main.py
```

This will start the scheduler and the Flask server. The server will listen on the default port (8080) and the scheduler will execute the tweet posting process at the specified intervals.

## Health Check

The application includes a simple health check endpoint to ensure that the server is running and responding to requests. To access the health check, navigate to http://localhost:8080/healthcheck. 