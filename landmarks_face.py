#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  maquiagemVirtual.py
 
# 
from PIL import Image, ImageDraw
import face_recognition
 
 
def main(args):
 
    # carrega o arquivo jpg em um array  numpy
    image = face_recognition.load_image_file("images/full photos/familia.jpg")
 
    # Obtem todas as caracteristicas de uma facee
    face_landmarks_list = face_recognition.face_landmarks(image)
 
    # trabalha com cada face identificada
    for face_landmarks in face_landmarks_list:
        pil_image = Image.fromarray(image)
        # mantem uma cópia do original para facilitar a comparação
        pil_image_original = pil_image.copy()
        # desenharemos sobre a área "d"
        d = ImageDraw.Draw(pil_image, 'RGBA')
 
        # Marca as sobrancelhas com um traço grossoe
        d.polygon(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 128))
        d.polygon(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 128))
        d.line(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 150), width=5)
        d.line(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 150), width=5)
 
        # pinte os lábios de batom vermelho
        d.polygon(face_landmarks['top_lip'], fill=(150, 0, 0, 128))
        d.polygon(face_landmarks['bottom_lip'], fill=(150, 0, 0, 128))
        d.line(face_landmarks['top_lip'], fill=(150, 0, 0, 64), width=8)
        d.line(face_landmarks['bottom_lip'], fill=(150, 0, 0, 64), width=8)
 
        # Faça os olhos faiscarem
        d.polygon(face_landmarks['left_eye'], fill=(255, 255, 255, 30))
        d.polygon(face_landmarks['right_eye'], fill=(255, 255, 255, 30))
 
        # aplicando um delineador nos olhos
        d.line(face_landmarks['left_eye'] + [face_landmarks['left_eye'][0]], fill=(0, 0, 0, 110), width=6)
        d.line(face_landmarks['right_eye'] + [face_landmarks['right_eye'][0]], fill=(0, 0, 0, 110), width=6)
 
        pil_image.show()
        pil_image_original.show()
    return 0
 
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))