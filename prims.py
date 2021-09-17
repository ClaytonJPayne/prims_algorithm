import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def importGraphData(graph_data):
    
    """Imports .csv of graph data to DataFrame"""
    
    graph_df = pd.read_csv(graph_data)
    print("Original Graph:\n")
    print(graph_df)

    return graph_df

def findMinimalTree(graph_df, number_points):
    
    """Find edges of minimally spanning tree, determine if connected"""
    
    tree_verts = []     # Create empty sets for tree
    tree_edges = []     
    tree_verts += [graph_df.iloc[0]['v1']]  # Add arbitrary vertex to tree to start

    print("\n----------------------------------------------------")
    print("\nSTEPS IN PRIM'S ALGORITHM:")

    print("\nStarting point: "+str(tree_verts[0]))
    
    while True:

        possible_edges = {} # Generate set of edges with one vert in and one out

        for edge, data in graph_df.iterrows():
            v1, v2, weight = data['v1'], data['v2'], data['weight']
            if edge in tree_edges:
                continue
            elif ((v1 not in tree_verts) and (v2 not in tree_verts)):
                continue
            elif ((v1 in tree_verts) and (v2 in tree_verts)):
                continue
            elif ((v1 in tree_verts) and (v2 not in tree_verts)):
                possible_edges[edge] = {'vert not in':v2, 'weight':weight}
            elif ((v1 not in tree_verts) and (v2 in tree_verts)):
                possible_edges[edge] = {'vert not in':v1, 'weight':weight}

        if len(possible_edges) == 0: # If no more possible edges; we're done.
           break

        print("\n"+str(possible_edges))
        weights = [data['weight'] for edge, data in possible_edges.items()]
        lowest_weight = min(weights)

        for edge, data in possible_edges.items(): # Pick edge of min. weight and add to tree
            if data['weight'] == lowest_weight:
                tree_edges += [edge]
                tree_verts += [data['vert not in']]
                print("Edge selected: "+str(edge)+"\nVertices: "+str(graph_df.loc[edge,'v1'])+str(graph_df.loc[edge,'v2']))
                break

    if len(tree_verts) == number_points: # Check to see if graph is connected
        print("\n----------------------------------------------------")
        print("\nGraph connected; spanning tree exists!\n")
        print("Minimal Spanning Tree:")
        connected = True
        
    else:
        print("\n----------------------------------------------------")
        print("\nGraph disconnected; no spanning tree exists. :(\n")
        print("Non-spanning tree:")
        connected = False

    tree_edges_df = pd.DataFrame()
    
    for e in tree_edges:
        tree_edges_df = tree_edges_df.append(graph_df.iloc[e])
        
    print("\n"+str(tree_edges_df))
    print("\n***********************************************************************")
    print("***********************************************************************\n")

    return (tree_edges_df, connected)

def getAdjacencyList(graph_df):
    
    """Determine adjacency list / number of points in graph"""
    
    points = []
    adjacency = {}
    unit_length = 25
    
    for edge, data in graph_df.iterrows():
        if data['v1'] not in points:
            points += [data['v1']]
        if data['v2'] not in points:
            points += [data['v2']]

    for point in points:
        adjacency[point] = []
        for edge, data in graph_df.iterrows(): # Populate adjacency list
            if data['v1'] == point:
                adjacency[point] += [data['v2']]
            if data['v2'] == point:
                adjacency[point] += [data['v1']]

    print("\nAdjacency List: " + str(adjacency))

    return len(points)

def createGraphs(edges, points):
    
    """Graph the stuff"""
    
    graph_df = importGraphData(edges)
    points_df = pd.read_csv(points, index_col="vertex")
    number_points = getAdjacencyList(graph_df)
    tree_edges_df, connected = findMinimalTree(graph_df, number_points)

    xmin = min(points_df['x']) - 10
    xmax = max(points_df['x']) + 10
    ymin = min(points_df['y']) - 10
    ymax = max(points_df['y']) + 20

    # Original graph
    plt.scatter(points_df['x'], points_df['y'], s=30, c='black')
    plt.title("Original graph",
              loc='center',
              y=1.0,
              fontdict={'fontsize':15} )
    plt.axis([xmin, xmax, ymin, ymax])
    plt.axis('off')

    for point, coordinates in points_df.iterrows():
        plt.annotate(str(point),
                     color='blue',
                     xy=(coordinates['x']-7,
                         coordinates['y']+7),
                     fontsize=15)

    for edge, data in graph_df.iterrows():
        v1 = data['v1']
        v2 = data['v2']
        v1_x = points_df.loc[v1, 'x']
        v1_y = points_df.loc[v1, 'y']
        v2_x = points_df.loc[v2, 'x']
        v2_y = points_df.loc[v2, 'y']
        
        plt.annotate(text=None,
                     xy = ( v2_x, v2_y ),
                     xytext = ( v1_x, v1_y ),
                     arrowprops = {'width':0.2, 'headwidth':0.2}
                     )
        
        plt.annotate(text=data['weight'],
                     color='r',
                     xy = ( ((v1_x + v2_x)/2 + 1) , ((v1_y + v2_y)/2 + 4) )
                     )
    plt.show()

    # Tree
    plt.scatter(points_df['x'], points_df['y'], s=30, c='black')
    
    if connected:
        plt.title("Minimally spanning tree",
                  loc='center',
                  y=1.0,
                  fontdict={'fontsize':15})
    if not connected:
        plt.title("Non-spanning tree",
                  loc='center',
                  y=1.0,
                  fontdict={'fontsize':15})
        
    plt.axis([xmin, xmax, ymin, ymax])
    plt.axis('off')

    for point, coordinates in points_df.iterrows():
        plt.annotate(str(point),
                     color='blue',
                     xy=(coordinates['x']-7,
                         coordinates['y']+7),
                     fontsize=15)

    for edge, data in tree_edges_df.iterrows():
        v1 = data['v1']
        v2 = data['v2']
        v1_x = points_df.loc[v1, 'x']
        v1_y = points_df.loc[v1, 'y']
        v2_x = points_df.loc[v2, 'x']
        v2_y = points_df.loc[v2, 'y']
        
        plt.annotate(text=None,
                     xy = ( v2_x, v2_y ),
                     xytext = ( v1_x, v1_y ),
                     arrowprops = {'width':0.2, 'headwidth':0.2}
                     )
        
        plt.annotate(text=data['weight'],
                     color='r',
                     xy = ( ((v1_x + v2_x)/2 + 1) , ((v1_y + v2_y)/2 + 4) )
                     )
    plt.show()

print("GRAPH 1\n")
createGraphs("weighted_graph_1.csv", "weighted_graph_1_points.csv")
print("GRAPH 2\n")
createGraphs("weighted_graph_2.csv", "weighted_graph_2_points.csv")
print("GRAPH 3\n")
createGraphs("weighted_graph_3.csv", "weighted_graph_3_points.csv")
print("GRAPH 4\n")
createGraphs("weighted_graph_4.csv", "weighted_graph_4_points.csv")
    


