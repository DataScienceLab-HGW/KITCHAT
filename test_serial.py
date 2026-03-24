import serial

def read_weights(ser):
    while True:
        raw = ser.readline()
        line = raw.decode('utf-8').strip()

        if raw == b'' or line.count(";") < 2:
            continue  # ignore empty bytes

        line = raw.decode('utf-8').strip()

        if not line:
            continue  # ignore empty strings after decoding

        print(line)

        try:
            # protocol: "Weight:float(w1);float(w2);float(w3)"
            weights_str = line.split(":", 1)[1]

            coffee_weight = float(weights_str.split(";")[0])
            frenchpress_weight = float(weights_str.split(";")[1])
            boiler_weight = float(weights_str.split(";")[2])

            return coffee_weight, frenchpress_weight, boiler_weight

        except (ValueError, IndexError):
            continue  # skip malformed lines

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

while 1 > 0:
    read_weights(ser)

