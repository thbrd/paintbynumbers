import cluster
import segment
import paint
import svg_gen

def run_pipeline(input_path, output_png, output_svg, num_colors, size):
    clustered_img, label_map, color_map = cluster.reduce_colors(input_path, num_colors, size)
    segments = segment.extract_segments(label_map)
    paint.render_numbered_image(clustered_img, segments, output_png)
    svg_gen.render_svg(segments, color_map, output_svg, size)
