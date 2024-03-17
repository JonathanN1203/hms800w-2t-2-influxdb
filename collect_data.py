from hoymiles_wifi.dtu import DTU
from influxdb import InfluxDBClient
import asyncio
import socket

inverter_ip = ""
inverter_location = ""

influxdb_ip = ""
influxdb_port = ""
influxdb_user = ""
influxdb_password = ""
influxdb_database = ""

dtu = DTU(inverter_ip)
response = asyncio.run(dtu.async_get_real_data_hms())

def write_date(dtu_data):
    print(dtu_data)

if response:
    print(response)
    client = InfluxDBClient(influxdb_ip, influxdb_port, influxdb_user, influxdb_password, influxdb_database)
    client.create_database(influxdb_database)

    json_hms800w_2t_inverter = [
        {
            "measurement": "hms800w_2t_inverter",
            "tags": {
                "dtu_sn": response.dtu_sn,
                "inverter_sn": response.inverter_state[0].inv_id,
                "dtu_location": inverter_location
            },
            "fields": {
                "grid_voltage": response.inverter_state[0].grid_voltage / 10,
                "grid_freq": response.inverter_state[0].grid_freq / 100,
                "pv_current_power": response.inverter_state[0].pv_current_power / 10,
                "pv_daily_yield": response.pv_daily_yield,
                "temperature": response.inverter_state[0].temperature / 10
            }
        }
    ]
    for i in response.port_state:
        json_hms800w_2t_panel = [
            {
                "measurement": "hms800w_2t_panel",
                "tags": {
                    "dtu_sn": response.dtu_sn,
                    "pv_port": i.pv_port,
                    "dtu_location": inverter_location
                },
                "fields": {
                    "pv_vol": i.pv_vol / 10,
                    "pv_cur": i.pv_cur / 100,
                    "pv_power": i.pv_power / 10,
                    "pv_energy_total": i.pv_energy_total,
                    "pv_daily_yield": i.pv_daily_yield
                }
            }
        ]
        client.write_points(json_hms800w_2t_panel)
    client.write_points(json_hms800w_2t_inverter)
