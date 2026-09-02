def get_confidence_level(confidence):
    """
    Convert model confidence into a human-readable confidence level.
    """

    if confidence >= 0.90:
        return "high"

    if confidence >= 0.70:
        return "moderate"

    return "low"


EXPLANATIONS = {
    "Potato___healthy": {
        "high": (
            "The model is highly confident that this potato leaf appears healthy. "
            "It did not detect strong visual patterns that are commonly associated "
            "with early blight or late blight in the image."
        ),
        "moderate": (
            "The model found that this potato leaf is more likely to be healthy "
            "than affected by early or late blight. However, the result is not "
            "completely certain, so it is worth keeping an eye on the plant."
        ),
        "low": (
            "The model has some indication that this potato leaf may be healthy, "
            "but the result is uncertain. Some features in the image may look "
            "similar to signs of disease, so this result should be treated with caution."
        ),
    },

    "Potato___Early_blight": {
        "high": (
            "The model is highly confident that this potato leaf shows visual "
            "patterns associated with early blight. Early blight can appear as "
            "dark spots or patches on the leaf, sometimes developing into larger "
            "areas of damage as the disease progresses."
        ),
        "moderate": (
            "The model found visual patterns that are more consistent with early "
            "blight than with the other conditions it was trained to recognize. "
            "The result is reasonably confident, but the plant should still be "
            "examined closely for other signs of the disease."
        ),
        "low": (
            "The model found some features that may be associated with early blight, "
            "but it is not very certain about the result. The image may contain "
            "features that can also appear in other conditions, so this prediction "
            "should be treated as an indication rather than a definite diagnosis."
        ),
    },

    "Potato___Late_blight": {
        "high": (
            "The model is highly confident that this potato leaf shows visual "
            "patterns associated with late blight. Late blight can cause dark, "
            "irregular, or water-soaked areas on potato leaves and can spread "
            "quickly when conditions are favorable."
        ),
        "moderate": (
            "The model found visual patterns that are more consistent with late "
            "blight than with the other conditions it was trained to recognize. "
            "The result is reasonably confident, but the plant should be checked "
            "carefully for additional signs of disease."
        ),
        "low": (
            "The model found some features that may be associated with late blight, "
            "but it is not very certain about the result. Because some leaf "
            "conditions can look similar, this prediction should be treated as "
            "an indication rather than a definite diagnosis."
        ),
    },
}


RECOMMENDATIONS = {
    "Potato___healthy": {
        "high": (
            "Continue monitoring the plant regularly, especially the older leaves "
            "and nearby plants. Keeping the growing area clean and giving the "
            "plants enough space for good airflow can also help reduce disease risk."
        ),
        "moderate": (
            "Continue monitoring the plant over the next few days. Check other "
            "leaves and nearby potato plants for unusual spots, discoloration, "
            "or other changes."
        ),
        "low": (
            "Take another clear photo of the leaf in good lighting and check the "
            "plant again. If you notice unusual spots, discoloration, or worsening "
            "symptoms, consider getting the plant examined by an agricultural expert."
        ),
    },

    "Potato___Early_blight": {
        "high": (
            "Inspect the other leaves and nearby potato plants for similar signs. "
            "Remove severely affected leaves where appropriate and keep the plants "
            "well spaced to improve airflow. Continue monitoring the plant for "
            "signs that the disease is spreading."
        ),
        "moderate": (
            "Check the other leaves and nearby potato plants for similar symptoms. "
            "Keep the growing area clean and improve airflow around the plants. "
            "Continue monitoring the affected plant closely."
        ),
        "low": (
            "Inspect the plant carefully and take another clear photo if possible. "
            "Look for similar spots or changes on other leaves. Avoid making major "
            "treatment decisions based on this result alone."
        ),
    },

    "Potato___Late_blight": {
        "high": (
            "Check nearby potato plants for similar symptoms because late blight "
            "can spread quickly. Remove severely affected plant material where "
            "appropriate, avoid keeping the leaves wet for long periods, and "
            "monitor the affected area closely."
        ),
        "moderate": (
            "Inspect nearby plants for similar symptoms and monitor this plant "
            "closely. Avoid overhead watering where possible and try to keep the "
            "leaves from remaining wet for long periods."
        ),
        "low": (
            "Inspect the plant and nearby leaves carefully before taking action. "
            "Take another clear photo in good lighting if possible, and consider "
            "getting the plant checked by an agricultural expert before starting "
            "any major treatment."
        ),
    },
}


def generate_explanation(prediction, confidence):
    """
    Generate a farmer-friendly explanation and recommendation
    based on the model prediction and confidence.
    """

    confidence_level = get_confidence_level(confidence)

    explanation = EXPLANATIONS[prediction][confidence_level]
    recommendation = RECOMMENDATIONS[prediction][confidence_level]

    return {
        "confidence_level": confidence_level,
        "explanation": explanation,
        "recommendation": recommendation,
    }