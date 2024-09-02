from util.imports import *
from util.locations import *
from util.variables import * 
from util.draw import *

class Data:
    def __init__(self, image_path, label_path, id):
        self.id = id
        self.image_path = image_path
        self.label_path = label_path
        self.annotations = None

        self.trees = None
        self.proportions = None

    def __str__(self):
        return f"Id: {self.id}, Annotations: {self.annotations}"
    
    def get_annotations(self) -> None:
        with open(self.label_path, 'r') as file:
            lines = file.readlines()
            annotations = [line.strip().split() for line in lines]
            self.annotations = []
            for annotation in annotations:
                self.annotations.append([int(annotation[0]), float(annotation[1]), float(annotation[2]), float(annotation[3]), float(annotation[4])])
    
    def get_stats(self) -> None:
        nb_trees = {label: 0 for label in INT_TO_LABELS.values()}
        if len(self.annotations) != 0:
            trees_sum = len(self.annotations)
            for annotation in self.annotations:
                tree_type = int(annotation[0])
                label = INT_TO_LABELS[tree_type]
                nb_trees[label] += 1
            proportions = {label: count / trees_sum for label, count in nb_trees.items()}
            self.trees = nb_trees
            self.proportions = proportions
        else:
            for key in list(LABELS_TO_INT.keys()):
                LABELS_TO_INT[key] = 0
            self.trees = LABELS_TO_INT
            self.proportions = LABELS_TO_INT
    
    def init(self) -> None:
        self.get_annotations()
        self.get_stats()

    def plot_proportions(self) -> None:
        labels = list(self.proportions.keys())
        proportions = list(self.proportions.values())

        plt.figure(figsize=(10, 6))
        plt.bar(labels, proportions)
        plt.xlabel('Type d\'arbre')
        plt.ylabel('Proportion')
        plt.title('Proportions des différents types d\'arbres')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        
