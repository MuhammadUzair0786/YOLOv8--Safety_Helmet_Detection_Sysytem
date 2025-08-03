import os
import shutil
import random

def setup_yolo_structure(base_path):
    images_path = os.path.join(base_path, "images")
    labels_path = os.path.join(base_path, "labels")

    # Subfolders to create
    for split in ["train", "valid"]:
        os.makedirs(os.path.join(images_path, split), exist_ok=True)
        os.makedirs(os.path.join(labels_path, split), exist_ok=True)

    # Get all image files (ignore subfolders)
    all_images = [f for f in os.listdir(images_path)
                  if f.lower().endswith(('.jpg', '.png', '.jpeg')) and os.path.isfile(os.path.join(images_path, f))]

    print(f"[INFO] Found {len(all_images)} total images.")
    if len(all_images) == 0:
        print("[ERROR] No images found in the images folder.")
        return

    random.shuffle(all_images)
    split_index = int(0.8 * len(all_images))
    train_files = all_images[:split_index]
    valid_files = all_images[split_index:]

    def copy_files(file_list, split):
        for img_file in file_list:
            label_file = os.path.splitext(img_file)[0] + ".txt"
            src_img = os.path.join(images_path, img_file)
            src_label = os.path.join(labels_path, label_file)

            dst_img = os.path.join(images_path, split, img_file)
            dst_label = os.path.join(labels_path, split, label_file)

            if os.path.exists(src_img) and os.path.exists(src_label):
                shutil.copy(src_img, dst_img)
                shutil.copy(src_label, dst_label)
            else:
                print(f"[WARNING] Missing image or label for {img_file}")

    copy_files(train_files, "train")
    copy_files(valid_files, "valid")

    # Write data.yaml
    yaml_path = os.path.join(base_path, "data.yaml")
    dataset_path = base_path.replace("\\", "/")

    with open(yaml_path, "w") as f:
        f.write(f"""path: {dataset_path}
train: images/train
val: images/valid
nc: 3
names: ['helmet', 'vest', 'person']
""")

    print(f"[INFO] Dataset structure prepared successfully!")
    print(f"[INFO] data.yaml created at: {yaml_path}")

# ✅ Run it
if __name__ == "__main__":
    setup_yolo_structure("E:/Dataset/Deep Learning Dataset/Safety_Detection_Dataset_Yolo")
