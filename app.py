# import flask downloaded before by pip install flask
from flask import Flask, render_template, request
from datetime import datetime
import json
import os

# create an instance of the app
app = Flask(__name__)
DB_FILE_NAME = "db.json"


# json.dump - write to file in json format
# json.load - read from json file

# read message from json file


def load_messages():
    # check if the file exists
    if not os.path.exists(DB_FILE_NAME) or not os.path.getsize(DB_FILE_NAME) > 0:
        return []

    with open(DB_FILE_NAME, "r") as file:
        data = json.load(file)
    return data.get("messages", [])


all_messages = load_messages()


# function for adding messages
def add_message(author, text):
    message = {
        "author": author,
        "text": text,
        "time": datetime.now().strftime("%H:%M:%S")
    }
    # add parametrized message
    all_messages.append(message)
    save_message()


# save message to json file
def save_message():
    all_messages_data = {
        "messages": all_messages
    }
    with open("db.json", "w") as file:
        json.dump(all_messages_data, file)


# make main page's endpoint
@app.route("/")
def main_page():
    return "Hello Lerka"


@app.route("/chat")
def chat_page():
    return render_template("form.html")


@app.route("/get_messages")
def get_messages():
    print("Get all the messages")
    return {"messages": all_messages}


@app.route("/send_message")
def send_message():
    name = request.args.get("name")  # get paramteers from query requests to the server
    text = request.args.get("text")
    print(f"user '{name}' sends '{text}'")
    add_message(name, text)
    return "ok"


@app.route("/status")
def get_status():
    msgs = load_messages()
    length_all_msgs = len(msgs)
    authors = []
    for msg in msgs:
        name = msg["author"]
        if name not in authors:
            authors.append(name)
    return {
        "msg_count": length_all_msgs,
        "authors_count": len(authors)
    }


if __name__ == "__main__":
    # configurate app running's parameters
    app.run(host='0.0.0.0', port=5005)





# some notes for hosting:
# ssh-keygen -t rsa - generate ssh key

# ssh -i <path_to_ssh_key> root@<ip_addr> - enter the server

# adduser <username> - create user

# usermod -aG sudo <username> - give administrator right to the user

# su <username> - change user

# scp -r <path_from> user@<id_addr>:<path_to> - copy to the server (-r  --> recursively)

# sudo apt-get update -update the system

# sudo apt install python3-pip - setup pip

# sudo apt install screen --> utilite for running the app at the background

# screen -d -m python3 main.py --> run the script at the background

# screen -ls --> all the processes' list

# screen -x -s  -- > process id
