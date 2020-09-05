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
		self.speed=0.4
		self.die=False

	def Draw(self):
		if (self.die==True):
			return

		if (self.hp<=0):
			self.die=True
			return

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

	def Attack(self):
		pass

	def Die(self):
		pass
	
	def Change(self,map):
		pass