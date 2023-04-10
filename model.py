import numpy as np
import glm
import moderngl as mgl
from cuboid_reader import CuboidReader

class Cube:
    def __init__(self, app):
        self.cuboid_reader = CuboidReader()
        self.app = app
        self.ctx = app.ctx
        self.vbo = None#self.get_vbo([])
        self.shader_program = self.get_shader_program('default')
        self.vao = None#self.get_vao()
        self.m_model = self.get_model_matrix()
        self.on_init()

    def get_model_matrix(self):
        m_model = glm.mat4()
        return m_model

    def update(self):
        # m_model = glm.rotate(self.m_model, self.app.time, glm.vec3(0,1,0))
        # self.shader_program['m_model'].write(m_model)
        self.shader_program['m_view'].write(self.app.camera.m_view)

    def on_init(self):
        self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['m_model'].write(self.m_model)

    def render(self):
        self.update()

        cuboids = self.cuboid_reader.get_vertices()

        for vertices in cuboids:
            self.vbo = self.get_vbo(vertices)
            self.vao = self.get_vao()
            self.vao.render(mgl.LINES)

        

    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def get_vao(self):
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '3f', 'in_position')])
        return vao
    
    def get_vertex_data(self, vertices):
        # vertices = [(-1,-1,1), (1,-1,1),(1,1,1),(-1,1,1),(-1,1,-1),(-1,-1,-1),(1,-1,-1),(1,1,-1)]
        indices = [(0,1), (1,2), (2,3),(3,0),(0,5),(5,6),(6,1),(5,4),(6,7),(4,7),(7,2),(4,3)]
        
        return self.get_data(vertices, indices)
    
    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for line in indices for ind in line]
        return np.array(data,dtype='f4')

    def get_vbo(self, vertices):
        vertex_data = self.get_vertex_data(vertices)
        vbo = self.ctx.buffer(vertex_data)
        return vbo
    
    def get_shader_program(self, shader_name):
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()
    
        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program
