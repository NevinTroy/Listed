from PIL import Image
import torch
import torchvision.transforms as transforms
from transformers import pipeline, AutoProcessor

image_captioner = pipeline("image-to-text", model="./image_captioning_model_GIT")

checkpoint = "microsoft/git-base"
processor = AutoProcessor.from_pretrained(checkpoint)


def load_image_from_path(image_paths):
    transform = transforms.Compose([
        transforms.Resize(299),
        transforms.CenterCrop(299),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])
    img = Image.open(image_paths)
    img = transform(img)
    return img

def predict_GIT_step(image_paths):
    img=Image.open(image_paths)
    # img=load_image_from_path(image_paths)

    inputs = processor(images=img, return_tensors="pt")
    pixel_values = inputs.pixel_values

    generated_ids = image_captioner.model.generate(pixel_values=pixel_values, max_length=50)
    generated_caption = image_captioner.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_caption
