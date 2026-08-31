from ai.inference.predict import predict


images = {
    "Early Blight": "ai/data/raw/Dataset/Potato___Early_blight/0a8a68ee-f587-4dea-beec-79d02e7d3fa4___RS_Early.B 8461.JPG",

    "Late Blight": "ai/data/raw/Dataset/Potato___Late_blight/0acdc2b2-0dde-4073-8542-6fca275ab974___RS_LB 4857.JPG",

    "Healthy": "ai/data/raw/Dataset/Potato___healthy/1b434c52-7be4-40c4-90d5-13220f1a3eba___RS_HL 5418.JPG"
}


for expected_class, image_path in images.items():

    result = predict(image_path)

    print("=" * 50)
    print(f"Expected: {expected_class}")
    print(f"Prediction: {result['prediction']}")
    print(f"Confidence: {result['confidence']:.2%}")