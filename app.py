import math
import json
import requests
import tweepy
from settings import * 
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Filter
from google.analytics.data_v1beta.types import FilterExpression
from google.analytics.data_v1beta.types import FilterExpressionList
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest

WIDTH = 10
game_stats_dict = {}
tweet = ''

# Google Analytics API

client = BetaAnalyticsDataClient()

request = RunReportRequest(
    property=f"properties/{PROPERTY_ID}",
    dimensions=[Dimension(name='eventName'), Dimension(name='pageTitle')],
    dimension_filter=FilterExpression(
        and_group=FilterExpressionList(
            expressions=[
                FilterExpression(
                    filter=Filter(
                        field_name="eventName",
                        in_list_filter=Filter.InListFilter(
                            values=["wami_victory", "wami_game_over"]
                        )
                    )
                ),
                FilterExpression(
                    filter=Filter(
                        field_name="pageTitle",
                        string_filter=Filter.StringFilter(
                            value="WAMI - Guess the Word"),
                    )
                ),
            ]
        )
    ),
    metrics=[Metric(name="activeUsers")],
    date_ranges=[DateRange(start_date="2daysAgo", end_date="1daysAgo")],
    limit=100000,
    offset=0,
)
response = client.run_report(request)

# Populate the game_stats_dict with Google Analytics data
if len(response.rows) != 0:
  for row in response.rows:
    game_stats_dict[row.dimension_values[0].value] = row.metric_values[0].value
else:
  # If there is no data, add dummy data
  game_stats_dict['wami_victory'] = 1
  game_stats_dict['wami_game_over'] = 1

# Create Tweet
victory = int(game_stats_dict['wami_victory'])
game_over = int(game_stats_dict['wami_game_over'])
total_players = victory + game_over
victory_percent = round((victory / total_players * 100), 2)
game_over_percent = round((game_over / total_players * 100), 2)
victory_emoji_count = math.floor((victory / total_players) * WIDTH)
game_over_emoji_count = math.ceil((game_over / total_players) * WIDTH)

# Twitter API

challenge_data = requests.get(WAMI_URL, headers={'x-api-key': WAMI_API_KEY})
json_data = json.loads(challenge_data.content)

tweet = '🎉 #WAMI STATS FOR ' + str(json_data['date']) + ' 🎉\n' \
+ 'The answer was #' + json_data['answer'].upper() + '!\n' \
+ str(total_players) + ' people played WAMI yesterday\n' \
+ str(victory_percent) + '% got the answer correct!\n' \
+ '🟩'* victory_emoji_count + '🟥' * game_over_emoji_count + '\n'

client = tweepy.Client(bearer_token=BEARER_TOKEN, consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)
response = client.create_tweet(text=tweet)