def convert(list):
    returnable = ''
    for i in range(len(list)):
        separator = ' '
        if i == len(list) -1:
            separator = ''
        
        returnable += list[i] + separator
        
    
    return returnable