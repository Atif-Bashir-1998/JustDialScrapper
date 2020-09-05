import requests
import os

def save_image(path, image_link, index):
    r = requests.get(image_link)
    with open(f'{index}.png', 'wb') as f:
        f.write(r.content)


save_image(f'images/uae', 'https://akam.cdn.jdmagicbox.com/intimages/us/jd_rwd/dtl_pg_img/gradient-result2.jpg', '1')