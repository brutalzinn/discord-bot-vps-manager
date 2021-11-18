import psutil
from psutil._common import bytes2human
from models.commands.command_model import command_model
from models.commands.command_register import command_register

async def cpu(command : command_model, message):
    fetchCPU = psutil.cpu_freq()
    currCPU = str(fetchCPU[0]) 
    maxCPU = str(fetchCPU[2])
    loadAvg = str(psutil.getloadavg())
    resultado = f"Velocidade de clock: {currCPU[0:1]}.{currCPU[1:2]} Ghz de {maxCPU[0:1]}.{maxCPU[1:2]} Ghz \n Carga média: {loadAvg}"
    return resultado
    
async def mem(command : command_model, message):
    mem_usage = psutil.virtual_memory()
    total_mem = bytes2human(mem_usage[0])
    used_mem = bytes2human(mem_usage[3])
    return f"{used_mem} de {total_mem} RAM usada."
  
def register(commands : command_register):
  command_model('cpu',method=cpu, descricao="Exibir uso de cpu do servidor", register=commands)
  command_model('ram', method=mem, descricao="Exibir uso de memória do servidor", register=commands)
  
