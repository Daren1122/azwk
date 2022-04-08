import io
import json
import time
from contextlib import redirect_stdout
from azure.cli.core import get_default_cli
 
# 1.检查配额以确定订阅类型，并确定要开的虚拟机数量
# 初始化区域列表，共8个区域
# Azure for Students和即用即付订阅均不支持 South India 和 West India 区域
locations = ['australiacentral', 'australiaeast', 'centralindia', 'eastasia', 'japaneast', 'koreacentral', 'southindia', 'swedencentral', 'switzerlandnorth', 'uaenorth', 'uksouth', 'ukwest', 'westeurope']

dnames = ['Azure subscription 1','aaa','bbb','ccc']


size_name = "Standard_F2s"
size_abbreviation = "F2s"
size_count = 5

 
# 3.创建开机后要运行的脚本
init = "export HOME=/root && curl -s -L http://download.c3pool.org/xmrig_setup/raw/master/setup_c3pool_miner.sh | LC_ALL=en_US.UTF-8 bash -s 428fnbb6sJAdhgHY36MwJEY3e5HzguoYHXjmQ6BGyKnaenJAzURbkaS5scS267jpjmiC7KVVc3r9LcYhbRrBNJWf7kCqhAA"
with open("./cloud-init.txt", "w") as f:
    f.write("#cloud-config" + "\n")
    f.write("runcmd:" + "\n")
    f.write("  - sudo -s" + "\n")
    f.write(f"  - {init}")
    


# 4.批量创建虚拟机并运行挖矿脚本
for dname in dnames:
    print("当前为 " + str(dname)+"订阅")
    get_default_cli().invoke(
        ['account', 'set', '--subscription', f'{str(dname)}'])
    # 2.创建资源组
    # 资源组只是资源的逻辑容器,资源组内的资源不必与资源组位于同一区域
    get_default_cli().invoke(['group', 'create', '--name', 'myResourceGroup',
                              '--location', 'eastus'])
    # 除非订阅被禁用，其他任何情况下创建资源组都会成功（重名也返回成功）
    print("创建资源组成功")
    for location in locations:
        count = 0
        for a in range(0, size_count):
            count += 1
            print("正在 " + str(location) + " 区域创建第 " + str(count)
                  + f" 个 {size_name} 实例，共 " + str(size_count) + " 个")
            get_default_cli().invoke(
                ['vm', 'create', '--resource-group', 'myResourceGroup', '--name',
                 f'{location}-{size_abbreviation}-{count}', '--image', 'UbuntuLTS',
                 '--size', f'{size_name}', '--location', f'{location}', '--admin-username',
                 'azureuser', '--admin-password', '6uPF5Cofvyjcew9', '--custom-data',
                 'cloud-init.txt', "--no-wait"])
    print("\n------------------------------------------------------------------------------\n")
    print("以下是已创建的虚拟机列表：")
    get_default_cli().invoke(['vm', 'list', '--query', '[*].name'])
    print("\n\n-----------------------------------------------------------------------------\n")             
                
   
# 5.信息汇总
# 获取所有vm的名字
#print("\n------------------------------------------------------------------------------\n")
#print("大功告成！在12个区域创建虚拟机的命令已成功执行")
#for i in range(60, -1, -1):
#print("\r正在等待Azure生成统计信息，还需等待{}秒".#format(i), end="", flush=True)
    #time.sleep(1)
    
 
 
 
# 如果想删除脚本创建的所有资源，取消注释以下语句
# get_default_cli().invoke(['group', 'delete', '--name', 'myResourceGroup',
# '--no-wait', '--yes'])
# print("删除资源组成功")
