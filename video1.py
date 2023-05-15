from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

#load the video clip
video = VideoFileClip("InShot_20230513_020415078.mp4")

#Define the timestamps and corresponding ss images
timestamps = [0, 7, 14, 21, 28, 35, 42]
screenshot_images = ["uo0v00/title.png", "uo0v00/i8c9y1e.png", "uo0v00/i8c8l6c.png", "uo0v00/i8c8g8a.png", "uo0v00/i8c1rxj.png", "uo0v00/i8bmkh8.png"]


#initialise an empty list to store the screenshot clips
screenshot_clips = []

#create screenshot clips for each timestamp
for timestamp, image_path in zip(timestamps, screenshot_images):
    # load the screenshot
    screenshot = ImageClip(image_path)
    # Set the duration of the screenshot to a small value (e.g., 0.1 seconds)
    screenshot = screenshot.set_duration(7.3)
    # Set the position of the screenshot to the center
    x_pos = (video.size[0] - screenshot.size[0]) // 2  # X-axis position
    y_pos = (video.size[1] - screenshot.size[1]) // 2 - 300 # Y-axis position
    screenshot = screenshot.set_position((x_pos, y_pos))

    # Set the start time of the screenshot
    screenshot = screenshot.set_start(timestamp)

    # Add the screenshot clip to the list
    screenshot_clips.append(screenshot)

    # Composite the video with the screenshot clips
    video_with_screenshots = CompositeVideoClip([video] + screenshot_clips)

    # Write the output video file
    video_with_screenshots.write_videofile("output.mp4", codec="libx264", audio_codec="aac")


