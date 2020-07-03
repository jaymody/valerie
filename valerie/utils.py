"""Utility functions."""
import logging

_logger = logging.getLogger(__name__)


def get_logger(logfile=None):
    """Gets a nicely formatted logger."""
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s:%(name)s: %(message)s")
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.handlers = [sh]

    if logfile:
        fh = logging.FileHandler(logfile)
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        logger.handlers.append(fh)

    return logger


def stats(values, plot=False):
    import statistics
    import seaborn as sns
    import matplotlib.pyplot as plt

    # workaround for multiple modes
    try:
        mode = statistics.mode(values)
    except:
        mode = None

    d = {
        "len": len(values),
        "max": max(values),
        "min": min(values),
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "mode": mode,
        "stdev": statistics.stdev(values),
    }

    if plot:
        sns.distplot(values)
        plt.show()

    return d
