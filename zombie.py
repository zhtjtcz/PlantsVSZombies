from setting import *
import pygame
import random

class NolMal_Zombie():
	def __init__(self,scr,id,line):
		self.picsit=1
		self.fps=1
		self.pos=CreateZom
		self.line=line
		self.screen=scr
		self.hp=Zombie_hp[id]
		self.dic=Zombie_dic[id]
		self.path=Zombie_path[id]
		self.sit='Walk'
		self.dic=Zombie_dic[id]
		self.pic_sum=self.dic[self.sit]
		self.slow=False
		self.speed=0.8
		self.die=False

	def Draw(self):
		if (self.die==True):
			return
		if (self.hp<=0):
			return

		img=pygame.image.load(self.path+'\\'+self.sit+str(self.picsit)+'.png')
		self.screen.blit(img,(self.pos,self.line))
		self.fps+=1
		self.pos-=self.speed
		if (self.fps>=Zombie_Move_FPS):
			self.fps=1
			self.sit+=1
			if (self.sit>self.pic_sum):
				self.sit=1
	
	def Attack(self):
		pass

	def Die(self):
		pass
	
	def Change(self,map):
		pass