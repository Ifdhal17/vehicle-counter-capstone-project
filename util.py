import cv2

WHITE = (255, 255, 255)
RED = (0, 0, 255)
GREEN = (0, 255, 0)


def center_crop(img, dim):
    """Returns center cropped image
    Args:
    img: image to be center cropped
    dim: dimensions (width, height) to be cropped
    """
    width, height = img.shape[1], img.shape[0]

    # process crop width and height for max available dimension
    crop_width = dim[0] if dim[0] < img.shape[1] else img.shape[1]
    crop_height = dim[1] if dim[1] < img.shape[0] else img.shape[0]
    mid_x, mid_y = int(width/2), int(height/2)
    cw2, ch2 = int(crop_width/2), int(crop_height/2)
    crop_img = img[mid_y-ch2:mid_y+ch2, mid_x-cw2:mid_x+cw2]
    return crop_img


def draw_label(frame, label_dict: dict, class_idx: int, x1: int, y1: int, id: int):
    cv2.putText(
        frame,
        f"#{id} {label_dict[class_idx]}",
        (x1, y1 - 10),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.6,
        color=(255, 255, 255),
        thickness=2
    )


def trigger_line(line_point1: int, line_point2: int, offset: int,  y_points: list) -> bool:
    """
        Determines if the center of a line defined by two points falls within a specified offset
        from the center of a bounding box defined by a list of y-coordinates.

        Args:
            line_point1 (int): The y-coordinate of the first point of the line.
            line_point2 (int): The y-coordinate of the second point of the line.
            offset (int): The allowable offset from the center of the bounding box.
            y_points (list): A list of y-coordinates defining the bounding box.

        Returns:
            bool: True if the center of the line is within the offset from the center of the bounding box, False otherwise.
    """
    bbox_y_center = sum(y_points) // len(y_points)

    line_point_center = (line_point1 + line_point2) // 2

    if line_point_center < (bbox_y_center + offset) and line_point_center > (bbox_y_center - offset):
        return True
    else:
        return False


def update_counter(class_idx: int, counter_dict: dict) -> None:
    """
    Updates the count of a specific class in the counter dictionary.

    Args:
        class_idx (int): The index of the class to be updated.
                         Expected values are 0 for 'bus', 1 for 'car', 2 for 'motorbike', and 3 for 'truck'.
        counter_dict (dict): A dictionary where keys are class labels ('bus', 'car', 'motorbike', 'truck')
                             and values are the counts to be updated.

    Returns:
        None
    """
    index_to_class = {0: 'bus', 1: 'car', 2: 'motorbike', 3: 'truck'}
    class_label = index_to_class.get(class_idx)
    if class_label in counter_dict:
        counter_dict[class_label] += 1


def draw_counter(frame, counter_dict: dict):
    bg_x1, bg_y1 = 0, 40  
    bg_x2, bg_y2 = 200, 160  
    cv2.rectangle(frame, (bg_x1, bg_y1), (bg_x2, bg_y2), (0, 0, 0), thickness=-1)

    cv2.putText(
        frame,
        text=f"Car: {counter_dict['car']}",
        org=(0, 60),
        fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL,
        thickness=1, fontScale=1.0, color=GREEN
    )

    cv2.putText(
        frame,
        text=f"Motorbike: {counter_dict['motorbike']}",
        org=(0, 90),
        fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL,
        thickness=1, fontScale=1.0, color=GREEN
    )

    cv2.putText(
        frame,
        text=f"Truck: {counter_dict['truck']}",
        org=(0, 120),
        fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL,
        thickness=1, fontScale=1.0, color=GREEN
    )

    cv2.putText(
        frame,
        text=f"Bus: {counter_dict['bus']}",
        org=(0, 150),
        fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL,
        thickness=1, fontScale=1.0, color=GREEN
    )


def draw_helper_line(img, img_w: int, img_h: int) -> None:
    """
    Draw visualization helper line
    """
    img_w_c, img_h_c = img_w // 2, img_h // 2
    cv2.line(img, pt1=(img_w_c, 0), pt2=(img_w_c, img_h), color=WHITE)
    cv2.line(img, pt1=(0, img_h_c), pt2=(img_w, img_h_c), color=WHITE)
