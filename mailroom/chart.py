import logging
import matplotlib.pyplot as plt

# Setting up the Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(format)
logger.addHandler(ch)


class Chart(object):
    """
    """

    def __init__(self, title="Untitled Chart"):
        self.title = title
        self.filename = title
        self.xlabel = ""
        self.ylabel = ""

    def make_bar(data):
        plt.bar(data)
        plt.xlabel(self.xlabel)
        plt.ylabel(ylabel)
        plt.savefig(f"{self.filename}.png")

    def make_line(data, xlabel="", ylabel=""):
        plt.plot(data)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig(f"{self.filename}.png")
