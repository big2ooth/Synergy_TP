import numpy as np


class KMeans:
    def __init__(self, k=3, n_iters=100, seed=42):
        self.k = k
        self.n_iters = n_iters
        self.seed = seed
        self.centroids = None
        self.inertia_ = None

    def fit(self, X):
        rng = np.random.default_rng(self.seed)
        n_samples = X.shape[0]
        init_idx = rng.choice(n_samples, self.k, replace=False)
        self.centroids = X[init_idx].copy()

        labels = self._assign_clusters(X)

        for i in range(self.n_iters):
            labels = self._assign_clusters(X)
            new_centroids = np.zeros_like(self.centroids)

            for cluster in range(self.k):
                points = X[labels == cluster]
                if len(points) == 0:
                    new_centroids[cluster] = self.centroids[cluster]
                else:
                    new_centroids[cluster] = points.mean(axis=0)

            if np.allclose(new_centroids, self.centroids):
                self.centroids = new_centroids
                break

            self.centroids = new_centroids

        labels = self._assign_clusters(X)
        self.inertia_ = self._compute_inertia(X, labels)
        return labels

    def _assign_clusters(self, X):
        distances = np.zeros((X.shape[0], self.k))
        for cluster in range(self.k):
            diff = X - self.centroids[cluster]
            distances[:, cluster] = np.sum(diff ** 2, axis=1)
        return np.argmin(distances, axis=1)

    def predict(self, X):
        return self._assign_clusters(X)

    def _compute_inertia(self, X, labels):
        total = 0.0
        for cluster in range(self.k):
            points = X[labels == cluster]
            diff = points - self.centroids[cluster]
            total += np.sum(diff ** 2)
        return total


def silhouette_score(X, labels, sample_size=500, seed=42):
    rng = np.random.default_rng(seed)
    n = X.shape[0]
    if n > sample_size:
        idx = rng.choice(n, sample_size, replace=False)
        X = X[idx]
        labels = labels[idx]

    scores = []
    for i in range(len(X)):
        same_cluster = labels == labels[i]
        other_points = X[same_cluster]
        if len(other_points) > 1:
            a = np.mean(np.sqrt(np.sum((other_points - X[i]) ** 2, axis=1)))
        else:
            a = 0.0

        b = None
        for cluster in np.unique(labels):
            if cluster == labels[i]:
                continue
            other = X[labels == cluster]
            dist = np.mean(np.sqrt(np.sum((other - X[i]) ** 2, axis=1)))
            if b is None or dist < b:
                b = dist

        if b is None:
            scores.append(0.0)
        else:
            scores.append((b - a) / max(a, b))

    return float(np.mean(scores))