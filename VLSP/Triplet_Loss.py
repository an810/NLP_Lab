import numpy as np

def triplet_loss(anchor, positive, negative, margin=0.2):
    # Calculate the Euclidean distances
    pos_dist = np.sum((anchor - positive) ** 2, axis=1)
    neg_dist = np.sum((anchor - negative) ** 2, axis=1)
    
    # Calculate the triplet loss
    loss = np.maximum(pos_dist - neg_dist + margin, 0)
    
    # Compute the mean loss
    mean_loss = np.mean(loss)
    
    return mean_loss
