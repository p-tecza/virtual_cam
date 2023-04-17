import glm
import pygame as pg
import numpy as np

FOV = 50
MIN_FOV, MAX_FOV = 10,100
NEAR = 0.1
FAR = 100
SPEED = 0.01
SENSITIVITY = 0.05

class Camera:
    def __init__(self,app, position = (0,0,0), yaw=-90, pitch=0, roll=0):
        self.translation_unit = 0.05
        self.ang_unit = glm.radians(4)
        self.current_angs = glm.vec3(0,0,0)
        self.app=app
        self.aspect_ratio = app.WIN_SIZE[0]/app.WIN_SIZE[1]
        self.position=glm.vec3(position)
        self.up = glm.vec3(0,1,0)
        self.right= glm.vec3(1,0,0)
        # forward to -1 bo układ prawoskrętny
        self.forward = glm.vec3(0,0,-1)
        self.m_translation = glm.mat4(1.0)
        self.m_rotation = glm.mat4(1.0)

        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll

        #view matrix
        self.m_view = self.get_view_matrix()

        # proj matrix
        self.m_proj = self.get_projection_matrix()

    def rotate(self):
        rel_x, rel_y=pg.mouse.get_rel()
        self.yaw += rel_x*SENSITIVITY
        self.pitch -= rel_y * SENSITIVITY
        self.pitch = max(-89,min(89,self.pitch))

        # print(rel_x)
        # keys = pg.key.get_pressed()
        # if keys[pg.K_y]:
        #     self.roll = 270
        # if keys[pg.K_u]:
        #     self.roll = 360

        

    def update_camera_vectors(self):
        yaw,pitch,roll = glm.radians(self.current_angs.x), glm.radians(self.current_angs.y), glm.radians(self.current_angs.z)
        # self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        # self.forward.y = glm.sin(pitch)
        # self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        inverted = glm.inverse(self.m_view)
        self.forward = glm.vec3(inverted[2])

        print("typ yaw")
        print(type(yaw))

        # right_vector = glm.vec3(0.0,glm.cos(roll), glm.sin(roll))
        
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0,1,0)))
        
        self.up = glm.normalize(glm.cross(self.right, self.forward))

        self.forward = glm.normalize(self.forward)


    def update(self):
        self.move()
        print("FORWARD VEC: ")
        print(self.forward)
        # self.rotate()
        # self.update_camera_vectors()
        # self.m_view = self.get_view_matrix()
        self.m_proj = self.get_projection_matrix()

    def move(self):
        velocity = SPEED * self.app.delta_time
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.position.y -= self.translation_unit
            self.m_translation *= self.update_view_matrix_translate(glm.vec4(0,-self.translation_unit,0,1))
        if keys[pg.K_s]:
            self.position.y += self.translation_unit
            self.m_translation *= self.update_view_matrix_translate(glm.vec4(0,self.translation_unit,0,1))
        if keys[pg.K_a]:
            self.position.x += self.translation_unit
            self.m_translation *= self.update_view_matrix_translate(glm.vec4(self.translation_unit,0,0,1))
        if keys[pg.K_d]:
            self.position.x -= self.translation_unit
            self.m_translation *= self.update_view_matrix_translate(glm.vec4(-self.translation_unit,0,0,1))
        if keys[pg.K_q]:
            self.position.z += self.translation_unit
            self.m_translation *= self.update_view_matrix_translate(glm.vec4(0,0,self.translation_unit,1))
            #self.m_translation *= self.update_view_matrix_translate(glm.vec4(self.translation_unit * self.forward.x,self.translation_unit*self.forward.y,self.translation_unit*self.forward.z,1))
        if keys[pg.K_e]:
            self.position.z -= self.translation_unit
            self.m_translation *= self.update_view_matrix_translate(glm.vec4(0,0,-self.translation_unit,1))
            #self.m_translation *= self.update_view_matrix_translate(glm.vec4(self.translation_unit * self.forward.x,self.translation_unit * self.forward.y,-self.translation_unit * self.forward.z,1))*glm.vec4(self.forward,1)
        global FOV, MIN_FOV, MAX_FOV
        if keys[pg.K_n]:
            if FOV<MAX_FOV:
                FOV+=1
        if keys[pg.K_m]:
            if FOV>MIN_FOV:
                FOV-=1
        if keys[pg.K_r]:
            self.roll -= 0.01
            self.current_angs.y += self.ang_unit * velocity
            ang = self.current_angs.y
            val1,val2,val3,val4 = glm.cos(ang),-glm.sin(ang),glm.sin(ang),glm.cos(ang)
            self.m_rotation = self.update_view_matrix_rotate([val1,val2,val3,val4],[[1,1],[1,2],[2,1],[2,2]])
        if keys[pg.K_t]:
            self.roll += 0.01
            self.current_angs.y -= self.ang_unit * velocity
            ang = self.current_angs.y
            val1,val2,val3,val4 = glm.cos(ang),-glm.sin(ang),glm.sin(ang),glm.cos(ang)
            self.m_rotation = self.update_view_matrix_rotate([val1,val2,val3,val4],[[1,1],[1,2],[2,1],[2,2]])
        if keys[pg.K_f]:
            self.pitch -= 0.01
            self.current_angs.x += self.ang_unit * velocity
            ang = self.current_angs.x
            val1,val2,val3,val4 = glm.cos(ang),glm.sin(ang),-glm.sin(ang),glm.cos(ang)
            self.m_rotation = self.update_view_matrix_rotate([val1,val2,val3,val4],[[0,0],[0,2],[2,0],[2,2]])
        if keys[pg.K_g]:
            self.pitch += 0.01
            self.current_angs.x -= self.ang_unit * velocity
            ang = self.current_angs.x
            val1,val2,val3,val4 = glm.cos(ang),glm.sin(ang),-glm.sin(ang),glm.cos(ang)
            self.m_rotation = self.update_view_matrix_rotate([val1,val2,val3,val4],[[0,0],[0,2],[2,0],[2,2]])
        if keys[pg.K_v]:
            self.yaw -= 0.01
            self.current_angs.z += self.ang_unit * velocity
            ang = self.current_angs.z
            val1,val2,val3,val4 = glm.cos(ang),-glm.sin(ang),glm.sin(ang),glm.cos(ang)
            self.m_rotation = self.update_view_matrix_rotate([val1,val2,val3,val4],[[0,0],[0,1],[1,0],[1,1]])
        if keys[pg.K_b]:
            self.yaw += 0.01
            self.current_angs.z -= self.ang_unit * velocity
            ang = self.current_angs.z
            val1,val2,val3,val4 = glm.cos(ang),-glm.sin(ang),glm.sin(ang),glm.cos(ang)
            self.m_rotation = self.update_view_matrix_rotate([val1,val2,val3,val4],[[0,0],[0,1],[1,0],[1,1]])
        
            # NEAR+=1
            # FAR-=1
        # self.roll = max(-89,min(89,self.roll))
           

    def update_view_matrix_translate(self, vec):

        m_translation = glm.mat4(1.0)
        m_translation[3][0] = vec[0]
        m_translation[3][1] = vec[1] 
        m_translation[3][2] = vec[2] 
        # print("TRANSLATION")
        # print(m_translation)
        # m_translation

        self.m_view = self.m_view * m_translation
        # print("SELF M VIEW")
        # print(self.m_view)
        # print("POSITION\n ",self.position)

        return m_translation

    def update_view_matrix_rotate(self, vals, cords):

        m_rotation = glm.mat4(1.0)
        m_identity = glm.mat4(1)
        # m_rotation[cords[0][0]][cords[0][1]] = vals[0]
        # m_rotation[cords[1][0]][cords[1][1]] = vals[1]
        # m_rotation[cords[2][0]][cords[2][1]] = vals[2]
        # m_rotation[cords[3][0]][cords[3][1]] = vals[3]
        m_rotation[1][1] = glm.cos(self.current_angs.x)
        m_rotation[1][2] = -glm.sin(self.current_angs.x)
        m_rotation[2][1] = glm.sin(self.current_angs.x)
        m_rotation[2][2] = glm.cos(self.current_angs.x)

        m_identity *= m_rotation

        m_rotation = glm.mat4(1)

        m_rotation[0][0] = glm.cos(self.current_angs.y)
        m_rotation[0][2] = glm.sin(self.current_angs.y)
        m_rotation[2][0] = -glm.sin(self.current_angs.y)
        m_rotation[2][2] = glm.cos(self.current_angs.y)

        m_identity *= m_rotation

        m_rotation = glm.mat4(1)

        m_rotation[0][0] = glm.cos(self.current_angs.z)
        m_rotation[0][1] = -glm.sin(self.current_angs.z)
        m_rotation[1][0] = glm.sin(self.current_angs.z)
        m_rotation[1][1] = glm.cos(self.current_angs.z)

        m_identity *= m_rotation

        # m_rotation[0][0] = glm.cos(self.current_angs.x)
        # m_rotation[0][1] = glm.co
        # m_rotation[0][2]

        # inversed_view_matrix = glm.inverse(self.m_view)
        # m_temp = inversed_view_matrix * self.m_view

        # print("m_temp")
        # print(m_temp)

        # m_temp = m_temp * m_rotation

        

        # m_current_angs = glm.inverse(self.m_view)
        # m_current_angs_final = glm.mat4(glm.mat3(m_current_angs))

        # print("mself_rot\n",self.m_rotation)
        m_temp = m_identity * m_rotation * self.m_rotation

        # self.m_rotation=glm.mat4(1)

        print("m_temp rotated")
        # print(m_temp)

        self.m_view = m_identity
        self.update_view_matrix_translate(glm.vec4(self.position,1))
        self.update_camera_vectors()
        return m_identity

    def get_view_matrix(self):

        view_matrix = glm.mat4(1)

        # print("x\n",view_matrix)

        return view_matrix

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)