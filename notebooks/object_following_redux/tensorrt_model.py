import torch
import tensorrt as trt
import atexit

def gigabyte(val):
    return val * 1024 * 1024 * 1024

class TensorRTModel:
    def __init__(self, model_path, input_names=None, output_names=None, final_shapes=None):
        self.logger = trt.Logger()
        self.builder = trt.Builder(self.logger)
        network_flags = 1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
        self.network = self.builder.create_network(flags=network_flags)
        self.config = self.builder.create_builder_config()
        
        # TODO: Guess parser based on model file extension
        # For now, just use UFF parser
        #self.parser = trt.UffParser()
        
        # Create a parser that will populate self.network with the Onnx model
        self.parser = trt.OnnxParser(self.network, self.logger)
        if self.parser.parse_from_file(model_path):
            print("Model parsed successfully")
        else:
            for i in range(self.parser.num_errors):
                error = self.parser.get_error(i)
                print("Error: " + trt.ParserError.desc(error))
            raise Exception("Failed to parse model")
        
    def build_engine():
        self.config.max_workspace_size = gigabyte(1)
        
def main():
    print("Hello world")
    
    model = TensorRTModel()
    
    
    
if __name__ == "main":
    main()
            