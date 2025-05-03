import pickle

def pickle_objects(objects, filename):
    with open(filename, 'wb') as file:
        pickle.dump(objects, file)

def unpickle_objects(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)