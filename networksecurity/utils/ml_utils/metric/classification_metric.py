from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.exception.exception import NetworkSecurityException
from sklearn.metrics import f1_score,precision_score,recall_score
import sys

def get_classification_score(y_true,y_pred)->ClassificationMetricArtifact:
    try:
            
        model_f1_score = f1_score(y_true, y_pred)
        model_recall_score = recall_score(y_true, y_pred)
        model_precision_score=precision_score(y_true,y_pred)

        classification_metric =  ClassificationMetricArtifact(f1_score=model_f1_score,
                    precision_score=model_precision_score, 
                    recall_score=model_recall_score)
        return classification_metric
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
# Input: The function takes two arrays/lists:
# y_true: Ground truth labels.
# y_pred: Model-generated predictions.

# Metric Computation:
# precision_score: Measures the ratio of correctly predicted positive observations to the total predicted positives. High precision means fewer false positives.
# recall_score: Measures the ratio of correctly predicted positive observations to all actual positives. High recall means fewer false negatives.
# f1_score: Harmonic mean of precision and recall. It provides a balance between the two, especially useful when classes are imbalanced.

# Packaging Results: The computed metrics are encapsulated in a ClassificationMetricArtifact data structure, enabling structured access and downstream logging or tracking.
# Return Value: Returns the ClassificationMetricArtifact object containing the precision, recall, and F1 score.
# Exception Handling: Any runtime exception during metric computation is caught and re-raised as a domain-specific NetworkSecurityException for consistent error handling across the pipeline.