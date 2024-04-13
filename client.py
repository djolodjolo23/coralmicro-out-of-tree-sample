#!/usr/bin/python3
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import base64
import requests
import sys
from PIL import Image
import os
import io


save_path = 'coral_dev_board_images'
if not os.path.exists(save_path):
    os.makedirs(save_path)  # Ensure the directory exists


def save_image(response, filename):
    result = get_field_or_die(response, 'result')
    image_data_base64 = get_field_or_die(result, 'base64_data')
    image_data = base64.b64decode(image_data_base64)
    width = get_field_or_die(result, 'width')
    height = get_field_or_die(result, 'height')
    image = Image.frombytes('RGB', (width, height), image_data)
    file_path = os.path.join(save_path, f'{filename}.png')  # Change the file extension to '.png'
    image.save(file_path)  # Save the image file as PNG
    print(f'Saved image to {file_path}')
    #image.show()  # Display the image



def get_field_or_die(data, field_name):
  if field_name not in data:
    print(f'Unable to parse {field_name} from data: {data}\r\n')
    sys.exit(1)
  return data[field_name]


def main():
    parser = argparse.ArgumentParser(description='Camera Triggered Example')
    parser.add_argument('--host', type=str, default='10.10.10.1', help='Hostname or IP Address of Coral Dev Board Micro')
    parser.add_argument('--image_width', type=int, default=700, help='Image width')
    parser.add_argument('--image_height', type=int, default=700, help='Image height')

    args = parser.parse_args()
    width = args.image_width
    height = args.image_height

    counter = 1  
    while True:
        try:
            response = requests.post(f'http://{args.host}:80/jsonrpc', json={
                'method': 'get_captured_image',
                'jsonrpc': '2.0',
                'id': 0,
                'params': [{'width': width, 'height': height}]
            }, timeout=10).json()
            save_image(response, f'captured_image_{counter}')
            counter += 1
        except requests.exceptions.ConnectionError:
            print('ERROR: Cannot connect to Coral Dev Board Micro, retrying...')
            continue

if __name__ == '__main__':
    main()