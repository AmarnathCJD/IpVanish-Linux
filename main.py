from aiohttp import web
from aiohttp_sse import sse_response
from configs import VPN, remove_duplicate_keys
from utils import get_network_speed, is_openvpn_installed, log_error, log_info
from os import getenv
import requests
from dotenv import load_dotenv
import json
import asyncio

import folium
from folium.plugins import MarkerCluster
import platform

if platform.system().lower() != "linux":
    log_error("This script only works on Linux")
    exit()

if not is_openvpn_installed():
    log_error("OpenVPN is not installed: 'sudo apt install openvpn'")
    exit()

load_dotenv()

USER = getenv("USERNAME")
PASS = getenv("PASSWORD")
NETWORK_INTERFACE = getenv("NETWORK_INTERFACE")

if not NETWORK_INTERFACE:
    log_info("NETWORK_INTERFACE not set, using default 'wlp4s0'")
    NETWORK_INTERFACE = "wlp4s0"

if not USER or not PASS:
    log_info("Please provide a valid IpVanish username and password")
    USER = input("Enter your IpVanish username: ")
    PASS = input("Enter your IpVanish password: ")

vpn = VPN(USER, PASS)

async def handle(request):
    with open("index.html") as f:
        return web.Response(text=f.read(), content_type="text/html")


async def get_countries(request):
    countries = []
    flags = []
    iso_names = []
    for config in VPN.CONFIGS:
        if config["country"] not in countries:
            countries.append(config["country"])
            flags.append(config["flag"])
            iso_names.append(config["iso_name"])

    countries_plus = []
    for a, b, c in zip(countries, flags, iso_names):
        countries_plus.append({"name": c, "code": a, "flag": b})

    return web.json_response(countries_plus)


async def get_cities(request):
    country = request.query.get("country")
    cities = []
    for config in VPN.CONFIGS:
        if config["country"] == country:
            cities.append(config["city"])

    cities.sort()

    return web.json_response(list(set(cities)))


async def get_servers(request):
    city = request.query.get("city")
    country = request.query.get("country")
    servers = []
    for config in VPN.CONFIGS:
        if config["city"] == city and config["country"] == country:
            servers.append(config["server"])

    list(set(servers)).sort()

    return web.json_response(servers)


async def connect(request):
    country = request.query.get("country")
    city = request.query.get("city")
    server = request.query.get("server")

    server_id = None
    for config in VPN.CONFIGS:
        if config["country"] == country:
            if config["city"].lower() in city.lower():
                if config["server"] == server:
                    server_id = config["id"]
                    break

    if server_id is None:
        return web.json_response({"error": "Invalid server"})
    vpn.connect(server_id)

    return web.json_response({"status": "connected"})


async def disconnect(request):
    vpn.disconnect()

    return web.json_response({"status": "disconnected"})


async def ip_info(request):
    req = requests.get("https://ipinfo.io/json",
                       headers={"User-Agent": "curl/7.64.1"})
    response = req.json()
    del response["readme"]
    del response["postal"]

    return web.json_response(response)


async def get_map(request):
    world_map = folium.Map(tiles="cartodbpositron")
    with open("configs/data.json", "r") as file:
        y = json.load(file)

    marker_cluster = MarkerCluster().add_to(world_map)

    for config in y:
        folium.Marker(location=[y[config][0], y[config][1]], popup=config).add_to(
            marker_cluster
        )

    world_map.fit_bounds(world_map.get_bounds(), max_zoom=4)

    return web.Response(text=world_map._repr_html_(), content_type="text/html")


async def get_map_city(request):
    world_map = folium.Map(tiles="openstreetmap")
    city = request.query.get("city")
    with open("configs/data.json", "r") as file:
        y = json.load(file)

    marker_cluster = MarkerCluster().add_to(world_map)

    for config in y:
        if config == city:
            folium.Marker(location=[y[config][0], y[config][1]], popup=config).add_to(
                marker_cluster
            )
            folium.Circle(
                location=y[config],
                color="Red",
                fill=True,
                fill_color="Red",
                radius=int(20000 * 30),
                tooltip=config,
            ).add_to(world_map)

    world_map.fit_bounds(world_map.get_bounds(), max_zoom=4)

    return web.Response(text=world_map._repr_html_(), content_type="text/html")


async def search(request):
    city = request.query.get("city")

    results = []
    for config in VPN.CONFIGS:
        if (
            city.lower() in config["city"].lower()
            or city.lower() in config["country"].lower()
            or city.lower() in config["iso_name"].lower()
        ):
            results.append(config)

    results = remove_duplicate_keys("city", results)

    return web.json_response(results)


async def get_network_speed_req(request):
    try:
        async with sse_response(request) as resp:
            while resp.is_connected():
                try:
                    recv, sent = await get_network_speed(interface=NETWORK_INTERFACE)
                    await resp.send(f"Upload: <span class='text-red-500'>{sent}/s</span>, Download: <span class='text-yellow-400 font-mono'>{recv}/s</span>")
                except Exception as e:
                    await resp.send(str(e))
                await asyncio.sleep(1)
    except:
        pass
    return resp


app = web.Application()
app.router.add_get("/", handle)
app.router.add_get("/countries", get_countries)
app.router.add_get("/cities", get_cities)
app.router.add_get("/servers", get_servers)
app.router.add_get("/connect", connect)
app.router.add_get("/disconnect", disconnect)
app.router.add_get("/ip", ip_info)
app.router.add_get("/map", get_map)
app.router.add_get("/map_city", get_map_city)
app.router.add_get("/search", search)
app.router.add_get("/speed", get_network_speed_req)

web.run_app(app, port=8081)
