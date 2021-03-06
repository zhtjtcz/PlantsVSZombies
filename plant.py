from setting import *
import pygame
import random
import sys
import os
import time
import threading
import psutil
import subprocess
from multiprocessing import Process
from PIL import Image, ImageTk

class Sun():
	def __init__(self,scr):
		self.time=pygame.time.get_ticks()
		self.path='Picture\Others\Sun\\'
		self.sunlist=[]
		self.screen=scr
		self.sum=500
		self.pick_list=[]
		random.seed(a=None)

	def Appear(self):
		if (pygame.time.get_ticks()-self.time<=6000):
			return
		
		self.sunlist.append([random.randint(50,600),80,1,1,pygame.time.get_ticks(),1])
		self.time=pygame.time.get_ticks()
	#阳光生成

	def Draw(self):
		a=[]
		b=[]
		for sun in self.sunlist:
			if (pygame.time.get_ticks() - sun[4] >= 15000):
				continue
			a.append(sun)
			pic=pygame.image.load(self.path+str(sun[2])+'.png')
			self.screen.blit(pic,(sun[0],sun[1]))
			if (sun[1]<=450):
				if (sun[5]>=1):
					sun[1]+=1.6
			
			sun[3]+=1
			if (sun[3]>=Plant_Move_FPS):
				sun[3]=1
				sun[2]+=1
			if (sun[2]>22):
				sun[2]=1

		for sun in self.pick_list:
			if (pygame.time.get_ticks()-sun[5]>=500):
				continue
			b.append(sun)
			deltatime=(pygame.time.get_ticks()-sun[5])/500
			pic=pygame.image.load(self.path+str(sun[2])+'.png')
			self.screen.blit(pic,(sun[0]-deltatime*sun[3],sun[1]-deltatime*sun[4]))

		self.sunlist=[]
		self.pick_list=[]

		for sun in a:
			self.sunlist.append(sun)

		for sun in b:
			self.pick_list.append(sun)

	def Pick(self,click):
		pos=( int(round(click[0])),int(round(click[1])) )
		for sun in self.sunlist:
			if (0<= pos[0]-sun[0] <=70 and 0<= pos[1]-sun[1]<=70):
				self.sum+=25
				sun[4]=-100000
				self.pick_list.append((sun[0],sun[1],sun[2],(sun[0]-50),(sun[1]-50),pygame.time.get_ticks()))
				break
	#阳光拾取
#阳光类

class Card():
	def __init__(self,scr,card_list):
		self.screen=scr
		self.path='Picture\Cards\\'
		self.card_list=[]
		self.cost_list=[]
		self.cd_list=[]
		self.time_list=[]
		self.pic_list=[]
		self.select=-1

		for i in card_list:
			self.card_list.append(i)
			self.cost_list.append(Plant_cost[i])
			self.cd_list.append(Plant_cd[i])
			self.time_list.append(-INF)

	def Draw(self,sunsum):
		for i in range(0,len(self.card_list)):
			img=pygame.image.load(self.path+str(self.card_list[i]+1)+'.png')
			
			gray=pygame.Surface((Card_scale[0],Card_scale[1]+5),flags=0,depth=32)
			gray.set_alpha(100)
			self.screen.blit(img,(Card_pos[0]+i*Card_size,Card_pos[1]))
			
			if (pygame.time.get_ticks()-self.time_list[i]<self.cd_list[i]):
				x=(pygame.time.get_ticks()-self.time_list[i])/self.cd_list[i]
				x=(1-x)
				self.screen.blit(gray,(Card_pos[0]+i*Card_size,Card_pos[1]))

				gray=pygame.Surface((Card_scale[0],int((Card_scale[1]+5)*x)),flags=0,depth=32)
				gray.set_alpha(100)
				self.screen.blit(gray,(Card_pos[0]+i*Card_size,Card_pos[1]))
			else:
				if (sunsum<self.cost_list[i]):
					self.screen.blit(gray,(Card_pos[0]+i*Card_size,Card_pos[1]))

	def Choose(self,click,sunsum):
		if (sunsum<=0):
			return
		pos=( int(round(click[0])),int(round(click[1])) )
		for i in range(len(self.card_list)):
			if (pygame.time.get_ticks()-self.time_list[i]<self.cd_list[i]):
				continue
			if (sunsum<self.cost_list[i]):
				continue
			if (0<= pos[0]-(Card_pos[0]+i*Card_size)<=Card_Width and 0<=pos[1]-Card_pos[1]<=Card_Height):
				self.select=self.card_list[i]

	def Put(self,id):
		for i in range(0,len(self.card_list)):
			if (self.card_list[i]==id):
				self.time_list[i]=pygame.time.get_ticks()
				return
