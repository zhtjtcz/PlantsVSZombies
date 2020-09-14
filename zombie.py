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

'''
共五种僵尸:普通僵尸,路障僵尸,铁桶僵尸，旗帜僵尸，读报僵尸
'''

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
		self.speed=0.6
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
			self.speed=0.3
		else:
			if (self.sit=='Walk'):
				self.slow=False
				self.speed=0.6
		
		#冰冻特效判断

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
					self.speed=0.6
					return
				continue
			if (pla.pos[0]!=self.line):
				continue
			if (pla.dic==Plant_dic[6]):
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
				#啃食植物
			
		if (flag==False and self.sit=='Attack'):
			self.sit='Walk'
			self.picsit=1
			self.fps=1
			self.pic_sum=self.dic[self.sit]
			self.speed=0.6
		#不再啃食,恢复行走状态

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
		#死亡特效,僵尸头部与身体分开单独绘制

	def Change(self,map):
		for pla in map:
			if (pla.hp<=0):
				x=Coordinate_origin[1]+(pla.pos[1]-1)*Block_size_width
				if (x<=self.pos and x+5>=self.pos and self.sit=='Attack'):
					self.sit='Walk'
					self.picsit=1
					self.fps=1
					self.pic_sum=self.dic[self.sit]
					self.speed=0.6
					return
				continue
# 普通僵尸

class ConeheadZombie():
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
		self.speed=0.6
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

		if (self.hp<=10):
			if (self.sit=='Walk'):
				self.sit='Walk2'
			if (self.sit=='Attack'):
				self.sit='Attack2'
		#判断头上路障是否还在

		if (self.slow==True and self.sit=='Walk' and pygame.time.get_ticks()-self.slow_time<=10000):
			self.speed=0.3
		else:
			if (self.sit=='Walk'):
				self.slow=False
				self.speed=0.6
		
		if (self.slow==True and self.sit=='Walk2' and pygame.time.get_ticks()-self.slow_time<=10000):
			self.speed=0.3
		else:
			if (self.sit=='Walk2'):
				self.slow=False
				self.speed=0.6
		
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
				if (x<=self.pos and x+5>=self.pos and (self.sit=='Attack' or self.sit=='Attack2')):
					if (self.hp>10):
						self.sit='Walk'
					else:
						self.sit='Walk2'
					self.picsit=1
					self.fps=1
					self.pic_sum=self.dic[self.sit]
					self.speed=0.6
					return
				continue
			if (pla.pos[0]!=self.line):
				continue
			if (pla.dic==Plant_dic[6]):
				continue
			x=Coordinate_origin[1]+(pla.pos[1]-1)*Block_size_width
			if (x<=self.pos and x+5>=self.pos):
				flag=True
				if (self.sit=='Attack' or self.sit=='Attack2'):
					pla.hp-=0.2
					continue
				if (self.hp>10):
					self.sit='Attack'
				else:
					self.sit='Attack2'
				self.picsit=1
				self.fps=1
				self.pic_sum=self.dic[self.sit]
				self.speed=0
		if (flag==False and (self.sit=='Attack' or self.sit=='Attack2')):
			if (self.hp>10):
				self.sit='Walk'
			else:
				self.sit='Walk2'
			self.picsit=1
			self.fps=1
			self.pic_sum=self.dic[self.sit]
			self.speed=0.6

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
		for pla in map:
			if (pla.hp<=0):
				x=Coordinate_origin[1]+(pla.pos[1]-1)*Block_size_width
				if (x<=self.pos and x+5>=self.pos and self.sit=='Attack'):
					self.sit='Walk'
					self.picsit=1
					self.fps=1
					self.pic_sum=self.dic[self.sit]
					self.speed=0.6
					return
				continue
# 路障僵尸

class BucketheadZombie():
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
		self.speed=0.6
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

		if (self.hp<=10):
			if (self.sit=='Walk'):
				self.sit='Walk2'
			if (self.sit=='Attack'):
				self.sit='Attack2'
		
		if (self.slow==True and self.sit=='Walk' and pygame.time.get_ticks()-self.slow_time<=10000):
			self.speed=0.3
		else:
			if (self.sit=='Walk'):
				self.slow=False
				self.speed=0.6
		
		if (self.slow==True and self.sit=='Walk2' and pygame.time.get_ticks()-self.slow_time<=10000):
			self.speed=0.3
		else:
			if (self.sit=='Walk2'):
				self.slow=False
				self.speed=0.6
		
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
				if (x<=self.pos and x+5>=self.pos and (self.sit=='Attack' or self.sit=='Attack2')):
					if (self.hp>10):
						self.sit='Walk'
					else:
						self.sit='Walk2'
					self.picsit=1
					self.fps=1
					self.pic_sum=self.dic[self.sit]
					self.speed=0.6
					return
				continue
			if (pla.pos[0]!=self.line):
				continue
			if (pla.dic==Plant_dic[6]):
				continue
			x=Coordinate_origin[1]+(pla.pos[1]-1)*Block_size_width
			if (x<=self.pos and x+5>=self.pos):
				flag=True
				if (self.sit=='Attack' or self.sit=='Attack2'):
					pla.hp-=0.2
					continue
				if (self.hp>10):
					self.sit='Attack'
				else:
					self.sit='Attack2'
				self.picsit=1
				self.fps=1
				self.pic_sum=self.dic[self.sit]
				self.speed=0
		if (flag==False and (self.sit=='Attack' or self.sit=='Attack2')):
			if (self.hp>10):
				self.sit='Walk'
			else:
				self.sit='Walk2'
			self.picsit=1
			self.fps=1
			self.pic_sum=self.dic[self.sit]
			self.speed=0.6

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
		for pla in map:
			if (pla.hp<=0):
				x=Coordinate_origin[1]+(pla.pos[1]-1)*Block_size_width
				if (x<=self.pos and x+5>=self.pos and self.sit=='Attack'):
					self.sit='Walk'
					self.picsit=1
					self.fps=1
					self.pic_sum=self.dic[self.sit]
					self.speed=0.6
					return
				continue
