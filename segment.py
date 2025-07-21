import cv2
import numpy as np

def extract_segments(label_map):
    h, w = label_map.shape
    segments = []
    for label in np.unique(label_map):
        mask = (label_map == label).astype('uint8') * 255
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                segments.append({'contour': cnt, 'center': (cx, cy), 'label': int(label)})
    return segments
