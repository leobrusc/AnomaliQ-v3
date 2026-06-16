import numpy as np

def generate_alerts(scores, threshold=0.7):
    alerts = np.where(scores >= threshold)[0]
    return alerts