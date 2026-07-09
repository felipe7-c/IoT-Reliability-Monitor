import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder


class RandomForestPredict:

    def __init__(self, model_path: str):
        self.model = joblib.load(model_path)
        self.scaler = StandardScaler()
        self.lb = LabelEncoder()
    
    def preprocess_data(self, data: pd.DataFrame):

        data = data.drop(columns=["UDI", "Product ID"], axis = 0)
        features_float = ["Air temperature [K]", "Process temperature [K]", "Rotational speed [rpm]", "Torque [Nm]", "Tool wear [min]"]

        data[features_float] = self.scaler.fit_transform(data[features_float])
        data['Type'] = self.lb.fit_transform(data['Type'])

        data = data.drop(["TWF", "HDF", "PWF", "OSF", "RNF"], axis=1)

        X = data.drop("Machine failure", axis = 1)
        y = data["Machine failure"]

        return X, y

    def predict(self, data: pd.DataFrame):
        
        X, y = self.preprocess_data(data)
        
        return self.model.predict(X), y
    