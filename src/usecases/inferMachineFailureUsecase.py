import pandas as pd
from src.inference.predictor import RandomForestPredict

class inferMachineFailureUsecase:

    def __init__(self, model_path: str):
        self.predictor = RandomForestPredict(model_path)

    def infer(self, data: pd.DataFrame):
        prediction, real_y = self.predictor.predict(data)

        return prediction, real_y
        