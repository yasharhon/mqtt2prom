from contextlib import asynccontextmanager
from json import loads as jsonloads

from fastapi import FastAPI, Request
from paho.mqtt.client import Client as MqttClient, CallbackAPIVersion


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.latest = {}

    client = MqttClient(CallbackAPIVersion.VERSION2)

    def on_message(client, userdata, msg):
        app.state.latest = jsonloads(msg.payload)

    client.on_message = on_message
    client.loop_start()

    yield

    client.disconnect()
    client.loop_stop()


app = FastAPI(lifespan=lifespan)


@app.get("/test")
def get_data(request: Request):
    return app.state.latest
