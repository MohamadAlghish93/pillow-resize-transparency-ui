from PIL import Image
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio import start_server
import io
from datetime import datetime
import time
import argparse

now = datetime.now()


# loading spin
def loading():
    with put_loading(shape='border', color='primary').style('width:4rem; height:4rem'):
        time.sleep(2)


# validate form data
def check_form(data):  # input group validation: return (input name, error msg) when validation fail
    for k, v in data.items():
        if v is None or len(str(v)) < 0:
            return k, 'Requierd!'


def main():
    try:
        func = select('Which function you want?', ['Resize image', 'Transparency image'])
        if func == 'Resize image':
            resize()
        else:
            tspncy()
    except Exception as e:
        put_text(f'Error : {e}').style('color: red;')


def resize():
    put_text('Home').style('color: blue;text-decoration: underline;').onclick(
        lambda: run_js('window.location.reload()'))

    data = input_group("Image info", [
        input('width new image', name='w', type=NUMBER),
        input('high new image', name='h', type=NUMBER)
    ], validate=check_form)

    img = file_upload("Select a image:", accept="image/*")

    if img is not None:
        w = data['w']
        h = data['h']
        image = Image.open(io.BytesIO(img['content']))

        new_image = image.resize((w, h))
        dt_string = now.strftime("%d%m%Y%H%M%S")
        new_name = f'{dt_string}_{w}_{h}.{image.format}'

        loading()

        out_image = new_image.convert('RGB')
        put_image(out_image)
        # File Output
        img_byte_arr = io.BytesIO()
        new_image.save(img_byte_arr, format=image.format)
        put_file(new_name, img_byte_arr.getvalue())

        put_table([
            ['format', image.format],
            ['mode', image.mode],
            ['orginal size', image.size],
            ['palette', image.palette],
            ['new size', new_image.size],
        ])


def tspncy():
    put_text('Home').style('color: blue;text-decoration: underline;').onclick(
        lambda: run_js('window.location.reload()'))
    img = file_upload("Select a image:", accept="image/*")
    if img is not None:
        image = Image.open(io.BytesIO(img['content']))
        image = image.convert("RGBA")
        datas = image.getdata()
        new_data = []

        with put_loading(shape='border', color='warning').style('width:4rem; height:4rem'):
            for item in datas:
                if item[0] == 255 and item[1] == 255 and item[2] == 255:
                    new_data.append((255, 255, 255, 0))
                else:
                    if item[0] > 150:
                        new_data.append((255, 255, 255, 0))
                    else:
                        new_data.append(item)

        image.putdata(new_data)
        dt_string = now.strftime("%d%m%Y%H%M%S")
        new_name = f'{dt_string}_transparency.png'

        loading()
        # # File Output
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        put_image(image.convert('RGB'))
        put_file(new_name, img_byte_arr.getvalue())


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(main, debug=False, port=args.port, cdn=False)
