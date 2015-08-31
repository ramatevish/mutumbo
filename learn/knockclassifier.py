from sklearn import svm


class KnockClassifier(object):
	def __init__(self):
		self.clf = svm.SVC()
		self.X = []
		self.Y = []
		self.trained = False

	def addData(self, x, y):
		self.X.append(x)
		self.Y.append(y)

	def addDatas(self, X, Y):
		self.X += X
		self.Y += Y

	def fit(self):
		self.clf.fit(self.X, self.Y)
		self.trained = True

	def classify(self, x):
		if not self.trained:
			self.fit()
		return self.clf.predict(x)
