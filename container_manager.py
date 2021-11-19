from sys import flags
import docker
dockerClient = docker.from_env()


def create_container(path, servername, port, environment):
    try:
        dockerClient.containers.run(image="itzg/minecraft-server", name=servername, ports={f'{port}/tcp': port},                                    
                                     environment=environment, volumes={path: {'bind': '/data', 'mode': 'rw'}},
                                    detach=True)
        return {"status":True}
    except Exception as err:
        print(err)
        return {"status":False, "mensagem":"Ocorreu um erro desconhecido."}
    except docker.errors.ImageNotFound:
        print("Puxando imagem itzg/minecraft-server")
        dockerClient.images.pull("itzg/minecraft-server")
        return {"status":True,"mensagem":"Imagem itzg/minecraft-server não encontrada. A imagem foi instalada e pronta para ser usada. \n execute esse comando novamente."}

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
    
    list = []
    containerList = dockerClient.containers.list(all=True, filters={"ancestor": "itzg/minecraft-server"})
    for item in containerList:
        containerInfo = dockerClient.containers.get(item.id)
        ports = containerInfo.attrs['HostConfig']['PortBindings'].items()
        finalPort = 0
        for key, value in ports:
            finalPort = value[0]['HostPort']
        list.append({'name': item.name, 'status': item.status, 'port': f"{finalPort}"})
    return list