import hvac_ir
import broadlink
import binascii

TICK = 32.6
IR_TOKEN = 0x26

def convert_bl(durations):
    result = bytearray()
    result.append(IR_TOKEN)
    result.append(0)
    result.append(len(durations) % 256)
    result.append(int(len(durations) / 256))
    for dur in durations:
        num = int(round(dur / TICK))
        if num > 255:
            result.append(0)
            result.append(int(num / 256))
        result.append(num % 256)
    result.append(0x0d)
    result.append(0x05)
    result.append(0x00)
    result.append(0x00)
    result.append(0x00)
    result.append(0x00)
    return result

def format_durations(data):
    result = ''
    for i in range(0, len(data)):
        if len(result) > 0:
            result += ' '
        result += ('+' if i % 2 == 0 else '-') + str(data[i])
    return result

def clim(bool, temp, mode, fan):
    Sender = hvac_ir.get_sender('Midea')
    if Sender is None:
        print("Unknown sender")
        exit(2)
    g = Sender()
    all_modes = {
        1: Sender.MODE_COOL,
        2: Sender.MODE_HEAT,
        3: Sender.MODE_FAN,
        4: Sender.MODE_AUTO,
        5: Sender.MODE_DRY
    }
    all_fans = {
        1: Sender.FAN_1,
        2: Sender.FAN_2,
        3: Sender.FAN_3,
        4: Sender.FAN_AUTO
    }
    if bool:
        g.send(Sender.POWER_ON, all_modes[mode], all_fans[fan], temp, Sender.VDIR_SWING_DOWN, Sender.HDIR_SWING, False)
    else:
        g.send(Sender.POWER_OFF, all_modes[mode], all_fans[fan], temp, Sender.VDIR_SWING_DOWN, Sender.HDIR_SWING, False)
    durations = g.get_durations()
    # print(format_durations(durations))

    BROADLINK_IP = '10.64.45.125'
    BROADLINK_MAC = "14:7d:da:19:02:70"

    bl = convert_bl(durations)
    # print(binascii.b2a_hex(bl))
    mac = binascii.unhexlify(BROADLINK_MAC.encode().replace(b':', b''))
    dev = broadlink.rm((BROADLINK_IP, 80), mac, devtype=10039)
    dev.auth()
    dev.send_data(bl)
