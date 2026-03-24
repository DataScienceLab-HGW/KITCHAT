import serial

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

line = ser.readline().decode('utf-8').strip()

# the protocol is basically encoding the serial output in : "Weight:float(w1), float(w2), float(w3)"
weights_str = line.split(":")[1]

coffee_weight = float(weights_str.split(";")[0])
frenchpress_weight = float(weights_str.split(";")[1])
boiler_weight = float(weights_str.split(";")[2])



print(coffee_weight, frenchpress_weight, boiler_weight) 