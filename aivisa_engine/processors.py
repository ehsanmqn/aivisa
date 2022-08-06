from rembg import remove
import cv2
from rembg.session_factory import new_session


def RemoveBackground(data):
    session = new_session("u2net_human_seg")

    output = remove(data=data,
                    alpha_matting=True,
                    # alpha_matting_foreground_threshold=300,
                    # alpha_matting_background_threshold=20,
                    alpha_matting_erode_size=5,
                    # only_mask=True,
                    post_process_mask=True,
                    session=session
                    )

    return output

