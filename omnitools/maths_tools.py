from numpy import zeros


def dot_convolve(data0, data1):
    shape = (len(data0), len(data0))
    matrix1 = zeros(shape)

    middle_index = len(data1) // 2
    for index in range(len(data0)):
        # get section of data1 to makes weights
        lhs = max((middle_index - index), 0)
        rhs = len(data1) if middle_index < (len(data0) - index) else middle_index + (len(data0) - index)
        tmp_weights = data1[lhs:rhs]
        # get indicies for filling in the matrix
        lhs = (index - middle_index) if (index - middle_index) > 0 else 0
        rhs = (index + middle_index) if (index + middle_index) < len(data0) else len(data0)
        rhs += 1
        matrix1[index, lhs:rhs] = tmp_weights
    # normalise the matrix
    matrix1 /= matrix1.sum(1)[:, None]
    # return the convolution.
    return matrix1.dot(data0)
