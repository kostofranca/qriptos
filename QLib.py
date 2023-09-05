"""
This lib includes some special matrices and functions related to classical and quantum probability operations
"""

def biased_coin(N,B = 50):
    """
    Print the biased coin flippind experiment N - 1 times with bias rate %B
    So send your experiment number as 10^k + 1 form
    """
    from random import randrange
    
    heads = 0
    tails = 0
    results = {}

    for j in range(1,N):

        if randrange(1,N) < (B/100)*(N-1):
            heads += 1
        else:
            tails += 1

    results[N-1] = (heads,tails)

    heads = 0
    tails = 0

    for i,j in results.items():
        print(f" {i} times experiment resulted in {j[0]} heads and {j[1]} tails")

def prob_matrix_mult(B,v):
    new_prob_state = []
    s = 0

    for rows in B:
        for i in range(len(rows)):
            s += rows[i]*v[i]
        new_prob_state.append(s)
        s = 0
    return new_prob_state

def normalize(vector):
    """
    normalize the given vector
    """
    sumation = sum(vector)
    for i in range(len(vector)):
        vector[i] /= sumation
    return vector

def transpose(matrix):
    rows = len(matrix)
    columns = len(matrix[0])

    matrix_T = []
    for j in range(columns):
        row = []
        for i in range(rows):
            row.append(matrix[i][j])
        matrix_T.append(row)

    return matrix_T

def create_prob_state(dim_of_vector, k = 2):
    """
    create a random probabilistic state that "dim_of_vector" dimension and precision "k".
    
    dim_of_vector => number_of_elements
    """
    from random import randint

    def normalize(vector):
        """
        normalize the given vector
        """
        sumation = sum(vector)
        for i in range(len(vector)):
            vector[i] /= sumation
        return vector

    N = 10**k + 1
    vector = []

    for i in range(dim_of_vector):
        vector.append(randint(1,N))

    return normalize(vector)

def create_rand_operator(dimension):
    """
    Create a random probabilistic operator for a given dimension.(Square matrix).
    
    dimension => number_of_elements
    """
    def transpose(matrix):
        rows = len(matrix)
        columns = len(matrix[0])

        matrix_T = []
        for j in range(columns):
            row = []
            for i in range(rows):
                row.append(matrix[i][j])
            matrix_T.append(row)

        return matrix_T
    
    operator = []

    for i in range(dimension):
        v = create_prob_state(dimension,2)
        operator.append(v)
    
    return transpose(operator)

def tensor(I,J):
    """
    Tensor product of given 1-dim vectors I,J
    """
    result = []
    for i in I:
        for j in J:
            result.append(i*j)
    return result

def vector_rep(binary):
    """
    Given a binary number in str form returns the vector represantation of it.
    """
    def tensor(I,J):
        result = []
        for i in I:
            for j in J:
                result.append(i*j)
        return result

    result = [1,0] # zero
    if (binary[0] == "1"):
        result = [0,1]

    for i in range(1,len(binary)):
        if (binary[i] == "0"):
            result = tensor(result,[1,0])
        else:
            result = tensor(result,[0,1])
    return result

def basis_generator(dim, type_basis = "vector"):
    """
    Create the basis of the given dimension on probabilistic space
    
    dim => 2**dim
    """
    def vector_list(dim):
        basis = []
        for i in range(2**dim):
            basis.append([1 if j == i else 0 for j in range(2**dim)])
        return basis
    
    def vector_str(dim):
        binary_reps = [str(bin(i)[2:]) for i in range(2**dim)] #create the basis
    
        for i in range(len(binary_reps)):
            if (len(binary_reps[i]) != dim):
                binary_reps[i] = "0"*(dim - len(binary_reps[i])) + binary_reps[i]
        return binary_reps
    if (type_basis == "vector"):
        return vector_list(dim)
    elif (type_basis == "str"):
        return vector_str(dim)
    else:
        print("Please enter a valid basis_type\n'vector' or 'str'")

def create_empty_square_matrix(dim):
    """
    

    Parameters
    ----------
    dim : INT
        number_of_elements.

    Returns
    -------
    dest : Matrix
        Empty square matrix in th given dim

    """

    dest = [list() for i in range(dim)]
    
    for i in dest:
        for j in range(dim):
            i.append(0.0)
    
    return dest

def I(dim = 1):
    """
    Create Identity matrix
    
    dim => 2**dim
    """
    identity = create_empty_square_matrix(2**dim)
    
    for i in range(2**dim):
            identity[i][i] += 1
            
    return identity

def cnot_calculator(dim = 2,key = [1,2]):
    """

    Parameters
    ----------
    dim : INT
        dim => 2**dim

    key : array of ints
        key[0] -> control bit
        key[1] -> target bit

    Returns
    -------
    array (matrix)
        CNOT Operator

    """
    def convert(list):
        return str("".join([str(i) for i in list]))
    
    def flipper(string, key):
    
        string = [int(i) for i in string]
        
        if string[key[0] - 1] == 1:
            string[key[1] - 1] = str((int(string[key[1] - 1]) + 1) % 2)
            
        return(string)
    
    def tensor(I,J):
        
        result = []
        for i in I:
            for j in J:
                result.append(i*j)
        return result
    
    def vector_rep(binary):
        result = [1,0] # zero
        if (binary[0] == "1"):
            result = [0,1]
    
        for i in range(1,len(binary)):
            if (binary[i] == "0"):
                result = tensor(result,[1,0])
            else:
                result = tensor(result,[0,1])
        return result

    binary_reps = [str(bin(i)[2:]) for i in range(2**dim)] #create the basis
    
    for i in range(len(binary_reps)):
        if (len(binary_reps[i]) != dim):
            binary_reps[i] = "0"*(dim - len(binary_reps[i])) + binary_reps[i]

    binaries = [convert(flipper(binary_reps[i],key)) for i in range(len(binary_reps))]
    
    return [vector_rep(i) for i in binaries]

