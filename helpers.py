def get_row_from_index(index,rows):
    return int(index) / int(rows)

def get_col_from_index(index,cols):
    return int(index) % int(cols)

def swap(a,b,list):
    temp = list[a]
    list[a] = list[b]
    list[b] = temp
    return
