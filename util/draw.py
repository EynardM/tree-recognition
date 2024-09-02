from util.imports import *
from util.variables import *
from util.locations import *

def draw_bbox(image, bbox, rect_color, text_color, text):
    center_x, center_y, width, height = bbox
    xmin = int((center_x - width / 2)*IMG_SIZE)
    ymin = int((center_y - height / 2)*IMG_SIZE)
    xmax = int((center_x + width / 2)*IMG_SIZE)
    ymax = int((center_y + height / 2)*IMG_SIZE)
    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), rect_color, 2)
    (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
    cv2.rectangle(image, (xmin, ymin - text_height - 5), (xmin + text_width, ymin), rect_color, -1)
    cv2.putText(image, text, (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 2)
    return image

def get_annotated_image(annotations, image, annotated_folder, filename):
    for annotation in annotations:
        tree_type, center_x, center_y, width, height = annotation
        rect_color, text_color = LABELS_TO_COLORS[tree_type]
        text = INT_TO_LABELS[tree_type]
        draw_bbox(image, annotation[1:], rect_color, text_color, text)
    annotated_path = os.path.join(annotated_folder, filename)
    cv2.imwrite(annotated_path, image)