#卡片槽类

class Car():
	def __init__(self,scr):
		self.screen=scr
		self.pos=[]
		self.img=pygame.image.load('Picture\Others\Car.png')
		for i in range(5):
			self.pos.append(Coordinate_origin[0]-65)
		self.sit=[0 for i in range(5)]

	def Draw(self):
		for i in range(5):
			if (self.sit[i]==2):
				continue
			self.screen.blit(self.img,(self.pos[i],Coordinate_origin[1]+i*Block_size_height))
	
	def Event(self,zombies):
		for i in range(5):
			if (self.sit[i]==2):
				continue
			if (self.sit[i]==1):
				for zom in zombies:
					if (zom.line!=i):
						continue
					if (zom.pos<=self.pos[i]+2):
						zom.hp=0
				self.pos[i]+=6.0
			if (self.pos[i]>=800):
				self.sit[i]=2
				continue
			
			for zom in zombies:
				if (i!=zom.line):
					continue
				if (zom.pos<=-70):
					self.sit[i]=1
					return
#小推车类

class Bullet():
	def __init__(self,scr,line,pos,id):
		self.screen=scr
		self.line=line
		self.pos=pos
		self.id=id
		self.speed=8
		self.path='Picture\Bullets\\'
		self.exist=True
		self.sit=0

	def Draw(self):
		if (self.pos>=800):
			self.exist=False
			return
		img=pygame.image.load(self.path+str(self.id)+'.png')
		if (self.id==3):
			self.screen.blit(img,(self.pos+100,Coordinate_origin[1]+Block_size_height*(self.line)))
		else:
			self.screen.blit(img,(self.pos,Coordinate_origin[1]+Block_size_height*(self.line)))
		if (self.id!=3):
			self.pos+=self.speed
		if (self.id==3):
			self.sit+=1
			if (self.sit==2):
				self.exist=False

	def Cha(self,a,b):
		return a[0]*b[1]-a[1]*b[0]

	def Vector(self,a,b):
		return [a[0]-b[0],a[1]-b[1]]

	def Cross(self,zombie):
		pos=[self.pos,Coordinate_origin[1]+Block_size_height*(self.line)]
		r=12
		D=[zombie.pos,Coordinate_origin[1]+Block_size_height*(self.line-0.5)]
		C=[zombie.pos+Block_size_width,Coordinate_origin[1]+Block_size_height*(self.line-0.5)]
		B=[zombie.pos+Block_size_width,Coordinate_origin[1]+Block_size_height*(self.line+0.5)]
		A=[zombie.pos,Coordinate_origin[1]+Block_size_height*(self.line+0.5)]
		if ():
			return True
		else:
			return False

	def Attack(self,zombie):
		if (self.id==3):
			return
		where=INF
		for zom in zombie:
			if (zom.hp<=0):
				continue
			if (self.line!=zom.line):
				continue
			if (abs(self.pos-zom.pos)<=10):
				where=min(where,zom.pos)
		
		if (where!=INF):
			for zom in zombie:
				if (zom.hp<=0):
					continue
				if (self.line!=zom.line):
					continue
				if (zom.pos==where):
					zom.hp-=1
					if (self.id==2):
						zom.slow=True
						zom.slow_time=pygame.time.get_ticks()
					self.id=3
					#self.pos+=60
					return

