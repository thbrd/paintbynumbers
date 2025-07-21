import cv2
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image

def reduce_colors(image_path, num_colors, size):
    image = Image.open(image_path).convert('RGB')
    w, h = image.size
    ratio = size / float(w)
    new_h = int(h * ratio)
    image = image.resize((size, new_h))
    img_np = np.array(image)
    h, w, c = img_np.shape
    data = img_np.reshape((-1, 3))
    kmeans = KMeans(n_clusters=num_colors, random_state=0).fit(data)
    labels = kmeans.labels_.reshape((h, w))
    clustered = kmeans.cluster_centers_.astype('uint8')[labels]
    clustered_img = clustered.reshape((h, w, 3))
    return clustered_img, labels, kmeans.cluster_centers_.astype('uint8')
