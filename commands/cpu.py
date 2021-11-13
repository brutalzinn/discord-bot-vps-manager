from psutil._common import bytes2human
import psutil

def cpu():
    fetchCPU = psutil.cpu_freq()
    currCPU = str(fetchCPU[0]) 
    maxCPU = str(fetchCPU[2])
    loadAvg = str(psutil.getloadavg())
    await message.channel.send("Velocidade de clock: " + currCPU[0:1] + "." + currCPU[1:2] + "Ghz" + " de " + maxCPU[0:1] + "." + maxCPU[1:2] + "Ghz")
    await message.channel.send("Carga média: " + loadAvg)