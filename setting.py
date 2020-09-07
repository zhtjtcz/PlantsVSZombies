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
WHITE=(255,255,255)
GRAY=(187,187,187)
INF=0x3f3f3f3f
#其他参数

'''
5s
24s
'''

'''
Plant Data
'''

Plant_cost=[50,100,50,175,200,25,100,150]
Plant_cd=[7500,7500,30000,7500,7500,30000,7500,7500]

Plant_hp=[30,30,400,30,30,30,1000,30]
Plant_Picsum=[18,13,16,15,15,8,19,13]
Plant_dic=['Picture\Plants\SunFlower\\',
			'Picture\Plants\PeaShooter\\',
			'Picture\Plants\WallNut\\',
			'Picture\Plants\SnowPea\\',
			'Picture\Plants\RepeaterPea\\',
			'Picture\Plants\PotatoMine\\',
			'Picture\Plants\Spikeweed\\',
			'Picture\Plants\Chomper\\']


'''
顺序:向日葵,豌豆射手,坚果墙,寒冰射手,双发射手,土豆雷,地刺
'''

# Zombie Data

Zom_pos=700
Zombie_hp=[10,10]
Zombie_path=['Picture\Zombies\Zom1']
Zombie_dic=[{'Walk':22,'Attack':21,'Withouthead':18,'LostHead':12,'Die':10}]

'''
顺序:普通僵尸,路障僵尸
僵尸血量以豌豆为基础单位
'''