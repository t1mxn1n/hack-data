import pickle
from train_dataset import tokenize, tokenize_sentence

ROLES = {
    0: 'businessman',
    1: 'accountant'
}


filename = 'model_v1.pk'


def main():
    with open(filename, 'rb') as f:
        loaded_model = pickle.load(f)


if __name__ == '__main__':
    main()
