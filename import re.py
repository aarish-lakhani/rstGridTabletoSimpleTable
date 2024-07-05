from itertools import chain

def find_nth(haystack, needle, n) -> int:
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

# def return_simple_grid(n_columns, grid_table):
#     # For first row
#     first_plus_index = 1
#     last_plus_index = find_nth(grid_table, '+', n_columns + 1)
#     middle_plus_list = []
#     for i in range((n_columns)-1):
#         i += 2
#         middle_plus_index = find_nth(grid_table, '+', i)
#         middle_plus_list.append(middle_plus_index)
#     starting_string = '='*(last_plus_index - first_plus_index + 1)
#     for i in range(len(middle_plus_list)):
#         index = middle_plus_list[i]
#         starting_string = starting_string[:index] + ' ' + starting_string[index + 1:]
#     grid_table = grid_table.replace(grid_table[first_plus_index:last_plus_index + 1], starting_string)
#     grid_table = grid_table.replace("|", " ")
#     return grid_table

def remove_equals_vert(grid_table, first_plus_index, last_plus_index, row_length, row_length_2, num_rows, starting_string, header):
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
            # elif substring.find(starting_string) == -1:
            #     grid_table = grid_table.replace("|", " ")
        else:
            if substring.find(starting_string) != -1:
                grid_table = grid_table[:fpi_adj] + ' '*row_length + grid_table[lpi_adj + 1:]
                count += 1
            # elif substring.find(starting_string) == -1:
            #     grid_table = grid_table.replace("|", " ")
    return grid_table

def remake_equals(biggest_len, flat_val_len, grid_table, first_plus_index, last_plus_index, middle_plus_list, row_length, row_length_2, row_range, row_of_interest, phrase_length):
    # count = 0
    for i in range(row_range + 1):
    # for i in range(12):
        fpi_adj = first_plus_index+(row_length_2 + biggest_len)*(i)
        mpi_adj = middle_plus_list[0]+flat_val_len+(row_length_2 + biggest_len)*(i)

        # print(grid_table[fpi_adj:mpi_adj + 1])
        # print("Truth?", grid_table[fpi_adj:mpi_adj + 1].find('='*3))
        if grid_table[fpi_adj:mpi_adj + 1].find('='*3) != -1:
            grid_table = grid_table[:mpi_adj] + '='*(biggest_len-flat_val_len) + grid_table[mpi_adj:]
            # if biggest_len > count:
            #     count = biggest_len
        elif i == row_of_interest - 1:
            grid_table = grid_table[:mpi_adj + phrase_length] + ' '*((biggest_len-flat_val_len) - phrase_length) + grid_table[mpi_adj + phrase_length:]
            # if biggest_len > count:
            #     count = biggest_len
        elif i == row_of_interest:
            grid_table = grid_table[:mpi_adj] + ' '*((biggest_len-flat_val_len)) + grid_table[mpi_adj:]
            # if biggest_len > count:
            #     count = biggest_len
        else:
            grid_table = grid_table[:mpi_adj] + ' '*(biggest_len-flat_val_len) + grid_table[mpi_adj:]
            # if biggest_len > count:
            #     count = biggest_len
    return grid_table

def big_boy(grid_table, first_plus_index, last_plus_index, middle_plus_list, row_length, row_length_2, num_rows, starting_string):
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
            grid_table = remake_equals(biggest_len, flat_val_len, grid_table, first_plus_index, last_plus_index, middle_plus_list, row_length, row_length_2, num_rows, empty[n], len(col_sub_2.strip()))

        flat_val_len += len(col_sub) - len(grid_table[fpi_adj_1:mpi_adj_1+1])

    return grid_table

def complete_simple_grid(n_columns, grid_table, header):
    # For first row
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
    grid_table = grid_table.replace(grid_table[first_plus_index:last_plus_index + 1], starting_string)

    grid_table = remove_equals_vert(grid_table, first_plus_index, last_plus_index, row_length, row_length_2, num_rows, starting_string, header)

    grid_table = big_boy(grid_table, first_plus_index, last_plus_index, middle_plus_list, row_length, row_length_2, num_rows, starting_string)

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

simple_grid = complete_simple_grid(n_columns, grid_table, header)
# print(grid_table)
print(simple_grid)