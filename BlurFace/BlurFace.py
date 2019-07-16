#!/usr/bin/env python
# -*- coding: utf-8 -*-

import face_recognition
import cv2
 
 
def main(args):

    # Cria um objeto de captura de video, na camera default
    video_capture = cv2.VideoCapture(0)
 
    # Inicialização da lista de coordenadas de localização das faces
    face_locations = []
 
    while True:
        # captura um quadro de video
        ret, frame = video_capture.read()
 
        # Redimensiona o quadro para ficar mais rápido
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
 
        # enconra as faces e armazena suas posições
        face_locations = face_recognition.face_locations(small_frame, model="cnn")
         
        # mostra o resultado
        for face_location in face_locations:
             
            top, right, bottom, left = face_location
            # recalcula as coordenadas que foram escalonadas anteriormente
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
 
            # Extrai a região da imagem que contem a face
            face_image = frame[top:bottom, left:right]
            # borra a face
            face_image = cv2.GaussianBlur(face_image, (99, 99), 30)
 
            # retorna a parte borrada para o quadro principal
            frame[top:bottom, left:right] = face_image
 
        # mostra a imagem resultante
        cv2.imshow('Video', frame)
 
         
        # pressione  'q' para sair do programa
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
 
    # Libere os recursos utilizados
    video_capture.release()
    cv2.destroyAllWindows()
 
    return 0
 
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
