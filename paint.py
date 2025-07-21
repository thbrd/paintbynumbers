import cv2
import numpy as np
from PIL import Image

def render_numbered_image(image_array, segments, out_path, label_map):
    result = image_array.copy()
    h, w = label_map.shape
    labels = np.unique(label_map)
    label_to_number = {label: i + 1 for i, label in enumerate(labels)}
    for s in segments:
        label_num = label_to_number[s['label']]
        cv2.drawContours(result, [s['contour']], -1, (0, 0, 0), 2, lineType=cv2.LINE_AA)
        cx, cy = s['center']
        # Check kleurcontrast: gebruik witte tekst bij donkere kleuren
        pixel = result[cy, cx]
        brightness = int((pixel[0] + pixel[1] + pixel[2]) / 3)
        text_color = (0, 0, 0) if brightness > 128 else (255, 255, 255)
        cv2.putText(result, str(label_num), (cx, cy),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2, cv2.LINE_AA)
    Image.fromarray(result).save(out_path)
