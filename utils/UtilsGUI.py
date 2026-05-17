import cv2, moviepy, pyautogui, time, numpy

def ScreenShot(path="ScreenShot.png"):
    screenshot = pyautogui.screenshot()
    screenshot.save(path)

def check_camera_available(max_cameras: int = 5):
    for index in range(max_cameras):
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            cap.release()
            return index
        cap.release()
    return None

def take_photo(path='WebCamPhoto.png'):
    camera_index = check_camera_available()
    
    if camera_index is None:
        return False

    cap = cv2.VideoCapture(camera_index)
    success, frame = cap.read()
    cap.release()
    if not success or frame is None:
        return False

    success = cv2.imwrite(path, frame)
    return success

def convert_avi_to_mp4(input_file: str, output_file: str):
    clip = moviepy.VideoFileClip(input_file)
    clip.write_videofile(output_file, codec='libx264', audio=False)

def ScreenVideo(duration_minutesScreen, output_filename: str = "output.avi", fps: int = 20):
    screen_size = pyautogui.size()

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(output_filename, fourcc, fps, screen_size)

    if not out.isOpened():
        return False

    end_time = time.time() + duration_minutesScreen * 60   

    while time.time() < end_time:
        try:
            img = pyautogui.screenshot()
            frame = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)
            out.write(frame)
        except Exception as e:
            out.release()
            cv2.destroyAllWindows()
            return False

    out.release()
    cv2.destroyAllWindows()
    return output_filename

def CameraVideo(duration_minutesWeb, output_filename: str = "camera_output.avi", fps: int = 20):
    camera_index = check_camera_available()
    if camera_index is None:
        return False
    
    width = 640
    height = 480
    duration = duration_minutesWeb * 60

    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        return False
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

    if not out.isOpened():
        cap.release()
        return False

    end_time = time.time() + duration
    frame_count = 0

    while time.time() < end_time:
        success, frame = cap.read()
        if not success or frame is None:
            break
        out.write(frame)
        frame_count += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    if frame_count == 0:
        return False
    return output_filename

