import pickle


def predict(data):
    with open("source/model.pkl", "rb") as file:
        model = pickle.load(file)

    prediction = model.predict(data)
    return prediction

