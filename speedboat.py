import time

from PIL import Image
from glob import glob
from numpy.random import choice
import os
from itertools import product

import random

project_meta_mock = {
    "name": "test",
    "des": "test dest",
    "n_finals_nft": 10000,
    "layers": {
        "bg": {
            "bg1": {
                "img_path": "xxx",
                "n": 5000
            },
            "bg2": {
                "img_path": "yyy",
                "n": 5000
            }
        },
        "body": {
            "body1": {
                "img_path": "sdf",
                "n": 234
            },
            "body2": {
                "img_path": "asdf",
                "n": 1235
            }
        }
    },
    "layer_priority": "bg|body"
}


def speedboat(key):
    project_data = get_meta(key)
    target = project_data["n_finals_nft"]
    layers = project_data["layers"]

    magic_options = {}
    file_map = {}
    for lay, opts in layers.items():
        magic_options[lay] = []
        for opt_key, opt_data in opts.items():
            magic_options[lay] += [opt_key] * opt_data["n"]
            file_map[opt_key] = opt_data["img_path"]
        if len(magic_options[lay]) < target:
            magic_options[lay] += ["__empty__"] * (target - len(magic_options[lay]))
        random.shuffle(magic_options[lay])

    stack = project_data['layer_priority'].split("|")
    print(magic_options)
    print(file_map)
    print(stack)
    for i in range(target):
        img = None

        meta = {
            "name": f"{project_data['name']} #{i}",
            "tokenId": i,
            "attributes": [],
            "image": key_to_root(key) + f"IMG/{i}"
        }
        for k in stack:
            opt = magic_options[k][i]
            if opt == "__empty__":
                continue
            meta["attributes"].append(
                {"trait_type": k, "value": opt}
            )

            tmp_path = file_map[opt]
            tmp = get_image(tmp_path)
            if img is None:
                img = tmp
            else:
                img.paste(tmp, (0, 0), tmp)

        upload_meta(meta, key_to_root(key) + f"URI/{i}")
        upload_img(img, key_to_root(key) + f"IMG/{i}")


def key_to_root(key):
    return "speedboat.studio/" + key + "/"


def get_meta(key):
    return project_meta_mock


def get_image(link):
    pass


def upload_img(img, path):
    print("upload_img", path)


def upload_meta(meta_dict, path):
    print("upload_meta", path, meta_dict)


speedboat("example_project")
