## Data Convert
# @param [in] self The object pointer.
# @param [in] data1 LSB
# @param [in] data2 MSB
# @retval Value MSB+LSB(int 16bit)
def dataConv(data1, data2):
    value = data1 | (data2 << 8)
    if (value & (1 << 16 - 1)):
        value -= (1 << 16)
    return value
