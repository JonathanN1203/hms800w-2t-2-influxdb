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
response = asyncio.run(dtu.async_get_real_data_new())

if response:
    print(response)
    client = InfluxDBClient(influxdb_ip, influxdb_port, influxdb_user, influxdb_password, influxdb_database)
    client.create_database(influxdb_database)

    json_hms800w_2t_inverter = [
        {
            "measurement": "hms800w_2t_inverter",
            "tags": {
                "dtu_sn": response.device_serial_number,
                "inverter_sn": response.sgs_data[0].serial_number,
                "dtu_location": inverter_location
            },
            "fields": {
                "pv_voltage": response.sgs_data[0].voltage / 10,
                "pv_frequency": response.sgs_data[0].frequency / 100,
                "pv_current_power": response.sgs_data[0].active_power / 10,
                "pv_current": response.sgs_data[0].current / 10,
                                "pv_power_factor": response.sgs_data[0].power_factor / 10,
                "pv_daily_yield": response.dtu_daily_energy,
                "pv_temperature": response.sgs_data[0].temperature / 10
            }
        }
    ]
    for i in response.pv_data:
        json_hms800w_2t_panel = [
            {
                "measurement": "hms800w_2t_panel",
                "tags": {
                    "dtu_sn": response.device_serial_number,
                    "pv_port": i.port_number,
                    "dtu_location": inverter_location
                },
                "fields": {
                    "pv_voltage": i.voltage / 10,
                    "pv_current": i.current / 100,
                    "pv_current_power": i.power / 10,
                    "pv_energy_total": i.energy_total,
                    "pv_daily_yield": i.energy_daily
                }
            }
        ]
        client.write_points(json_hms800w_2t_panel)

    client.write_points(json_hms800w_2t_inverter)
