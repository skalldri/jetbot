import tensorflow as tf
import os
from tensorflow.python.tools import freeze_graph
from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2

### USAGE ##
def wrap_frozen_graph(graph_def, inputs, outputs, print_graph=False):
    def _imports_graph_def():
        tf.compat.v1.import_graph_def(graph_def, name="")

    wrapped_import = tf.compat.v1.wrap_function(_imports_graph_def, [])
    import_graph = wrapped_import.graph

    print("-" * 50)
    print("Frozen model layers: ")
    layers = [op.name for op in import_graph.get_operations()]
    if print_graph == True:
        for layer in layers:
            print(layer)
    print("-" * 50)
    
    import_graph.inputs
    import_graph.outputs

    return wrapped_import.prune(
        tf.nest.map_structure(import_graph.as_graph_element, inputs),
        tf.nest.map_structure(import_graph.as_graph_element, outputs))


## Example Usage ###
# Load frozen graph using TensorFlow 1.x functions
with tf.io.gfile.GFile("./frozen_trt_optimized_models/frozen_ssd_mobilenet_v2.pb", "rb") as f:
    graph_def = tf.compat.v1.GraphDef()
    print("Parsing model...")
    loaded = graph_def.ParseFromString(f.read())
    print("Model parsed")

# Wrap frozen graph to ConcreteFunctions
print("getting input function")
frozen_func = wrap_frozen_graph(graph_def=graph_def,
                                inputs=["input_tensor:0"],
                                outputs=["Identity:0"],
                                print_graph=True)

print("Got frozen function")

print("-" * 50)

print("Frozen model inputs: ")
print(frozen_func.inputs)

print("Frozen model outputs: ")
print(frozen_func.outputs)

# Load some test data
test_image = tf.io.read_file("test.jpg")
# Turn test data into tensor
test_image_tensor = tf.image.decode_jpeg(test_image)

test_image_tensor = tf.image.resize_with_pad(test_image_tensor, 320, 320)

# Indicate batch-size == 1 by adding a dimension 1 into the first posision of the tensor's shape
test_image_tensor_batch = tf.expand_dims(input=test_image_tensor, axis=0)

# Get predictions for test images
predictions = frozen_func(test_image_tensor_batch)
# Print the prediction for the first image
print("-" * 50)
print("Example prediction reference:")
print(predictions)