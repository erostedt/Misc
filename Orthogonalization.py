import numpy as np
import scipy.linalg as la
from copy import deepcopy
import time


class Orthogonalization:
    def __init__(self):
        pass

    def gramschmidt(self, A, tolerance = 1e-15):
        """
         Applies Gram–Schmidt orthogonalization on a matrix A.
         returns Q with n column vectors that is orthogonal basis  vectors of  range(A).
         :param A: Matrix A, tolerance=1e-15 for finding dependent column vector.
         :return: Orthogonal matrix V
         """
        _, n = np.shape(A)

        # Apply G-S algo
        V = A[:, 0]/np.linalg.norm(A[:, 0])  # set v_1 = a_1/||v_1||
        for i in range(1, n):
            v = A[:, i] - np.dot(V, np.dot(np.transpose(V), A[:, i])) # v_i = a_i - sum_j(dot(a_i,v_j))
            if np.linalg.norm(v) < tolerance: # if linear dependent
                break
            V = np.column_stack([V, v / np.linalg.norm(v)])
        return V

    def testGS(self, tolerance=1e-08):
        """
        Task 2.
        :param tolerance:
        :return:
        """
        print("testGS - - - - - - - - - - - - - - - - - - -")
        for i in range(1,4):
            n = np.power(10, i)
            m = n+2
            test_matrix = self.gramschmidt(np.random.rand(n, m))
            print("Is the 2-norm one : " , np.linalg.norm(test_matrix,2)-1 < tolerance)
            test_matrix2 = np.matmul(test_matrix.transpose(),test_matrix)
            print("Deviation of Q'Q from identity : ",np.linalg.norm(test_matrix2-np.eye(m),2))
            w,_ = np.linalg.eig(test_matrix2)
            print("Eigenvalue of Q'Q : ",w)
            print("determinant of Q'Q : ",np.linalg.det(test_matrix2))
            print("__________________________________")

    def testQR(self, tolerance=1e-08):
        """
        Task 3.
        :param tolerance:
        :return:
        """
        print("testQR - - - - - - - - - - - - - - - - - - -")
        for i in range(4):
            n = np.power(10, i)
            m = n+2
            test_matrix,_ = np.linalg.qr(np.random.rand(n,m))
            print("Is the 2-norm one : ", np.linalg.norm(test_matrix, 2) - 1 < tolerance)
            test_matrix2 = np.matmul(test_matrix.transpose(), test_matrix)
            print("Deviation of Q'Q from identity : ", np.linalg.norm(test_matrix2 - np.eye(len(test_matrix2)), 2))
            w, _ = np.linalg.eig(test_matrix2)
            print("Eigenvalue of Q'Q : ", w)
            print("determinant of Q'Q : ", np.linalg.det(test_matrix2))
            print("__________________________________")

    def QR(self, A):
        """
        QR decomposition using Householder's reflection.
        :param A: Matrix A.
        :return: Orthogonal matrix Q and upper triangular matrix R.
        """
        m, n = np.shape(A)
        # Renaming for clarity, don't rename for efficiency
        R = deepcopy(A)
        Q = np.eye(m)
        for i in range(min(m, n)):
            H = np.eye(m)
            H[i:, i:] = self.Householder(R[i:, i:])
            Q = Q @ H
            R = H @ R
        return Q, R

    def Householder(self, A):
        """
        Calculates an orthogonal using Householder's reflection.
        :param A: Matrix A
        :return: Orthogonal matrix Q
        """
        a = A[:, 0]
        size = A.shape[0]
        a_hat = np.array([la.norm(a)] + (size - 1) * [0.])
        v = a - a_hat
        if la.norm(v) != 0:
            v = v / la.norm(v)
        Q = np.eye(size) - 2 * np.outer(v, v)
        return Q

    def test_QR(self, A, Q, R, type, tol=1e-8):
        if type == 0:
            print('Testing Householder: ')
        elif type == 1:
            print('Testing Givens: ')
        else: print('Must be type 0 or 1')
        m, n = np.shape(A)

        minimum = min(m, n)
        test_matrix_A_eq_QR = A - Q @ R
        test_matrix_orth_1 = Q @ np.transpose(Q) - np.eye(minimum, minimum)
        test_matrix_orth_2 = np.transpose(Q) @ Q - np.eye(minimum, minimum)

        for r in range(minimum):
            for c in range(minimum):
                if abs(test_matrix_orth_1[r, c]) > tol or abs(test_matrix_orth_2[r, c]) > tol:
                    print('Not orthogonal')
                    print('Not QR')
                    return

        for r in range(m):
            for c in range(n):
                if abs(test_matrix_A_eq_QR[r, c]) > tol:
                    print('Not QR')
                    return
        print('Q is orthogonal and A = QR')

    def QR_givens(self, A):
        """
        QR decomposition using Given's rotation
        :param A: Matrix A
        :return: Orthogonal matrix Q and upper triangular matrix R
        """
        m, n = np.shape(A)
        # Renaming for clarity, don't rename for efficiency.
        R = deepcopy(A)
        Q = np.eye(m)
        for j in range(n):
            for i in range(m-1, j, -1):
                G = np.eye(m)
                c, s = self.givens_rotation(R[i-1, j], R[i, j])
                G[i-1, i-1] = c
                G[i-1, i] = -s
                G[i, i-1] = s
                G[i, i] = c
                R = np.transpose(G) @ R
                Q = Q @ G
        return Q, R

    def givens_rotation(self, x, y):
        """
        Calculates the 2x2 Given's matrix:
        [c, -s]
        [s, c]
        Based on the hypot function.
        :param x: scalar value.
        :param y: scalar value
        :return: returns values c and s for the matrix[[c, -s], [s, c]]
        """
        if y == 0:
            return 1, 0
        else:
            if abs(y) > abs(x):
                d = x/y
                s = 1/np.sqrt(1 + d*d)
                return s*d, s
            else:
                d = y/x
                c = 1/np.sqrt(1 + d*d)
                return c, c*d

    def Holder_vs_Givens(self, A):
        start = time.perf_counter()
        for i in range(100):
            self.QR(A)
        elapsed = time.perf_counter()
        elapsed = elapsed - start
        print('100 Householder: ', elapsed, 's')
        start = time.perf_counter()
        for i in range(100):
            self.QR_givens(A)
        elapsed = time.perf_counter()
        elapsed = elapsed - start
        print('100 Givens: ', elapsed, 's')


O = Orthogonalization()

A = 100 * np.random.rand(202, 200)

O.Holder_vs_Givens(A)

