import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import os

# Download ImageNet labels
LABELS_URL = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
LABELS_PATH = "imagenet_classes.txt"

if not os.path.exists(LABELS_PATH):
    import urllib.request
    urllib.request.urlretrieve(LABELS_URL, LABELS_PATH)

with open(LABELS_PATH, "r") as f:
    idx_to_labels = [line.strip() for line in f.readlines()]

# Identify dog-related classes from ImageNet
dog_classes = [label.lower() for label in idx_to_labels if any(x in label.lower() for x in [
    "dog", "retriever", "terrier", "spaniel", "sheepdog", "poodle", "hound", "husky", "dachshund"
])]

# Preprocessing pipeline for ResNet
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# Load pre-trained ResNet18 model
model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
model.eval()

def classify_image(image_path):
    img = Image.open(image_path).convert("RGB")
    input_tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        output = model(input_tensor)
    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    top5 = torch.topk(probabilities, 5)

    print(f"\n🖼 Image: {os.path.basename(image_path)}")
    for i in range(5):
        label = idx_to_labels[top5.indices[i]]
        prob = top5.values[i].item()
        print(f"  {i+1}. {label} ({prob*100:.2f}%)")

    return idx_to_labels[top5.indices[0]].lower()

def test_images_in_folder(folder_path):
    misclassified = []
    dog_files = [f for f in os.listdir(folder_path) if "dog" in f.lower()]

    for filename in dog_files:
        img_path = os.path.join(folder_path, filename)
        top1_label = classify_image(img_path)

        if top1_label not in dog_classes:
            misclassified.append((filename, top1_label))

    print("\n📊 Misclassified Dog Images:")
    for fname, prediction in misclassified:
        print(f" - {fname}: predicted '{prediction}'")

    print(f"\nTotal Dog Images Tested: {len(dog_files)}")
    print(f"Misclassified Dogs: {len(misclassified)}")

    return misclassified

# MAIN FUNCTION ENTRY POINT
if __name__ == "__main__":
    folder = "test_images"  # Change as needed

    if not os.path.exists(folder):
        print(f"⚠ Folder '{folder}' not found. Please create it and add test images.")
    else:
        test_images_in_folder(folder)
