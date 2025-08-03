import os
from xml.etree import ElementTree as ET
from PIL import Image

input_dir = 'E:/Dataset/Deep Learning Dataset/Safety_Detection_Dataset_Yolo/annotations'
output_dir = 'E:/Dataset/Deep Learning Dataset/Safety_Detection_Dataset_Yolo/labels'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

classes = ["helmet", "vest", "person"] # 👈 Update according to your classes

for filename in os.listdir(input_dir):
    if not filename.endswith(".xml"):
        continue

    tree = ET.parse(os.path.join(input_dir, filename))
    root = tree.getroot()
    image_file = root.find('filename').text
    image_path = os.path.join('E:/Dataset/Deep Learning Dataset/Safety_Detection_Dataset_Yolo/images', image_file)
    img = Image.open(image_path)
    width, height = img.size

    label_file = open(os.path.join(output_dir, filename.replace(".xml", ".txt")), "w")

    for obj in root.findall('object'):
        class_name = obj.find('name').text
        if class_name not in classes:
            continue
        class_id = classes.index(class_name)

        xml_box = obj.find('bndbox')
        xmin = int(xml_box.find('xmin').text)
        ymin = int(xml_box.find('ymin').text)
        xmax = int(xml_box.find('xmax').text)
        ymax = int(xml_box.find('ymax').text)

        x_center = ((xmin + xmax) / 2) / width
        y_center = ((ymin + ymax) / 2) / height
        box_width = (xmax - xmin) / width
        box_height = (ymax - ymin) / height

        label_file.write(f"{class_id} {x_center} {y_center} {box_width} {box_height}\n")

    label_file.close()
    print(f"Converted {filename} to YOLO format.")