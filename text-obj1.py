import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

model_files = {
    "a": "Arm3.obj",
}

def load_model(file):
    vertices = []
    faces = []
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.split()
            if not parts:  # Skip empty lines
                continue
            if parts[0] == "v":
                vertices.append(list(map(float, parts[1:])))
            elif parts[0] == "f":
                face_parts = parts[1:]
                face = []
                for part in face_parts:
                    split_part = part.split("/")
                    face.append([int(p) if p else 0 for p in split_part])
                faces.append(face)
    return (vertices, faces)

def draw_model(model):
    glColor3f(1.0, 0.0, 0.0)  # Set the color to red
    vertices, faces = model
    glPushMatrix()  # Save the current matrix
    glRotatef(90, 0, 1, 0)  # Rotate the matrix by 90 degrees around the y-axis
    for face in faces:
        glBegin(GL_POLYGON)
        for vertex in face:
            glVertex3fv(vertices[vertex[0] - 1])
        glEnd()
    glPopMatrix()  # Restore the original matrix

models = {letter: load_model(file) for letter, file in model_files.items()}

def interpret_text(text):
    text = text.lower()
    model_sequence = []
    for char in text:
        if char in models:
            model_sequence.append(models[char])
    return model_sequence

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(4.0, -5.0, -30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        text = "a"
        model_sequence = interpret_text(text)

        for model in model_sequence:
            draw_model(model)

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
