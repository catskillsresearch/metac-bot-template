curl -X 'GET' \
  'https://www.metaculus.com/api/posts/?tournaments=3349&tournaments=32506&tournaments=32627&tournaments=32721&statuses=resolved&limit=100&offset=0&forecast_type=binary&forecast_type=numeric&forecast_type=date&forecast_type=multiple_choice&forecast_type=conditional&forecast_type=group_of_questions&forecast_type=notebook&order_by=-published_at' \
  -H 'accept: application/json' \
  -H 'Authorization: 53fa494e32f946af249a72b918c5c8c62410fd9d' > questions1.json
  