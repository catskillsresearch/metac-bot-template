import websocket
import threading
import json
import asyncio
import requests
import websockets

"""
https://www.perplexity.ai/search/how-do-i-do-this-request-in-py-LKWOZo0lRNegn9r7ALA1dw

Must first run

google-chrome   --remote-debugging-port=9222   --user-data-dir="$HOME/.chrome-debug-test"   https://forecasttrader.interactivebrokers.com/eventtrader/
curl http://localhost:9222/json
"""

# --- Step 1: Auto-fetch cookies from Chrome's DevTools session ---
def get_websocket_debugger_url(domain="forecasttrader.interactivebrokers.com", port=9222):
    tabs = requests.get(f"http://localhost:{port}/json").json()
    for tab in tabs:
        if domain in tab.get("url", ""):
            return tab["webSocketDebuggerUrl"]
    raise Exception("ForecastTrader tab not found.")

async def get_cookie_header_from_chrome_devtools():
    ws_url = get_websocket_debugger_url()
    async with websockets.connect(ws_url) as ws:
        await ws.send(json.dumps({"id": 1, "method": "Network.enable"}))
        await ws.recv()  # Discard ack

        await ws.send(json.dumps({"id": 2, "method": "Network.getAllCookies"}))

        while True:
            response = await ws.recv()
            message = json.loads(response)
            if message.get("id") == 2:
                cookies = message["result"]["cookies"]
                relevant = [
                    f"{c['name']}={c['value']}"
                    for c in cookies
                    if "interactivebrokers.com" in c["domain"]
                ]
                return "; ".join(relevant)

# --- Step 2: Get OI Mapping via WebSocket ---
def get_OI_for_conids(conids, cookie_header):
    WS_URL = "wss://forecasttrader.interactivebrokers.com/portal.proxy/v1/etp/ws"
    FIELDS = ["7638"]
    oi_results = {}
    received_conids = set()
    lock = threading.Lock()
    done_event = threading.Event()

    # Prepare headers
    headers = [
        "Origin: https://forecasttrader.interactivebrokers.com",
        "Referer: https://forecasttrader.interactivebrokers.com/en/home.php",
        "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        f"Cookie: {cookie_header}"
    ]

    def on_open(ws):
        for conid in conids:
            msg = f'smd+{conid}+{json.dumps({"fields": FIELDS, "backout": True})}'
            ws.send(msg)

    def on_message(ws, message):
        try:
            data = json.loads(message)
            if "7638" in data and "conid" in data:
                conid = str(data["conid"])
                oi = data["7638"]
                with lock:
                    if conid not in received_conids:
                        oi_results[conid] = oi
                        received_conids.add(conid)
                    if len(received_conids) >= len(conids):
                        done_event.set()
                        ws.close()
        except Exception:
            pass

    def on_error(ws, error):
        print("❌ WebSocket error:", error)
        done_event.set()

    def on_close(ws, code, msg):
        done_event.set()

    ws_app = websocket.WebSocketApp(
        WS_URL,
        header=headers,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    thread = threading.Thread(target=ws_app.run_forever)
    thread.daemon = True
    thread.start()

    done_event.wait(timeout=20)
    if ws_app.keep_running:
        ws_app.close()
    return oi_results

# --- Step 3: Async wrapper to run it all ---
async def run_get_OI(conids):
    cookie_header = await get_cookie_header_from_chrome_devtools()
    result = get_OI_for_conids(conids, cookie_header)
    return result

# --- Example usage ---
# Run this in an async environment like Jupyter or an asyncio-compatible main
#await run_get_OI(["796056520", "796056525"])
