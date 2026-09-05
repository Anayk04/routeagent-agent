import json
from typing import Any
import requests
from langchain.tools import tool
from config import BACKEND_URL, BACKEND_JWT_TOKEN
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {BACKEND_JWT_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _request(method: str, url: str, **kwargs: Any) -> str:
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=_headers(),
            timeout=30,
            **kwargs,
        )
        response.raise_for_status()
        if not response.content:
            return json.dumps({"success": True, "status_code": response.status_code})
        try:
            data = response.json()
        except ValueError:
            data = {"response": response.text}
        return json.dumps(data, indent=2)
    except requests.RequestException as exc:
        return json.dumps({"success": False, "error": str(exc)}, indent=2)


@tool
def get_pending_shipments() -> str:
    """Fetches all shipments with PENDING status that need dispatch."""
    return _request("GET", f"{BACKEND_URL}/api/shipments", params={"status": "PENDING"})


@tool
def get_available_drivers() -> str:
    """Returns all drivers currently available, including their current location."""
    return _request("GET", f"{BACKEND_URL}/api/drivers", params={"status": "AVAILABLE"})


@tool
def get_idle_vehicles() -> str:
    """Returns all idle vehicles ready for use, including their current location."""
    return _request("GET", f"{BACKEND_URL}/api/vehicles", params={"status": "IDLE"})


@tool
def calculate_distance(origin: str, destination: str) -> str:
    """
    Calculates real driving distance and duration between two locations
    using Google Maps Distance Matrix API.
    Use this to find how far a vehicle or driver is from a shipment pickup point.
    Args:
        origin: Starting location (e.g. 'Mumbai, India')
        destination: Destination location (e.g. 'Delhi, India')
    Returns distance in km and estimated travel duration.
    """
    try:
        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "origins": origin,
            "destinations": destination,
            "units": "metric",
            "key": GOOGLE_MAPS_API_KEY,
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("status") != "OK":
            return json.dumps({
                "error": f"API error: {data.get('status')}",
                "origin": origin,
                "destination": destination,
            })

        element = data["rows"][0]["elements"][0]

        if element.get("status") != "OK":
            return json.dumps({
                "error": f"Route not found: {element.get('status')}",
                "origin": origin,
                "destination": destination,
            })

        distance_km = element["distance"]["value"] / 1000
        duration_min = element["duration"]["value"] // 60

        return json.dumps({
            "origin": origin,
            "destination": destination,
            "distanceKm": round(distance_km, 1),
            "durationMinutes": duration_min,
            "distanceText": element["distance"]["text"],
            "durationText": element["duration"]["text"],
        })

    except Exception as e:
        return json.dumps({
            "error": str(e),
            "origin": origin,
            "destination": destination,
        })


@tool
def dispatch_shipment(
    shipment_id: str,
    driver_id: str,
    vehicle_id: str,
    reasoning: str,
) -> str:
    """
    Assigns a driver and vehicle to a shipment and triggers dispatch.
    Always provide detailed reasoning including weight, capacity,
    real driving distance from vehicle to shipment origin, and why
    this combination was optimal.
    """
    payload = {
        "shipmentId": shipment_id,
        "driverId": driver_id,
        "vehicleId": vehicle_id,
        "reasoning": reasoning,
    }
    return _request("POST", f"{BACKEND_URL}/api/dispatch", json=payload)


TOOLS = [
    get_pending_shipments,
    get_available_drivers,
    get_idle_vehicles,
    calculate_distance,
    dispatch_shipment,
]