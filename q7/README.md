# Cat & Dog Classifier (ResNet18, ImageNet)

This Python script uses a pre-trained ResNet18 model to classify images of dogs (and other objects) using ImageNet labels. It tests all images in a folder whose filenames contain "dog" and reports any misclassifications.

## Features

- Downloads ImageNet class labels automatically
- Uses PyTorch and torchvision's ResNet18 model
- Preprocesses images for ResNet18
- Classifies each image and prints top-5 predictions
- Checks if "dog" images are correctly classified
- Reports misclassified dog images

## Requirements

- Python 3.8+
- PyTorch
- torchvision
- Pillow

Install dependencies:
```
pip install torch torchvision pillow
```

## How to Use

1. **Prepare your images:**  
   Create a folder named `test_images` in the same directory as `cat_dog_classifier.py`.  
   Add images of dogs (filenames should contain "dog") and other test images.

2. **Run the script:**
   ```
   python cat_dog_classifier.py
   ```

3. **Output:**  
   - For each image, prints the top-5 predicted classes and their probabilities.
   - Lists any dog images that were not classified as a dog.
   - Shows total tested and misclassified dog images.

## Example Output

```
🖼 Image: dog1.jpg
  1. golden retriever (85.23%)
  2. Labrador retriever (10.12%)
  3. cocker spaniel (2.34%)
  4. Pembroke (1.12%)
  5. toy poodle (0.45%)

📊 Misclassified Dog Images:
 - dog_mislabel.jpg: predicted 'tabby cat'

Total Dog Images Tested: 10
Misclassified Dogs: 1
```

## Customization

- To test other animals, change the filename filter in `test_images_in_folder`.
- To use a different folder, edit:
  ```python
  folder = "test_images"
  ```

---

**Author:**  
IIUM Assignment  
September 2025