from sys import flags
import docker
dockerClient = docker.from_env()
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
    except:
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
    print(list)
    return list