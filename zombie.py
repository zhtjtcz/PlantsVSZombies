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
			return

		img=pygame.image.load(self.path+'\\'+self.sit+'\\'+str(self.picsit)+'.png')
		self.screen.blit(img,(self.pos,95+(self.line-1)*Block_size_height))
		if (self.line>4):
			print("!!!")
		self.fps+=1
		self.pos-=self.speed
		if (self.fps>=Zombie_Move_FPS):
			self.fps=1
			self.picsit+=1
			if (self.picsit>self.pic_sum):
				self.picsit=1
	
	def Attack(self):
		pass

	def Die(self):
		pass
	
	def Change(self,map):
		pass