from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from flask_compress import Compress
import time
from threading import Thread, Event
import csv
import os
from datetime import datetime

app = Flask(__name__, static_folder="static")
Compress(app)
socketio = SocketIO(app)
tasks: list[Thread] = []

val1 = 10
val2 = 12
# stop_event: Event

condition = lambda d1, d2: d1 == d2


def stop_thread():
    global stop_event
    stop_event.set()


def read_csv_file(start_line: int, end_line: int, date):
    json_data = []
    total = 0
    with open(os.path.join(os.getcwd(), "static/data_test.csv"), "r") as file:
        lines = csv.reader(file, delimiter=",")
        if date is not None:
            total = sum(1 for l in lines if condition(date, l[0].split(" ")[0]))
        else:
            total = sum(1 for l in lines)
        file.close()
    with open(os.path.join(os.getcwd(), "static/data_test.csv"), "r") as file:
        csv_data = csv.reader(file, delimiter=",")
        for i, row in enumerate(csv_data):
            if date is not None and not condition(date, row[0].split(" ")[0]):
                continue
            if i < start_line:
                continue
            if i > end_line:
                break
            data_dict = {
                "date": row[0],
                "diam1": float(row[1]),
                "diam2": float(row[2]),
                "height": float(row[3]),
                "wieght": float(row[4]),
                "emiss1": float(row[5]),
                "emiss2": float(row[6]),
                "airh1": float(row[7]),
                "airh2": float(row[8]),
                "temp1": float(row[9]),
                "temp2": float(row[10]),
                "temp3": float(row[11]),
            }
            json_data.append(data_dict)
        file.close()
    return {"data": json_data, "total": total}


@app.route("/", methods=["GET"])
def hello():
    # page = request.args.get("page", 1, type=int)
    # per_page = request.args.get("perPage", 500, type=int)
    # end = per_page * page
    # start = (end - per_page) + 1
    # json_data = read_csv_file(start, end)
    # json_data["page"] = page
    # json_data["perPage"] = per_page
    return render_template("index.html")


@app.route("/data", methods=["POST", "GET"])
def data():
    body = request.json
    date = body["date"]
    if date is not None and date != "null":
        orig_date = datetime.strptime(date, "%Y-%m-%d")
        date = datetime.strftime(orig_date, "%d-%m-%Y")
    else:
        date = None
    page = body["page"]
    per_page = body["perPage"]
    end = int(per_page) * int(page)
    start = (end - per_page) + 1  # Skill the header line

    json_data = read_csv_file(start, end, date)
    json_data["page"] = page
    json_data["perPage"] = per_page
    json_data["isRecording"] = False

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
