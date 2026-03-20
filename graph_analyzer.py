#!/usr/bin/env python3
"""
Graph Analyzer package

This package perform a structural analysis of an undirected graph
and their attribute-defined subgraphs. returning multiple metrics
related to composition, connectivity, assortativity, distribution
and centrality.
"""

import sys
import argparse
import numpy as np
import pandas as pd

# CONSTANTS

UW = "Unweigthed"
W = "Weighted"


def load_graph(edges_file: str, node_file: str, attribute: str) \
    -> list[pd.DataFrame, pd.DataFrame, str]:
    """Check and store the input files of the graph

    Args:
        gff_path: Path to the input GFF file.
        fasta_path: Path to the input fasta file.
        attribute: String representing the attribute for subgraphs.

    Returns:
        list [edges_df, nodes_df, graph_type] where:
            - edges_df: pandas dataframe of edges in a network.
            - nodes_df: pandas dataframe of nodes attributes of a network.
            - graph_type: String representing type of graph to analyze.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file cannot be read.
        pd.errors.ParserError: If either input file cannot be parsed.
        OSError: If any other I/O error occurs.
    """
    
    try:
        edges_df = pd.read_csv(
            edges_file, 
            sep='\t', 
            dtype={'Source': str, 'Target': str,'Weight': float}
        )
        
        if not set(["Source","Target"]).issubset(edges_df.columns.values):
            print(f"'Source' or 'Target' columns were not found in the edge file")
            sys.exit(1)
        else:
            if len(edges_df.columns) == 3:
                if "Weight" not in edges_df.columns.values:
                    print(f"'Weight' column has a bad name in the edge file")
                    sys.exit(1)
                else:
                    graph_type = UW
            elif len(edges_df.columns) > 3:
                sys.exit(f"edge file have more than three colums")
            else:
                graph_type = W
    except FileNotFoundError:
        sys.exit(f"Error: Data file '{edges_df}' not found.")
    except PermissionError:
        sys.exit(f"Error: No read permission for '{edges_df}'.")
    except pd.errors.ParserError as e:
        sys.exit(f"Error parsing data file '{edges_df}': {e}")
        
    try:
        nodes_df = pd.read_csv(
            node_file, 
            sep='\t', 
            dtype={'NodeID': str}
        )

        if "NodeID" not in nodes_df.columns.values:
            sys.exit(f"'NodeID' column is missing in node attributes file")
        else:
            if len(nodes_df.columns) == 1:
                sys.exit(f"nodes attribute file only have the NodeID column")
    except FileNotFoundError:
        sys.exit(f"Error: Data file '{node_file}' not found.")
    except PermissionError:
        sys.exit(f"Error: No read permission for '{node_file}'.")
    except pd.errors.ParserError as e:
        sys.exit(f"Error parsing data file '{node_file}': {e}")
        
    if attribute not in nodes_df.columns:
        sys.exit(f"Atribute '{attribute}' is not available in the given node atribute table")

    nodes_id_nodes = np.sort(nodes_df["NodeID"].to_numpy())
    nodes_id_edges = np.unique(np.array([edges_df["Source"].to_numpy(),edges_df["Target"].to_numpy()]))
    
    if not np.array_equal(nodes_id_nodes, nodes_id_edges):
        difference = np.setxor1d(nodes_id_nodes,nodes_id_edges)
        print(f"The following nodes differ between files:")
        print(f"{difference}")
        sys.exit(1)

    return edges_df, nodes_df, graph_type


def main() -> None:
    """Parse command-line arguments and launch the graph analyzer pipeline."""
    parser = argparse.ArgumentParser(description="Structural analysis of graph and attribute-base subgraphs")
    parser.add_argument('-e', '--edges-file', type=str, required=True, help="Input TSV file with edges.")
    parser.add_argument('-n', '--node-file', type=str, required=True, help="Input TSV file with node attributes.")
    parser.add_argument('-o', '--output-dir', type=str, default='./', help="Directory for output files.")
    parser.add_argument('-a', '--attribute', type=str, default=1, help="Name of the attribute for subgraphs")

    args = parser.parse_args()
    edges, nodes, type = load_graph(args.edges_file, args.node_file, args.attribute)
    

if __name__ == "__main__":
    main()
