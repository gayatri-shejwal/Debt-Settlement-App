import networkx as nx


def calculate_total_debt(graph):
    # Initialize a dictionary to store total debt for each person
    total_debt = {node: 0 for node in graph.nodes}

    # Iterate through each edge in the graph
    for edge in graph.edges:
        # Get the source and target nodes of the edge
        source, target = edge

        # Get the amount of debt on this edge
        debt_amount = graph[source][target]['debt']

        # Update the total debt for both source and target nodes
        total_debt[source] -= debt_amount
        total_debt[target] += debt_amount

    return total_debt
