import math

class Matrix():
    def __init__(self, m: int=0, n: int=0, data = None):  # m - кол-во строк; n - кол-во столбцов
        if data:
            if not isinstance(data[0], list):
                data = [[x] for x in data]
            self.data = data
            self.m = len(self.data)
            self.n = len(self.data[0])
        else:
            self.m = m
            self.n = n
            self.data = [[0 for _ in range(n)] for _ in range(m)]
    def __repr__(self):
        return '\n'.join(map(str, self)) if self.n != 1 else str([row[0] for row in self.data])
    def __iter__(self):
        return iter(self.data)
    def __getitem__(self, idx):
        return self.data[idx]
    def __len__(self):  # кол-во строк
        return self.m
    def __add__(self, other):
        return Matrix(self.m, self.n, [[self[m][n] + other[m][n] for n in range(self.n)] for m in range(self.m)])
    def __mul__(self, other):
        other_cols = other.get_columns()
        return Matrix(self.m, other.n, [[sum(self[m][idx] * other_cols[n][idx] for idx in range(self.n))for n in range(other.n)]for m in range(self.m)])
    def get_columns(self):  # >
        return [[self[m][n] for m in range(self.m)] for n in range(self.n)]

class M_tr(Matrix):
    def __init__(self, dx, dy, dz):
        m, n = 4, 4
        data = [[1 if n == m else 0 for n in range(n)] for m in range(m)]
        data[0][3] = dx
        data[1][3] = dy
        data[2][3] = dz
        
        super().__init__(m, n, data)
        
class M_rot_y(Matrix):
    def __init__(self, angle_deg):
        m, n = 4, 4
        angle = math.radians(angle_deg)
        s = math.sin(angle)
        c = math.cos(angle)
        
        data = [[1 if i == j else 0 for j in range(4)] for i in range(4)]
        
        data[0][0] = c
        data[0][2] = s
        data[2][0] = -s
        data[2][2] = c
        
        super().__init__(m, n, data)

class Cube:
    def __init__(self, x0: int=0, y0: int=0, z0: int=0, a: int=1):
        # front face
        v0 = Matrix(data=[x0, y0, z0, 1])  # left up
        v1 = Matrix(data=[x0 + a, y0, z0, 1])  # right up
        v2 = Matrix(data=[x0 + a, y0 - a, z0, 1])  # right down
        v3 = Matrix(data=[x0, y0 -a, z0, 1])  # left down
        #
        v4 = Matrix(data=[x0, y0, z0 - a, 1])
        v5 = Matrix(data=[x0 + a, y0, z0 - a, 1])
        v6 = Matrix(data=[x0 + a, y0 - a, z0 - a, 1])
        v7 = Matrix(data=[x0, y0 -a, z0 - a, 1])
        self.verticales = [v0, v1, v2, v3, v4, v5, v6, v7]
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]
        
