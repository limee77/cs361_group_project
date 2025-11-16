import zmq
import os
import random
import shutil

# Image Service Program (Backend)
# Author: Liam Gold
# Description: This file contains ONLY backend logic for getting images,
# saving images, deleting them, and clearing history. It does NOT handle
# user input or UI. It communicates with the UI through ZMQ messages.

# ZMQ Setup (Server Side)
# image_service.py is the RESPONSE side (REP)
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
print("Image Service online and listening on PORT:5555")

# Default folder paths
IMAGE_ROOT = "images/"
HISTORY_FOLDER = "history"

# Ensure the history folder exists before saving files
os.makedirs(HISTORY_FOLDER, exist_ok=True)

def get_random_image(noun):
    # returns a random image path from the noun folder (cat, dog)
    folder_path = os.path.join(IMAGE_ROOT, noun)

    # check if the folder exists
    if not os.path.exists(folder_path):
        return {"status": "error", "message": "Folder not found"}

    # get list of PNG images in the folder
    all_files = os.listdir(folder_path)
    image_files = [f for f in all_files if f.endswith(".png")]

    if len(image_files) == 0:
        return {"status": "error", "message": "No images found"}

    # choose a random image
    selected = random.choice(image_files)
    full_path = os.path.join(folder_path, selected)

    return {"status": "ok", "path": full_path}


def get_history():
    # returns a list of images stored in the history folder
    files = [f for f in os.listdir(HISTORY_FOLDER) if f.endswith(".png")]
    return {"status": "ok", "history": files}


def save_image(path):
    # saves an image into the history folder
    try:
        shutil.copy(path, HISTORY_FOLDER)
        return {"status": "ok"}
    except:
        return {"status": "error", "message": "Failed to save image"}


def delete_image(filename):
    # deletes one specific file from the history folder
    file_path = os.path.join(HISTORY_FOLDER, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        return {"status": "ok"}
    return {"status": "error", "message": "File not found"}


def clear_history():
    # deletes ALL PNG images in the history folder
    for f in os.listdir(HISTORY_FOLDER):
        if f.endswith(".png"):
            os.remove(os.path.join(HISTORY_FOLDER, f))
    return {"status": "ok"}

while True:
    request = socket.recv_json()   # receive a JSON command dictionary from the UI

    command = request.get("command")  # extract the command type from UI

    # process commands sent from the UI
    if command == "GET":
        noun = request["noun"]
        response = get_random_image(noun)

    elif command == "SAVE":
        path = request["path"]
        response = save_image(path)

    elif command == "HISTORY":
        response = get_history()

    elif command == "DELETE":
        filename = request["filename"]
        response = delete_image(filename)

    elif command == "CLEAR":
        response = clear_history()

    else:
        response = {"status": "error", "message": "Unknown command"}

    socket.send_json(response)  # send the response back to the UI
