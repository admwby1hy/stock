# -*- coding: cp936 -*-

#!/usr/bin/python

import struct

class TStock:
	def getdata(self,gpdm):
		"""��ȡ�������ݣ�gpdm---��Ʊ����"""
		sFormat = 'lllllfll'
		sPath = ''
		#sFile = 'sz002163.day'
		sFile = 'sz'+gpdm+'.day'
		data=[]
		f = open(sPath+sFile,'rb')
		q = f.read(32)
		while q<>'':
			data.append(struct.unpack(sFormat,q))
			q = f.read(32)
		f.close()
		return data
	
	def getnumdate(self,data):
		"""��Ʊ��������"""
		return len(data)
	
	def getMaxMindata(self,data,nstart,nend):
		"""����nstart,nend�������ֵ����Сֵ"""
		i_max = data[nstart][2]
		i_min = data[nstart][3]
		i_maxVol = data[nstart][6]
		for i in range(nstart,nend):
			if data[i][2]>i_max:
				i_max = data[i][2]
			if data[i][3]<i_min:
				i_min = data[i][3]
			if data[i][6]>i_maxVol:
				i_maxVol = data[i][6]
		return (i_max,i_min,i_maxVol)
		
if __name__=="__main__":
	gpdm = '002163'
	q = TStock()
	Cdata = q.getdata(gpdm)
	num = q.getnumdate(Cdata)
	ff = q.getMaxMindata(Cdata,1,42)
	print Cdata