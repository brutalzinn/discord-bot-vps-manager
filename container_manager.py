from sys import flags
from config import dockerClient, docker

def create_container(path, servername, port, environment):
    try:
        dockerClient.containers.run(image="itzg/minecraft-server:java8", name=servername, ports={f'{port}/tcp': port},                                    
                                     environment=environment, volumes={path: {'bind': '/data', 'mode': 'rw'}},
                                    detach=True)
        return {"status":True}
    except Exception as err:
        print(err)
        return {"status":False, "mensagem":str(err)}
    except docker.errors.ImageNotFound as err:
        print("Puxando imagem itzg/minecraft-server")
        print(err)
        dockerClient.images.pull("itzg/minecraft-server")
        return {"status":False,"mensagem":"Imagem itzg/minecraft-server não encontrada. A imagem foi instalada e pronta para ser usada. \n execute esse comando novamente."}

def restart_container(servername):
   
    try:
        dockerClient.api.restart(servername)
        return True
    except:
        return False


def start_container(servername):
    try:
        dockerClient.api.start(servername)
        return True
    except:
        return False


def stop_container(servername):
  
    try:
        dockerClient.api.stop(servername)
        return True
    except Exception as err:
        print(err)
        return False
    
def list_container():
    list = ''
    containerList = dockerClient.containers.list(all=True, filters={"ancestor": "itzg/minecraft-server"})
    if len(containerList) == 0:
        list = 'Nenhum servidor criado.'
    for item in containerList:
        containerInfo = dockerClient.containers.get(item.id)
        ports = containerInfo.attrs['HostConfig']['PortBindings'].items()
        finalPort = 0
        for key, value in ports:
            finalPort = value[0]['HostPort']
        list += f'Nome: {item.name}, status: {item.status}, port: {finalPort} \n'
    return list