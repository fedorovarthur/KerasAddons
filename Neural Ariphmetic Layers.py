import keras.backend as K
from keras.engine.topology import Layer

class NAC(Layer):

    def __init__(self, output_dim, **kwargs):
        self.output_dim = output_dim
        super(NAC, self).__init__(**kwargs)

    def build(self, input_shape):
        # Create a trainable weight variable for this layer.
        self._M_hat = self.add_weight(name='M_hat', 
                                      shape=(input_shape[1], self.output_dim),
                                      initializer='glorot_normal',
                                      trainable=True)
        self._W_hat = self.add_weight(name='W_hat', 
                                      shape=(input_shape[1], self.output_dim),
                                      initializer='glorot_normal',
                                      trainable=True)
        super(NAC, self).build(input_shape)  # Be sure to call this at the end

    def call(self, x):
        self._W = K.tanh(self._W_hat)*K.sigmoid(self._M_hat)
        return K.dot(x, self._W)

    def compute_output_shape(self, input_shape):
        return (input_shape[0], self.output_dim)

class NALU(Layer):

    def __init__(self, output_dim, **kwargs):
        self.output_dim = output_dim
        super(NALU, self).__init__(**kwargs)

    def build(self, input_shape):
        # Create a trainable weight variable for this layer.
        #TODO: allow to specify init distribution
        self._W_hat = self.add_weight(name='W_hat', 
                                      shape=(input_shape[1], self.output_dim),
                                      initializer='glorot_normal',
                                      trainable=True)
        self._M_hat = self.add_weight(name='M_hat', 
                                      shape=(input_shape[1], self.output_dim),
                                      initializer='glorot_normal',
                                      trainable=True)
        self._G = self.add_weight(name='G', 
                                  shape=(input_shape[1], self.output_dim),
                                  initializer='glorot_normal',
                                  trainable=True)
        super(NALU, self).build(input_shape)  # Be sure to call this at the end

    def call(self, x):
        #TODO: allow to specify epsilon
        self._W = K.tanh(self._W_hat)*K.sigmoid(self._M_hat)
        self._a = K.dot(x, self._W)
        self._m = K.exp(K.dot(K.log(K.abs(x) + K.epsilon), self._W))
        self._g = K.dot(x, self._G)
        return self._g*self._a + (1 - self._g)*self._m

    def compute_output_shape(self, input_shape):
        return (input_shape[0], self.output_dim)