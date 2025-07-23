def get_forecastex_markets(tree):
    results = []

    def recurse(node):
        if not isinstance(node, dict):
            return

        for value in node.values():
            if isinstance(value, dict):
                # Check if this node has ForecastEx markets
                if value.get('markets'):
                    for market in value['markets']:
                        if market.get('exchange') == 'FORECASTX':
                            results.append({
                                'symbol': market['symbol'],
                                'conid': market['conid'],
                                'name': market.get('name', '')
                            })
                recurse(value)
                
    recurse(tree)
    return results