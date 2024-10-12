def rectangles_overlap(x1, y1, w1, h1, x2, y2, w2, h2):
    if abs(y1-y2) <= h2:
        return "Overlap"
    if abs(x1-x2) <= w1:
        return "Overlap"
    return "No overlap"

print(rectangles_overlap(0, 0, 2, 2, 1, 1, 2, 2))