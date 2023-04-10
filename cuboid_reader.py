

class CuboidReader():
    def __init__(self):
        self.filename = "cuboids.txt"

    def get_vertices(self):
        return self.read_vertices()
    
    def read_vertices(self):
        f = open(self.filename, "r")
        cuboids_amount = int(f.readline())
        cuboids = []
        for _ in range(cuboids_amount):
            cuboid = []
            for _ in range(8):
                row = f.readline()
                vertices = row.split()
                for v in vertices:
                    v = int(v)
                vertices = tuple(vertices)
                cuboid.append(vertices)
            cuboids.append(cuboid)

        # print(cuboids)

        f.close()
        return cuboids

if __name__ == "__main__":
    test = CuboidReader()
    test.read_vertices()