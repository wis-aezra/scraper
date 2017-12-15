import subprocess
from os import listdir
from os.path import isfile, join
from PIL import Image


files = [f for f in listdir('pdfs') if isfile(join('pdfs', f))]
subprocess.run(f'mkdir -p images/tmp', shell=True)


def coerce_filename(file_name):
    file_no_ext = file_name[0:-4]
    splitted_file = file_no_ext.split(' ')
    if len(splitted_file) > 1:
        coerced_file = '{}_{}'.format(splitted_file[0],
                                      splitted_file[len(splitted_file) - 1])
    else:
        coerced_file = splitted_file[0]
    return coerced_file


def image_extractor(file_name):
    reworked_file = coerce_filename(file_name)
    target_string = f'pdfimages -f 1 -l 1 ' \
                    f'"pdfs/{file_name}" "images/tmp/{reworked_file}"'
    subprocess.run(target_string, shell=True)

for file in files:
    image_extractor(file)
    tmp_files = [f for f in listdir('images/tmp') if isfile(join('images/tmp',
                                                                 f))]
    if len(tmp_files) > 0:
        squares = {}
        for tmp_file in tmp_files:
            im = Image.open(f'images/tmp/{tmp_file}')
            width, height = im.size
            squares[tmp_file] = width * height

        cover_image = max(squares, key=squares.get)
        subprocess.run(f'mv "images/tmp/{cover_image}" "images/{cover_image}"',
                       shell=True)
        subprocess.run(f'rm -rfv images/tmp/*', shell=True)
    else:
        renamed_file = coerce_filename(file)
        subprocess.run(f'cp images/default/default.jpg '
                       f'images/{renamed_file}.ppm', shell=True)
