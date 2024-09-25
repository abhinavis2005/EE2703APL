def matrix_multiply(matrix1, matrix2):
    """
    Multiplies matrix1 with matrix2

    parameters:
    matrix1: a matrix made of a nested list like datatype
    matrix2: a matrix made of a nested list like datatype,
    eg [[1,2,3],[,4,5,6]]

    performs matrix multiplication in an iterative way.
    """
    ret_matrix = []  # matrix to be returned
    allowed_types = (int, float, complex)

    try:
        a = len(matrix1)
        b = len(matrix1[0])
        c = len(matrix2)
        d = len(matrix2[0])

        # checking for empty matrix
        if len(matrix1) == 0 or len(matrix2) == 0:
            raise ValueError()

        # checking for incompatible dimensions
        if b != c:
            raise ValueError()

        # iterating over rows in matrix1
        for row_num, row in enumerate(matrix1):
            ret_row = []

            # check for well defined matrix
            if len(row) != b:
                raise ValueError()

            # multiplication algorithm
            # iterating through columns in matrix2
            for j in range(d):
                sum = 0
                # iterating through the row in matriX1
                for i, num1 in enumerate(row):
                    # if matrix is not well defined
                    if len(matrix2[i]) != d:
                        raise ValueError()

                    num2 = matrix2[i][j]

                    # multiplying after checking datatypes
                    if isinstance(num1, allowed_types) and isinstance(
                        num2, allowed_types
                    ):
                        sum += num2 * num1
                    else:
                        raise TypeError()
                ret_row.append(sum)

            # check if we are missing elements
            if len(ret_row) == d:
                ret_matrix.append(ret_row)
            else:
                raise ValueError()
    except TypeError:
        raise
    except ValueError:
        raise
    except:
        raise ValueError()

    return ret_matrix
