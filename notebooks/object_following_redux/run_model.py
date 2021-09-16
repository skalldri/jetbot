
# Checkout https://stackoverflow.com/questions/60974077/how-to-save-keras-model-as-frozen-graph

import tensorflow as tf
from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2

saved_model_loaded = tf.saved_model.load("trt-optimized", tags=[tf.saved_model.SERVING])
graph_func = saved_model_loaded.signatures[tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY]
frozen_func = convert_variables_to_constants_v2(graph_func)

# Load some test data
test_image = tf.io.read_file("test.jpg")
# Turn test data into tensor
test_image_tensor = tf.image.decode_jpeg(test_image)
# Indicate batch-size == 1 by adding a dimension 1 into the first posision of the tensor's shape
test_image_tensor_batch = tf.expand_dims(input=test_image_tensor, axis=0)

# Feed the tensor into the model
predictions = frozen_func(test_image_tensor_batch)