# 铁桶僵尸

class FlagZombie():
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
		self.speed=0.6
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

		self.pic_sum=self.dic[self.sit]

		if (self.slow==True and self.sit=='Walk' and pygame.time.get_ticks()-self.slow_time<=10000):
			self.speed=0.3
		else:
			if (self.sit=='Walk'):
				self.slow=False
				self.speed=0.6
		
		#冰冻特效判断

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
					self.speed=0.6
					return
				continue
			if (pla.pos[0]!=self.line):
				continue
			if (pla.dic==Plant_dic[6]):
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
				#啃食植物
			
		if (flag==False and self.sit=='Attack'):
			self.sit='Walk'
			self.picsit=1
			self.fps=1
			self.pic_sum=self.dic[self.sit]
			self.speed=0.6
		#不再啃食,恢复行走状态

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
		#死亡特效,僵尸头部与身体分开单独绘制

	def Change(self,map):
		for pla in map:
			if (pla.hp<=0):
				x=Coordinate_origin[1]+(pla.pos[1]-1)*Block_size_width
				if (x<=self.pos and x+5>=self.pos and self.sit=='Attack'):
					self.sit='Walk'
					self.picsit=1
					self.fps=1
					self.pic_sum=self.dic[self.sit]
					self.speed=0.6
					return
				continue
# 旗帜僵尸

class PaperZombie():
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
		self.speed=0.6
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

		if (self.hp<=10):
			if (self.sit=='Walk'):
				self.sit='Walk2'
				if (self.picsit>=14):
					self.picsit=14
				self.pic_sum=self.dic[self.sit]
			if (self.sit=='Attack'):
				self.sit='Attack2'
				if (self.picsit==8):
					self.picsit-=1
				self.pic_sum=self.dic[self.sit]
			if (self.sit != 'Attack' and self.sit!='Attack2'):
				self.speed=1.5*0.6

		
		if (self.slow==True and self.sit=='Walk' and pygame.time.get_ticks()-self.slow_time<=10000):
			self.speed=0.3
		else:
			if (self.sit=='Walk'):
				self.slow=False
				self.speed=0.6*1.5
		
		if (self.slow==True and self.sit=='Walk2' and pygame.time.get_ticks()-self.slow_time<=10000):
			self.speed=0.3*1.5
		else:
			if (self.sit=='Walk2'):
				self.slow=False
				self.speed=0.6*1.5
		
		self.pic_sum=self.dic[self.sit]
		

		img=pygame.image.load(self.path+'\\'+self.sit+'\\'+str(self.picsit)+'.png').convert()
		img.set_colorkey(WHITE)
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
				if (x<=self.pos and x+5>=self.pos and (self.sit=='Attack' or self.sit=='Attack2')):
					if (self.hp>10):
						self.sit='Walk'
					else:
						self.sit='Walk2'
					self.picsit=1
					self.fps=1
					self.pic_sum=self.dic[self.sit]
					self.speed=0.6
					return
				continue
			if (pla.pos[0]!=self.line):
				continue
			if (pla.dic==Plant_dic[6]):
				continue
			x=Coordinate_origin[1]+(pla.pos[1]-1)*Block_size_width
			if (x<=self.pos and x+5>=self.pos):
				flag=True
				if (self.sit=='Attack' or self.sit=='Attack2'):
					pla.hp-=0.2
					continue
				if (self.hp>10):
					self.sit='Attack'
				else:
					self.sit='Attack2'
				self.picsit=1
				self.fps=1
				self.pic_sum=self.dic[self.sit]
				self.speed=0
		if (flag==False and (self.sit=='Attack' or self.sit=='Attack2')):
			if (self.hp>10):
				self.sit='Walk'
			else:
				self.sit='Walk2'
			self.picsit=1
			self.fps=1
			self.pic_sum=self.dic[self.sit]
			self.speed=0.6

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
		for pla in map:
			if (pla.hp<=0):
				x=Coordinate_origin[1]+(pla.pos[1]-1)*Block_size_width
				if (x<=self.pos and x+5>=self.pos and self.sit=='Attack'):
					self.sit='Walk'
					self.picsit=1
					self.fps=1
					self.pic_sum=self.dic[self.sit]
					self.speed=0.6
					return
				continue
# 读报僵尸