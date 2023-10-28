import pandas as pd
import cv2
import matplotlib.pyplot as plt
import utility as util

# This let us run similar commands that we would run on the terminal when calling the ffmpeg
import subprocess


# This will make the terminal command line from ffmpeg to convert the video file from mov to mp4, using the subprocess
# input_file = f"media/videos/car_on_track_sample_1.mov"
# subprocess.run(['ffmpeg', '-i', input_file, '-qscale', '0', 'car_on_track_sample_1.mp4', '-loglevel', 'quiet'])
# As we don't need to convert each time we execute the code, we will leave it commented


def process_frame_information():
    # With this we will load in the video capture object
    cap = cv2.VideoCapture('media/videos/car_on_track_sample_1.mp4')

    # Now we can use some cv2 methods to extract metadata that will help us
    # This will take the number of frames from the video
    n_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print(f'Number of Frames: {n_frames}')

    # This will take the height and width of the frame from the video
    frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    print(f'Height {frame_height}, Width {frame_width}')

    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f'FPS: {fps:0.2f}')

    # Finally, when we are done of using or interacting with the video, we will use the release() method to stop
    # using it
    cap.release()


def display_cv2_img(image, fig_size=(10, 10)):
    img_ = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    figure, ax = plt.subplots(figsize=fig_size)
    ax.imshow(img_)
    ax.axis("off")


def capture_first_video_frame():
    # We capture the video again to keep processing things, here we will be pulling the images from the video
    cap = cv2.VideoCapture('media/videos/car_on_track_sample_1.mp4')

    # This method will return two things, the return result (which will be True for each capture of the video until
    # we reach the end of it) and the image
    ret, img = cap.read()  # The read method will iterate through each image of the video
    print(f'Returned {ret} and img of shape {img.shape}')

    # This will let us display the image captured with the read() method, the problem with this is that the image
    # will not be quite the same as we saw on the video, so, we will use a function display_cv2_img to make it quite
    # the same as the one on the video plt.imshow(img)

    display_cv2_img(img)
    plt.savefig('media/img/Capture_1.png')
    cap.release()


def process_multiple_video_frames():
    # This will create a grid of images (25 images) that we will be using to capture multiple frames of the video,
    # as the video has 2398 frames, we will need to capture a limited number of frames as this subplot can only get
    # 25 of those
    fig, set_subplot = plt.subplots(5, 5, figsize=(30, 20))
    set_subplot = set_subplot.flatten()  # This wil collapse the array into one dimension (a list) so we can add the
    # images x frame

    # As we did before, we will take the video and get the number of frames, converting it to int, so we can iterate
    # through each frame
    cap = cv2.VideoCapture('media/videos/car_on_track_sample_1.mp4')
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frame_index = 0
    for frame in range(n_frames):
        ret, img = cap.read()
        if not ret:  # This will check if there are still frames available to process, if there is not, will stop
            # looping
            break
        if frame % 100 == 0:
            # As said before, we can only take up to 25 frames, so we will be getting each frame multiple of 100
            set_subplot[frame_index].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))  # This will convert the colors from
            # BGR to RGB
            set_subplot[frame_index].set_title(f'Frame: {frame}')  # We will set the number of the frame we are on
            set_subplot[frame_index].axis('off')  # Also we will remove the axis from the image
            frame_index += 1

    plt.tight_layout()  # This function will adjust the padding between and around the subplots
    plt.savefig('media/img/Multiple_Captures.png')
    cap.release()


def add_annotations_to_frame():
    labels = pd.read_csv('media/csv/mot_labels.csv', low_memory=False)  # Here we take the CSV that has the labels on it
    video_labels = (labels.query('videoName == "026c7465-309f6d33"').reset_index(drop=True).copy())  # As it is a
    # very large dataset, we will make a request to take only the labels concerning our video
    video_labels["video_frame"] = (video_labels["frameIndex"] * 11.9).round().astype("int")  # The video we are
    # processing and the labels on the CSV does not have the same frame rate, for that, we will take the frameIndex
    # from the CSV and convert it into the frame rate of the video we are iterating
    value_counts = video_labels["category"].value_counts()  # This will take the unique values from the DF
    # (DataFrame) from the "category" column
    print(value_counts)

    # The next piece of code will take the frame 1035 so we can process it and add annotations to it
    cap = cv2.VideoCapture('media/videos/car_on_track_sample_1.mp4')
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    for frame in range(n_frames):
        ret, img = cap.read()
        if not ret:
            break
        if frame == 1035:
            break

    frame_1035_labels = video_labels.query('video_frame == 1035')
    img = print_annotations_to_frame(frame_1035_labels, img)
    display_cv2_img(img)
    plt.savefig('media/img/Frame_1035.png')
    cap.release()


def add_annotations_to_video():

    labels = pd.read_csv('media/csv/mot_labels.csv', low_memory=False)
    video_labels = (labels.query('videoName == "026c7465-309f6d33"').reset_index(drop=True).copy())
    video_labels["video_frame"] = (video_labels["frameIndex"] * 11.9).round().astype("int")

    result_video = cv2.VideoWriter("media/videos/video_with_annotations.mp4", cv2.VideoWriter_fourcc(*util.VIDEO_CODEC), util.fps,
                                   (util.width, util.height))

    cap = cv2.VideoCapture('media/videos/car_on_track_sample_1.mp4')
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    for frame in range(n_frames):
        ret, img = cap.read()
        if not ret:
            break
        max_frame = video_labels.query("video_frame <= @frame")["video_frame"].max()
        frame_labels = video_labels.query("video_frame == @max_frame")
        img = print_annotations_to_frame(img, frame_labels)
        result_video.write(img)

    result_video.release()
    cap.release()


def print_annotations_to_frame(img, frame_labels):
    # This will define the font we will use to put text on the img
    # font = cv2.FONT_HERSHEY_TRIPLEX
    for i, d in frame_labels.iterrows():  # This let us iterate over the DF rows as pairs of index/series
        point_1 = int(d['box2d.x1']), int(d['box2d.y1'])  # This will take the coord from the series of the DF so we
        point_2 = int(d['box2d.x2']), int(d['box2d.y2'])  # can know where are the points we want to print
        color = util.color_map[d['category']]
        img = cv2.rectangle(img, point_1, point_2, color, 3)  # This will create the rectangle on the img we specify
        # as parameter, using both points, the color (B, G, R) and the line thickness
        # If we want to add some text on the boxes, for example, the name of each category, we will put the next two
        # lines of code, as this video has a lot of boxes, I'll keep it commented so it does not overload the img
        # pt_text = int(d["box2d.x1"]) + 5, int(d["box2d.y1"]) + 10
        # img = cv2.putText(img, d["category"], pt_text, font, 0.5, color)
    return img


if __name__ == "__main__":
    # process_frame_information()
    # capture_first_video_frame()
    # process_multiple_video_frames()
    # add_annotations_to_frame()
    add_annotations_to_video()

    # We can comment/uncomment each function to test different things, right now it will add all the annotations on the
    # video, if we want to capture frames or process a frame information, we can use the other examples.