#子弹类
#共三种豌豆,分别为普通豌豆,寒冰豌豆,爆开的豌豆

class Sunflower():
	def __init__(self,scr,id,pos):
		self.sit=1
		self.fps=1
		self.pos=pos
		self.cd=24000
		self.screen=scr
		self.hp=Plant_hp[id]
		self.dic=Plant_dic[id]
		self.pic_sum=Plant_Picsum[id]
		self.time=pygame.time.get_ticks()-random.randint(0,self.cd)
		self.pic_pos=(Coordinate_origin[0]+Block_size_width*pos[1],Coordinate_origin[1]+Block_size_height*pos[0])
		#参数预处理

	def Draw(self):
		img=pygame.image.load(self.dic+str(self.sit)+'.png')
		self.screen.blit(img,self.pic_pos)
		self.fps+=1
		if (self.fps>=Plant_Move_FPS):
			self.fps=1
			self.sit+=1
			if (self.sit>self.pic_sum):
				self.sit=1
	#绘制图像
	#每一幅图显示固定帧数，以达到动态显示的效果

	def Danger(self,zomlist):
		if (self.hp<=0):
			return
		cnt=0
		for zom in zomlist:
			if (zom.hp<=0):
				continue
			if (zom.die==True):
				continue
			if (zom.pos-self.pic_pos[0]<=50):
				cnt+=1
		while (cnt>=0):
			self.time-=0.02
			cnt-=1

	def Event(self,a,bulllist,zomlist):
		if (self.hp<=0):
			return
		flag=0
		for zom in zomlist:
			if (zom.hp<=0):
				continue
			if (zom.die==True):
				continue
			if (zom.pos-self.pic_pos[0]<=50):
				flag=1
		if (flag>=1):
			self.Danger(zomlist)

		if (pygame.time.get_ticks()-self.time >= self.cd):
			a.sunlist.append([self.pic_pos[0]+10,self.pic_pos[1]+10,1,1,pygame.time.get_ticks(),0])
			self.time=pygame.time.get_ticks()
	#阳光产出判定
#向日葵类

class PeaShooter():
	def __init__(self,scr,id,pos):
		self.sit=1
		self.fps=1
		self.pos=pos
		self.cd=1400
		self.screen=scr
		self.hp=Plant_hp[id]
		self.dic=Plant_dic[id]
		self.pic_sum=Plant_Picsum[id]
		self.time=pygame.time.get_ticks()-1000
		self.pic_pos=(Coordinate_origin[0]+Block_size_width*pos[1],Coordinate_origin[1]+Block_size_height*pos[0])

	def Draw(self):
		img=pygame.image.load(self.dic+str(self.sit)+'.png')
		self.screen.blit(img,self.pic_pos)
		self.fps+=1
		if (self.fps>=Plant_Move_FPS):
			self.fps=1
			self.sit+=1
			if (self.sit>self.pic_sum):
				self.sit=1

	def Danger(self,zomlist):
		if (self.hp<=0):
			return
		cnt=0
		for zom in zomlist:
			if (zom.hp<=0):
				continue
			if (zom.die==True):
				continue
			if (zom.pos-self.pic_pos[0]<=50):
				cnt+=1
		while (cnt>=0):
			self.time-=0.02
			cnt-=1

	def Event(self,a,bulllist,zomlist):
		if (self.hp<=0):
			return
		if (pygame.time.get_ticks()-self.time <= self.cd):
			return
		
		flag=0
		for zom in zomlist:
			if (zom.hp<=0):
				continue
			if (zom.die==True):
				continue
			if (zom.pos-self.pic_pos[0]<=50):
				flag=1
		if (flag>=1):
			self.Danger(zomlist)
		
		for zom in zomlist:
			if (self.pos[0]!=zom.line):
				continue
			if (zom.die==True):
				continue
			bulllist.append(Bullet(self.screen,self.pos[0],Coordinate_origin[1]+self.pos[1]*Block_size_width-5,1))
			self.time=pygame.time.get_ticks()
			return
	#攻击判定
