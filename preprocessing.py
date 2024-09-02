from util.imports import *
from util.variables import *

def is_not_annotated(category_path):
    return category_path[-1] != "7"

def create_directory(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
        os.makedirs(directory_path)
    else :
        os.makedirs(directory_path)

def get_files_and_path(source, category, directory_to_create):
    category_path = os.path.join(source, category)
    if is_not_annotated(category_path) or category_path in directory_to_create:
        return 0, 0, 0, 0
    else:
        annotations = os.listdir(category_path)[0]
        images = os.listdir(category_path)[1]
        annotation_path = os.path.join(source, category, annotations)
        image_path = os.path.join(source, category, images)
        annotation_files = sorted(os.listdir(annotation_path))
        image_files = sorted(os.listdir(image_path))
        return annotation_files, image_files, annotation_path, image_path

def gather_image_annotation(annotation_files, image_files):
    gathered_files = []
    for annotation in annotation_files:
        for image in image_files:
            if annotation.split(".")[0] in image:
                gathered_files.append((annotation, image))
                continue
    return gathered_files

def split_spot(gathered_list, split_ratio):
    train_split = int(split_ratio[0] * len(gathered_list))
    test_split = train_split + int(split_ratio[1] * len(gathered_list))
    return train_split, test_split

def create_src_path(anot_imag, annotations_path, images_path):
    annotation = anot_imag[0]
    image = anot_imag[1]
    src_path_annotation = os.path.join(annotations_path, annotation)
    src_path_image = os.path.join(images_path, image)
    return src_path_annotation, src_path_image

# For converting XML annotations to YOLO format for a single image
def convert_xml_to_YOLOformat(source, destination):
    """
    Converts XML annotations to YOLO format for a single image.

    Parameters:
    - source (str): Path to the source XML file.
    - destination (str): Path to the destination TXT file (YOLO format).

    Returns:
    None
    """
    tree = ET.parse(source)
    root = tree.getroot()

    # Get image size
    image_size = root.find("size")
    image_width = int(image_size.find("width").text)
    image_height = int(image_size.find("height").text)

    # Open a TXT file for writing
    txt_filename = destination
    with open(txt_filename, 'w') as txtfile:
        # Extract data and write lines
        for obj in root.findall("object"):
            tree_type = obj.find("tree").text
            damage = obj.find("damage").text
            bndbox = obj.find("bndbox")
            xmin = float(bndbox.find("xmin").text)
            ymin = float(bndbox.find("ymin").text)
            xmax = float(bndbox.find("xmax").text)
            ymax = float(bndbox.find("ymax").text)

            # Convert coordinates to YOLO format with normalization
            x_center = (xmin + xmax) / 2.0 / image_width
            y_center = (ymin + ymax) / 2.0 / image_height
            width = (xmax - xmin) / image_width
            height = (ymax - ymin) / image_height

            # Format the line based on tree type and damage
            if tree_type == "Other":
                label = LABELS_TO_INT[tree_type]
                line = f"{label} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n"
            else:
                label = LABELS_TO_INT[f"{tree_type}-{damage}"]
                line = f"{label} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n"
            txtfile.write(line)

    print(f"TXT file '{txt_filename}' has been created.")

def resize_image(source,destination,new_size=(640,640)):
    """
    Resize an image and save the resized image to the destination directory.

    Parameters:
    - source (str): Path to the source image file.
    - destination (str): Path to the destination directory.
    - new_size (tuple): Tuple specifying the new size (width, height) for the resized image.

    Returns:
    None
    """

    filename =source.split("/")[-1]
    try:
        # Open the image file
        image_path = source
        img = Image.open(image_path)

        # Resize the image
        resized_img = img.resize(new_size)

        # Save the resized image to the destination directory
        destination_path = f"{destination}/{filename}"
        resized_img.save(destination_path)

        print(f"Resized {filename} successfully.")
    except Exception as e:
        print(f"Error processing {filename}: {e}")


def clean_and_preprocess_data(source, train_dir, test_dir, val_dir, split_ratio=(0.8, 0.1, 0.1)):
    """
    Cleans and preprocesses data by splitting them into training, testing, and validation sets.
    Converts XML annotations to YOLO format for each image.
    
    Parameters:
    - source (str): Path to the source directory.
    - train_dir (str): Path to the training set directory.
    - test_dir (str): Path to the testing set directory.
    - val_dir (str): Path to the validation set directory.
    - split_ratio (tuple): Split ratios for training, testing, and validation.

    Returns:
    None
    """
    text_extension = ".txt"
    images_dir = "images"
    labels_dir = "labels"
    directory_to_create = [train_dir, test_dir, val_dir]

    for directory in directory_to_create:
        create_directory(f"{directory}/{images_dir}/")
        create_directory(f"{directory}/{labels_dir}/")

    # Iterate through the source directories
    for category in sorted(os.listdir(source)):
        annotation_files, image_files, annotation_path, image_path = get_files_and_path(source, category, directory_to_create)

        if annotation_files == 0:
            continue

        gathered_list = gather_image_annotation(annotation_files, image_files)
        shuffled_list = random.sample(gathered_list, len(gathered_list))
        train_split, test_split = split_spot(gathered_list=gathered_list, split_ratio=split_ratio)

        # Move files to respective directories
        for i, anot_imag in enumerate(shuffled_list):
            try:
                root = anot_imag[0].split(".")[0]
                src_path_annotation, src_path_image = create_src_path(anot_imag, annotation_path, image_path)
                dest_path = (
                    train_dir if i < train_split else test_dir if i < test_split else val_dir
                )
                convert_xml_to_YOLOformat(source=src_path_annotation, destination=f"{dest_path}/{labels_dir}/{root}{text_extension}",LABELS_TO_INT=LABELS_TO_INT)
                resize_image(source=src_path_image,destination=f"{dest_path}/{images_dir}")
            except Exception as e:
                print(f"Error {e}")

if __name__ == "__main__":
    source_directory = "Larch_Dataset"
    destination_directory = "Datasets"
    train_directory = f"{destination_directory}/train"
    test_directory = f"{destination_directory}/test"
    val_directory = f"{destination_directory}/valid"

    clean_and_preprocess_data(source_directory, train_directory, test_directory, val_directory)
