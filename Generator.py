from abc import abstractmethod

import numpy as np
import time
import pandas as pd


class Generator:
    """
    Generate random sequences
    This is an abstract definition of other genrator classes
    """

    def __init__(self, start_data, end_data):
        """
        Basic constructor
        :param start_data: start date
        :param end_data: end date
        """
        self.start_date = start_data
        self.end_data = end_data

    def Generate(self, **kwargs) -> pd.Series:
        """
        Generate indices and ley subclasses generate both data and noises
        :param kwargs:
        :return:
        """
        indices = pd.date_range(start=self.start_date, end=self.end_data, periods=kwargs["sample_size"])
        data = self.generateData(indices, **kwargs)

        self.addNoises(data, **kwargs)

        return pd.Series(data, index=indices)

    @abstractmethod
    def generateData(self, indices, **kwargs):
        raise NotImplemented("Please implement this method")

    @abstractmethod
    def addNoises(self, data, **kwargs):
        raise NotImplemented("Please implement this method")


class RandomDataGenerator(Generator):
    """
    This class generate float value sequences
    """

    def __init__(self, start_date, end_date):
        super().__init__(start_date, end_date)

    def generateData(self, indices, **kwargs):
        """

        :param indices: list of indices
        :param kwargs: contain sample_size, upper_bound and anomaly_rate
        anomaly_rate is the rate of noiy data
        :return:
        """
        data = np.random.random(kwargs['sample_size']) * kwargs['upper_bound']

        return data

    def addNoises(self, data, **kwargs):
        """
        Add Noises to the data
        :param data:
        :param kwargs:
        :return:
        """

        # generate indices
        anomaly_indices = np.random.choice(kwargs['sample_size'], int(kwargs['sample_size'] * kwargs['anomaly_rate']),
                                           replace=False)
        data[anomaly_indices] *= 5  # Introduce anomalies as outliers


class SeasonalDataGenerator(Generator):
    """
    This class generate sin data with noises
    """

    def __init__(self, start_data, end_data):
        super().__init__(start_data, end_data)

    def generateData(self, indices, **kwargs):
        """
         Generate Sin wave data
         :param indices: list of indices
         """
        data = kwargs['seasonality_amplitude'] * np.sin(2 * np.pi * np.arange(kwargs['sample_size']) / 365)

        return data

    def addNoises(self, data, **kwargs):
        """
        Add noises to Sin Date
         :param data: data to add noise

         :return:
         """
        # generate noise and  anomaly indices
        noise = np.random.randn(kwargs['sample_size'])
        anomaly_indices = np.random.choice(kwargs['sample_size'], int(kwargs['sample_size'] * kwargs['anomaly_rate']),
                                           replace=False)

        # initial values of anomalies
        anomalies = np.zeros(kwargs['sample_size'])

        # loop over indices and add noise on each point
        for index in anomaly_indices:
            start_index = max(0, index - kwargs['anomaly_duration'] // 2)
            end_index = min(kwargs['sample_size'] - 1, index + kwargs['anomaly_duration'] // 2)
            anomalies[start_index:end_index + 1] = kwargs['anomaly_magnitude']

        # Combine components (Add the anomaly :)  )
        data += noise + anomalies


if __name__ == "__main__":
    # test the time of large sample
    start = time.time()
    #
    # obj = RandomDataGenerator("1-1-2024")
    # sample = obj.Generate(sample_size=500, upper_bound=20, anomaly_rate=0.01)
    obj = SeasonalDataGenerator('1-1-2024', '1-1-2025')
    sample = obj.Generate(sample_size=4000, seasonality_amplitude=10, anomaly_rate=0.002, anomaly_duration=10,
                          anomaly_magnitude=20)

    print(f"sample size {sample.shape}")
    end = time.time()
    print(sample)
    print(f"time is {end - start}")
    # print(generate_data_stream(366))
