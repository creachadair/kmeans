from KMeans import *
from pprint import pprint as pp

km = KMeans()

km.add_data(
    (0, 7), (2, 1), (4, 4), (8, 1),
    (16, 15), (20, 8), (23, 12), (40, 7),
    (40, 20), (47, 16), (47, 23)
    )

km.add_centroid((2, 1))
km.add_centroid((4, 4))
km.add_centroid((23, 12))

km.start()
