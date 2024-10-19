import sys

from Helpers import generate_random_data, generate_seasonal_data
from AnomalyDetector import MADAnomalyDetector, IsolatedForestDetecto

from time import sleep
import seaborn as sb
import matplotlib.pyplot as plt
import tkinter as tk


def on_close(e):
    """
    CLose the window
    :param e: Sender of the event
    :return: None
    """
    sys.exit()


def PlotSinedData():
    """
    THis function used to iterate throw generate_seasonal_data which generate chunks of data then it
    apply anomaly detection algorithms and plot the result as two axes to show the deferent between two algorithms

    :return:
    """
    for data in generate_seasonal_data('1-1-2024', '1-1-2025', 300):
        # generate data
        random_labels = mad.Detect(data, combinations=0.05)
        if_labels = isolated_forest.Detect(data, combinations=0.05)

        ax.clear()

        # plot both mad and isolated forests
        ax1 = plt.subplot(1, 2, 1)
        sb.scatterplot(data[random_labels == 0], ax=ax1, color="green")
        sb.scatterplot(data[random_labels == 1], ax=ax1, color="red")
        ax1.set_title("Mean absolute Devision   Algorithm")

        ax2 = plt.subplot(1, 2, 2)
        sb.scatterplot(data[if_labels == 1], ax=ax2, color="green")
        sb.scatterplot(data[if_labels == -1], ax=ax2, color="red")
        ax2.set_title("Isolated Forest Algorithm")
        plt.show(block=False)
        plt.pause(1)
        ax1.clear()
        ax2.clear()


def PlotRandomData():
    """
      THis function used to iterate throw generate_random_data which generate chunks of data then it
      apply anomaly detection algorithms and plot the result as two axes to show the deferent between two algorithms
      :return:
      """
    for data in generate_random_data('1-1-2024', '1-1-2025', 300):
        # generate data
        random_labels = mad.Detect(data, combinations=0.05)
        if_labels = isolated_forest.Detect(data, combinations=0.05)

        ax.clear()

        # plot both mad and isolated forests
        ax1 = plt.subplot(1, 2, 1)
        sb.scatterplot(data[random_labels == 0], ax=ax1, color="green")
        sb.scatterplot(data[random_labels == 1], ax=ax1, color="red")
        ax1.set_title("Mean absolute Devision   Algorithm")

        ax2 = plt.subplot(1, 2, 2)
        sb.scatterplot(data[if_labels == 1], ax=ax2, color="green")
        sb.scatterplot(data[if_labels == -1], ax=ax2, color="red")
        ax2.set_title("Isolated Forest Algorithm")

        plt.show(block=False)
        plt.pause(1)
        ax1.clear()
        ax2.clear()


# prepare matplotlib for visualizing
fig, ax = plt.subplots()
mad = MADAnomalyDetector()
isolated_forest = IsolatedForestDetecto()
plt.gcf().canvas.mpl_connect('close_event', on_close)

if __name__ == "__main__":
    # create main frame
    root = tk.Tk()
    root.geometry("300x300")

    # Create the buttons
    button1 = tk.Button(root, text="Random  Data Simulator", command=PlotSinedData)
    button2 = tk.Button(root, text="Seasonal Data Simulator", command=PlotRandomData)

    # add buttons to the main frame
    button1.pack()
    button2.pack()

    # Run the main loop
    root.mainloop()
