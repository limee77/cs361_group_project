**Image Finder Microservice<br/>**

**A local Python microservice using ZeroMQ. The service provides random images from categories (currently 'cat' and 'dog'), allowing the user to save images to a history folder, list saved images, delete specified images, and clear history.**

**The image-service runs as a backend microservice, all commands are sent from the UI using structured messages.**

Requirements for running the program:

`python3 -m venv venv`\
`source venv/bin/activate`\
`pip install pillow rich pyzmq`


pyzmq (ZeroMQ Messaging)\
Pillow (PIL) (view images)\
rich (UI formatting)

How to run:\
Terminal 1 -\
`python3 image_service.py`
- Expected output: Image service online and listening on PORT:5555

Terminal 2 -\
`python3 test_client.py`
- This will launch the text-based UI

Example commands sent to the service:
GET a random image -\
`{ "command": "GET", "noun": "cat" }`

SAVE an image to history:\
`{ "command": "SAVE", "path": "images/cat/cat3.png" }`

LIST all saved images:\
`{ "command": "HISTORY" }`

DELETE one image:\
`{ "command": "DELETE", "filename": "cat5.png" }`

CLEAR all history:\
`{ "command": "CLEAR" }`

Example responses:\
Successful - \
`{ "status": "ok", "path": "images/cat/cat7.png" }`

Error - \
`{ "status": "error", "message": "Folder not found" }`

**Provided UML Diagram to show ZeroMQ request flow**
<img width="1221" height="843" alt="Screenshot 2025-11-16 at 1 43 50 PM" src="https://github.com/user-attachments/assets/096a9901-a497-4f52-bc1c-40e6bd21b6e0" />







