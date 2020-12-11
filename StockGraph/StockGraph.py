# -*- coding: utf-8 -*-

import wx
import getstockdata

class StockGraph(wx.Window):
	"""??Ʊ??ͼ??	"""
	def __init__(self,parent,title):
		print 'window-init'
		wx.Window.__init__(self,parent)
		self.title = title
		self.titleFont = wx.Font(10, wx.SWISS, wx.NORMAL,wx.NORMAL)
		self.kdata = getstockdata.TStock()
		self.stockCode = '000060'
		self.stockName = '?н?????'
		self.cdata = self.kdata.getdata(self.stockCode)
		self.InitBuffer()
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_IDLE,self.OnIdle)
		self.Bind(wx.EVT_CHAR,self.OnKey)
		
	def OnSize(self,evt):
		self.reInitBuffer = True
		#self.InitBuffer()
	
	def OnIdle(self,evt):
		if self.reInitBuffer:
			print 'on idle'
			self.InitPaintBuffer()
			
	def OnPaint(self, evt):
		print 'on paint'
		dc = wx.BufferedPaintDC(self, self.buffer)#1 ʹ?û????????ˢ?´???

	def OnKey(self,evt):
		KeyCode = evt.GetKeyCode()
		if KeyCode == 314:
			self.PressKeyLeft()
		elif KeyCode ==316:
			self.PressKeyRight()
		else:
			print KeyCode
	
	def PressKeyLeft(self):
		dc = wx.ClientDC(self)
		dc.SetFont(self.titleFont)
		dc.SetTextForeground('white')
		dc.SetBrush(wx.Brush('black'))
		dc.SetPen(wx.Pen('white',1))
		if self.IndexCurrent>self.IndexStart:
			dc.SetLogicalFunction(wx.XOR)
			dc.DrawLine(self.rectKLine.left + (self.IndexCurrent-self.IndexStart) * self.Thickness, self.rectKLine.top,self.rectKLine.left + (self.IndexCurrent-self.IndexStart) * self.Thickness,self.rectKVol.bottom)
			self.IndexCurrent = self.IndexCurrent - 1
			dc.DrawLine(self.rectKLine.left + (self.IndexCurrent-self.IndexStart) * self.Thickness, self.rectKLine.top,self.rectKLine.left + (self.IndexCurrent-self.IndexStart) * self.Thickness,self.rectKVol.bottom)
			dc.SetLogicalFunction(wx.COPY)
			dc.DrawRectangle(self.rectAll.left+200, self.rectAll.top+2,400,18)
			dc.DrawText(str(self.cdata[self.IndexCurrent][0])
			    +' ??:'+str(self.cdata[self.IndexCurrent][1])
			    +' ??:'+str(self.cdata[self.IndexCurrent][2])
			    +' ??:'+str(self.cdata[self.IndexCurrent][3])
			    +' ??:'+str(self.cdata[self.IndexCurrent][4])
			    +' ??:'+str(self.cdata[self.IndexCurrent][6])
			    ,self.rectAll.left+200, self.rectAll.top+2)

	def PressKeyRight(self):
		dc = wx.ClientDC(self)
		dc.SetFont(self.titleFont)
		dc.SetTextForeground('white')
		dc.SetBrush(wx.Brush('black'))
		dc.SetPen(wx.Pen('white',1))
		if self.IndexCurrent<self.IndexEnd:
			dc.SetLogicalFunction(wx.XOR)
			dc.DrawLine(self.rectKLine.left + (self.IndexCurrent-self.IndexStart) * self.Thickness, self.rectKLine.top,self.rectKLine.left + (self.IndexCurrent-self.IndexStart) * self.Thickness,self.rectKVol.bottom)
			self.IndexCurrent = self.IndexCurrent + 1
			dc.DrawLine(self.rectKLine.left + (self.IndexCurrent-self.IndexStart) * self.Thickness, self.rectKLine.top,self.rectKLine.left + (self.IndexCurrent-self.IndexStart) * self.Thickness,self.rectKVol.bottom)
			dc.SetLogicalFunction(wx.COPY)
			dc.DrawRectangle(self.rectAll.left+200, self.rectAll.top+2,400,18)
			dc.DrawText(str(self.cdata[self.IndexCurrent][0])
			    +' ??:'+str(self.cdata[self.IndexCurrent][1])
			    +' ??:'+str(self.cdata[self.IndexCurrent][2])
			    +' ??:'+str(self.cdata[self.IndexCurrent][3])
			    +' ??:'+str(self.cdata[self.IndexCurrent][4])
			    +' ??:'+str(self.cdata[self.IndexCurrent][6])
			    ,self.rectAll.left+200, self.rectAll.top+2)

	def InitBuffer(self):
		dw,dh = self.GetClientSize()
		self.buffer = wx.EmptyBitmap(dw,dh)
		dc = wx.BufferedDC(wx.ClientDC(self),self.buffer)
		
	def InitPaintBuffer(self):
		dw,dh = self.GetClientSize()
		self.buffer = wx.EmptyBitmap(dw,dh)
		dc = wx.BufferedDC(wx.ClientDC(self),self.buffer)
		self.reInitBuffer = False
		self.InitData()
		self.DrawGraph(dc)
		
	def InitData(self):
		self.MarginTop        = 40
		self.MarginBottom     = 18
		self.HeightSubtitle   = 15
		self.WidthSubtitle    = 70
		self.WidthParameter   = 100
		self.WidthVertAxis    = 40
		self.HeightDateAxis   = 20
		self.DefaultThickness = 6
		self.Thickness    = self.DefaultThickness
		self.LastsDate    = 0
		self.CurKType     = 0
		self.CurKFormat   = 0
		self.CurKLineMode = 0		
		self.IndexStart   = 0
		self.IndexEnd     = 0
		self.IndexCurrent = 0
		#???ڸ???????????[x1,y1,x2,y2]
		self.ResetClient()
		
	def ResetClient(self):
		dw,dh = self.GetClientSize()
		self.rectAll = wx.Rect(0,0,dw,dh)
		self.rectKLine  = wx.Rect(self.rectAll.left,
		                          self.rectAll.top + self.MarginTop,
		                          self.rectAll.width - self.WidthParameter - self.WidthVertAxis,
		                          (self.rectAll.height - self.MarginTop - self.HeightDateAxis) * 0.60)	#??K?ߴ?????
		self.rectKVol   = wx.Rect(self.rectAll.left,
		                          self.rectKLine.bottom,
		                          self.rectKLine.width,
		                          (self.rectAll.height - self.MarginTop - self.HeightDateAxis) * 0.20)	#?ɽ?????ʾ??
		self.rectTech   = wx.Rect(self.rectAll.left,
		                          self.rectKVol.bottom,
		                          self.rectKLine.width,
		                          (self.rectAll.height - self.MarginTop - self.HeightDateAxis) * 0.20)	#ָ????ʾ??
		self.rectVertAxis  = wx.Rect(self.rectKLine.right,
		                          self.rectAll.top,
		                          self.WidthVertAxis,
		                          self.rectAll.height)	#??ֵ??????
		self.rectReport = wx.Rect(self.rectVertAxis.right,
		                          self.rectAll.top,
		                          self.WidthParameter,
		                          self.rectAll.height)	#?Ҳ౨????
	def DrawGraph(self,dc):
		#dc.SetBackground(wx.Brush('black'))
		dc.SetTextForeground('white')
		dc.SetPen(wx.Pen('red',1))
		dc.SetBrush(wx.Brush('black'))
		dc.DrawRectangleRect(self.rectAll)
		dc.DrawRectangleRect(self.rectVertAxis)
		#dc.DrawText('rectVertAxis',self.rectVertAxis.left + self.rectVertAxis.width/2,self.rectVertAxis.top + self.rectVertAxis.height/2)
		dc.DrawRectangleRect(self.rectKLine)
		#dc.DrawText('rectKline',self.rectKLine.left + self.rectKLine.width/2,self.rectKLine.top + self.rectKLine.height/2)
		dc.DrawRectangleRect(self.rectKVol)
		#dc.DrawText('rectKVol',self.rectKVol.left + self.rectKVol.width/2,self.rectKVol.top + self.rectKVol.height/2)
		dc.DrawRectangleRect(self.rectTech)
		#dc.DrawText('rectTech',self.rectTech.left + self.rectTech.width/2,self.rectTech.top + self.rectTech.height/2)
		self.DrawTitle(dc)
		self.DrawKLine(dc,self.cdata,self.rectKLine,self.rectKVol)
	
	def DrawTitle(self,dc):
		dc.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL,wx.NORMAL))
		dc.SetTextForeground('red')
		dc.DrawText(self.stockCode+' '+self.stockName,5,10)
		
	def DrawKLine(self,dc,data,rKLine,rKVol):
		allDataNumber = len(data)
		NumberCurser = rKLine.width/self.Thickness
		if allDataNumber > NumberCurser:
			xianshi = NumberCurser
		else:
			xianshi = allDataNumber
		KLineWidth = self.Thickness
		#print '??Ʊ????:'+str(allDataNumber),'????ʾ??Ŀ??'+str(NumberCurser),xianshi
		lmax,lmin,lVol = self.kdata.getMaxMindata(data,allDataNumber - xianshi,allDataNumber)
		
		self.IndexStart = allDataNumber - xianshi
		self.IndexEnd = allDataNumber - 1
		self.IndexCurrent = allDataNumber - 1
		
		#???????????ἰ?۸?
		dc.SetPen(wx.Pen('red',1,wx.DOT))
		dc.SetFont(self.titleFont)
		dc.SetTextForeground('white')
		for i in range(1,5):
			dc.DrawLine(rKLine.left,rKLine.top+i*rKLine.height/5,rKLine.right,rKLine.top + i*rKLine.height/5)
			dc.DrawText(str(lmax-i*(lmax-lmin)/5),self.rectVertAxis.left+2,rKLine.top+i*rKLine.height/5-7)
		#??K??
		for i in range(0,xianshi):
			zbOpen = rKLine.top+(lmax-data[self.IndexStart+i][1])*rKLine.height/(lmax-lmin)
			zbHigh = rKLine.top+(lmax-data[self.IndexStart+i][2])*rKLine.height/(lmax-lmin)
			zbLow  = rKLine.top + (lmax - data[self.IndexStart + i][3]) * rKLine.height / (lmax-lmin)
			zbClose= rKLine.top+(lmax-data[self.IndexStart+i][4])*rKLine.height/(lmax-lmin)
			zbVol  = rKVol.top + data[self.IndexStart+i][6]*rKVol.height/lVol
			if zbClose>zbOpen:
				dc.SetPen(wx.Pen("blue", 1))
				dc.SetBrush(wx.Brush("blue"))
				dc.DrawLine(rKLine.left+(KLineWidth-1)/2+i*KLineWidth,zbHigh,rKLine.left+(KLineWidth-1)/2+i*KLineWidth,zbOpen)
				dc.DrawLine(rKLine.left+(KLineWidth-1)/2+i*KLineWidth,zbClose,rKLine.left+(KLineWidth-1)/2+i*KLineWidth,zbLow)
				dc.DrawRectangle(rKLine.left+i*KLineWidth,zbOpen,KLineWidth-1,zbClose-zbOpen)
				dc.DrawRectangle(rKVol.left+i*KLineWidth,zbVol,KLineWidth-1,rKVol.bottom-zbVol)
			elif zbClose<zbOpen:
				dc.SetPen(wx.Pen("red", 1))
				dc.SetBrush(wx.Brush("red"))
				dc.DrawLine(rKLine.left+(KLineWidth-1)/2+i*KLineWidth,zbHigh,rKLine.left+(KLineWidth-1)/2+i*KLineWidth,zbClose)
				dc.DrawLine(rKLine.left+(KLineWidth-1)/2+i*KLineWidth,zbOpen,rKLine.left+(KLineWidth-1)/2+i*KLineWidth,zbLow)
				dc.DrawRectangle(rKLine.left+i*KLineWidth,zbClose,KLineWidth-1,zbOpen-zbClose)
				dc.DrawRectangle(rKVol.left+i*KLineWidth,zbVol,KLineWidth-1,rKVol.bottom-zbVol)
			else:
				dc.SetPen(wx.Pen("white", 1))
				dc.SetBrush(wx.Brush("white"))
				dc.DrawLine(rKLine.left+(KLineWidth-1)/2+i*KLineWidth,zbHigh,rKLine.left+(KLineWidth-1)/2+i*KLineWidth,zbLow)
				dc.DrawLine(rKLine.left+i*KLineWidth,zbOpen,rKLine.left+(i+1)*KLineWidth-1,zbClose)
				dc.DrawRectangle(rKVol.left+i*KLineWidth,zbVol,KLineWidth-1,rKVol.bottom-zbVol)

class TestFrame(wx.Frame):
	def __init__(self):
		print 'TestFrame-init'
		wx.Frame.__init__(self, None, title="Double Buffered Drawing",size=(800,600))
		self.plot = StockGraph(self,'StockGraph')
		statusBar = self.CreateStatusBar()
class App(wx.App):
	def __init__(self,redirect=False,filename=None):
		print "App__init__"
		wx.App.__init__(self,redirect,filename)
		
	def OnInit(self):
		print 'app-oninit'
		self.frm = TestFrame()
		self.frm.Show(True)
		self.SetTopWindow(self.frm)
		return True

if __name__=='__main__':
	app = App(redirect = False)
	app.MainLoop()