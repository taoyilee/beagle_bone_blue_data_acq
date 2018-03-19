## Data Convert
# @param [in] self The object pointer.
# @param [in] data1 LSB
# @param [in] data2 MSB
# @retval Value MSB+LSB(int 16bit)
def dataConv(data1, data2):
    value = data1 | (data2 << 8)
    if value & (1 << 16 - 1):
        value -= (1 << 16)
    return value


def dataConv_20bit(data_msb, data_lsb, data_xlsb):
    value = data_msb << 12 | (data_lsb << 4) | data_xlsb
    if value & (1 << 20 - 1):
        value -= (1 << 20)
    return value
