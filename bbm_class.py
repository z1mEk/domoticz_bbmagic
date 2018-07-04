######################################################################################
# Descirption: BBMagic class use the bbmagic_lib for support the MMBagic devices.
#              Site of BBMagic project is http://bbmagic.net
# author: Gabriel Zima (z1mEk)
# e-mail: gabriel.zima@wp.pl
# date: 2018-07-02
# compatibile bbmagic_lib version: 1.2
######################################################################################

import ctypes
from ctypes import *
bbm_bt_lib = ctypes.CDLL("./bbmagic_lib_1.2.so")

class BBMagic:
    def __init__(self) :
        self.BBMAGIC_M_METEO = 1
        self.BBMAGIC_M_MOTION = 2
        self.BBMAGIC_M_BUTTON = 3
        self.BBMAGIC_M_ADC = 2
        self.BBMAGIC_M_FLOOD = 4
        self.BBMAGIC_M_CONTACTRON = 5
        self.BBMAGIC_M_KYE_REG = 0xFE
        self.BBMAGIC_M_UNKNOWN = 0xFF
        self.BBMAGIC_DEVICE_WORKTIME_0 = 0
        self.BBMAGIC_DEVICE_WORKTIME_1 = 1
        self.BBMAGIC_DEVICE_WORKTIME_2 = 2
        self.BBMAGIC_DEVICE_WORKTIME_3 = 3
        self.BBMAGIC_DEVICE_TYPE = 4
        self.BBMAGIC_DEVICE_V_SUP = 5
        self.BBMAGIC_DEVICE_ADV_TIME = 6
        self.BBMAGIC_DEVICE_DIO_STATE = 7
        self.BBMAGIC_DEVICE_USR_ADC_1_MSB = 12
        self.BBMAGIC_DEVICE_USR_ADC_1_LSB = 13
        self.BBMAGIC_DEVICE_USR_ADC_2_MSB = 14
        self.BBMAGIC_DEVICE_USR_ADC_2_LSB = 15
        self.BBMAGIC_DEVICE_ADDR_5 = 16
        self.BBMAGIC_DEVICE_ADDR_4 = 17
        self.BBMAGIC_DEVICE_ADDR_3 = 18
        self.BBMAGIC_DEVICE_ADDR_2 = 19
        self.BBMAGIC_DEVICE_ADDR_1 = 20
        self.BBMAGIC_DEVICE_ADDR_0 = 21
        self.BBMAGIC_DEVICE_RSSI = 22
        self.BBM_METEO_TEMPER_MSB = 8
        self.BBM_METEO_TEMPER_LSB = 9
        self.BBM_METEO_HUM = 10
        self.BBM_METEO_LIGHT= 11
        self.BBM_MOTION_MOTION_ALERTS = 8
        self.BBM_MOTION_LIGHT = 11
        self.BBM_BUTTON_BUTTON_FUNCTION = 7
        self.BBM_BUTTON_CFG_PINS = 8
        self.BBM_BUTTON_CHIP_TEMP = 9
        self.BBM_BUTTON_LIGHT = 10
        self.BBM_FLOOD_ALERT_FLAG = 7
        self.BBM_FLOOD_CHIP_TEMP = 8
        self.BBM_FLOOD_FIRM_1 = 14
        self.BBM_FLOOD_FIRM_0 = 15
        self.BBLIB_FRAME_SIZE = 23
        self.BBM_BT_ADDR_SIZE = 6
        self.BBMAGIC_VCC_DIVIDER = 71
        self.bbm_buf = (c_byte * self.BBLIB_FRAME_SIZE)()

    #Function: open bt hci and starts bt scanning
    def bbm_bt_open(self, led_pin):
        return bbm_bt_lib.bbm_bt_open(led_pin)

    #Function: stops bt scanning and closes bt hci
    def bbm_bt_close(self):
        return bbm_bt_lib.bbm_bt_close()

    #Function: reads data from bbmagic modules
    def bbm_bt_read(self, bbm_data):
        i = bbm_bt_lib.bbm_bt_read(byref(self.bbm_buf))
        j = 0
        for b in self.bbm_buf :
            bbm_data[j] = b
            j += 1
        return i

    #Function: returns version of bbm_bt library
    def bbm_bt_lib_version(self):
        v = bbm_bt_lib.bbm_bt_lib_version()
        return format(v, 'x')

    #Function: read data from bbmagic modules and parse to json format
    def bbm_bt_read_json(self):
        i = self.bbm_bt_read(self.bbm_buf)

        bbm_buf_bytes = bytearray(self.bbm_buf)

        d = dict()
        d['result'] = i

        if i > 0 :
            d['raw'] = self.bbm_buf
            
            worktime = self.BBMAGIC_DEVICE_WORKTIME_3 * 0xFFFFFF
            worktime += self.BBMAGIC_DEVICE_WORKTIME_2 * 0xFFFF
            worktime += self.BBMAGIC_DEVICE_WORKTIME_1 * 0xFF
            worktime += self.BBMAGIC_DEVICE_WORKTIME_0
            d['worktime'] = worktime

            device_mac = ''
            for i in range(self.BBMAGIC_DEVICE_ADDR_5, self.BBMAGIC_DEVICE_ADDR_0 + 1) :
                device_mac += "{:x}".format(bbm_buf_bytes[i])
            d['mac'] = device_mac.upper()
            
            d['rssi'] = self.bbm_buf[self.BBMAGIC_DEVICE_RSSI]
            d['v_supl'] = "{:4.2f}".format(float(bbm_buf_bytes[self.BBMAGIC_DEVICE_V_SUP]) / self.BBMAGIC_VCC_DIVIDER)
            d['adv_time'] = self.bbm_buf[self.BBMAGIC_DEVICE_ADV_TIME] * 2
            d['dio_state'] = self.bbm_buf[self.BBMAGIC_DEVICE_DIO_STATE]

            device_type = self.bbm_buf[self.BBMAGIC_DEVICE_TYPE]
            d['type'] = device_type

            if device_type == self.BBMAGIC_M_FLOOD :
                d['flood_alert_flag'] = self.bbm_buf[self.BBM_FLOOD_ALERT_FLAG]
                d['flood_chip_temp'] = self.bbm_buf[self.BBM_FLOOD_CHIP_TEMP]
                d['flood_firm_1'] = self.bbm_buf[self.BBM_FLOOD_FIRM_1]
                d['flood_firm_0'] = self.bbm_buf[self.BBM_FLOOD_FIRM_0]
            elif device_type == self.BBMAGIC_M_MOTION :
                d['motion_alert_flag'] = self.bbm_buf[self.BBM_MOTION_MOTION_ALERTS]
                d['motion_light'] = self.bbm_buf[self.BBM_MOTION_LIGHT]
            elif device_type == self.BBMAGIC_M_BUTTON :
                d['button_function'] = self.bbm_buf[self.BBM_BUTTON_BUTTON_FUNCTION]
                d['button_cfg_pins'] = self.bbm_buf[self.BBM_BUTTON_CFG_PINS]
                d['button_chip_temp'] = self.bbm_buf[self.BBM_BUTTON_CHIP_TEMP]
                d['button_light'] = self.bbm_buf[self.BBM_BUTTON_LIGHT]
            elif device_type == self.BBMAGIC_M_METEO :
                d['meteo_hum'] = self.bbm_buf[self.BBM_METEO_HUM]
                #d['meteo_temp'] = self.bbm_buf[self.BBM_METEO_TEMPER_MSB] #self.bbm_buf[self.BBM_METEO_TEMPER_LSB]
                d['meteo_light'] = self.bbm_buf[self.BBM_METEO_LIGHT]
            else:
                d['err_message'] = "Unknown device type"
        return d
