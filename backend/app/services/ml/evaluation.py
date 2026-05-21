from sklearn.metrics import accuracy_score, log_loss


def evaluate_model(model, X_val, y_val):
    """
    Evalúa el modelo sobre el conjunto de validación.

    Métricas:
    - accuracy: porcentaje de aciertos
    - log_loss: mide la calidad probabilística de la predicción
    """
    y_pred = model.predict(X_val)
    y_proba = model.predict_proba_matrix(X_val)

    # Para log_loss necesitamos las etiquetas codificadas
    y_val_encoded = model.label_encoder.transform(y_val)

    metrics = {
        "accuracy": round(accuracy_score(y_val, y_pred), 4),
        "log_loss": round(
            log_loss(y_val_encoded, y_proba, labels=model.classifier.classes_),
            4
        )
    }

    return metrics