import pickle

def pickle_network(network_object):
    # pickle the network objects
    return pickle.dumps(network_object)

def unpickle_network(network_object):
    # unpickle the network objects
    return pickle.loads(network_object)
