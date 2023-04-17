import glm
import pygame as pg
import numpy as np

FOV = 50
MIN_FOV, MAX_FOV = 25,100
NEAR = 0.1
FAR = 100
SPEED = 0.01
SENSITIVITY = 0.05

class Camera:
    def __init__(self,app, position = (0,0,0), yaw=-90, pitch=0, roll=0):
        self.translation_unit = 0.05
        self.ang_unit = glm.radians(0.75)
        self.current_angs = glm.vec3(0,0,0)
        self.app=app
        self.aspect_ratio = app.WIN_SIZE[0]/app.WIN_SIZE[1]
        self.position=glm.vec3(position)
        self.up = glm.vec3(0,1,0)
        self.right= glm.vec3(1,0,0)
        # forward to -1 bo układ prawoskrętny
        # self.forward = glm.vec3(0,0,-1)
        self.forward = glm.vec3(0,0,-1)
        self.m_translation = glm.mat4(1.0)
        self.m_rotation = glm.mat4(1.0)

        #view matrix
        self.m_view = self.get_view_matrix()

        # proj matrix
        self.m_proj = self.get_projection_matrix()
        

    def update_camera_vectors(self):

        inverted = glm.inverse(self.m_view)
        self.forward = glm.vec3(inverted[2])
        self.up = glm.vec3(inverted[1])
        self.right = glm.vec3(inverted[0])

        self.forward = glm.normalize(-self.forward)
        self.up = glm.normalize(self.up)
        self.right = glm.normalize(self.right)

    def update(self):
        self.move()
        self.m_proj = self.get_projection_matrix()

    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            translation_vector = glm.vec4(-self.translation_unit * self.up.x,-self.translation_unit * self.up.y,-self.translation_unit * self.up.z,1)
            self.position += glm.vec3(translation_vector)
            self.m_translation *= self.update_view_matrix_translate(translation_vector)
        if keys[pg.K_s]:
            translation_vector = glm.vec4(self.translation_unit * self.up.x,self.translation_unit * self.up.y,self.translation_unit * self.up.z,1)
            self.position += glm.vec3(translation_vector)
            self.m_translation *= self.update_view_matrix_translate(translation_vector)
        if keys[pg.K_d]:
            translation_vector = glm.vec4(-self.translation_unit * self.right.x,-self.translation_unit * self.right.y,-self.translation_unit * self.right.z,1)
            self.position += glm.vec3(translation_vector)
            self.m_translation *= self.update_view_matrix_translate(translation_vector)
        if keys[pg.K_a]:
            translation_vector = glm.vec4(self.translation_unit * self.right.x,self.translation_unit * self.right.y,self.translation_unit * self.right.z,1)
            self.position += glm.vec3(translation_vector)
            self.m_translation *= self.update_view_matrix_translate(translation_vector)
        if keys[pg.K_q]:
            translation_vector = glm.vec4(-self.translation_unit * self.forward.x,-self.translation_unit * self.forward.y,-self.translation_unit * self.forward.z,1)
            self.position += glm.vec3(translation_vector)
            self.m_translation *= self.update_view_matrix_translate(translation_vector)
        if keys[pg.K_e]:
            translation_vector = glm.vec4(self.translation_unit * self.forward.x,self.translation_unit*self.forward.y,self.translation_unit*self.forward.z,1)
            self.position += glm.vec3(translation_vector)
            self.m_translation *= self.update_view_matrix_translate(translation_vector)
        global FOV, MIN_FOV, MAX_FOV
        if keys[pg.K_n]:
            if FOV<MAX_FOV:
                FOV+=1
        if keys[pg.K_m]:
            if FOV>MIN_FOV:
                FOV-=1
        if keys[pg.K_r]:
            self.m_rotation = self.update_view_matrix_rotate(glm.vec3(0,self.ang_unit,0))
        if keys[pg.K_t]:
            self.m_rotation = self.update_view_matrix_rotate(glm.vec3(0,-self.ang_unit,0))
        if keys[pg.K_f]:
            self.m_rotation = self.update_view_matrix_rotate(glm.vec3(self.ang_unit,0,0))
        if keys[pg.K_g]:
            self.m_rotation = self.update_view_matrix_rotate(glm.vec3(-self.ang_unit,0,0))
        if keys[pg.K_v]:
            self.m_rotation = self.update_view_matrix_rotate(glm.vec3(0,0,self.ang_unit))
        if keys[pg.K_b]:
            self.m_rotation = self.update_view_matrix_rotate(glm.vec3(0,0,-self.ang_unit))
    
           

    def update_view_matrix_translate(self, vec):
        m_translation = glm.mat4(1.0)
        m_translation[3][0] = vec[0]
        m_translation[3][1] = vec[1] 
        m_translation[3][2] = vec[2] 
        self.m_view = self.m_view * m_translation
        return m_translation

    def update_view_matrix_rotate(self, angles):

        m_rotation = glm.mat4(1.0)
        m_identity = glm.mat4(1.0)

        m_rotation[1][1] = glm.cos(angles.x)
        m_rotation[1][2] = -glm.sin(angles.x)
        m_rotation[2][1] = glm.sin(angles.x)
        m_rotation[2][2] = glm.cos(angles.x)

        m_identity *= m_rotation

        m_rotation = glm.mat4(1)

        m_rotation[0][0] = glm.cos(angles.y)
        m_rotation[0][2] = glm.sin(angles.y)
        m_rotation[2][0] = -glm.sin(angles.y)
        m_rotation[2][2] = glm.cos(angles.y)

        m_identity *= m_rotation

        m_rotation = glm.mat4(1)

        m_rotation[0][0] = glm.cos(angles.z)
        m_rotation[0][1] = -glm.sin(angles.z)
        m_rotation[1][0] = glm.sin(angles.z)
        m_rotation[1][1] = glm.cos(angles.z)

        m_identity *= m_rotation

        m_identity *= self.m_rotation

        self.m_view = m_identity
        self.update_view_matrix_translate(glm.vec4(self.position,1))
        self.update_camera_vectors()
        return m_identity

    def get_view_matrix(self):
        view_matrix = glm.mat4(1)
        return view_matrix

    def get_projection_matrix(self):
        projection = glm.mat4(1)
        projection[3][3] = 0
        projection[2][3] = 1
        projection[3][2] = -1
        projection[0][0] = FOV/50
        projection[1][1] = FOV/50*self.aspect_ratio
        return projection
        