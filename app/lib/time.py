def time_str_to_ms(time_str:str) -> int:
    '''
    time_str should be in format of HH:MM:SS:MS
    '''
    h, m, s, ms = map(int, time_str.split(':'))
    return h * 3600000 + m * 60000 + s * 1000 + ms
