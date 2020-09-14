import pygame
import os
from setting import *
from time import *
from plant import *
from zombie import *
from pygame.locals import *
import sys
import time
import threading
import psutil
import subprocess
from multiprocessing import Process
from PIL import Image, ImageTk

class Menu():
	def __init__(self):
		pygame.init()
		pygame.mixer.init()
		pygame.display.set_caption("Plant VS Zombies")
		icon=pygame.image.load('Picture\Others\Flower.ico')
		icon.set_colorkey((0,0,0))
		pygame.display.set_icon(icon)
		self.screen=pygame.display.set_mode((Screen_Width, Screen_Height))
		self.clock=pygame.time.Clock()
		self.bgp=pygame.image.load('Picture\Menu\MainMenu.png')
		self.adv=pygame.image.load('Picture\Menu\Adventure.png')
		self.sur=pygame.image.load('Picture\Menu\Survive.png')
		'''
		有Warning
		'''

	def Click(self,click):
		pos=( int(round(click[0])),int(round(click[1])) )
		rect1=self.adv.get_rect()
		rect2=self.sur.get_rect()
		if (460<=pos[0]<=460+rect1[2] and 60<=pos[1]<=60+rect1[3]):
			return 1
		if (480<=pos[0]<=480+rect2[2] and 180<=pos[1]<=180+rect2[3]):
			return 2
		return 0

	def Run(self):
		self.screen.blit(self.bgp,(0,0))
		self.screen.blit(self.adv,(460,60))
		self.screen.blit(self.sur,(480,180))
		pygame.display.flip()
		while 1:
			for event in pygame.event.get():
				if (event.type==pygame.QUIT):
					return
				if event.type == pygame.MOUSEBUTTONUP:
					x=self.Click(pygame.mouse.get_pos())
					if (x>0):
						return	x
			self.clock.tick(Fps)
'''
游戏初始页面
'''

