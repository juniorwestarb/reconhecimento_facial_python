#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# 
import face_recognition
import cv2 as cv
import glob
import time
import os
from PIL import Image
from imutils.video import FPS


def main(args):
    # Cria um objeto de captura de vídeo
    video_capture = cv.VideoCapture(0)
    fps = FPS().start()
    #video_capture.open("http://192.168.43.58:8080/videofeed")
    #video_capture.open()
    
    # Carrega uma  face a ser reconhecida.
    dir_files = str(os.path.dirname(os.path.abspath(__file__))) + '/images/matrizes/'
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
        # Preenche a  array associado com os nomes das faces seguindo o mesmo indice
        known_face_names.append(file[:-4])
    print(known_face_names)

 
    # Inicialização de algumas variaveis
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
 
    while True:
        # Captura um quadro de video
        ret, frame = video_capture.read()
        
        # Redimensiona o quadro para ficar mais rápido
        small_frame = cv.resize(frame, (0, 0), fx=0.25, fy=0.25)
 
        # Converte a imagem de BGR (utiizado pelo OpenCV) para RGB (utilizado pela face_recognition)
        rgb_small_frame = small_frame[:, :, ::-1]
 
        # processa quadros intercalodos para economia de tempo
        if process_this_frame:
            # obtem todas as faces e suas respectivas codificações
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
 
            face_names = []
             
            for face_encoding in face_encodings:
                # ve se ha coincidencia estre as faces
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Desconhecido"
 
                # se tem semelhança, obtem o nome.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                face_names.append(name)
 
        process_this_frame = not process_this_frame
 
 
        # Mostra os resultados
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
 
            # Desenha um retangulo sobre a face
            cv.rectangle(frame, (left, top), (right, bottom), (255, 10, 0), 2)
 
            # Desenha uma etiqueta com o nome abaixo da face
            cv.rectangle(frame, (left, bottom - 35), (right, bottom), (50, 10, 0), cv.FILLED)
            font = cv.FONT_HERSHEY_DUPLEX
            cv.putText(frame, name.upper()[:10], (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
 
        # Mostra a imagem resultante
        cv.imshow('Video', frame)
        
 
        # 'ESC' para sair do programa!
        if cv.waitKey(1) & 0xFF == 27:
            break
        fps.update()
 
    fps.stop()
    # Libera os recursos de video utilizados
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    video_capture.release()
    cv.destroyAllWindows()
    return 0
 
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
