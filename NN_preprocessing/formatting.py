import ErrorCodes as errors

def binary(number,length=12):
    """ Changes number into a binary fomat"""
    bin_list = []
    current_num = number
    while(current_num>0):
        bin_list.append(current_num % 2)
        current_num = int(current_num/2)
        print(current_num)
    if len(bin_list)<length:
        amount = length - len(bin_list)
        for bit in range(amount) :
            bin_list.append(0)
    elif len(bin_list)>length:
        return errors.error_BIG
    bin_list = bin_list[::-1]
    return bin_list

