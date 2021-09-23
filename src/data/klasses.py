class Vector4:
    v1: int
    v2: int
    v3: int
    v4: int

    def __init__(self):
        self.v1 = 0
        self.v2 = 0
        self.v3 = 0
        self.v4 = 0

    def from1234(self, v1, v2, v3, v4):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.v4 = v4
        return self

    def symmetric(self, h, v):
        self.v1 = h
        self.v2 = v
        self.v3 = h
        self.v4 = v
        return self
