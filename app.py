import math
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
    date_ranges=[DateRange(start_date="yesterday", end_date="today")],
    limit=100000,
    offset=0,
)
response = client.run_report(request)

for row in response.rows:
  game_stats_dict[row.dimension_values[0].value] = row.metric_values[0].value

# Create Tweet

victory = int(game_stats_dict['wami_victory'])
game_over = int(game_stats_dict['wami_game_over'])
total_players = victory + game_over
victory_percent = round((victory / total_players * 100), 2)
game_over_percent = round((game_over / total_players * 100), 2)
victory_emoji_count = math.floor((victory / total_players) * WIDTH)
game_over_emoji_count = math.ceil((game_over / total_players) * WIDTH)

test_word = 'test'
tweet = '🎉 WAMI STATS FOR YESTERDAY 🎉\n' \
+ 'The answer was ' + test_word.upper() + '!\n' \
+ str(total_players) + ' people played WAMI yesterday\n' \
+ str(victory_percent) + '% got the answer correct!\n' \
+ '     ' + '🟩'* victory_emoji_count + '🟥' * game_over_emoji_count + '\n' \
+ '#WAMI #wordgame #bot #statistics'

# Twitter API

print(tweet)

# client = tweepy.Client(bearer_token=BEARER_TOKEN, consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)
# response = client.create_tweet(text=tweet)