## Docker ##

### **Установка Docker** ###

---

```commandline
sudo apt install docker.io
```

```commandline
sudo systemctl status docker
```

---


### **Установка Docker-compose** ###

---

```commandline
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

```commandline
sudo chmod +x /usr/local/bin/docker-compose
```

```commandline
docker-compose --version
```

---

### **Настройка после установки** ###

Мы должны выдать ```docker``` пользователю ```root``` права, чтобы при вводе команд докера, не приписывать в начало ```sudo```

```commandline
sudo usermod -aG docker $USER 
```

```commandline
su - ${USER}
```

```commandline
id -nG
```

```commandline
sudo chmod +666 /var/run/docker. sock
```

---

### **Полезные команды** ###

* *Вывести все работающие контейнеры*

```commandline
docker ps
```

* *Вывести все контейнеры*

```commandline
docker ps -a
```

* *Собрать контейнер на основе Dockerfile*

```commandline
docker build -t <container_name> . -f <Docker_dile_path>
```

* *Запустить ```Docker-compose``` файл*

```commandline
docker-compose up --build
```

* *Запустить ```Docker-compose``` файл в фоновом режиме*

```commandline
docker-compose up --build -d
```

* *Запустить ```docker``` контейнер*

```commandline
docker start <container_id>
```

* *Зайти внутрь ```docker``` контейнера (и выход из него)*

```commandline
docker exec -it <container_id> bin/sh
```

```commandline
exit
```

```Build the Docker Image
docker build -t myimage .
```

```Start the Docker Container
docker run -d --name mycontainer -p 80:80 myimage
```

```Открыть консоль контейнера
docker exec -it <container> bash
```

* *Удалить все контейнеры и образы соответственно*

```commandline
docker rm -f $(docker ps -aq)
```

```commandline
docker rmi -f $(docker images -aq)
```

* *Удалить конкретный контейнер и образ соответственно*

```commandline
docker rm -f <container_id>
```

```commandline
docker rmi -f <image_id>
```

---