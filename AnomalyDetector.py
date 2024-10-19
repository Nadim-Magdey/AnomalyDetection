import time
from abc import abstractmethod

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

from Generator import Generator
from Generator import RandomDataGenerator
from pyod.models.mad import MAD


class AnomalyDetector:
    """
    The vase class for all Anomaly detectors
    This class use to implement various algorithms for anomaly detection
    """

    def __init__(self):
        pass

    @abstractmethod
    def Detect(self, data: pd.Series, **kwargs) -> np.ndarray:
        raise NotImplemented("Please implement this method")


class MADAnomalyDetector(AnomalyDetector):
    """
    This class Implement Mean Absolute DEvision Algorithm
    """
    def __init__(self):
        super().__init__()

    def Detect(self, data: pd.Series, **kwargs) -> np.ndarray:
        """
        :param data: time series data
        :return: 1d array of prediction result
        0 mean not anomaly and 1 mean it's anomaly
        """
        df = pd.DataFrame(data, columns=["values"])
        model = MAD().fit(df)
        labels = model.labels_
        return labels

class IsolatedForestDetecto(AnomalyDetector):
    """
    This class implement IsolatedForest algorithm
    """
    def __init__(self):
        super().__init__()

    def Detect(self, data: pd.Series, **kwargs) -> np.ndarray:
        """
        :param data: time series data
        :return: 1d array of prediction result
        -1 mean not anomaly and 1 mean its anomaly
        """
        model = IsolationForest(contamination=kwargs['combinations'])
        model.fit(data.values.reshape(-1, 1))

        # Predict anomalies
        predictions = model.predict(data.values.reshape(-1, 1))
        return predictions


if __name__ == "__main__":
    # test time required to predict anomalies in a small sample
    start = time.time()

    rg = RandomDataGenerator("1-1-2024", '1-1-2025')
    sample = rg.Generate(sample_size=500, upper_bound=20, anomaly_rate=0.01)

    # mad = MADAnomalyDetector()
    # labels = mad.Detect(data = sample)

    isolated_forest = IsolatedForestDetecto()
    labels = isolated_forest.Detect(sample, combinations=0.05)

    end = time.time()

    print(f" time {end - start}")