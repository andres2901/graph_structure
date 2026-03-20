#!/usr/bin/env python3
"""
Graph Analyzer package

This package perform a structural analysis of an undirected graph
and their attribute-defined subgraphs. returning multiple metrics
related to size, density, connectivity and centrality.
"""

import sys
import argparse
import numpy as np
import pandas as pd

def load_graph(edges_file: str, node_file: str, attribute: str) \
    -> list[pd.DataFrame, pd.DataFrame]:
    """Check and store the input files of the graph

    Args:
        gff_path: Path to the input GFF file.
        fasta_path: Path to the input fasta file.

    Returns:
        list [edges_df, nodes_df] where:
            - edges_df: pandas dataframe of edges in a network.
            - nodes_df: pandas dataframe of nodes attributes of a network.

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
    except FileNotFoundError:
        sys.exit(f"Error: Data file '{node_file}' not found.")
    except PermissionError:
        sys.exit(f"Error: No read permission for '{node_file}'.")
    except pd.errors.ParserError as e:
        sys.exit(f"Error parsing data file '{node_file}': {e}")
        
    if attribute not in nodes_df.columns:
        print(f"Atribute '{attribute}' is not available in the given node atribute table")
        sys.exit(1)

    nodes_id = np.sort(nodes_df["NodeID"].values)
    nodes_id2 = np.unique(np.array([edges_df["Source"].values,edges_df["Target"].values]))
    
    if not np.array_equal(nodes_id, nodes_id2):
        difference = np.setxor1d(nodes_id,nodes_id2)
        print(f"The following nodes differ between files:")
        print(f"{difference}")
        sys.exit(1)
        
    return edges_df, nodes_df

def main() -> None:
    """Parse command-line arguments and launch the graph analyzer pipeline."""
    parser = argparse.ArgumentParser(description="Structural analysis of graph and attribute-base subgraphs")
    parser.add_argument('-e', '--edges-file', type=str, required=True, help="Input TSV file with edges.")
    parser.add_argument('-n', '--node-file', type=str, required=True, help="Input TSV file with node attributes.")
    parser.add_argument('-o', '--output-dir', type=str, default='./', help="Directory for output files.")
    parser.add_argument('-a', '--attribute', type=str, default=1, help="Name of the attribute for subgraphs")

    args = parser.parse_args()
    edges, nodes = load_graph(args.edges_file, args.node_file, args.attribute)
    
if __name__ == "__main__":
    main()
