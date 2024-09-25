def matrix_multiply(matrix1, matrix2):
    try:
        if not (isinstance(matrix1, list) and isinstance(matrix2, list)):
            raise TypeError("The inputs must be of the type 2-D lists")
        if len(matrix1) == 0 or len(matrix2) == 0:
            raise ValueError("One of the matrices is empty")
        if not (isinstance(matrix1[0], list) and isinstance(matrix2[0], list)):
            raise TypeError("The inputs must be of the type 2-D lists")

        if len(matrix1[0]) != len(matrix2):
            raise ValueError("Matrices with the given dimensions cannot be multiplied")
        for i in matrix1:
            if len(i) != len(matrix1[0]):
                raise ValueError(
                    "All the rows in the matrix must have same number of elements"
                )
        for j in matrix2:
            if len(j) != len(matrix2[0]):
                raise ValueError(
                    "All the rows in the matrix must have same number of elements"
                )
        num_rows1 = len(matrix1)
        num_cols1 = len(matrix1[0])
        num_rows2 = len(matrix2)
        num_cols2 = len(matrix2[0])
        matrix3 = [[0 for _ in range(num_cols2)] for _ in range(num_rows1)]
        for i in range(num_rows1):
            for j in range(num_cols1):
                for k in range(num_cols2):
                    if not (
                        isinstance(matrix1[i][j], (int, float, complex))
                        or isinstance(matrix2[i][j], (int, float, complex))
                    ):
                        raise TypeError(
                            "Elements of the matrices must be int or float or complex"
                        )
                    matrix3[i][k] += matrix1[i][j] * matrix2[j][k]
        return matrix3
    except TypeError:
        raise
    except ValueError:
        raise
    except:
        raise ValueError()


#  raise NotImplementedError("Matrix multiplication function not implemented")
