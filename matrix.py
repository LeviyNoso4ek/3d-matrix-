import math
from vec import Vec3

class MatrixRow:
    def __init__(self, row_data: list):
        self.row_data = row_data

    def __getitem__(self, idx: int):
        return self.row_data[idx]

    def __setitem__(self, idx: int, value):
        self.row_data[idx] = float(value)

    def __repr__(self):
        return str(self.row_data)


class Matrix():
    def __init__(self, m: int=0, n: int=0, data: list=None):  # m - кол-во строк; n - кол-во столбцов
        if data:
            if isinstance(data, Vec3):
                data = [[float(x)] for x in data] + [[1.0]]
            elif not isinstance(data[0], list):
                data = [[float(x)] for x in data]
            self.data = [[float(x) for x in row] for row in data]
            self.m = len(self.data)
            self.n = len(self.data[0])
        else:
            self.m = m
            self.n = n
            self.data = [[0.0 for _ in range(n)] for _ in range(m)]
    def __repr__(self):
        return '\n'.join(map(str, self)) if self.n != 1 else str([row[0] for row in self.data])
    def __iter__(self):
        return iter(self.data)
    def __getitem__(self, idx):
        return MatrixRow(self.data[idx])
    def __setitem__(self, idx, value):
        if isinstance(idx, tuple):
            row, col = idx
            self.data[row][col] = float(value)
        else:
            self.data[idx] = [float(x) for x in value]
    def __len__(self):  # кол-во строк
        return self.m
    def __add__(self, other):
        if self.m != other.m or self.n != other.n:
            raise ValueError(f'you cannot add matrices of different sizes: A({self.m}x{self.n}) and B({other.m}x{other.n})')
        return Matrix(self.m, self.n, [[self[m][n] + other[m][n] for n in range(self.n)] for m in range(self.m)])
    def __mul__(self, other):
        if self.n != other.m:
            raise ValueError(f'Inconsistent sizes for multiplication: A({self.m}x{self.n}) and B({other.m}x{other.n})')
        other_cols = other.get_columns()
        return Matrix(self.m, other.n, [[sum(self[m][idx] * other_cols[n][idx] for idx in range(self.n))for n in range(other.n)]for m in range(self.m)])
    def get_columns(self):  # >
        return [[self[m][n] for m in range(self.m)] for n in range(self.n)]
    @classmethod
    def from_vec(cls, v: Vec3):
        
        return Matrix(data=[v.x, v.y, v.z, 1])

M_PROJ = Matrix(data=[
                    [1, 0, 0, 0], #   [2]   [2]
                    [0, 1, 0, 0], #   [4]   [4]
                    [0, 0, 1, 0], # X [5] = [5]
                    [0, 0, 1, 0]  #   [1]   [5]
                ])

class M_tr(Matrix):
    def __init__(self, dx: int | float, dy: int | float, dz: int | float):
        m, n = 4, 4
        data = [[1 if n == m else 0 for n in range(n)] for m in range(m)]
        data[0][3] = dx  # [1, 0, 0, dx]     [2]   [2 + dx]
        data[1][3] = dy  # [0, 1, 0, dy]     [3]   [3 + dy]
        data[2][3] = dz  # [0, 0, 1, dz]  X  [0] = [0 * dz]
                         # [0, 0, 0,  1]     [1]   [  1   ]
        super().__init__(m, n, data)
        
class M_rot_x(Matrix):
    def __init__(self, angle_deg: int | float):
        m, n = 4, 4
        angle = math.radians(angle_deg)
        s = math.sin(angle)
        c = math.cos(angle)
        
        data = [[1 if i == j else 0 for j in range(4)] for i in range(4)]
        
        data[1][1] = c   # [  1,      0,       0,    0]
        data[1][2] = -s  # [  0,   cos(a),  -sin(a), 0]
        data[2][1] = s   # [  0,   sin(a),   cos(a), 0]
        data[2][2] = c   # [  0,      0,       0,    1] 
        
        super().__init__(m, n, data)
        
class M_rot_y(Matrix):
    def __init__(self, angle_deg: int | float):
        m, n = 4, 4
        angle = math.radians(angle_deg)
        s = math.sin(angle)
        c = math.cos(angle)
        
        data = [[1 if i == j else 0 for j in range(4)] for i in range(4)]
        
        data[0][0] = c   # [cos(a),   0,    sin(a), 0]
        data[0][2] = s   # [  0,      1,      0,    0]
        data[2][0] = -s  # [-sin(a)   0,    cos(a), 0]
        data[2][2] = c   # [  0,      0,      0,    1] 
        
        super().__init__(m, n, data)
        
class M_rot_z(Matrix):
    def __init__(self, angle_deg: int | float):
        m, n = 4, 4
        angle = math.radians(angle_deg)
        s = math.sin(angle)
        c = math.cos(angle)
        
        data = [[1 if i == j else 0 for j in range(4)] for i in range(4)]
        
        data[0][0] = c   # [cos(a), -sin(a),   0,    0]
        data[0][1] = -s  # [sin(a),  cos(a),   0,    0]
        data[1][0] = s   # [  0,      0,       1,    0]
        data[1][1] = c   # [  0,      0,       0,    1] 
        
        super().__init__(m, n, data)