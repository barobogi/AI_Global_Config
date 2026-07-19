import os
import json

CHANNELS_FILE = r"D:\AI\25_auto_pobbagi\channels.json"

def load_channels():
    if os.path.exists(CHANNELS_FILE):
        with open(CHANNELS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # 호환성 위해 딕셔너리를 객체로 변환
            for k, v in data.items():
                if isinstance(v, str):
                    data[k] = {"name": v, "weight": 1.0}
            return data
    return {}

def save_channels(data):
    with open(CHANNELS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def update_channel_weight(channel_id, feedback):
    channels = load_channels()
    if channel_id in channels:
        current_weight = channels[channel_id].get("weight", 1.0)
        if feedback == "good":
            current_weight = min(2.0, current_weight + 0.1)
        elif feedback == "pass":
            current_weight = max(0.5, current_weight - 0.05)
        channels[channel_id]["weight"] = current_weight
        save_channels(channels)

def add_channel(channel_id, channel_name):
    channels = load_channels()
    channels[channel_id] = {"name": channel_name, "weight": 1.0}
    save_channels(channels)

def remove_channel(channel_id):
    channels = load_channels()
    if channel_id in channels:
        del channels[channel_id]
        save_channels(channels)
