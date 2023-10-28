# Here we will create a color for each category on the labels of the video, so we can better represent each thing that
# appears on the video we are processing
color_map = {
    "car": (0, 0, 255),
    "truck": (0, 0, 100),
    "pedestrian": (255, 0, 0),
    "other vehicle": (0, 0, 150),
    "rider": (200, 0, 0),
    "bicycle": (0, 255, 0),
    "other person": (200, 0, 0),
    "trailer": (0, 150, 150),
    "motorcycle": (0, 150, 0),
    "bus": (0, 0, 100),
}

VIDEO_CODEC = "mp4v"
fps = 59.94
width = 1280
height = 720