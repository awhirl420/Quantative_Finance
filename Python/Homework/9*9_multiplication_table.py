for i in range(1, 10):
    for j in range(1, 10):
        result = i*j
        print('{}*{}={:<3d}'.format(i,j, result), end='')
    print()
