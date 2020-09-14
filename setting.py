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
Plant Data
'''

Plant_cost=[50,100,50,175,200,25,100,150]
Plant_cd=[7500,7500,30000,7500,7500,30000,7500,7500]
#植物阳光消耗与CD时间(单位:ms)

Plant_hp=[30,30,400,30,30,30,1000,30]
Plant_Picsum=[18,13,16,15,15,8,19,13]
#植物血量与图片数目

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

'''
Zombie Data
'''

Zom_pos=700
#僵尸生成位置

Zombie_hp=[10,25,55,10,25]
Zombie_path=['Picture\Zombies\Zom1','Picture\Zombies\Zom2','Picture\Zombies\Zom3','Picture\Zombies\Zom4','Picture\Zombies\Zom5']
#血量与图片路径

Zombie_dic=[{'Walk':22,'Attack':21,'Withouthead':18,'LostHead':12,'Die':10},
			{'Walk':21,'Walk2':22,'Attack':11,'Attack2':21,'Withouthead':18,'LostHead':12,'Die':10},
			{'Walk':15,'Walk2':22,'Attack':11,'Attack2':21,'Withouthead':18,'LostHead':12,'Die':10},
			{'Walk':12,'Attack':11,'Withouthead':12,'LostHead':12,'Die':10},
			{'Walk':19,'Walk2':14,'Attack':7,'Attack2':7,'Withouthead':18,'LostHead':16,'Die':10}]
#不同状态下的图片数目

'''
顺序:普通僵尸,路障僵尸,铁桶僵尸,旗帜僵尸
僵尸血量以豌豆为基础单位
'''

Zom_create=[
	[[20,0],[48,0],[74,0],[96,0],[96,0],[110,0],[110,0],[120,0],[120,0],[140,0],[140,0],[140,0],[155,0],[155,0],[155,0]],
	[[20,0],[48,0],[74,0],[96,0],[96,0],[96,0],[110,0],[110,0],[110,0],[120,0],[120,0],[140,0],[140,0],[140,0],[155,0],[155,0],[155,0],[160,0],[160,0],[160,0],[160,0],[160,0],[160,0],[160,0],[160,0]],
	[[20,0],[48,0],[74,0],[96,1],[96,0],[96,0],[110,1],[110,0],[110,0],[120,1],[120,1],[140,0],[140,0],[140,0],[155,1],[155,1],[155,0],[160,1],[160,1],[160,1],[160,0],[160,0],[160,0],[160,0],[160,0]],
	[[20,0],[48,0],[74,0],[96,0],[96,1],[110,0],[110,1],[120,1],[120,2],[140,2],[140,2],[140,0],[155,1],[155,2],[155,2]],
	[[20,0],[48,0],[74,0],[96,1],[96,0],[96,0],[110,1],[110,0],[110,0],[120,1],[120,2],[140,0],[140,1],[140,1],[155,1],[155,2],[155,0],[160,1],[160,2],[160,2],[160,0],[160,0],[160,0],[160,2],[160,2]],
]
#关卡信息