import numpy as np 
import random

class Network:
    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes # Neurons in each layer
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x) 
                           for x, y in zip(sizes[:-1], sizes[1:])]
    
    def feedforward(self, a):
        """Return the output of the network if 'a' is input."""
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a) + b)
        return a
    
    def SGD(self, training_data, epochs, mini_batch_size, 
            lr, test_data=None):
        """
        SGD = Stochastic gradient descent. 
        Train the neural network using mini-batch stochastic gradient 
        descent. The 'training data' is a list of tuples (x, y) 
        representing training inputs and the desired outputs. 
        If test_data is provided, the network will be evaluated against 
        the test data after each epoch, and partial progress printed. 
        """
        if test_data: 
            n_test = len(test_data)
        n = len(training_data)
        for j in range(epochs):
            random.shuffle(training_data) # SGD chooses a few random samples
            mini_batches = [
                training_data[k:k+mini_batch_size]
                    for k in range(0, n, mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, lr)
            if test_data: 
                print("Epoch {}: {} / {}".format(
                    j, self.evaluate(test_data), n_test))
            else: 
                print("Epoch {} complete".format(j))
    
    def update_mini_batch(self, mini_batch, lr): 
        """
        Update the network's weights and biases via gradient descent 
        with backpropogation to a single mini batch. lr is learning 
        rate. 
        """ 
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [w - (lr/len(mini_batch)) * nw
                           for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b - (lr/len(mini_batch)) * nb
                          for b, nb in zip(self.biases, nabla_b)]
    
    def backprop(self, x, y):
        """
        x: a sample in the training data (28x28=784 pixels) with weights 
           of intensity of gray in image
        y: a 10x1 ndarray unit vector, with a 1 in the index of correct 
           number
        Returna  tuple (nabla_b, nabla_w) representing gradient of the 
        cost function. nabla_b and nabla_w are layer-by-layer lists of 
        numpy arrays, similar to self.biases and self.weights. 
        """
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        
        # Feedforward 
        activation = x 
        activations = [x] # list to store activations, layer by layer 
        zs = [] # list to store z vectors, layer by layer 
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation) + b 
            zs.append(z) 
            activation = sigmoid(z) # Applies sigmoid to each element 
            activations.append(activation)
        
        # Backward pass 
        delta = self.cost_derivative(activations[-1], y) * \
            sigmoid_prime(zs[-1]) 
        nabla_b[-1] = delta # Set last layer 
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        for i in range(2, self.num_layers):
            # We now fill in the nabla_b, nabla_w from the back 
            z = zs[-i]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-i + 1].transpose(), delta) * sp 
            nabla_b[-i] = delta 
            nabla_w[-i] = np.dot(delta, activations[-i - 1].transpose())
        return (nabla_b, nabla_w)
    
    def evaluate(self, test_data): 
        """
        Return number of test inputs for which our network outputs the 
        correct results, choosing them by argmax. 
        """
        test_results = [(np.argmax(self.feedforward(x)), y)
                           for x, y in test_data]
        return sum(int(x == y) for x, y in test_results)

    def cost_derivative(self, output_activations, y):
        """Return vector of partial derivatives of cost function"""
        return (output_activations - y)

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def sigmoid_prime(z):
    """Derivative of sigmoid function"""
    return sigmoid(z) * (1 - sigmoid(z))
