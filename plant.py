from setting import *
import pygame
import random

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

	def Draw(self):
		a=[]
		b=[]
		for sun in self.sunlist:
			if (pygame.time.get_ticks() - sun[4] >= 15000):
				continue
			a.append(sun)
			pic=pygame.image.load(self.path+str(sun[2])+'.png')
			self.screen.blit(pic,(sun[0],sun[1]))
			if (sun[1]<=450 and sun[5]>=1):
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
			self.time_list.append(0)

	def Draw(self):
		for i in self.card_list:
			img=pygame.image.load(self.path+str(i+1)+'.png')
			
			gray=pygame.Surface((Card_scale[0],Card_scale[1]+5),flags=0,depth=32)
			gray.set_alpha(100)

			self.screen.blit(img,(Card_pos[0]+i*Card_size,Card_pos[1]))
			self.screen.blit(gray,(Card_pos[0]+i*Card_size,Card_pos[1]))
			self.screen.blit(gray,(Card_pos[0]+i*Card_size,Card_pos[1]))

	def Choose(self,click,sunsum):
		if (sunsum<=0):
			return
		pos=( int(round(click[0])),int(round(click[1])) )
		for i in range(len(self.card_list)):
			if (self.time_list[i]>0):
				continue
			if (sunsum<self.cost_list[i]):
				continue
			if (0<= pos[0]-(Card_pos[0]+i*Card_size)<=Card_Width and 0<=pos[1]-Card_pos[1]<=Card_Height):
				self.select=self.card_list[i]
		print(self.select)

	def Put(self,click):
		pos=( int(round(click[0])),int(round(click[1])) )

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
		self.screen.blit(img,(self.pos,Coordinate_origin[1]+Block_size_height*(self.line)))
		if (self.id!=3):
			self.pos+=self.speed
		if (self.id==3):
			self.sit+=1
			if (self.sit==2):
				self.exist=False

	def Attack(self,zombie):
		if (self.id==3):
			return
		where=INF
		for zom in zombie:
			if (zom.hp<=0):
				continue
			if (self.line!=zom.line):
				continue
			if (abs(self.pos-zom.pos)<=30):
				where=min(where,zom.pos)
		
		if (where!=INF):
			for zom in zombie:
				if (zom.hp<=0):
					continue
				if (self.line!=zom.line):
					continue
				if (zom.pos==where):
					zom.hp-=1
					self.id=3
					self.pos+=60
					return

	'''
	有盲区,有待修正
	'''

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
	
	def Draw(self):
		img=pygame.image.load(self.dic+str(self.sit)+'.png')
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
		if (pygame.time.get_ticks()-self.time >= self.cd):
			a.sunlist.append([self.pic_pos[0]+10,self.pic_pos[1]+10,1,1,pygame.time.get_ticks(),0])
			self.time=pygame.time.get_ticks()

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

	def Event(self,a,bulllist,zomlist):
		if (self.hp<=0):
			return
		if (pygame.time.get_ticks()-self.time <= self.cd):
			return
		for zom in zomlist:
			if (self.pos[0]!=zom.line):
				continue
			if (zom.die==True):
				continue
			bulllist.append(Bullet(self.screen,self.pos[0],Coordinate_origin[1]+self.pos[1]*Block_size_width,1))
			self.time=pygame.time.get_ticks()
			return

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

	def Event(self,a,bulllist,zomlist):
		if (self.hp<=0):
			return
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