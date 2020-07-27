def average_rainfall(input_list):
    new_list = [num for num in input_list if num > 0]
    total=0
    list_len=len(new_list)
    for value in new_list:
        total+=value
    mean=total/list_len
    return mean #<-- change this!

# Don't touch anything below this line.
if __name__ == "__main__":
    import sys

    # We get the arguments assuming that they are a list of *integers*
    # We parse the input to get the right type.
    # There's no error checking!
    rainfall_measurements = list(map(int, sys.argv[1:]))

    # We print the average.
    print(average_rainfall(rainfall_measurements))

#print(press enter to exit)
