from contextlib import asynccontextmanager
from json import loads as jsonloads

from fastapi import FastAPI
from paho.mqtt.client import Client as MqttClient, CallbackAPIVersion

from routes import metrics_router
from settings import AppSettings

settings = AppSettings(_env_file=".env")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.latest = {}

    client = MqttClient(CallbackAPIVersion.VERSION2)

    def on_message(client, userdata, msg):
        app.state.latest = jsonloads(msg.payload)

    client.on_message = on_message
    client.connect(settings.mqtt_host, settings.mqtt_port, 60)
    client.loop_start()

    yield

    client.disconnect()
    client.loop_stop()


app = FastAPI(lifespan=lifespan)

app.include_router(metrics_router)
