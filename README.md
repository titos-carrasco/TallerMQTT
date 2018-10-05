# TallerMQTT
Taller introductorio a MQTT

# Software requerido
Para poder realizar las actividades de este taller debes preparar tu computador personal con varios programas. Para esto sigue las indicaciones dadas en el documento  [Taller - 00 Instalación Software.pdf](Taller - 00 Instalación Software.pdf)

# Conceptos iniciales y motivación
Los primeros 20 minutos del taller los dedicaremos a entregarte los conceptos básicos de MQTT y, para motivarte, te mostraremos como mover un robot desde `cualquier parte del mundo`. El contenido qu te entregaremos se encuentra resumido en el documento [Taller MQTT.pdf](Taller MQTT.pdf)

Finalizado el demo realizaremos un conjunto variado de actividades para transmitir y leer información a través de la red utilizando MQTT

# Actividad: Enviar un número
Envia un número al tópico `rcr/numero/XX`, cambiando `XX` por 01, 02, ... según te lo indiquen. El docente mostrará una página con los números que se están recibiendo.
Utiliza Node-Red, MQTT Fx y MQTT Dash para desarrollar la actividad

![](images/Actividad-Enviar-Numero-01.png)
<br />
<br />
![](images/Actividad-Enviar-Numero-02.png)
<br />
<br />
![](images/Actividad-Enviar-Numero-03.png)

# Actividad:Leer una estación meteorológica
Lee los datos de la estación meteorológica que publica sus datos en el tópico `rcr/weather`. Es importante señalar que los datos son enviados en formato JSON.
Utiliza Node-Red, MQTT Fx y MQTT Dash para desarrollar la actividad

![](images/Actividad-Estacion-01.png)
<br />
<br />
![](images/Actividad-Estacion-02.png)
<br />
<br />
![](images/Actividad-Estacion-03.png)
<br />
![](images/Actividad-Estacion-04.png)

# Actividad: Transmisión y recepción de video
Lee la data que se transmitirá en el tópico `rcr/video`. Utiliza Node-Red y MQTT Dash

![](images/Actividad-Video-01.png)
<br />
<br />
![](images/Actividad-Video-02.png)


