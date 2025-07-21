import svgwrite

def render_svg(segments, color_map, out_path, size):
    dwg = svgwrite.Drawing(out_path)
    for seg in segments:
        points = seg['contour'].reshape(-1, 2)
        path_data = "M " + " L ".join([f"{x},{y}" for x, y in points])
        dwg.add(dwg.path(d=path_data, fill='none', stroke='black', stroke_width=0.5))
        cx, cy = seg['center']
        dwg.add(dwg.text(str(seg['label']), insert=(cx, cy), font_size='6px', fill='black'))
    dwg.save()
