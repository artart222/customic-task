from PIL import Image, ImageDraw, ImageFont

from celery import shared_task

from .models import Mockup, MockupTask

from customic.settings import BASE_SHIRT_DIR, FONT_SIZE, FONTS_DIR

import os
from pathlib import Path


# TODO:  Refactor this function and seperate it jobs into different functions.
# TODO:  Add more comments.
# TODO:  Add type hints.
# TODO:  Add logger.
# TODO:  Find better way to align text on shirt.
# TODO:  Write unit tests.
# FIXME: FIX picking custom font.
@shared_task()
def make_mockup_image(task_id):
    mockup_task = MockupTask.objects.get(task_id=task_id)

    text = mockup_task.text
    font = mockup_task.font
    used_font_name = ""
    text_color = mockup_task.text_color
    shirt_color = mockup_task.shirt_color

    # If shirt_color isn't provided it will list all default
    # shirt images in BASE_SHIRT_DIR directory.
    if shirt_color is None:
        shirt_color = []
        for file in os.listdir(BASE_SHIRT_DIR.as_posix()):
            shirt_color.append(Path(file).stem)

    try:
        font_location = FONTS_DIR.as_posix() + "/" + str(font)
        font = ImageFont.truetype(font_location, FONT_SIZE)
        used_font_name = mockup_task.font
    except (OSError, AttributeError):
        font = ImageFont.load_default(size=FONT_SIZE)
        used_font_name = "Arial"

    for item in shirt_color:
        # Finding absoulte path to base shirt image.
        input_file_locations = BASE_SHIRT_DIR / f"{item}.png"

        # Making output file name.
        # BUG: Using counting objects can create duplicate
        # filenames if two tasks run in parallel I think?
        built_mockup_items = Mockup.objects.count()
        output_file_location = f"media/mockups/{built_mockup_items + 1}.png"

        with Image.open(input_file_locations) as img:
            draw = ImageDraw.Draw(img)

            position = (round(img.size[0] * 0.35), round(img.size[1] * 0.3))

            if text_color is None:
                text_color = calculate_good_text_color(img.getpixel(position))

            image_url = f"http://127.0.0.1:8000/{output_file_location}"  # TODO: Fix this magic url.

            draw.text(position, text, fill=text_color, font=font, font_size=FONT_SIZE)

            # Save the modified image
            img.save(output_file_location)
            Mockup.objects.create(
                task=mockup_task,
                text=text,
                font=used_font_name,
                text_color=text_color,
                shirt_color=item,
                image_url=image_url,
            )

            # Reset text_color at the end of loop so luminance function
            # can work without problem. If you don't do this and luminance
            # function calculate the correct color for text it will remember
            # that and use it on all t-shirts and because of that we can have
            # white on white and black on black.
            text_color = None or mockup_task.text_color

        mockup_task.status = "SUCCESS"  # TODO: Fix this magic string.
        mockup_task.message = (
            "ساخت تصویر با موفقیت به اتمام رسید"  # TODO: Fix this magic string.
        )
        mockup_task.save()


def calculate_good_text_color(rgb: tuple):
    # standard luminance formula
    r, g, b = rgb[0], rgb[1], rgb[2]
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    # Return desired text color based on luminance.
    return (0, 0, 0) if luminance > 127 else (255, 255, 255)
