from time import sleep

import pandas as pd

from Generator import RandomDataGenerator, SeasonalDataGenerator
from AnomalyDetector import MADAnomalyDetector, IsolatedForestDetecto


def generate_random_data(start_data, end_data, rounds) -> pd.Series:
    """
    Generate chuns of random data using RandomDataGenerator class
    :param start_data: start date
    :param end_data: end data
    :param rounds: number of chunks
    :return:
    """
    rg = RandomDataGenerator(start_data, end_data)

    counter = -1
    while counter < rounds:
        sample = rg.Generate(sample_size=500, upper_bound=20, anomaly_rate=0.01)
        yield sample
        counter += 1


def generate_seasonal_data(start_data, end_data, rounds) -> pd.Series:
    """
    Generate chuns of random data using RandomDataGenerator class
    :param start_data: start date
    :param end_data: end data
    :param rounds: number of chunks
    :return:
    """
    sg = SeasonalDataGenerator(start_data, end_data)

    counter = -1
    while counter < rounds:
        sample = sg.Generate(sample_size=4000, seasonality_amplitude=10, anomaly_rate=0.002, anomaly_duration=10,
                             anomaly_magnitude=20)
        yield sample
        counter += 1


if __name__ == '__main__':
    # test two functions above
    for s in generate_seasonal_data('1-1-2024', '1-1-2025', rounds=10):
        sleep(1)
        print(len(s))
        print()
