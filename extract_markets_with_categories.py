# The input data is assumed to be loaded into a variable named `data`.
# For example: data = {...}  # the given JSON structure loaded as a dictionary

def extract_markets_with_categories(data):
    # Prepare a lookup dictionary of all nodes by their ID to facilitate parent name access
    nodes = data

    # Cache node id to name mapping
    id_to_name = {node_id: node['name'] for node_id, node in nodes.items()}

    # Function to recursively build category path for a node
    def build_category_path(node_id):
        path = []
        current_id = node_id
        while current_id in nodes and 'parent_id' in nodes[current_id]:
            parent_id = nodes[current_id].get('parent_id')
            if parent_id is None:
                break
            path.append(id_to_name.get(parent_id, ''))
            current_id = parent_id
        return list(reversed(path))

    # Recursive function to traverse hierarchy starting at given node
    def traverse(node_id):
        node = nodes[node_id]
        markets_list = []

        # If node contains markets, process them
        if 'markets' in node:
            category = build_category_path(node_id)
            # include current node's own name at the end, since leading to market
            category.append(node['name'])

            for market in node['markets']:
                # Add category field (copy to avoid mutation)
                market_copy = dict(market)
                market_copy['category'] = category
                markets_list.append(market_copy)

        # Find children nodes (nodes where this node_id is their parent_id)
        children = [nid for nid, n in nodes.items() if n.get('parent_id') == node_id]

        for child_id in children:
            markets_list.extend(traverse(child_id))

        return markets_list

    # Find root nodes (nodes without a parent_id)
    root_nodes = [nid for nid, n in nodes.items() if 'parent_id' not in n or n['parent_id'] is None]

    # Collect all markets with categories from all root nodes
    all_markets = []
    for root_id in root_nodes:
        all_markets.extend(traverse(root_id))

    return all_markets


# Example usage:
# Assuming the JSON content you provided is loaded into a variable `data`
# markets_with_categories = extract_markets_with_categories(data)
# for market in markets_with_categories:
#     print(market)

