#!/usr/bin/env python

import rospy
import turtlesim
from geometry_msgs.msg import Twist
from math import floor #funcao para arredondar pra baixo
import time

def publish_vel(vel_lin, vel_ang, pub):
    msg_vel = Twist()
    msg_vel.linear.x = vel_lin
    msg_vel.angular.z = vel_ang
    rospy.loginfo(msg_vel)
    pub.publish(msg_vel)

try:
    
    rospy.init_node('talker', anonymous=True)
    pub_velocity = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        
        #Exemplo de entrada para o input abaixo: [20.0, 10.0, 5.0]
        #Caso a distancia linear ou o angulo de rotacao nao forem multiplos
        #da velocidade, o valor da distancia linear real ou do angulo de rotacao 
        #real sera o maior multiplo da velocidade menor que esse valor passado
        lista = input("""Informe uma lista com a distancia linear, o angulo de rotacao
e a velocidade linear separados por virgula: """)

        if(type(lista)!=list and type(lista)!=tuple):
            print("\nEntrada informada nao e uma lista.")
            continue
        if (len(lista)!=3 or len(filter(lambda i: type(i)==int or type(i)==float, lista))!=3):
            print("""\nEntrada invalida, informe os tres valores da lista corretamente (distancia 
linear, angulo de rotacao, velocidade linear).""")
            continue

        if ((lista[0]>=0 and lista[2]>=0) or (lista[0]<=0 and lista[2]<=0)):

            if abs(lista[0])>=abs(lista[2]): #Se o absoluto da distancia for maior ou igual o absoluto da velocidade
                vel_lin = lista[2]

                #Por padrao o turtlesim anda a velocidade dada durante 1 segundo
                #logo precisamos da "quantidade de velocidades" a serem publicadas
                #para obter uma certa distancia
                qtd_vel = int(floor(lista[0]/lista[2])) if (lista[0]!=0 and lista[2]!=0) else 1

                #vel_ang e calculado assim para que a cada segundo no
                #movimento linear no loop haja um mesmo falor fixo de rotacao
                #tal que quando o movimento linear for finalizado, o movimento de rotacao seja 
                #finalizado junto (assim sera possivel andar em circulos se desejarmos)            
                vel_ang = float(lista[1])/qtd_vel
                
            else: #Se a distancia for menor que a velocidade
                vel_lin = lista[0]
                vel_ang = lista[1]
                qtd_vel = 1 #Os valores definidos nas duas linhas acima serao publicados uma vez e a tartaruga se
                            #movimentara durante 1 seg
        else:
            print("""\nNao e possivel executar o movimento pois a distancia linear e a velocidade
linear tem sinais opostos.""")
            continue

        for a in range(0, qtd_vel):
            publish_vel(vel_lin, vel_ang, pub_velocity)
            time.sleep(1)

        rate.sleep()

except rospy.ROSInterruptException:
    pass