class GameControl():
	def __init__(self,mode):
		pygame.init()
		pygame.mixer.init()
		pygame.display.set_caption("Plant VS Zombies")
		icon=pygame.image.load('Picture\Others\Flower.ico')
		icon.set_colorkey((0,0,0))
		pygame.display.set_icon(icon)
		#图标无法设置为透明

		self.screen=pygame.display.set_mode((Screen_Width, Screen_Height))
		self.all_sprites=pygame.sprite.Group()
		self.clock=pygame.time.Clock()
		self.sun=Sun(self.screen)
		if (mode==1):
			self.sun.sum=50
		else:
			self.sun.sum=3000
		
		File=open('info.in','r')
		self.level=int(File.readline())
		File.close()

		self.zomid=0

		self.mode=mode
		self.card=Card(self.screen,[])
		self.map=[[-1 for i in range(9)] for i in range(5)]
		self.plant=[]
		self.zombies=[]
		self.bullet_list=[]
		self.car=Car(self.screen)
		self.time=pygame.time.get_ticks()

	# Page initialization

	def Play_BackGround_Music(self):
		pygame.mixer.music.load('Music\Grasswalk.mp3')
		pygame.mixer.music.play(-1,0)
	#播放BGM

	def blit_alpha(self,source,location,position,val):
		x=location[0]
		y=location[1]
		temp = pygame.Surface((source.get_width(),source.get_height())).convert()
		temp.blit(self.screen,(-position[0],-position[1]))
		temp.blit(source,location)
		temp.set_alpha(val)
		self.screen.blit(temp,position)
	#将一个图片变为半透明

	def Mousedraw(self):
		if self.card.select==-1:
			return
		
		now=pygame.mouse.get_pos()
		pos=( int(round(now[0])),int(round(now[1])) )
		x=(pos[0]-Coordinate_origin[0])//Block_size_width
		y=(pos[1]-Coordinate_origin[1])//Block_size_height
		
		if (x<0 or x>8 or y<0 or y>4):
			return
		if (self.map[y][x]!=-1):
			return
		
		img=pygame.image.load('Picture\Plants\Special\\'+str(self.card.select)+'.png').convert_alpha()
		img.set_colorkey(WHITE)
		pos=(Coordinate_origin[0]+Block_size_width*x,Coordinate_origin[1]+Block_size_height*y)
		rect=img.get_rect()
		if (self.card.select==7):
			pos=(pos[0],pos[1]-20)
		if (self.card.select==6):
			pos=(pos[0],pos[1]+Block_size_height*0.5)
		self.blit_alpha(img,rect,pos,150)
		#透明植物绘制

	def SetPlant(self,click):
		pos=( int(round(click[0])),int(round(click[1])) )
		x=(pos[0]-Coordinate_origin[0])//Block_size_width
		y=(pos[1]-Coordinate_origin[1])//Block_size_height
		
		if (x<0 or x>8 or y<0 or y>4):
			self.card.select=-1
			return
		if (self.map[y][x]!=-1):
			self.card.select=-1
			return
		self.map[y][x]=self.card.select
		self.card.Put(self.card.select)
		self.card.select=-1
		self.sun.sum-=self.card.cost_list[self.card.card_list.index(self.map[y][x])]
		if (self.map[y][x]==0):
			self.plant.append(Sunflower(self.screen,0,(y,x)))
		elif (self.map[y][x]==1):
			self.plant.append(PeaShooter(self.screen,1,(y,x)))
		elif (self.map[y][x]==2):
			self.plant.append(WallNut(self.screen,2,(y,x)))
		elif (self.map[y][x]==3):
			self.plant.append(SnowPea(self.screen,3,(y,x)))
		elif (self.map[y][x]==4):
			self.plant.append(RepeaterPea(self.screen,4,(y,x)))
		elif (self.map[y][x]==5):
			self.plant.append(PotatoMine(self.screen,5,(y,x)))
		elif (self.map[y][x]==6):
			self.plant.append(Spikeweed(self.screen,6,(y,x)))
		elif (self.map[y][x]==7):
			self.plant.append(Chomper(self.screen,7,(y,x)))	
		#安放植物
	
	def PlantDraw(self):
		a=[]
		for pla in self.plant:
			if (pla.hp<=0):
				self.map[pla.pos[0]][pla.pos[1]]=-1
				continue
			a.append(pla)
			pla.Draw()

		self.plant=[]
		for pla in a:
			self.plant.append(pla)
	
	def PlantEvent(self):
		a=[]
		for pla in self.plant:
			if (pla.hp<=0):
				self.map[pla.pos[0]][pla.pos[1]]=-1
				continue
			a.append(pla)
			pla.Event(self.sun,
					self.bullet_list,
					self.zombies)

		self.plant=[]
		for pla in a:
			if (pla.hp>0):
				self.plant.append(pla)
	#植物事件判定
	#攻击与特殊事件

	def BulletDraw(self):
		a=[]
		for bull in self.bullet_list:
			if (bull.exist==False):
				continue
			bull.Draw()
			a.append(bull)
		self.bullet_list=[]
		for bull in a:
			if (bull.exist==True):
				self.bullet_list.append(bull)

	def BulletEvent(self):
		a=[]
		for bull in self.bullet_list:
			if (bull.exist==False):
				continue
			bull.Attack(self.zombies)
			a.append(bull)
		self.bullet_list=[]
		for bull in a:
			self.bullet_list.append(bull)
		#子弹判定

	def CreateZom(self):
		if (self.mode==1):
			if (self.zomid>=len(Zom_create[self.level])):
				return
			if ((pygame.time.get_ticks() - self.time)/1000>= Zom_create[self.level][self.zomid][0]):
				if (Zom_create[self.level][self.zomid][1]==0):
					self.zombies.append(NolMal_Zombie(self.screen,0,random.randint(0,4)))	
				elif (Zom_create[self.level][self.zomid][1]==1):
					self.zombies.append(ConeheadZombie(self.screen,1,random.randint(0,4)))	
				else:
					self.zombies.append(BucketheadZombie(self.screen,2,random.randint(0,4)))	
				self.zomid+=1
		else:
			if (pygame.time.get_ticks() - self.time>=5000):
				self.time=pygame.time.get_ticks()
				x=random.randint(0,4)
				if (x==0):
					self.zombies.append(NolMal_Zombie(self.screen,0,random.randint(0,4)))	
				elif (x==1):
					self.zombies.append(ConeheadZombie(self.screen,1,random.randint(0,4)))	
				elif (x==2):
					self.zombies.append(BucketheadZombie(self.screen,2,random.randint(0,4)))
				elif (x==3):
					self.zombies.append(FlagZombie(self.screen,3,random.randint(0,4)))
				else:
					self.zombies.append(PaperZombie(self.screen,4,random.randint(0,4)))
	#根据关卡信息生成僵尸

	def ZomDraw(self):
		a=[]
		for zom in self.zombies:
			if (zom.die==True):
				continue
			zom.Draw()
			a.append(zom)
		self.zombies=[]
		for zom in a:
			self.zombies.append(zom)
		
	def ZomEvent(self):
		a=[]
		for zom in self.zombies:
			if (zom.die==True):
				continue
			zom.Event(self.plant)
			a.append(zom)
		self.zombies=[]
		for zom in a:
			self.zombies.append(zom)
	#僵尸事件判定

	def SelectDraw(self,screen,lis):
		bgp=pygame.image.load('Picture\BackGround\Day.png')
		cd=pygame.image.load('Picture\BackGround\SeedBank.png')
		screen.blit(bgp,(0,0))
		screen.blit(cd,(0,0))

		board=pygame.image.load('Picture\Menu\Board.png')
		screen.blit(board,(0,87))
		
		if (len(lis)==6):
			img=pygame.image.load('Picture\Menu\Begin.png')
			screen.blit(img,(156,547))
		
		for i in range(len(lis)):
			img=pygame.image.load('Picture\Cards\\'+str(lis[i]+1)+'.png')
			screen.blit(img,(Card_pos[0]+i*Card_size,Card_pos[1]))
			#rec=img.get_rect()
			#print(rec[2],rec[3])

		gray=pygame.Surface((Card_scale[0]-2,Card_scale[1]-3),flags=0,depth=32)
		gray.set_alpha(100)
		for i in range(8):
			img=pygame.image.load('Picture\Cards\\'+str(i+1)+'.png')
			img=pygame.transform.scale(img,(int(Card_scale[0]*0.95),int(Card_scale[1]*0.95)))
			screen.blit(img,(Card_pos[0]-60+i*(Card_size-7),120+Card_pos[1]))
			if (i in lis):
				screen.blit(gray,(Card_pos[0]-60+i*(Card_size-7),120+Card_pos[1]))
		pygame.display.flip()
		#绘制卡片槽

	def BeginGame(self,lis):
		if (len(lis)<6):
			return False
		click=pygame.mouse.get_pos()
		pos=( int(round(click[0])),int(round(click[1])) )
		if (156<=pos[0]<=390 and 547<=pos[1]<=700):
			return True
		return False

	def SelectPlant(self,lis,click):
		a=[]
		pos=( int(round(click[0])),int(round(click[1])) )
		for i in range(len(lis)):
			x=Card_pos[0]+i*Card_size
			y=Card_pos[1]
			if (x<=pos[0]<=x+Card_size and y<=pos[1]<=y+Card_scale[1]):
				for j in range(len(lis)):
					if (j!=i):
						a.append(lis[j])
				return a
		if (len(lis)>=6):
			return lis
		for i in range(8):
			if (i in lis):
				continue
			x=Card_pos[0]-60+i*(Card_size-7)
			y=120+Card_pos[1]
			if (x<=pos[0]<=x+Card_size-7 and y<=pos[1]<=y+Card_scale[1]):
				for j in lis:
					a.append(j)
				a.append(i)
				return a
		return lis

	def Select(self):
		screen=pygame.display.set_mode((Screen_Width, Screen_Height))
		plants=[]

		while 1:
			self.SelectDraw(screen,plants)
			for event in pygame.event.get():
				if (event.type==pygame.QUIT):
					return plants
				if event.type == pygame.MOUSEBUTTONUP:
					if (self.BeginGame(plants)):
						return plants
					a=self.SelectPlant(plants,pygame.mouse.get_pos())
					plants=[]
					for i in a:
						plants.append(i)
	#游戏开始时选择植物

	def WinCheck(self):
		if (self.mode==2):
			return -1
		if (self.zomid >= len(Zom_create[self.level]) and len(self.zombies)==0):
			return 1
		for zom in self.zombies:
			if (zom.hp<=0):
				continue
			if (zom.pos<=-90):
				return 0
	#游戏终止判定

	def Test(self):
		bgp=pygame.image.load('Picture\BackGround\Day.png')
		cd=pygame.image.load('Picture\BackGround\SeedBank.png')
		self.Play_BackGround_Music()

		while 1:
			for event in pygame.event.get():
				if (event.type==pygame.QUIT):
					exit()
				if event.type == pygame.MOUSEBUTTONUP:
					if (self.card.select!=-1):
						self.SetPlant(pygame.mouse.get_pos())
					self.sun.Pick(pygame.mouse.get_pos())
					self.card.Choose(pygame.mouse.get_pos(),self.sun.sum)
			
			self.screen.blit(bgp,(0,0))
			self.screen.blit(cd,(0,0))
			self.card.Draw(self.sun.sum)

			
			font=pygame.font.SysFont(None,22)
			text=font.render(str(self.sun.sum),True,BLACK)
			self.screen.blit(text,Sun_Pos)

			#预处理阶段

			self.Mousedraw()
			self.car.Draw()
			self.car.Event(self.zombies)

			self.PlantDraw()
			self.PlantEvent()

			self.CreateZom()
			self.ZomDraw()
			self.ZomEvent()

			self.BulletDraw()
			self.BulletEvent()

			self.sun.Appear()
			self.sun.Draw()

			if (self.WinCheck()==0):
				img=pygame.image.load('Picture\Menu\Lost.png')
				rec=img.get_rect()
				new=pygame.display.set_mode((rec[2],rec[3]))
				new.blit(img,(0,0))
				pygame.display.flip()
				sleep(3)
				return
			elif (self.WinCheck()==1):
				File=open('info.in','w')
				x=self.level+1
				if (x>5):
					x=1
				File.write(str(x))
				File.close()

				img=pygame.image.load('Picture\Menu\Win.png')
				rec=img.get_rect()
				new=pygame.display.set_mode((rec[2],rec[3]))
				new.blit(img,(0,0))
				pygame.display.flip()
				sleep(3)
				return

			pygame.display.flip()
			# 事件发生阶段

			self.clock.tick(Fps)

	def Run(self,plants):
		self.time=pygame.time.get_ticks()
		self.sun.time=pygame.time.get_ticks()
		self.card=Card(self.screen,plants)
		self.Test()
		pygame.quit()