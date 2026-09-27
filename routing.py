import networkx as nx


def create_road_network():

    graph = nx.Graph()

    roads = [
        ("Warehouse A", "Road 1", 10, False),
        ("Road 1", "Camp 1", 15, False),

        ("Warehouse A", "Road 2", 12, True),
        ("Road 2", "Camp 2", 10, True),

        ("Warehouse B", "Road 3", 8, False),
        ("Road 3", "Camp 3", 12, False),

        ("Warehouse B", "Road 4", 15, False),
        ("Road 4", "Camp 4", 20, False),

        ("Warehouse C", "Road 5", 10, False),
        ("Road 5", "Camp 5", 18, False),

        ("Warehouse C", "Road 6", 8, True),
        ("Road 6", "Camp 4", 12, True),
    ]

    for start, end, distance, flooded in roads:

        # Flooded roads cannot be used.
        if not flooded:
            graph.add_edge(
                start,
                end,
                distance=distance
            )

    return graph


def find_route(warehouse, camp):

    graph = create_road_network()

    try:

        route = nx.shortest_path(
            graph,
            warehouse,
            camp,
            weight="distance"
        )

        distance = nx.shortest_path_length(
            graph,
            warehouse,
            camp,
            weight="distance"
        )

        return route, distance

    except nx.NetworkXNoPath:

        return None, None
