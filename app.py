from settings import PROPERTY_ID
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Filter
from google.analytics.data_v1beta.types import FilterExpression
from google.analytics.data_v1beta.types import FilterExpressionList
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest

game_stats_dict = {}
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
                            values=["wami victory", "wami game over"]
                        )
                    )
                ),
                FilterExpression(
                    filter=Filter(
                        field_name="pageTitle",
                        string_filter=Filter.StringFilter(
                            value="WAMI - Guess the Word - Quentin Lintz"),
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

# {'wami victory': '5'}
print(game_stats_dict)

