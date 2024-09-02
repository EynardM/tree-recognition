from util.imports import *
from util.helpers import *
from util.objects import *

dataset_train = get_datasets()
dataset_augmented = create_dataset(DATASET_AUGMENTED_PATH)
dataset_concatenated = create_dataset(DATASET_CONCATENATED_PATH)

dataset_augmented.plot_proportions(use_plotly=True, save_figure=True)
dataset_concatenated.plot_proportions(use_plotly=True, save_figure=True)