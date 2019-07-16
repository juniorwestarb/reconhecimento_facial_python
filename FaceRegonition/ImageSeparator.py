#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  
from PIL import Image
from PIL import ImageChops
 
import face_recognition
import os
import uuid

path = str(os.path.dirname(os.path.abspath(__file__))) + '/images'


 
def main(args):
    dir_temp = path + '/temp/'
    dir_biblioteca = path + '/agrupamento/'
    # Carrega a foto em um Array Numpy
    image = face_recognition.load_image_file("images/originals/familia.jpg")
 
    # Busca os rostos na imagem usando o modelo padrão HOG.
    face_locations = face_recognition.face_locations(image)
 
    print("Encontrei {} face(s) nesta foto.".format(len(face_locations)))
    #mostra a imagem original
    pil_image_original = Image.fromarray(image)
    pil_image_original.show()
     

    for face_location in face_locations:
        try:
            # Mostra a posição de cada face
            top, right, bottom, left = face_location
            print("Uma face é localizada na posição Topo: {}, Esquerda: {}, Fundo: {}, Direita: {}".format(top, left, bottom, right))
    
            # Captura a imagem separadamente e salva na pasta images/temp:
            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            person_id = str(uuid.uuid4()) + ".jpg"

            pil_image.save(dir_temp + person_id ,"jpeg")

            file_image = face_recognition.load_image_file(dir_temp + person_id)
            file_face_locations = face_recognition.face_locations(file_image)
            file_face_encoding = face_recognition.face_encodings(file_image, file_face_locations)[0]
            # faz a pesquisa se existe nas matrizes correspondência, se existir ele separa por nomes, senão ele adiciona na pasta desconhecido.
            name = searchFace(file_face_encoding)
            if not os.path.exists(dir_biblioteca + name):
                os.mkdir(dir_biblioteca + name)
            pil_image.save(dir_biblioteca + name + "/{0}".format(person_id) ,"jpeg")
            pil_image.show()
        except:
            next
 
    return 0


def searchFace(imageEncoding):
    dir_files = path + '/matrizes/'
    name = "desconhecido"
    # Carrega uma  face a ser reconhecida.
    files = []
    if os.path.exists(dir_files):
        files = os.listdir(dir_files)

    known_face_encodings = []
    known_face_names = []

    for file in files:
        # carrega a foto
        file_image = face_recognition.load_image_file(dir_files + file)
        # Identifica a codificação da face
        file_face_encoding = face_recognition.face_encodings(file_image)[0]
        # Preenche a array de faces ja codificadas
        known_face_encodings.append(file_face_encoding)
        known_face_names.append(file[:-4])

    

    matches = face_recognition.compare_faces(known_face_encodings, imageEncoding)

    if True in matches:
        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]
    return name
    
 
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))