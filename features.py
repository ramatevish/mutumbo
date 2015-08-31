from scipy.spatial import distance as sdistance

def max_distance(A0, A1):
	max_distance = 0.
	for a0, a1 in zip(A0, A1):
		distance = a1 - a0
		if distance > max_distance:
			max_distance = distance
	return max_distance

def euclidean_distance(a0, a1):
    if type(a0) == 'dict':
        return sdistance.euclidean((a1['x'], a1['y'], a1['z']), (a2['x'], a2['y'], a2['z']))
    return sdistance.euclidean(a0, a1)
