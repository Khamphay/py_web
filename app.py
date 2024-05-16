from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from flask_compress import Compress
import time
from threading import Thread, Event
import csv
import os

app = Flask(__name__, static_folder="static")
Compress(app)
socketio = SocketIO(app)
tasks: list[Thread] = []

val1 = 10
val2 = 12
# stop_event: Event


def stop_thread():
    global stop_event
    stop_event.set()


def read_csv_file(start_line: int, end_line: int):
    json_data = []
    total = 0
    with open(os.path.join(os.getcwd(), "static/data_test.csv"), "r") as file:
        csv_data = csv.reader(file, delimiter=",")
        for i, row in enumerate(csv_data):
            if i < start_line:
                continue
            if i > end_line:
                break
            data_dict = {
                "date": row[0],
                "diam1": row[1],
                "diam2": row[2],
                "height": row[3],
                "wieght": row[4],
                "emiss1": row[5],
                "emiss2": row[6],
                "airh1": row[7],
                "airh2": row[8],
                "temp1": row[9],
                "temp2": row[10],
                "temp3": row[11],
            }
            json_data.append(data_dict)
        total = sum(1 for _ in csv_data)
        file.close()
    return {"data": json_data, "total": total}


@app.route("/", methods=["GET"])
def hello():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("perPage", 500, type=int)
    end = per_page * page
    start = (end - per_page) + 1
    json_data = read_csv_file(start, end)
    json_data["page"] = page
    json_data["perPage"] = per_page
    return render_template("index.html", data=json_data, page=4)

@app.route("/data", methods=["POST"])
def data():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("perPage", 500, type=int)
    end = per_page * page
    start = (end - per_page) + 1
    json_data = read_csv_file(start, end)
    json_data["page"] = page
    json_data["perPage"] = per_page
    return jsonify(json_data)


@app.route("/monitor", methods=["POST", "GET"])
def monitor():
    return render_template("monitor.html")


@socketio.on("connect")
def onConnect(client):
    print(f"Client {request.sid} connected!!!")

    def onSendData(interval: int, stop: Event):
        while not stop.is_set():
            global val1
            val1 += 1
            global val2
            val2 += 2
            print("Emit code!!!")
            socketio.emit("data", {"val1": val1, "val2": val2})
            time.sleep(interval)

    global stop_event
    stop_event = Event()
    client = Thread(
        target=onSendData, name=request.sid, args=(5, stop_event), daemon=True
    )
    client.start()
    tasks.append(client)


@socketio.on("disconnect")
def onDisconnect():
    for client in tasks:
        if client.getName() == request.sid:
            stop_thread()
            client.join()
            print(f"Client {request.sid} !!!")
            tasks.remove(client)
            return


if __name__ == "__main__":
    socketio.run(debug=True, port=5000)
