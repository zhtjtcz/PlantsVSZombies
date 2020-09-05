'''

Basic settings

'''

Screen_Width=800
Screen_Height=590
#屏幕大小

Fps=30
Plant_Move_FPS=4
Zombie_Move_FPS=5
#动作持续帧数

Coordinate_origin=(40,85)
#草坪左上角

Block_size_width=80
Block_size_height=100
# 草坪一格横纵长度

Card_size=60
Card_pos=(83,10)
Card_scale=(50,65)
Sun_Pos=(30,65)
Card_Width=40
Card_Height=65
#卡片槽参数


BLACK=(0,0,0)
#其他参数

'''
5s
24s
'''

'''
Plant Data
'''

Plant_cost=[50,100]
Plant_cd=[5,5]

Plant_hp=[10,20]
Plant_Picsum=[18]
Plant_dic=['Picture\Plants\SunFlower\\','Picture\Plants\Pea_Shooter\\']

'''
顺序:向日葵,豌豆射手
以僵尸啃食次数为基础单位
'''

# Zombie Data

Zom_pos=880
Zombie_hp=[10,10]
Zombie_path=['Picture\Zombies\Zom1']
Zombie_dic=[{'Walk':22,'Attack':21,'Withouthead':18,'LostHead':12,'Die':10}]

'''
顺序:普通僵尸,路障僵尸
僵尸血量以豌豆为基础单位
'''