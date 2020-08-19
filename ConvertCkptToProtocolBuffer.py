import tensorflow as tf
from tensorflow.python.framework import graph_util


def freeze_graph(input_checkpoint, output_graph):
    '''

    :param input_checkpoint: xxx.ckpt (Do not add the following xxx.ckpt.data, go to ckpt!)
         :param output_graph: PB model save path
    :return:
    '''
    # checkpoint = tf.train.get_checkpoint_state(model_folder) #Check if the status of the ckpt file is available in the directory.
    # input_checkpoint = checkpoint.model_checkpoint_path #  ckptFile Path

    # Specify the node name of the output, the node name must be the node existing in the original model
    output_node_names = "SemanticPredictions" #Model input node, customize according to the situation
    saver = tf.train.import_meta_graph(input_checkpoint + '.meta', clear_devices=True)
    graph = tf.get_default_graph() # Get the default map
    input_graph_def = graph.as_graph_def()  # return a serialized graph representing the current graph

    with tf.Session() as sess:
        saver.restore(sess, input_checkpoint) #   and get the data
        output_graph_def = graph_util.convert_variables_to_constants(  #Model persistence, fixed variable values
            sess=sess,
            input_graph_def=input_graph_def,# equal to: sess.graph_def
            output_node_names=output_node_names.split(","))# If there are multiple output nodes, separated by commas

        with tf.gfile.GFile(output_graph, "wb") as f: #Save model
            f.write(output_graph_def.SerializeToString()) # 
        print("%d ops in the final graph." % len(output_graph_def.node)) #Get the current graph has several operation nodes

path ='D:\\Projects\\TensorflowModelsRepo\\models-master\\research\\deeplab\\datasets\\ContainerSeg\\exp\\train_on_trainval_set_mobilenetv2\\train\\model.ckpt-90000'
freeze_graph(path, ".\\semanticSegmentationModel3.pb")