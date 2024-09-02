from util.imports import *
from util.locations import *
from util.objects import *

def save_datasets(dict_datasets):
    pickle_folder = "pickles"
    os.makedirs(pickle_folder, exist_ok=True)
    for name, dataset in dict_datasets.items():
        filename = os.path.join(pickle_folder, f"dataset_{name}.pkl")
        with open(filename, 'wb') as f:
            pickle.dump(dataset, f)

def load_datasets():
    datasets = {}
    pickle_folder = "pickles"
    for name in ['train', 'augmented', 'test', 'valid']:
        filename = os.path.join(pickle_folder, f"dataset_{name}.pkl")
        with open(filename, 'rb') as f:
            dataset = pickle.load(f)
            datasets[name] = dataset
    return datasets

def print_colored(variable, color):
    color_map = {
        "blue": Fore.BLUE,
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "cyan": Fore.CYAN,
        "magenta": Fore.MAGENTA,
        "white": Fore.WHITE,
        "bright_black": Fore.BLACK + Style.BRIGHT,
        "bright_red": Fore.RED + Style.BRIGHT,
        "bright_green": Fore.GREEN + Style.BRIGHT,
        "bright_yellow": Fore.YELLOW + Style.BRIGHT,
        "bright_cyan": Fore.CYAN + Style.BRIGHT,
        "bright_magenta": Fore.MAGENTA + Style.BRIGHT,
        "bright_white": Fore.WHITE + Style.BRIGHT,
    }

    if color not in color_map:
        print("Couleur non supportée.")
        return

    color_code = color_map[color]
    reset_code = Style.RESET_ALL

    frame = inspect.currentframe().f_back
    variable_name = [name for name, value in frame.f_locals.items() if value is variable][0]

    print(f"{color_code}{variable_name} = {variable}{reset_code}")

def create_dataset(dataset_path):
    dataset = Dataset(dataset_path)
    dataset.populate()
    print(len(dataset.elements))
    dataset.get_stats()
    return dataset

def get_datasets():
    train_dataset = create_dataset(DATASET_TRAIN_PATH)
    test_dataset = create_dataset(DATASET_TEST_PATH)
    valid_dataset = create_dataset(DATASET_VALID_PATH)
    return train_dataset, test_dataset, valid_dataset

def generate_dataset(new_dataset_folder, dataset):
    if not os.path.exists(new_dataset_folder):
        os.makedirs(new_dataset_folder)
        os.makedirs(os.path.join(new_dataset_folder, 'images'))
        os.makedirs(os.path.join(new_dataset_folder, 'labels'))

    # Elements
    if new_dataset_folder == DATASET_AUGMENTED_PATH:
        elements = dataset.augmented_elements

    else:
        elements = dataset.elements

    # Création du dataset
    for element in elements:
        image_path = element.image_path
        label_path = element.label_path

        image_filename = os.path.basename(image_path)
        label_filename = os.path.basename(label_path)

        new_image_path = os.path.join(new_dataset_folder, 'images', image_filename)
        shutil.copyfile(image_path, new_image_path)

        new_label_path = os.path.join(new_dataset_folder, 'labels', label_filename)
        shutil.copyfile(label_path, new_label_path)
    return new_dataset_folder

def create_data_yaml(train_path, valid_path):
    data_yaml = f"""\
train: {train_path}
val: {valid_path}
nc: 4
names: ['Other','Larch-H', 'Larch-LD', 'Larch-HD']
"""
    with open('data.yaml', 'w') as f:
        f.write(data_yaml)

def load_training_config(config_file):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config