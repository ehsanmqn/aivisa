from rembg import remove

def RemoveBackground(data):
    output = remove(data=data,
                    alpha_matting=True,
                    alpha_matting_foreground_threshold=240,
                    alpha_matting_background_threshold=10,
                    alpha_matting_erode_size=10,
                    only_mask=False,
                    post_process_mask=False,
                    session="u2net_human_seg")

    return output
