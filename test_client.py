from rich import print
from PIL import Image
import zmq
import os

# Image Finder Program (UI)
# Author: Liam Gold
# Description: Handles ALL user interaction, menus, input, viewing images,
# and sends requests to the image-service backend through ZMQ.

# ZMQ setup (Client Side)
# test_client.py is the REQUEST side (REQ)
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
print("[green]Connected to Image Service on PORT 5555[/green]\n")


def generate_image():
    # handles displaying a random image from the backend
    # asks the user if they want to view the image
    # asks the user if they want to save the image to their history folder

    print("[bold blue]Finding an image takes a couple of seconds...[/bold blue]")

    # ask user to choose a noun category (cat/dog)
    noun = input("Enter noun (cat/dog): ").lower()

    # send GET request to backend
    socket.send_json({"command": "GET", "noun": noun})
    reply = socket.recv_json()

    # handle missing folder or missing files
    if reply["status"] != "ok":
        print(f"[bold red]{reply['message']}[/bold red]")
        return

    # backend returned full path to selected image
    image_path = reply["path"]
    print(f"[bold green]Selected Image: {image_path}[/bold green]")

    # ask user if they would like to view the image
    open_image = input("Would you like to view the image? (Yes/No)\n")
    if open_image.lower() == "yes":
        Image.open(image_path).show()

    # ask user if they want to save to history
    to_history = input("Would you like to save image to history folder? (Yes/No):\n")
    if to_history.lower() == "yes":
        socket.send_json({"command": "SAVE", "path": image_path})
        save_reply = socket.recv_json()

        if save_reply["status"] == "ok":
            print("[blue]Image saved to history![/blue]")
        else:
            print("[red]Failed to save image...[/red]")
    else:
        print("Press enter to return to menu...\n")


def history():
    # displays saved images in history folder
    # allows user to delete specific images from history

    print("[bold blue]Welcome to the history page. Here you can delete and view saved images.[/bold blue]")

    # request full history list from backend
    socket.send_json({"command": "HISTORY"})
    reply = socket.recv_json()

    images = reply["history"]

    # if the history folder is empty, handle it
    if len(images) == 0:
        print("[yellow bold]No images found in history...[/yellow bold]")
        input("Press enter to return to menu...\n")
        return

    # display all history images
    print("[bold green]Saved images:[/bold green]", images)

    # ask user if they want to delete any images
    delete_option = input("Would you like to delete an image? (Yes/No): ")

    while delete_option.lower() == "yes":
        print("[bold red]Warning: Deleting an image permanently removes it from your history folder.\n[/bold red]")

        delete_image_name = input("Enter the image filename to delete: ")

        # send delete request to backend
        socket.send_json({"command": "DELETE", "filename": delete_image_name})
        del_reply = socket.recv_json()

        if del_reply["status"] == "ok":
            print(f"[green]{delete_image_name} has been deleted.[/green]")
        else:
            print("[red]Image not found in history.[/red]")

        delete_option = input("Would you like to delete another image? (Yes/No): ")


def settings():
    # allows users to fully clear the entire history folder
    # WARNING: this permanently removes all saved images

    print("[bold blue]Welcome to the settings page. Here you can fully clear your image history[/bold blue]")

    clear_history = input("Would you like to clear your history? (Yes/No): ")

    while clear_history.lower() == "yes":
        print("[bold red]Warning: Clearing history permanently removes ALL images.\n[/bold red]")

        socket.send_json({"command": "CLEAR"})
        reply = socket.recv_json()

        if reply["status"] == "ok":
            print("[green]All images have been removed from history.[/green]")
        else:
            print("[red]Error clearing history[/red]")

        clear_history = input("Press enter to return to menu\n")


# Main menu loop (UI loop)
while True:
    # text-based banner
    print(r"[bold red] __  _  _   __    ___  ____    ____  __  __ _  ____  ____  ____  ")
    print(r"[bold red](  )( \/ ) / _\  / __)(  __)  (  __)(  )(  ( \(    \(  __)(  _ \ ")
    print(r"[bold red] )( / \/ \/    \( (_ \ ) _)    ) _)  )( /    / ) D ( ) _)  )   / ")
    print(r"[bold red](__)\_)(_/\_/\_/ \___/(____)  (__)  (__)\_)__)(____/(____)(__\_) ")

    print("\n[bold blue]Welcome to the Image Finder App![/bold blue]")
    print("This app helps users find and view images based on user input nouns.")
    print("It also saves and manages image history.\n")

    # menu options
    print("\nSelect an option:\n 1. Find Image\n 2. View Image History\n 3. Settings\n 4. Exit Program")

    # user choice
    choice = input("Select a choice between (1-4)\n")

    # menu navigation
    if choice == "1":
        generate_image()
    elif choice == "2":
        history()
    elif choice == "3":
        settings()
    elif choice == "4":
        print("\n[bold red]Exiting program...\n[/bold red]")
        break
    else:
        print("[bold red]Invalid input... Please choose between 1 and 4[/bold red]")
        input("Press enter to return to menu...")