def print_matrix(array):
    from IPython.display import display, Math
    matrix = ''
    for row in array:
        try:
            for number in row:
                matrix += f'{number}&'
        except TypeError:
            matrix += f'{row}&'
        matrix = matrix[:-1] + r'\\'
    display(Math(r'\begin{bmatrix}'+matrix+r'\end{bmatrix}'))

def random_quantum_operator(dim):
    
    from random import randrange
    from math import sqrt
    
    """
    Given the number_of_qubit(dim) that we are working on this function return a Quantum Operator. 
    
    dim => 2**dim
    """
    
    def normalize(vector):
        """
        normalize the given vector
        """
        sumation = sum(vector)
        for i in range(len(vector)):
            vector[i] /= sumation
            
        return vector

    def transpose(matrix):
        rows = len(matrix)
        columns = len(matrix[0])

        matrix_T = []
        for j in range(columns):
            row = []
            for i in range(rows):
                row.append(matrix[i][j])
            matrix_T.append(row)
    
        return matrix_T

    v = []
    result = []

    for i in range(2**dim):
        for j in range(2**dim):
            v.append(randrange(100))
        v = [sqrt(i) for i in normalize(v)]
        result.append(v)
        v = []

    return transpose(result)

def random_quantum_state(dim):
    """
    dim => 2**dim
    """

    from random import randrange
    from math import sqrt

    def normalize(vector):
        """
        normalize the given vector
        """
        summation = sum(vector)
        
        for i in range(len(vector)):
            vector[i] /= summation

        return vector

    v = []

    for i in range(2**dim):
        v.append(randrange(100))

    v = normalize(v)

    for i in range(2**dim):
            v[i] = sqrt(v[i])

    result = [0 for i in range(len(v))]

    for i in range(2**dim):
        if (randrange(2)):
            result[i] = -v[i]
        else:
            result[i] = v[i]

    return result

def is_quantum_state(vector):
    sum1 = 0
    
    for i in range(len(vector)):
        sum1 += vector[i]**2
    if (sum1 - 1) <= 0.01:
        return(True)
    return(False)

def random_qstate_by_angle():
    """
    Returns
    -------
    2-dim quantum vector

    """

    from random import randrange
    from math import cos,sin,pi

    angle = randrange(360)
    angle_radian = 2*pi*angle/360
    return [cos(angle_radian),sin(angle_radian)]

def expected_quantum_output(q_state, shots = 1000):
    """

    Parameters
    ----------
    q_state : 1-qubit quantum_system (list)
    shots : INT
        Number of experiment. The default is 1000.

    Returns
    -------
    list
        [expected numberof 0's, expected number of 1's].
    """

    from quantum_state import angle_qstate
    from math import pi,cos,sin

    x,y = q_state[0], q_state[1]

    rotation_angle = angle_qstate(x,y)*pi/180

    the_expected_number_of_zeros = shots*cos(rotation_angle)**2
    the_expected_number_of_ones = shots*sin(rotation_angle)**2

    return [round(the_expected_number_of_zeros,4), round(the_expected_number_of_ones,4)]

def rotate_quantum_state(q_state = [1,0], rotation_angle = 0):
    """
    Parameters
    ----------
    q_state : LIST, optional
        1-qubit quantum_system (list). The default is [1,0].
    rotation_angle : float(degree), optional
        Rotation degree. The default is 0.

    Returns
    -------
    list
        Rotated quantum state.

    """
    from quantum_state import angle_qstate
    from math import cos,sin,pi

    angle = angle_qstate(q_state[0],q_state[1])*pi/180

    quantum_state = [cos(rotation_angle + angle), sin (rotation_angle + angle)]

    return [round(quantum_state[0],4), round(quantum_state[1],4)]

def reflect_quantum_state(q_state = [1,0], reflection_angle = 0):
    """
    Parameters
    ----------
    q_state : LIST, optional
        1-qubit quantum_system (list). The default is [1,0].
    reflection_angle : float(degree), optional
        Reflection degree. The default is 0.

    Returns
    -------
    list
        Reflected quantum state.

    """

    from math import cos, sin

    from QLib import prob_matrix_mult

    R = [[cos(2*reflection_angle), sin (2*reflection_angle)], 
         [sin(2*reflection_angle),  -cos(2*reflection_angle)]]

    return prob_matrix_mult(R, q_state)  

def Hadamard(dim = 1, target = 1):
    """

    Parameters
    ----------
    dim : INT, optional
        2**dim. The default is 1.
    target : INT, optional
        action qubit. The default is 1.

    Returns
    -------
    List
        QState after Hadamard.

    """
    
    import numpy as np
    
    H = [[1/2**0.5,1/2**0.5],[1/2**0.5,-1/2**0.5]]

    process = []

    I = [[1,0],
         [0,1]]

    for i in range(dim):
        if i == target - 1:
            process.append(H)
            continue
        process.append(I)

    if dim == 1:
        return (process[0])
    else:
        result = np.kron(process[1],process[0])
        for i in range(dim - 2):
            result = np.kron(process[i+2], result)
        return (result)