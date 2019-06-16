##
## Name:     KMeans.py
## Purpose:  Implements J. B. MacQueen's K-Means clustering algorithm.
## Author:   M. J. Fromberger (@creachadair)
##
## A KMeans object represents a collection of points that can be clustered
## using the K-means algorithm.  Points are represented as individual objects
## or as ordered tuples of objects, provided the objects in question support
## addition and division.
##
from random import randint

def euclidean_distance(pt1, pt2):
    """Compute the square of standard Euclidean distance between two points
    represented as n-tuples.  This is the default distance metric for the
    K-means object.
    """
    if len(pt1) != len(pt2):
        raise ValueError("Points are of different dimensionality.")
    
    return sum((x - y) ** 2 for (x, y) in zip(pt1, pt2))

def argmin(fn, C):
    """Given a mapping function fn and a collection C, return the offset of an
    x in C such that fn(x) is minimal among all the elements of C.  Comparison
    is done using the < operator.
    """
    ic = iter(C)
    try:
        mv = fn(next(ic))
    except StopIteration:
        raise ValueError("Cannot find argmin of empty sequence")
    
    mp = 0
    for pos, val in enumerate(ic):
        cv = fn(val)
        if cv < mv:
            mv = cv
            mp = pos + 1
    
    return mp

class KMeans (object):
    """A KMeans object is used to find clusters among a set of data using the
    K-Means algorithm.  Clustering is determined by a distance metric, which
    may be given to the constructor as a function.
    
    To add sample points, use .add_data().
    To manually choose starting centroids, use .add_centroid().
    To randomly choose starting centroids, use .random_centroids().
    To run the k-means algorithm, use .run(); run uses this protocol:
       .start()   -- initialize internal data structures (once).
       .step()    -- recompute centroids and move points once.
       .run([m])  -- run until no points move, or m iterations.

    To extract the results, use .get_clusters().
    """
    def __init__(self, dist = euclidean_distance):
        """Construct a new KMeans object with no data points and no centroids.
        If specified, the dist function is used as the distance metric.  It
        must take two points and return some comparable value.
        """
        self._dist = dist    # Distance metric (function)
        self.clear()
    
    def clear(self):
        """Discard all data points, clusters, and centroids."""
        self._kctr = []    # Cluster centroids
        self._kmem = []    # Cluster affiliations
        self._data = set() # Sample data

    def data(self):
        """Return the set of data points known."""
        return set(s if len(s) > 1 else s[0]
                   for s in self._data)
    
    def find_cluster(self, pt):
        """Find the centroid closest to the given point, without adding the
        point to the collection.
        """
        for pos, data in enumerate(self._kmem):
            if pt in data:
                return self._kctr[pos]
        else:
            # Point is not in the data set, compute directly
            ploc = argmin(lambda c: self._dist(pt, c), self._kctr)
            return self._kctr[ploc]
    
    def reset_clusters(self):
        """Discard existing clusters."""
        for pos in xrange(len(self._kmem)):
            self._kmem[pos] = set()

    def reset_centroids(self):
        """Discard existing centroids."""
        self._kctr = []
    
    def add_centroid(self, pt):
        """Add a new cluster centroid.  The centroid may or may not be one of
        the data points; centroids are not added to the data set by this
        operation.
        """
        if pt not in self._kctr:
            try:
                self._kctr.append(tuple(iter(pt)))
            except TypeError:
                self._kctr.append((pt,))
            self._kmem.append(set())
    
    def add_data(self, pt, *pts):
        """Add one or more data points."""
        for elt in (pt,) + pts:
            try:
                self._data.add(tuple(iter(elt)))
            except TypeError:
                self._data.add((elt,))
    
    def random_centroids(self, k):
        """Choose k random centroids from among the data points."""
        if len(self._data) < k:
            raise ValueError("Insufficient data to choose %d centroids" % k)
        
        c = set() ; d = list(self._data) 
        while len(c) < k:
            c.add(d[randint(1, len(d)) - 1])
        
        self._kctr = list(c)
        self._kmem = []
        for elt in c: self._kmem.append(set())
    
    def start(self):
        """Initialize a new run of the k-means algorithm.  Call this function
        once at the beginning of each run to seed the clusters with their
        initial points.
        """
        if len(self._kctr) == 0:
            raise ValueError("No cluster centroids are defined")
        
        self.reset_clusters()
        for pt in self._data:
            ploc = argmin(lambda c: self._dist(pt, c), self._kctr)
            self._kmem[ploc].add(pt)
    
    def step(self):
        """Run one step of the k-means algorithm.  Returns the number of points
        that were moved.
        """
        def centroid(pts):
            cur = [0] * max(len(p) for p in pts)
            for p in pts:
                for pos, v in enumerate(p):
                    cur[pos] += v
            
            return tuple(x / len(pts) for x in cur)
        
        # Compute new centroids for each group.  If there are no data points,
        # leave the centroid as it was before.
        for pos, data in enumerate(self._kmem):
            if len(data) > 0:
                self._kctr[pos] = centroid(data)
        
        moves = 0
        for cloc, data in enumerate(self._kmem):
            for pt in data.copy():
                ploc = argmin(lambda c: self._dist(pt, c), self._kctr)
                if ploc != cloc:
                    data.discard(pt)
                    self._kmem[ploc].add(pt)
                    moves += 1
        
        return moves
    
    def run(self, max = None):
        """Run k-means until the .step() method reports that no more points
        have been moved, or until max iterations have passed.
        """
        self.start()
        while self.step() != 0:
            if max == 0: break
            if max > 0:
                max -= 1
    
    def get_clusters(self):
        """Extract a list of the clusters found by the algorithm.  Each cluster
        is returned as a tuple (c, [d, ...]) where c is the centroid point, and
        the d values are the points in the cluster.
        """
        return [ (self._kctr[p], list(self._kmem[p]))
                 for p in xrange(len(self._kctr)) ]

__all__ = [ "KMeans", "argmin", "euclidean_distance" ]

# Here there be dragons
