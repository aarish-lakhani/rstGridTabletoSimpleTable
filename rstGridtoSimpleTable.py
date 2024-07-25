"""
Created for _________

@author: lakhani
"""

# Find the nth iteration of a string
def find_nth(haystack, needle, n) -> int:
    start = haystack.find(needle)

    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
   
    return start

# Returns a very rudimentary simple table from grid table, initial iteration of rstGridtoSimpleTable
def prelim_return_simple_table(n_columns, grid_table):
    # For first row
    first_plus_index = 1
    last_plus_index = find_nth(grid_table, '+', n_columns + 1)
    middle_plus_list = []
    for i in range((n_columns)-1):
        i += 2
        middle_plus_index = find_nth(grid_table, '+', i)
        middle_plus_list.append(middle_plus_index)
    starting_string = '='*(last_plus_index - first_plus_index + 1)
    for i in range(len(middle_plus_list)):
        index = middle_plus_list[i]
        starting_string = starting_string[:index] + ' ' + starting_string[index + 1:]
    grid_table = grid_table.replace(grid_table[first_plus_index:last_plus_index + 1], starting_string)
    grid_table = grid_table.replace("|", " ")
   
    return grid_table

# Replace +------+ with =
def replace_plus_dash(grid_table, n_columns):

    first_plus_index = 1
    last_plus_index = find_nth(grid_table, '+', n_columns + 1)
    middle_plus_list = []
    for i in range((n_columns)-1):
        i += 2
        middle_plus_index = find_nth(grid_table, '+', i)
        middle_plus_list.append(middle_plus_index)
    row_length = last_plus_index - first_plus_index + 1
    row_length_2 = find_nth(grid_table, '\n', 2) - find_nth(grid_table, '\n', 1)
    num_rows = int((len(grid_table)-1)/row_length_2)
    starting_string = '='*(row_length)
    for i in range(len(middle_plus_list)):
        index = middle_plus_list[i]
        starting_string = starting_string[:index-1] + ' ' + starting_string[index:]

    return grid_table, num_rows, first_plus_index, last_plus_index, starting_string, row_length, row_length_2, middle_plus_list

# Removes extra equals after replace_plus_dash is called
def remove_extra_equals(grid_table, first_plus_index, last_plus_index, row_length, row_length_2, num_rows, starting_string, header):

    count = 0
    for i in range(1, num_rows-1):
        fpi_adj = first_plus_index+row_length_2*i
        lpi_adj = last_plus_index+row_length_2*i
        substring = grid_table[fpi_adj:lpi_adj + 1]
        if header == True:
            if substring.find(starting_string) != -1 and count == 0:
                count += 1
            elif substring.find(starting_string) != -1:
                grid_table = grid_table[:fpi_adj] + ' '*row_length + grid_table[lpi_adj + 1:]
                count += 1
        else:
            if substring.find(starting_string) != -1:
                grid_table = grid_table[:fpi_adj] + ' '*row_length + grid_table[lpi_adj + 1:]
                count += 1
   
    return grid_table

# Remakes the equals and text column width if a new row has a larger set of characters for one line than the previous largest
def remake_column_width(biggest_len, flat_val_len, grid_table, first_plus_index, middle_plus_list, row_length_2, row_range, row_of_interest, phrase_length):

    for i in range(row_range + 1):
        fpi_adj = first_plus_index+(row_length_2 + biggest_len)*(i)
        mpi_adj = middle_plus_list[0]+flat_val_len+(row_length_2 + biggest_len)*(i)
        if grid_table[fpi_adj:mpi_adj + 1].find('='*3) != -1:
            grid_table = grid_table[:mpi_adj] + '='*(biggest_len-flat_val_len) + grid_table[mpi_adj:]
        elif i == row_of_interest - 1:
            grid_table = grid_table[:mpi_adj + phrase_length] + ' '*((biggest_len-flat_val_len) - phrase_length) + grid_table[mpi_adj + phrase_length:]
        elif i == row_of_interest:
            grid_table = grid_table[:mpi_adj] + ' '*((biggest_len-flat_val_len)) + grid_table[mpi_adj:]
        else:
            grid_table = grid_table[:mpi_adj] + ' '*(biggest_len-flat_val_len) + grid_table[mpi_adj:]
    
    return grid_table