#豌豆射手类

class WallNut():
	def __init__(self,scr,id,pos):
		self.sit=1
		self.fps=1
		self.pos=pos
		self.screen=scr
		self.hp=Plant_hp[id]
		self.dic=Plant_dic[id]
		self.path='Nolmal\\'
		self.pic_sum=Plant_Picsum[id]
		self.pic_pos=(Coordinate_origin[0]+Block_size_width*pos[1],Coordinate_origin[1]+Block_size_height*pos[0])
	
	def Draw(self):
		img=pygame.image.load(self.dic+self.path+str(self.sit)+'.png')
		self.screen.blit(img,self.pic_pos)
		self.fps+=1
		if (self.fps>=Plant_Move_FPS):
			self.fps=1
			self.sit+=1
			if (self.sit>self.pic_sum):
				self.sit=1		

	def Danger(self,zomlist):
		if (self.hp<=0):
			return
		cnt=0
		for zom in zomlist:
			if (zom.hp<=0):
				continue
			if (zom.die==True):
				continue
			if (zom.pos-self.pic_pos[0]<=50):
				cnt+=1
		while (cnt>=0):
			self.hp+=0.002
			cnt-=1

	def Event(self,a,bulllist,zomlist):
		if (self.hp<=0):
			return
				
		flag=0
		for zom in zomlist:
			if (zom.hp<=0):
				continue
			if (zom.die==True):
				continue
			if (zom.pos-self.pic_pos[0]<=50):
				flag=1
		if (flag>=1):
			self.Danger(zomlist)

		if (self.hp<=133 and self.path!='Cracked2\\'):
			self.path='Cracked2\\'
			self.sit=1
			self.fps=1
			self.pic_sum=15
		elif (133<self.hp<=267 and self.path!='Cracked1\\'):
			self.path='Cracked1\\'
			self.sit=1
			self.fps=1
			self.pic_sum=11
	#检测血量并更新图片
#坚果墙类

class SnowPea():
	def __init__(self,scr,id,pos):
		self.sit=1
		self.fps=1
		self.pos=pos
		self.cd=1400
		self.screen=scr
		self.hp=Plant_hp[id]
		self.dic=Plant_dic[id]
		self.pic_sum=Plant_Picsum[id]
		self.time=pygame.time.get_ticks()-1000
		self.pic_pos=(Coordinate_origin[0]+Block_size_width*pos[1],Coordinate_origin[1]+Block_size_height*pos[0])

	def Draw(self):
		img=pygame.image.load(self.dic+str(self.sit)+'.png')
		self.screen.blit(img,self.pic_pos)
		self.fps+=1
		if (self.fps>=Plant_Move_FPS):
			self.fps=1
			self.sit+=1
			if (self.sit>self.pic_sum):
				self.sit=1

	def Danger(self,zomlist):
		if (self.hp<=0):
			return
		cnt=0
		for zom in zomlist:
			if (zom.hp<=0):
				continue
			if (zom.die==True):
				continue
			if (zom.pos-self.pic_pos[0]<=50):
				cnt+=1
		while (cnt>=0):
			self.time-=0.02
			cnt-=1

	def Event(self,a,bulllist,zomlist):
		if (self.hp<=0):
			return
		if (pygame.time.get_ticks()-self.time <= self.cd):
			return
		
		flag=0
		for zom in zomlist:
			if (zom.hp<=0):
				continue
			if (zom.die==True):
				continue
			if (zom.pos-self.pic_pos[0]<=50):
				flag=1
		if (flag>=1):
			self.Danger(zomlist)


		for zom in zomlist:
			if (self.pos[0]!=zom.line):
				continue
			if (zom.die==True):
				continue
			bulllist.append(Bullet(self.screen,self.pos[0],Coordinate_origin[1]+self.pos[1]*Block_size_width-5,2))
			self.time=pygame.time.get_ticks()
			return
#寒冰射手类,基本上同豌豆射手

