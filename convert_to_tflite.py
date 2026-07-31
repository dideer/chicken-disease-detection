import tensorflow as tf

model_path = r"D:\TUMBA\FINAL PROJECT\Poultry Disease\backend\best_model.keras"
output_path = r"D:\TUMBA\FINAL PROJECT\Poultry Disease\backend\best_model.tflite"

print("Loading model...")
model = tf.keras.models.load_model(model_path)

print("Converting to TFLite...")
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open(output_path, 'wb') as f:
    f.write(tflite_model)

print("✅ Done! File saved as best_model.tflite")