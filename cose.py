model1 = keras.models.Sequential()
model1.add(keras.layers.Embedding(input_dim=num_words, output_dim=10))
model1.add(keras.layers.LSTM(units = 6))
model1.add(keras.layers.Dense(1, activation="sigmoid"))

model1.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

model1.summary()

history1 = model1.fit(X_train_trim, y_train, epochs=10, batch_size=128, validation_data=(X_valid_trim, y_valid))

class DQL:
    def __init__(self,nm):
        self.name = nm
    
    def train(self):
        pass

    def predict(self):

