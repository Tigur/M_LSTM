import ErrorCodes as errors

def binary(number,length=20):
    """ Changes number into a binary fomat"""

    number = int(number)
    bin_list = []
    if number < 0 :
        bin_list.append(1)
    else:
        bin_list.append(0)
    number = abs(number)

    current_num = number
    while(current_num>0):
        bin_list.append(current_num % 2)
        current_num = int(current_num/2)
    if len(bin_list)<length:
        amount = length - len(bin_list)
        for bit in range(amount) :
            bin_list.append(0)
    elif len(bin_list)>length:

        #print("ERROR !!!!!!!!!!! BIG")
        #print(number)
        return errors.error_BIG
    bin_list = bin_list[::-1]
    return bin_list

