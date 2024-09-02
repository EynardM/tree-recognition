from util.helpers import *
from util.objects import *
from util.decorators import *

def concatenate_datasets(train_dataset: Dataset, augmented_dataset: Dataset):
    concatenated_dataset = deepcopy(train_dataset)
    
    unique_image_paths = set()
    unique_elements = []
    for element in concatenated_dataset.elements:
        unique_image_paths.add(element.image_path)
        unique_elements.append(element)
    
    for element in augmented_dataset.augmented_elements:
        if element.image_path not in unique_image_paths:
            unique_image_paths.add(element.image_path)
            unique_elements.append(element)
    
    concatenated_dataset.elements = unique_elements
    
    concatenated_dataset.get_stats()
    return concatenated_dataset

def get_augmented_dataset(train_dataset: Dataset):
    train_dataset.get_stats()

    augmented_datasets = []
    for i in trange(len(np.arange(6.0, -0.2, -0.2))):
        k = np.arange(6.0, -0.2, -0.2)[i]
        augmented_dataset_copy = deepcopy(train_dataset)
        augmented_dataset_copy.data_augmentation(k=k)
        augmented_dataset_copy.get_stats()
        augmented_datasets.append(augmented_dataset_copy)
    
    min_dispersion = float('inf')
    optimal_i = None
    for i, dataset in enumerate(augmented_datasets):
        proportions = dataset.proportions
        dispersion = stdev(proportions.values())
        if dispersion < min_dispersion:
            min_dispersion = dispersion
            optimal_i = i

    return augmented_datasets[optimal_i]

def main():
    train_dataset, test_dataset, valid_dataset = get_datasets()
    augmented_dataset = get_augmented_dataset(train_dataset=train_dataset)
    concatenated_dataset = concatenate_datasets(train_dataset, augmented_dataset)

    datasets = {
        'augmented': augmented_dataset,
        'concatenated': concatenated_dataset
    }

    for name, dataset in datasets.items():
        if name == 'augmented':
            dataset_path = DATASET_AUGMENTED_PATH
        elif name == 'concatenated':
            dataset_path = DATASET_CONCATENATED_PATH
        generate_dataset(dataset_path, dataset)
        
if __name__ == "__main__":
    main()
