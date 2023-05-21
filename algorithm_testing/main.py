from matplotlib.lines import Line2D

import time
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import OPTICS
import hdbscan

import matplotlib.pyplot as plt


def generate_random_clusters(num_clusters, num_points_per_cluster, noise_level):
    clusters = []

    # Generate random clusters
    for _ in range(num_clusters):
        center = np.random.uniform(0, 300, size=2)  # Random center for each cluster
        cluster = center + np.random.randn(num_points_per_cluster, 2) * noise_level
        clusters.append(cluster)

    # Add some random noise points
    noise_points = np.random.uniform(0, 300, size=(int(num_points_per_cluster / 2), 2))
    clusters.append(noise_points)

    return clusters


def run_clustering_algorithms(points):
    algorithms = {
        'K-means': KMeans(n_clusters=10, n_init='auto'),
        'DBSCAN': DBSCAN(eps=10, min_samples=5),
        'OPTICS': OPTICS(eps=10, min_samples=5),
        'HDBSCAN': hdbscan.HDBSCAN(min_samples=5, min_cluster_size=3)
    }

    results = {}
    time_results = {}

    for algorithm_name, algorithm in algorithms.items():
        print(f"Running {algorithm_name} algorithm...")
        start_time = time.time()

        # Fit the algorithm to the data
        algorithm.fit(points)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{algorithm_name} algorithm executed in {execution_time:.4f} seconds.")
        time_results[algorithm_name] = execution_time
        # Save the cluster labels
        results[algorithm_name] = algorithm.labels_

    # Plot the clustering results
    plot_clustering_results(points, results)

    return time_results


def run_multiple_times(num_times):
    num_clusters = 10
    points_per_cluster = 30
    noise_level = 20

    total_time_results = {}

    for i in range(num_times):
        separate_clusters = generate_random_clusters(num_clusters, points_per_cluster, noise_level)
        concat_clusters = np.concatenate(separate_clusters)
        time_results = run_clustering_algorithms(concat_clusters)

        # Add the current run's time results to the total
        for algorithm_name, execution_time in time_results.items():
            if algorithm_name in total_time_results:
                total_time_results[algorithm_name] += execution_time
            else:
                total_time_results[algorithm_name] = execution_time

    # Calculate the average runtime for each algorithm
    avg_time_results = {}

    for algorithm_name, total_execution_time in total_time_results.items():
        avg_execution_time = total_execution_time / num_times
        avg_time_results[algorithm_name] = avg_execution_time

    return avg_time_results


def plot_clustering_results(points, results):
    # Plotting parameters
    plt.figure(figsize=(15, 10))
    plt.subplots_adjust(left=.02, right=.98, bottom=.001, top=.96, wspace=.05, hspace=.01)
    plot_num = 1

    # Iterate over each algorithm's results and plot them
    for algorithm_name, cluster_labels in results.items():
        # Create a subplot for the algorithm
        plt.subplot(2, 2, plot_num)

        # Get a unique color for each cluster
        num_clusters = len(np.unique(cluster_labels))
        cmap = plt.cm.get_cmap('viridis', num_clusters)

        # Plot the points with the assigned labels
        cluster_alpha = max(0.5, 1.0 / len(points))
        plt.scatter(points[:, 0], points[:, 1], c=cluster_labels, cmap=cmap, alpha=cluster_alpha)

        # Set the subplot title and adjust the layout
        plt.title(algorithm_name)
        plt.axis('equal')
        plt.subplots_adjust(hspace=0.4)
        plot_num += 1

        # Add legend for clusters
        legend_handles = []
        for i in range(num_clusters):
            color = cmap(i)
            handle = Line2D([0], [0], marker='o', color=color, label=f'Cluster {i}', markersize=10)
            legend_handles.append(handle)
        plt.legend(handles=legend_handles)

    # Show the plot
    plt.show()


if __name__ == '__main__':
    # Example usage:
    num_clusters = 5
    num_points_per_cluster = 30
    noise_level = 25.0

    separate_clusters = generate_random_clusters(num_clusters, num_points_per_cluster, noise_level)
    concat_clusters = np.concatenate(separate_clusters)
    time_results = run_clustering_algorithms(concat_clusters)

    """
     num_times = 50
     avg_times = run_multiple_times(num_times)
     print("Average Runtimes:")
     for algorithm_name, avg_execution_time in avg_times.items():
        print(f"{algorithm_name}: {avg_execution_time:.4f} seconds")
    """