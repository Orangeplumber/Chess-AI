import numpy as np

class BackPropagationNetwork:
	"""a bp network"""
	# class members
	# 
	layerCount=0
	shape=None
	weights=[]
	# 
	# class members
	# 
	def __init__(self,layerSize):
		"""Initialize the network"""

		# Layer info
		self.layerCount=len(layerSize)-1
		self.shape=layerSize

		# Data from last run
		self._layerInput=[]
		self._layerOutput=[]
		self._previousWeightDelta=[]

		# Create the weight arrays
		for (l1,l2) in zip(layerSize[:-1],layerSize[1:]):
			self.weights.append(np.random.normal(scale=0.01,size=(l2,l1+1)))
			self._previousWeightDelta.append(np.random.normal(scale=0.01,size=(l2,l1+1)))

	# 
	# Run method
	# 
	def Run(self,input):
		"""run the network based on input data"""
		lnCases=input.shape[0]

		# Clear out the previous intermediate value lists
		self._layerInput=[]
		self._layerOutput=[]

		# Run it!
		for index in range(self.layerCount):
			 # Determine layer input
			 if index==0:
			 	layerInput=self.weights[0].dot(np.vstack([input.T,np.ones([1,lnCases])]))
			 else:
			 	layerInput=self.weights[index].dot(np.vstack([self._layerOutput[-1],np.ones([1,lnCases])]))

			 self._layerInput.append(layerInput)
			 self._layerOutput.append(self.sgm(layerInput))

		return self._layerOutput[-1].T
	# 
	# TrainEpoch method
	#
	def TrainEpoch(self,input,target,trainingRate=0.0005,momentum=0.5):
		"""This method trains the network for one epoch"""
		delta=[]
		lnCases=input.shape[0]

		# First run the network
		self.Run(input)

		# Calculate our deltas
		for index in reversed(range(self.layerCount)):
			if index==self.layerCount-1:
				# Compare to the target values
				# print self._layerOutput[index]
				output_delta=self._layerOutput[index]-target.T
				error=np.sum(output_delta**2)
				delta.append(output_delta*self.sgm(self._layerInput[index],True))
			else:
				# Compare to the following layer's delta
				delta_pullback=self.weights[index+1].T.dot(delta[-1])
				delta.append(delta_pullback[:-1, :]*self.sgm(self._layerInput[index],True))

		# Compute the weight deltas
		for index in range(self.layerCount):
			delta_index=self.layerCount-1-index

			if index==0:
				layerOutput=np.vstack([input.T,np.ones([1,lnCases])])
			else:
				layerOutput=np.vstack([self._layerOutput[index-1],np.ones([1,self._layerOutput[index-1].shape[1]])])

			curWeightDelta=np.sum(\
							   layerOutput[None,:,:].transpose(2,0,1)*delta[delta_index][None,:,:].transpose(2,1,0)\
							   , axis=0)
			weightDelta=trainingRate*curWeightDelta+momentum*self._previousWeightDelta[index]
			self.weights[index]-=weightDelta
			self._previousWeightDelta[index]=weightDelta

		return error



	# Transfer function
	def sgm(self,x,Derivative=False):
		if not Derivative:
			return 1/(1+np.exp(-x))
		else:
			out=self.sgm(x)
			return out*(1-out)
# 
# if script run --create a test object
# 
if __name__=="__main__":
	# bpn=BackPropagationNetwork((2,2,1))
	# print bpn.shape
	# print bpn.weights

	# lvInput=np.array([[0,0],[1,1],[0,1],[1,0]])
	# lvTarget=np.array([[0.05],[0.05],[0.95],[0.95]])

	# lnMax=100000
	# lnErr=1e-5
	# for i in range(lnMax+1):
	# 	err=bpn.TrainEpoch(lvInput,lvTarget)
	# 	if i%2500==0:
	# 		print "Iteration {0}\tError: {1:0.6f}".format(i,err)
	# 	if err<=lnErr:
	# 		print "Minimum error reached at iteration {0}".format(i)
	# 		break

	# # Display output
	# lvOutput=bpn.Run(lvInput)
	# print "Input: {0}\nOutput: {1}".format(lvInput,lvOutput)

	bpn=BackPropagationNetwork((768,6,6,3))
	lvInput=np.genfromtxt("input_vector1.csv", delimiter=" ")
	lvTarget=np.genfromtxt("output_vector1.csv", delimiter=" ")

	lnMax=10000
	lnErr=1
	for i in range(lnMax+1):
		err=bpn.TrainEpoch(lvInput,lvTarget)
		# if i%1==0:
		print "Iteration {0}\tError: {1:0.1f}".format(i,err)
		if err<=lnErr:
			print "Minimum error reached at iteration {0}".format(i)
			break
	print bpn.weights[0][0]


