import cv2
import numpy as np
from PIL import Image

def render_numbered_image(image_array, segments, out_path):
    result = image_array.copy()
    for s in segments:
        cv2.drawContours(result, [s['contour']], -1, (0, 0, 0), 1)
        cx, cy = s['center']
        cv2.putText(result, str(s['label']), (cx, cy),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
    Image.fromarray(result).save(out_path)
