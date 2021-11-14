import psutil
from psutil._common import bytes2human
from models.commands.command_model import command_model


def cpu(message):
    fetchCPU = psutil.cpu_freq()
    currCPU = str(fetchCPU[0]) 
    maxCPU = str(fetchCPU[2])
    loadAvg = str(psutil.getloadavg())
  #  await message.channel.send("Velocidade de clock: " + currCPU[0:1] + "." + currCPU[1:2] + "Ghz" + " de " + maxCPU[0:1] + "." + maxCPU[1:2] + "Ghz")
  #  await message.channel.send("Carga média: " + loadAvg)
    print(message)
    print('TESTEEEE CPU')
    
async def mem(message):
    mem_usage = psutil.virtual_memory()
    total_mem = bytes2human(mem_usage[0])
    used_mem = bytes2human(mem_usage[3])
    await message.channel.send(used_mem + " de " + total_mem + " RAM usada.")
    
