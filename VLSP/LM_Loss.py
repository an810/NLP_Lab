import numpy as np

def large_margin_loss(embeddings, labels, margin=0.2):
    # Calculate the pairwise cosine similarity matrix
    similarity_matrix = np.dot(embeddings, embeddings.T)
    
    # Calculate the diagonal of the similarity matrix
    diagonal = np.diagonal(similarity_matrix)
    
    # Compute the numerator and denominator for the large margin loss
    numerator = np.exp(similarity_matrix - margin)
    denominator = np.sum(np.exp(similarity_matrix), axis=1) - np.exp(diagonal - margin)
    
    # Calculate the large margin loss
    loss = -np.log(numerator / denominator)
    
    # Use only the positive samples (where labels match)
    mask = labels[:, None] == labels
    loss = loss * mask
    loss = np.sum(loss) / np.sum(mask)
    
    return loss

