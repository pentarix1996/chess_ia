import chess
import time
import torch
import tensorflow as tf

from business_logic.board import DisplayThread
from level3.ia_level import ChessAgent
from lib.training import Model


IA_MODE = True


def main():
    ia_input = input("Que IA quieres que juegue?\n1) Keras NeuralNet\n2) Mercutos\n>>> ").lower()
    board = chess.Board()
    agent = None

    if IA_MODE:
        if ia_input == "1":
            try:
                print("Modelo cargado de 500 episodios")
                model = tf.keras.models.load_model("model_WHITE.h5")
            except:
                print("Test")
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(8, 8, 12)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(128, activation='relu'),
                    tf.keras.layers.Dense(4096, activation='softmax')
                ])
                model.compile(optimizer='adam', loss='mean_squared_error')
            
            agent = ChessAgent(model, chess.WHITE)
        elif ia_input == "2":
            saved_model = Model()
            f = open("./data/savedModels/bestModel.txt", "r")
            f.readline()
            model_path = f.readline()
            f.close()
            saved_model.load_state_dict(torch.load(model_path))
            agent = saved_model

    display_thread = DisplayThread(board, IA_MODE, agent)
    display_thread.start()

    while display_thread.is_alive():
        time.sleep(0.01)

    print("El juego ha terminado. Resultado: " + ('1-0' if board.is_checkmate() else '1/2-1/2'))

    display_thread.stop()
    display_thread.join()


if __name__ == "__main__":
    main()
