import smbus
bus = smbus.SMBus(1)
address = 0x04
try:
    bus.write_block_data(address,0x01,[255,178,46,125])
except IOError:
    pass