class Dataset:
    def __init__(self, data_folder):
        self.data_folder = data_folder
        self.name = os.path.basename(data_folder)
        
        self.proportions = None
        self.trees = None

        self.elements = []
        self.augmented_elements = []

    def __str__(self):
        return f"Name: {self.name}\n"

    def populate(self) -> None:
        for file in os.listdir(os.path.join(self.data_folder, 'images')):
            if file.endswith('.JPG') or file.endswith('.jpg'):
                file_id = os.path.splitext(file)[0]
                image_path = os.path.join(self.data_folder, 'images', file)
                label_file = file_id + '.txt'
                label_path = os.path.join(self.data_folder, 'labels', label_file)
                if os.path.isfile(label_path):
                    element = Data(image_path, label_path, file_id)
                    self.elements.append(element)

    def get_stats(self) -> None:
        nb_trees_total = {label: 0 for label in INT_TO_LABELS.values()}
        total_trees = 0
        for element in self.elements + self.augmented_elements:
            element.get_annotations()
            element.get_stats()
            total_trees += sum(element.trees.values())
            for label, count in element.trees.items():
                nb_trees_total[label] += count

        proportions_total = {label: count / total_trees for label, count in nb_trees_total.items()}

        self.proportions = proportions_total
        self.trees = nb_trees_total
        
    def plot_proportions(self, use_plotly=False, save_figure=False):
        labels = list(self.proportions.keys())
        proportions = list(self.proportions.values())
        filename_prefix = os.path.basename(self.data_folder)

        if use_plotly:
            fig = go.Figure(data=[go.Bar(x=labels, y=proportions)])
            fig.update_layout(
                title=f'Proportions of different types of trees in {self.name} Dataset',
                xaxis_title='Tree Type',
                yaxis_title='Proportion',
                xaxis_tickangle=-45,
                xaxis_tickmode='linear',
                xaxis_tickvals=labels,
                xaxis_ticktext=labels,
                bargap=0.1
            )
            if save_figure:
                filename = f"{filename_prefix}_proportions_plot"
                fig.write_image(filename + ".png", width=800, height=600)
            else:
                fig.show()
        else:
            plt.figure(figsize=(10, 6))
            plt.bar(labels, proportions)
            plt.xlabel('Tree Type')
            plt.ylabel('Proportion')
            plt.title(f'Proportions of different types of trees in {self.name} Dataset')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            if save_figure:
                filename = f"{filename_prefix}_proportions_plot"
                plt.savefig(filename + ".png")
            else:
                plt.show()

    def data_augmentation(self, k=2):
        selected_elements = []
        for element in self.elements:
            if (element.proportions['Larch-H'] >= element.proportions['Larch-LD'] * k) or \
                (element.proportions['Larch-HD'] >= element.proportions['Larch-LD'] * k):
                selected_elements.append(element)

        for element in selected_elements:
            image = cv2.imread(element.image_path)
            filtered_image = cv2.GaussianBlur(image, (5, 5), 0)

            for angle in range(3):
                rotated_image = cv2.rotate(image, angle)
                filtered_rotated_image = cv2.GaussianBlur(rotated_image, (5, 5), 0)

                rotated_annotations = []
                for annotation in element.annotations:
                    tree_type, x, y, box_width, box_height = annotation

                    if angle == 2:
                        rotated_x = y  
                        rotated_y = 1 - x  
                        rotated_box_width = box_height
                        rotated_box_height = box_width

                    elif angle == 1:
                        rotated_x = 1 - x  
                        rotated_y = 1 - y   
                        rotated_box_width = box_width
                        rotated_box_height = box_height

                    elif angle ==  0:
                        rotated_x = 1 - y  
                        rotated_y = x  
                        rotated_box_width = box_height
                        rotated_box_height = box_width

                    rotated_annotations.append([tree_type, rotated_x, rotated_y, rotated_box_width, rotated_box_height])

                filename = f"{element.id}_{angle}"
                augmented_image_path = os.path.join(DATASET_TMP_PATH+'/images', filename+".jpg")
                cv2.imwrite(augmented_image_path, rotated_image)

                augmented_label_path = os.path.join(DATASET_TMP_PATH+'/labels', filename+".txt")
                with open(augmented_label_path, 'w') as f:
                    for annotation in rotated_annotations:
                        f.write(' '.join(map(str, annotation)) + '\n')

                augmented_element = Data(augmented_image_path, augmented_label_path, filename)
                self.augmented_elements.append(augmented_element)

                filtered_image_path = os.path.join(DATASET_TMP_PATH+'/images', filename+"_f"+".jpg")
                cv2.imwrite(filtered_image_path, filtered_rotated_image)

                filtered_label_path = os.path.join(DATASET_TMP_PATH+'/labels', filename+"_f"+".txt")
                with open(filtered_label_path, 'w') as f:
                    for annotation in rotated_annotations:
                        f.write(' '.join(map(str, annotation)) + '\n')

                augmented_element = Data(filtered_image_path, filtered_label_path, filename+"_f")
                self.augmented_elements.append(augmented_element)

            filtered_label_path = os.path.join(DATASET_TMP_PATH+'/labels', filename+"_f"+".txt")
            with open(filtered_label_path, 'w') as f:
                for annotation in element.annotations:
                    f.write(' '.join(map(str, annotation)) + '\n')

            mirrored_image = cv2.flip(image, 1)
            mirrored_annotations = [[ann[0], 1 - ann[1], ann[2], ann[3], ann[4]] for ann in element.annotations]
            mirrored_image_path = os.path.join(DATASET_TMP_PATH+'/images', filename+"_m"+".jpg")
            mirrored_label_path = os.path.join(DATASET_TMP_PATH+'/labels', filename+"_m"+".txt")          
            cv2.imwrite(mirrored_image_path, mirrored_image)

            with open(mirrored_label_path, 'w') as f:
                for annotation in mirrored_annotations:
                    f.write(' '.join(map(str, annotation)) + '\n')

            augmented_element = Data(mirrored_image_path, mirrored_label_path, filename+"_m")
            self.augmented_elements.append(augmented_element)
            
            mirrored_filtered_image = cv2.flip(filtered_image, 1)  
            mirrored_filtered_path = os.path.join(DATASET_TMP_PATH+'/images', filename+"_f_m"+".jpg")
            mirrored_filtered_label_path = os.path.join(DATASET_TMP_PATH+'/labels', filename+"_f_m"+".txt")
            cv2.imwrite(mirrored_filtered_path, mirrored_filtered_image)
            
            with open(mirrored_filtered_label_path, 'w') as f:
                for annotation in mirrored_annotations:
                    f.write(' '.join(map(str, annotation)) + '\n')

            augmented_element = Data(mirrored_image_path, mirrored_filtered_label_path, filename+"_f_m")
            self.augmented_elements.append(augmented_element)