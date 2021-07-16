import pickle
import numpy as np


"""
В этом файле будет реализован полный 
пайплайн по обработке данных и предсказанию
"""

class PREDICT:
    def __init__(self,paths=["STD.pkl","FORESR.pkl","LIN_REG.pkl"]):

        self.download_file(paths)

    def download_file(self, paths):
        """
        paths - список с путями  к фалам с моделями
        и стандартизатором. 
        paths[0]- StandardScaler
        paths[1]- RandomForest
        paths[2]- LinearRegression
        """
        self.MODELS = {}
        for path, key in zip(paths, ['std', 'forest', 'lin_reg']):
            with open(path, 'rb') as f:
                self.MODELS[key] = pickle.load(f)
    

    def Make_predict(self, X):
        """
        Это функция предсказывает примет ли клиент 
        участие в акции и какое предложение ему сделать.
        Если модель говорит, что клиент не будет 
        участвовать в акции, то предсказание предложения не 
        происходит
        """
        std_X = self.MODELS['std'].transform(X)
        pred_parc= self.MODELS['forest'].predict(std_X)
        if pred_parc!=0:
            pred_Amp = self.MODELS['lin_reg'].predict(std_X)
            return  pred_Amp.argmax()
        else:
            return -1


        