class RepeaterPea():
	def __init__(self,scr,id,pos):
		self.sit=1
		self.fps=1
		self.pos=pos
		self.cd=1400
		self.screen=scr
		self.hp=Plant_hp[id]
		self.dic=Plant_dic[id]
		self.pic_sum=Plant_Picsum[id]
		self.time=pygame.time.get_ticks()-1000
		self.pic_pos=(Coordinate_origin[0]+Block_size_width*pos[1],Coordinate_origin[1]+Block_size_height*pos[0])

	def Draw(self):
		img=pygame.image.load(self.dic+str(self.sit)+'.png')
		self.screen.blit(img,self.pic_pos)
		self.fps+=1
		if (self.fps>=Plant_Move_FPS):
			self.fps=1
			self.sit+=1
			if (self.sit>self.pic_sum):
				self.sit=1

	def Danger(self,zomlist):
		if (self.hp<=0):
			return
		cnt=0
		for zom in zomlist:
			if (zom.hp<=0):
				continue
			if (zom.die==True):
				continue
			if (zom.pos-self.pic_pos[0]<=50):
				cnt+=1
		while (cnt>=0):
			self.time-=0.02
			cnt-=1

	def Event(self,a,bulllist,zomlist):
		if (self.hp<=0):
			return
		if (pygame.time.get_ticks()-self.time <= self.cd):
			return
		
		flag=0
		for zom in zomlist:
			if (zom.hp<=0):
				continue
			if (zom.die==True):
				continue
			if (zom.pos-self.pic_pos[0]<=50):
				flag=1
		if (flag>=1):
			self.Danger(zomlist)


		for zom in zomlist:
			if (self.pos[0]!=zom.line):
				continue
			if (zom.die==True):
				continue
			bulllist.append(Bullet(self.screen,self.pos[0],Coordinate_origin[1]+self.pos[1]*Block_size_width-5,1))
			bulllist.append(Bullet(self.screen,self.pos[0],Coordinate_origin[1]+self.pos[1]*Block_size_width+25,1))
			self.time=pygame.time.get_ticks()
			return
#双发射手类,同豌豆射手

class PotatoMine():
	def __init__(self,scr,id,pos):
		self.sit=1
		self.fps=1
		self.pos=pos
		self.screen=scr
		self.hp=Plant_hp[id]
		self.dic=Plant_dic[id]
		self.pic_sum=Plant_Picsum[id]
		self.time=pygame.time.get_ticks()
		self.sleep=True
		self.pic_pos=(Coordinate_origin[0]+Block_size_width*pos[1],Coordinate_origin[1]+Block_size_height*pos[0])

	def Draw(self):
		if (pygame.time.get_ticks()-self.time>=15000):
			self.sleep=False

		if (self.sleep==True):
			img=pygame.image.load(self.dic+'sleep\\'+str(self.sit)+'.png').convert()
			img.set_colorkey(WHITE)
			self.screen.blit(img,self.pic_pos)
			return
		
		if (self.sit==-1):
			if (self.fps==36):
				self.hp=-100
				return
			img=pygame.image.load(self.dic+'1.png').convert()
			img.set_colorkey(WHITE)
			self.screen.blit(img,self.pic_pos)
			self.fps+=1
			return
		img=pygame.image.load(self.dic+'Nolmal\\'+str(self.sit)+'.png').convert()
		img.set_colorkey(WHITE)
		self.screen.blit(img,self.pic_pos)
		self.fps+=1
		if (self.fps>=Plant_Move_FPS):
			self.fps=1
			self.sit+=1
			if (self.sit>self.pic_sum):
				self.sit=1

	def Event(self,a,bulllist,zomlist):
		if (self.hp<=0):
			return
		if (self.sleep==True):
			return
		if (self.sit==-1):
			return
		for zom in zomlist:
			if (self.pos[0]!=zom.line):
				continue
			if (zom.die==True):
				continue
			if (self.pic_pos[0]<=zom.pos and self.pic_pos[0]+5>zom.pos):
				self.fps=1
				self.sit=-1
				zom.die=True
				return
	#休眠与爆炸判定
