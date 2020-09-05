import pygame
import os
from setting import *
from time import *
from plant import *
from zombie import *
from pygame.locals import *

class GameControl():
	def __init__(self):
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
		self.card=Card(self.screen,[0,1,2])
		self.map=[[-1 for i in range(9)] for i in range(5)]
		self.plant=[]
		self.zombies=[]
		self.bullet_list=[]
		
		self.time=pygame.time.get_ticks()

		'''
		background_img=pygame.image.load('Picture\BackGround\Day.jpg')
		self.screen.blit(background_img,(0,0))
		self.all_sprites.update()
		self.all_sprites.draw(self.screen)
		pygame.display.flip()
		'''
	# Page initialization

	'''
	def Draw_Zombie():

	def Draw_Bullets():
	'''

	def Play_BackGround_Music(self):
		pygame.mixer.music.load('Music\Grasswalk.mp3')
		pygame.mixer.music.play(-1,0)

	def blit_alpha(self,source,location,position,val):
		x=location[0]
		y=location[1]
		temp = pygame.Surface((source.get_width(),source.get_height())).convert()
		temp.blit(self.screen,(-position[0],-position[1]))
		temp.blit(source,location)
		temp.set_alpha(val)
		self.screen.blit(temp,position)

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
		pos=(Coordinate_origin[0]+Block_size_width*x,Coordinate_origin[1]+Block_size_height*y)
		rect=img.get_rect()

		self.blit_alpha(img,rect,pos,150)

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
		self.card.select=-1
		self.sun.sum-=self.card.cost_list[self.map[y][x]]
		if (self.map[y][x]==0):
			self.plant.append(Sunflower(self.screen,0,(y,x)))
		elif (self.map[y][x]==1):
			self.plant.append(PeaShooter(self.screen,1,(y,x)))
		elif (self.map[y][x]==2):
			self.plant.append(WallNut(self.screen,2,(y,x)))

		'''
		植物名称与ID不符,有待修正
		'''
	
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
			pla.Event(self.sun,self.bullet_list,self.zombies)
		self.plant=[]
		for pla in a:
			self.plant.append(pla)

	def BulletDraw(self):
		a=[]
		for bull in self.bullet_list:
			if (bull.exist==False):
				continue
			bull.Draw()
			a.append(bull)
		self.bullet_list=[]
		for bull in a:
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
	
	def CreateZom(self):
		if (pygame.time.get_ticks() - self.time <= 10000):
			return
		self.zombies.append(NolMal_Zombie(self.screen,0,random.randint(0,4)))
		self.time=pygame.time.get_ticks()
	'''
	将被覆盖
	'''

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

	def Test(self):
		bgp=pygame.image.load('Picture\BackGround\Day.png')
		cd=pygame.image.load('Picture\BackGround\SeedBank.png')
		card1=pygame.image.load('Picture\Cards\\'+'1.png')
		card1=pygame.transform.scale(card1,Card_scale)

		card2=pygame.image.load('Picture\Cards\\'+'2.png')
		card2=pygame.transform.scale(card2,Card_scale)
		self.Play_BackGround_Music()

		while 1:
			for event in pygame.event.get():
				if (event.type==pygame.QUIT):
					exit()
			
			self.screen.blit(bgp,(0,0))
			self.screen.blit(cd,(0,0))
			self.card.Draw()

			font=pygame.font.SysFont(None,22)
			text=font.render(str(self.sun.sum),True,BLACK)
			self.screen.blit(text,Sun_Pos)

			#预处理阶段

			self.Mousedraw()
			self.PlantDraw()
			self.PlantEvent()

			self.BulletDraw()
			self.BulletEvent()

			self.CreateZom()
			self.ZomDraw()
			self.ZomEvent()

			self.sun.Appear()
			self.sun.Draw()
			
			pygame.display.flip()
			# 事件发生阶段
			
			if event.type == pygame.MOUSEBUTTONUP:
				print(event.pos,self.card.select)
				if (self.card.select!=-1):
					self.SetPlant(pygame.mouse.get_pos())
				self.sun.Pick(pygame.mouse.get_pos())
				self.card.Choose(pygame.mouse.get_pos(),self.sun.sum)
				
				#sleep(0.001)

			self.clock.tick(Fps)
			# 交互阶段
	
	def Run(self):
		self.Test()
		pygame.quit()