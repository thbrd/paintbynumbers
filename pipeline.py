import cv2
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import svgwrite

def generate_paint_by_numbers(input_path, output_png_path, output_svg_path, num_colors):
    img = Image.open(input_path).convert('RGB')
    img_np = np.array(img)
    h, w, c = img_np.shape

    # KMeans clustering
    data = img_np.reshape((-1, 3))
    kmeans = KMeans(n_clusters=num_colors, random_state=42).fit(data)
    clustered = kmeans.cluster_centers_.astype('uint8')[kmeans.labels_]
    clustered_img = clustered.reshape((h, w, 3))

    # Convert to labeled regions
    labels = kmeans.labels_.reshape((h, w))
    unique_labels = np.unique(labels)

    # Create result image with contours and numbers
    result_img = clustered_img.copy()
    gray = cv2.cvtColor(clustered_img, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for i, cnt in enumerate(contours):
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            region_label = labels[cy][cx]
            cv2.putText(result_img, str(region_label), (cx, cy),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)

        cv2.drawContours(result_img, [cnt], -1, (0, 0, 0), 1)

    Image.fromarray(result_img).save(output_png_path)

    # SVG output
    dwg = svgwrite.Drawing(output_svg_path, size=(w, h))
    for i, cnt in enumerate(contours):
        points = cnt.reshape(-1, 2)
        path = "M " + " L ".join([f"{x},{y}" for x, y in points])
        dwg.add(dwg.path(d=path, stroke='black', fill='none', stroke_width=0.5))
    dwg.save()
