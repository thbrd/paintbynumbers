import cv2
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

def generate_paint_by_numbers(input_path, output_path, num_colors):
    img = Image.open(input_path).convert('RGB')
    img = img.resize((600, 600))
    img_np = np.array(img)

    h, w, c = img_np.shape
    data = img_np.reshape((-1, 3))

    kmeans = KMeans(n_clusters=num_colors, random_state=42).fit(data)
    clustered = kmeans.cluster_centers_.astype('uint8')[kmeans.labels_]
    clustered_img = clustered.reshape((h, w, 3))

    result_img = Image.fromarray(clustered_img)
    result_img.save(output_path)
