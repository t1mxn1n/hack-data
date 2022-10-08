import pickle
from train_dataset import tokenize, tokenize_sentence

filename = 'model_v1.pk'


def main():
    with open(filename, 'rb') as f:
        loaded_model = pickle.load(f)


if __name__ == '__main__':
    main()