#土豆雷类

class Spikeweed():
	def __init__(self,scr,id,pos):
		self.sit=1
		self.fps=1
		self.pos=pos
		self.screen=scr
		self.hp=Plant_hp[id]
		self.dic=Plant_dic[id]
		self.pic_sum=Plant_Picsum[id]
		self.time=pygame.time.get_ticks()
		self.pic_pos=(Coordinate_origin[0]+Block_size_width*pos[1],Coordinate_origin[1]+Block_size_height*(pos[0]+0.5))

	def Draw(self):
		img=pygame.image.load(self.dic+str(self.sit)+'.png').convert()
		img.set_colorkey(WHITE)
		self.screen.blit(img,self.pic_pos)
		self.fps+=1
		if (self.fps>=Plant_Move_FPS):
			self.fps=1
			self.sit+=1
			if (self.sit>self.pic_sum):
				self.sit=1

	def Event(self,a,bulllist,zomlist):
		if (self.hp<=0):
			return
		if (pygame.time.get_ticks()-self.time<=700):
			return
		self.time=pygame.time.get_ticks()
		for zom in zomlist:
			if (self.pos[0]!=zom.line):
				continue
			if (zom.die==True):
				continue
			if (zom.pos<=self.pic_pos[0] and zom.pos>=self.pic_pos[0]-Block_size_width):
				zom.hp-=1
	#攻击判定,同时具有不可啃食特性
#地刺类

class Chomper():
	def __init__(self,scr,id,pos):
		self.sit=1
		self.fps=1
		self.pos=pos
		self.screen=scr
		self.hp=Plant_hp[id]
		self.dic=Plant_dic[id]
		self.pic_sum=Plant_Picsum[id]
		self.time=pygame.time.get_ticks()
		self.path='Nolmal'
		self.pic_pos=(Coordinate_origin[0]+Block_size_width*pos[1],Coordinate_origin[1]+Block_size_height*pos[0]-20)

	def Draw(self):
		if (self.hp<=0):
			return
		if (self.path=='Eating' and pygame.time.get_ticks()-self.time>=42000):
			self.fps=1
			self.sit=1
			self.path='Nolmal'
		if (self.path=='Attack'):
			img=pygame.image.load(self.dic+self.path+'\\'+str(self.sit)+'.png')
			self.screen.blit(img,self.pic_pos)
			self.fps+=1
			if (self.fps>=3):
				self.fps=1
				self.sit+=1
				if (self.sit>9):
					self.time=pygame.time.get_ticks()
					self.path='Eating'
					self.fps=1
					self.sit=1
					return
		elif (self.path=='Eating'):
			img=pygame.image.load(self.dic+self.path+'\\'+str(self.sit)+'.png')
			self.screen.blit(img,self.pic_pos)
			self.fps+=1
			if (self.fps>=Plant_Move_FPS):
				self.fps=1
				self.sit+=1
				if (self.sit>6):
					self.sit=1
		else:
			img=pygame.image.load(self.dic+self.path+'\\'+str(self.sit)+'.png')
			self.screen.blit(img,self.pic_pos)
			self.fps+=1
			if (self.fps>=Plant_Move_FPS):
				self.fps=1
				self.sit+=1
				if (self.sit>13):
					self.sit=1

	def Event(self,a,bulllist,zomlist):
		if (self.hp<=0):
			return
		if (self.path=='Eating'):
			return
		for zom in zomlist:
			if (self.pos[0]!=zom.line):
				continue
			if (zom.die==True):
				continue
			if (self.pic_pos[0]<=zom.pos and self.pic_pos[0]+5>zom.pos):
				if (self.path=='Attack'):
					if (self.sit>=3):
						zom.die=True
					return
				self.time=pygame.time.get_ticks()
				self.path='Attack'
				self.sit=1
				self.fps=1
				return
	#攻击与咀嚼判定
#大嘴花类