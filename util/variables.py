INT_TO_LABELS = {0:"Other",1: "Larch-H", 2: "Larch-LD", 3: "Larch-HD"}
LABELS_TO_INT = {"Other": 0, "Larch-H": 1, "Larch-LD": 2, "Larch-HD": 3}
# LABELS_TO_COLORS = {0: [(255, 0, 255), (0, 0, 0)], 1: [(0, 255, 0), (0, 0, 0)], 2: [(0, 255, 255), (0, 0, 0)], 3: [(0, 0, 255), (0, 0, 0)],}
IMG_SIZE = 640
CO2_TO_KWH = 2.32
LABELS_TO_COLORS = {
    0: [(255, 0, 0), (0, 0, 0)],     # Rouge pour contour, Noir pour remplissage
    1: [(255, 182, 193), (0, 0, 0)], # Saumon pour contour, Noir pour remplissage
    2: [(255, 165, 0), (0, 0, 0)],   # Orange pour contour, Noir pour remplissage
    3: [(255, 255, 0), (0, 0, 0)],   # Jaune pour contour, Noir pour remplissage
}
