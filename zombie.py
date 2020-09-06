from setting import *
import pygame
import random

class NolMal_Zombie():
	def __init__(self,scr,id,line):
		self.picsit=1
		self.fps=1
		self.pos=Zom_pos
		self.line=line
		self.screen=scr
		self.hp=Zombie_hp[id]
		self.dic=Zombie_dic[id]
		self.path=Zombie_path[id]
		self.sit='Walk'
		self.dic=Zombie_dic[id]
		self.pic_sum=self.dic[self.sit]
		self.slow=False
		self.slow_time=0
		self.speed=0.4
		self.die=False

		self.head_pic=1
		self.head_fps=1
		self.die_fps=1
		self.die_pic=1
		self.body_pic=1

	def Draw(self):
		if (self.die==True):
			return

		if (self.hp<=0 and self.sit!='WithoutHead'):
			self.sit='WithoutHead'

		if (self.hp<=0):
			self.Die()
			return			

		if (self.slow==True and self.sit=='Walk' and pygame.time.get_ticks()-self.slow_time<=10000):
			self.speed=0.2
		else:
			if (self.sit=='Walk'):
				self.slow=False
				self.speed=0.4
		
		img=pygame.image.load(self.path+'\\'+self.sit+'\\'+str(self.picsit)+'.png')
		self.screen.blit(img,(self.pos,115+(self.line-1)*Block_size_height))

		self.fps+=1
		self.pos-=self.speed
		if (self.fps>=Zombie_Move_FPS):
			self.fps=1
			self.picsit+=1
			if (self.picsit>self.pic_sum):
				self.picsit=1

	def Event(self,map):
		if (self.die==True):
			return
		if (self.hp<=0):
			return
		
		flag=False

		for pla in map:
			if (pla.hp<=0):
				x=Coordinate_origin[1]+(pla.pos[1]-1)*Block_size_width
				if (x<=self.pos and x+5>=self.pos and self.sit=='Attack'):
					self.sit='Walk'
					self.picsit=1
					self.fps=1
					self.pic_sum=self.dic[self.sit]
					self.speed=0.4
					return
				continue
			if (pla.pos[0]!=self.line):
				continue
			
			x=Coordinate_origin[1]+(pla.pos[1]-1)*Block_size_width
			if (x<=self.pos and x+5>=self.pos):
				flag=True
				if (self.sit=='Attack'):
					pla.hp-=0.2
					continue
				self.sit='Attack'
				self.picsit=1
				self.fps=1
				self.pic_sum=self.dic[self.sit]
				self.speed=0
		if (flag==False and self.sit=='Attack'):
			self.sit='Walk'
			self.picsit=1
			self.fps=1
			self.pic_sum=self.dic[self.sit]
			self.speed=0.4

	def Die(self):
		if (self.head_pic!=-1):
			img=pygame.image.load('Picture\Zombies\Zom1\WithoutHead\\'+str(self.head_pic)+'.png')
			self.screen.blit(img,(self.pos,115+(self.line-1)*Block_size_height))

			img=pygame.image.load('Picture\Zombies\Zom1\LostHead\\'+str(self.head_pic)+'.png')
			self.screen.blit(img,(self.pos+60,115+(self.line-1)*Block_size_height))
			self.pos-=self.speed
			self.head_fps+=1

			if (self.head_fps>=Zombie_Move_FPS):
				self.head_fps=1
				self.head_pic+=1
			if (self.head_pic>12):
				self.head_pic=-1
				self.head_fps=1
		else:
			img=pygame.image.load('Picture\Zombies\Zom1\Die\\'+str(self.body_pic)+'.png')
			self.screen.blit(img,(self.pos,115+(self.line-1)*Block_size_height))
			self.head_fps+=1
			if (self.head_fps>=Zombie_Move_FPS):
				self.head_fps=1
				self.body_pic+=1
			if (self.body_pic>10):
				self.die=True

	def Change(self,map):
		pass