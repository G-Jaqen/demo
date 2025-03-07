import numpy as np
from sklearn.neighbors import LocalOutlierFactor
from itertools import product
from sklearn.ensemble import IsolationForest


def lof_with_hyperparameters(data, flags, areas, n_neighbors, contamination, metric, algorithm, leaf_size, p_value):
    data = np.array(data)
    flags = np.array(flags)

    all_indices = []
    all_data_points = []

    for area in areas:
        start, end = area['start'], area['end']
        all_indices.extend(range(start, end + 1))
        all_data_points.extend(data[start:end + 1])

    if not all_data_points:
        return flags.tolist()

    all_data_points = np.array(all_data_points).reshape(-1, 1)

    lof = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=contamination,
                             metric=metric, algorithm=algorithm, leaf_size=leaf_size, p=p_value)
    predictions = lof.fit_predict(all_data_points)

    for idx, point_idx in enumerate(all_indices):
        flags[point_idx] = (predictions[idx] == -1).astype(int)

    return flags.tolist()


def i_forest_with_hyperparameters(data, flags, areas, n_estimators, contamination, max_samples):
    data = np.array(data)
    flags = np.array(flags)

    all_indices = []
    all_data_points = []

    for area in areas:
        start, end = area['start'], area['end']
        all_indices.extend(range(start, end + 1))
        all_data_points.extend(data[start:end + 1])

    if not all_data_points:
        return flags.tolist()

    all_data_points = np.array(all_data_points).reshape(-1, 1)

    i_forest = IsolationForest(n_estimators=n_estimators, contamination=contamination,max_samples=max_samples)
    predictions = i_forest.fit_predict(all_data_points)

    for idx, point_idx in enumerate(all_indices):
        flags[point_idx] = (predictions[idx] == -1).astype(int)

    return flags.tolist()


def lof_without_hyperparameters(data, flags, areas):
    data = np.array(data)
    flags = np.array(flags)

    all_indices = []
    all_data_points = []

    for area in areas:
        start, end = area['start'], area['end']
        all_indices.extend(range(start, end + 1))
        all_data_points.extend(data[start:end + 1])

    if not all_data_points:
        return flags.tolist()

    all_data_points = np.array(all_data_points).reshape(-1, 1)

    n_neighbors_range = [5, 10, 20, 30, 50, 100, 150, 200]
    contamination_range = [0.005, 0.01, 0.05, 0.1, 0.2, 0.25, 0.3, 0.5]

    best_detected_flags = np.zeros_like(flags)

    for n_neighbors, contamination in product(n_neighbors_range, contamination_range):
        lof = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=contamination, metric='euclidean')
        predictions = lof.fit_predict(all_data_points)

        detected_flags = np.zeros_like(flags)
        for idx, point_idx in enumerate(all_indices):
            detected_flags[point_idx] = (predictions[idx] == -1).astype(int)


        if np.all((flags == 1) <= (detected_flags == 1)):
            return detected_flags.tolist()


    return best_detected_flags.tolist()


def i_forest_without_hyperparameters(data, flags, areas):
    data = np.array(data)
    flags = np.array(flags)

    all_indices = []
    all_data_points = []

    for area in areas:
        start, end = area['start'], area['end']
        all_indices.extend(range(start, end + 1))
        all_data_points.extend(data[start:end + 1])

    if not all_data_points:
        return flags.tolist()

    all_data_points = np.array(all_data_points).reshape(-1, 1)

    contamination = max(0.01, min(0.1, np.sum(flags == 1) / len(flags)))*1.2

    iforest = IsolationForest(n_estimators=150, contamination=contamination, max_samples='auto', random_state=42)
    predictions = iforest.fit_predict(all_data_points)

    detected_flags = flags.copy()
    for idx, point_idx in enumerate(all_indices):
        if flags[point_idx] != 1:
            if predictions[idx] == -1:
                detected_flags[point_idx] = 3

    return detected_flags.tolist()





