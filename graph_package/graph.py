import networkx as nx
import pandas as pd
import numpy as np

# CONSTANTS

UW = "Unweighted"
W = "Weighted"
VALID_TYPES = {W, UW}


class GraphObject:
    """
    A class used to represent graphs and their related metrics.

    Attributes:
        edges: Pandas dataframe of edges
        nodes: Pandas dataframe of node attributes
        graph_type: Type of graph
        records: List of records loaded from the input file.
        results: List of processed results.
    """

    def __init__(
        self,
        edges: pd.DataFrame,
        nodes: pd.DataFrame,
        graph_type: str
    ) -> None:
        """Initialize the DataProcessor with file paths and parameters.

        Args:
            edges: pandas dataframe of edges in a network.
            nodes: pandas dataframe of nodes attributes of a network.
            graph_type: string identifying the type of graph: weighted or unweighted
            graph: NetworkX graph.
            node_number: Number of nodes in the graph.
            egde_number: NUmber of edges in the graph.
            density: dnsity of the graph.

        Raises:
            ValueError: If the graph type is not valid.
        """

        if graph_type not in VALID_TYPES:
            raise ValueError(f"Invalid graph_type '{graph_type}'. Must be '{W}' or '{UW}'.")

        self.graph_type = graph_type
        self.edges = edges
        self.nodes = nodes

        if self.graph_type == W:
        
            graph = nx.Graph()
            for _, row in self.edges.iterrows():
                graph.add_edge(row["Source"], row["Target"], weight=float(row["Weight"]))
        elif self.graph_type == UW:
            pairs = [tuple(x) for x in self.edges[["Source", "Target"]].to_numpy(dtype = str)]
            graph = nx.Graph(pairs)
        else:
            raise ValueError(f"Unknown graph type: '{self.graph_type}'. "
                             f"Use '{W}' or '{UW}'.")

        self.graph = graph

        print(f"Graph built: {graph.number_of_nodes()} nodes, "
              f"{graph.number_of_edges()} edges ({self.graph_type}).")


    def composition_metrics(
        self) -> None:
        """Calculate the composition-related metrics of the graph"""

        self.node_number = self.graph.number_of_nodes()
        self.edge_number = self.graph.number_of_edges()
        self.density = nx.density(self.graph)