# Iterates through text, finds rows where there are multiple lines, combines into one line
# Then calls remake_column_width if text combined into one line is bigger than previous column width
def big_boy(grid_table, first_plus_index, last_plus_index, middle_plus_list, row_length_2, num_rows):

    indicator = False
    empty = []
    count = 1
    for i in range(1, num_rows-1):
        fpi_adj = first_plus_index+row_length_2*i
        lpi_adj = last_plus_index+row_length_2*i
        substring = grid_table[fpi_adj:lpi_adj + 1].replace("|", " ")
        if (len(substring) - len(substring.lstrip())) == 2 and indicator == False:
            indicator = True
        elif (len(substring) - len(substring.lstrip())) == 2 and indicator == True:
            empty.append(i)
        elif (len(substring) - len(substring.lstrip())) != 2:
            indicator = False
            count = 1

    print("Rows of Interest:", empty)

    biggest_len = 0
    flat_val_len = 0

    for n in range(0, len(empty)):
        init_row = empty[n]-1

        fpi_adj_1 = first_plus_index+(row_length_2 + biggest_len)*(init_row)
        mpi_adj_1 = middle_plus_list[0]+biggest_len+(row_length_2 + biggest_len)*(init_row)
        col_sub_1 = grid_table[fpi_adj_1 + 1:mpi_adj_1]

        fpi_adj_2 = first_plus_index+(row_length_2 + biggest_len)*(init_row+1)
        mpi_adj_2 = middle_plus_list[0]+biggest_len+(row_length_2 + biggest_len)*(init_row+1)
        col_sub_2 = grid_table[fpi_adj_2 + 1:mpi_adj_2]

        col_sub_pre = ' ' + col_sub_1.strip() + ' ' + col_sub_2.strip()

        diff = len(col_sub_1) - len(col_sub_pre)
        if diff < 0:
            diff = 1

        col_sub = '| ' + col_sub_1.strip() + ' ' + col_sub_2.strip() + ' '*(diff) + '|'

        big = len(col_sub) - len(grid_table[fpi_adj_1:mpi_adj_1+1])

        grid_table = grid_table[:fpi_adj_1] + col_sub + grid_table[mpi_adj_1+1:]

        grid_table = grid_table[:fpi_adj_2 + big+1] + ' '*(len(col_sub_2)) + grid_table[mpi_adj_2 + big:]

        if (len(col_sub) - len(grid_table[fpi_adj_1:mpi_adj_1+1])) + biggest_len > biggest_len:
            biggest_len = len(col_sub) - len(grid_table[fpi_adj_1:mpi_adj_1+1]) + biggest_len
            grid_table = remake_column_width(biggest_len, flat_val_len, grid_table, first_plus_index, middle_plus_list, row_length_2, num_rows, empty[n], len(col_sub_2.strip()))

        flat_val_len += len(col_sub) - len(grid_table[fpi_adj_1:mpi_adj_1+1])
    
    return grid_table

def return_simple_table(n_columns, grid_table, header):
    
    grid_table, num_rows, first_plus_index, last_plus_index, starting_string, row_length, row_length_2, middle_plus_list = replace_plus_dash(grid_table, n_columns)
    grid_table = grid_table.replace(grid_table[first_plus_index:last_plus_index + 1], starting_string)
    grid_table = remove_extra_equals(grid_table, first_plus_index, last_plus_index, row_length, row_length_2, num_rows, starting_string, header)
    grid_table = big_boy(grid_table, first_plus_index, last_plus_index, middle_plus_list, row_length_2, num_rows)
    grid_table = grid_table.replace('|', ' ')

    return grid_table

n_columns = 4
header = True

# Example usage
grid_table = """
+-------------------------+-----------------+------+-----------------+
| Catfish Description     | Tomato Variable | Worm | Ink             |
| top Sun level           | *YieldR         | (YJ) |                 |
+-------------------------+-----------------+------+-----------------+
| Breeze Branch Bug       | Chicken Insect  | Jump | Pepper          |
+-------------------------+-----------------+------+-----------------+
| Candy Squirrel Autumn   | Chicken 24-bit  |Cheese| Cap             |
+-------------------------+-----------------+------+-----------------+
| PupCake: Autumn Bath    | Flea 64-bit     |Cheese| Bolt            |
| piece Bug at the Support| piece Leaf      |Autumn| Cattle          |
+-------------------------+-----------------+------+-----------------+
| Bugger Cloud Paws       | Worm 48-bit     |Cheese| Tuna            |
+-------------------------+-----------------+------+-----------------+
| Squirrel Airship Air    | Bath 16-bit     | (Tie | [deg] bath:     |
| display, [deg] airplane | [deg]) Airship  | Air  | paws ( MSL      |
+-------------------------+-----------------+------+-----------------+
"""

simple_table = return_simple_table(n_columns, grid_table, header)

print(simple_table)