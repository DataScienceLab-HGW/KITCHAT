import serial
from utils import make_state_string
import datetime as dt
import pandas as pd
from struct import unpack


def setup_serial_com(dev_name):
    print(f'### Opening serial communication with device {dev_name}')
    ser_com = serial.Serial(dev_name, 115200, timeout=1)
    return ser_com
    
# get data from sensors and update the state
def compute_data_and_state(serial_obj, weights)-> pd.DataFrame:
    coffee_in_place, frenchpress_in_place, boiler_in_place, boiler_full_water = False, False, False, False
    
    coffee_weight, frenchpress_weight, boiler_weight = read_weights(serial_obj)

    weights.loc[len(weights.index)] = [dt.datetime.now().strftime('%H:%M:%S'), coffee_weight, frenchpress_weight, boiler_weight]
    print("COmputing data...")
    if coffee_weight > 410:
        coffee_in_place = True
    
    if frenchpress_weight>310:
        frenchpress_in_place = True
    
    if boiler_weight > 250:
        boiler_in_place = True

    if boiler_weight > 500:
        boiler_full_water = True

    print("Observed weights:", [coffee_weight, frenchpress_weight, boiler_weight])
    print("Observed (encoded):",[int(coffee_in_place), int(frenchpress_in_place), int(boiler_in_place), int(boiler_full_water)])
    return [int(coffee_in_place), int(frenchpress_in_place), int(boiler_in_place), int(boiler_full_water)], weights

def read_weights(ser):
    while True:
        raw = ser.readline()
        line = raw.decode('utf-8').strip()

        if raw == b'' or line.count(";") < 2:
            continue  # ignore empty bytes

        line = raw.decode('utf-8').strip()

        if not line:
            continue  # ignore empty strings after decoding

        try:
            # protocol: "Weight:float(w1);float(w2);float(w3)"
            weights_str = line.split(":", 1)[1]

            coffee_weight = float(weights_str.split(";")[0])
            frenchpress_weight = float(weights_str.split(";")[1])
            boiler_weight = float(weights_str.split(";")[2])

            return coffee_weight, frenchpress_weight, boiler_weight

        except (ValueError, IndexError):
            continue  # skip malformed lines
