# -*- coding: utf-8 -*-

import urllib,urllib2,urlfetch, re, os, json
from utils import *

#xread('http://ip-api.com/json')

def gibberishAES(string, key=''):
	import ctypes
	def aa(l,s=4):
		a=[]
		for i in range(0,len(l),s):a.append((l[i:i+s]))
		return a

	def j2p(v):return ctypes.c_int(v).value
	def rshift(val, n): return (val % 0x100000000) >> n

	e = 14
	r = 8
	n = False
		
	def f(e):
		try:result=urllib.quote(e)
		except:result=str(e)
		return result
		
	def c(e):
		try:result=urllib.quote(e, safe='~()*!.\'')
		except:result=str(e)
		return result

	def t(e):
		f = [0]*len(e)
		if 16 >len(e):
			r = 16 - len(e)
			f = [r, r, r, r, r, r, r, r, r, r, r, r, r, r, r, r]
		for n in range(len(e)):f[n] = e[n]
		return f

	def o(e):
		n = ""
		for r in len(e):n += ("0" if 16 > e[r] else "") + format(e[r], 'x')
		return n

	def u(e, r):
		c = []
		if not r:e=f(e)
		for n in range(len(e)):c.append(ord(e[n]))
		return c

	def i(n):
		if n==128:e = 10; r = 4
		elif n==192:e = 12;r = 6
		elif n==256:e = 14;r = 8

	def b(e):
		n = []
		for r in range(e):n.append(256)
		return n

	def h(n, f):
		d=[];t= 3 if e >= 12 else 2; i = n + f; d.append(L(i));u=[c for c in d[0]]
		for c in range(1,t):d.append(L(d[c - 1] + i));u+=d[c]
		return {'key': u[0 : 4 * r],'iv': u[4 * r : 4 * r + 16]}

	def a1(e, r=False):
		c = ""
		if (r):
			n = e[15]
			#if n > 16:print "Decryption error: Maybe bad key"
			if 16 != n:
				for f in range(16 - n):c += chr(e[f])
		else:
			for f in range(16):c += chr(e[f])
		return c

	def a(e, r=False):
		if not r:c=''.join(chr(e[f])for f in range(16))
		elif 16!=e[15]:c=''.join(chr(e[f]) for f in range(16-e[15]))
		else:c=''
		return c

	def v(e, r, n, f=''):
		r = S(r); o = len(e) / 16; u = [0]*o
		d=[e[16 * t: 16 * (t + 1)] for t in range(o)]
		for t in range(len(d) - 1,-1,-1):
			u[t] = p(d[t], r)
			u[t] = x(u[t], n) if 0 == t else x(u[t], d[t - 1])
		
		i=''.join(a(u[t]) for t in range(o-1))
		i += a(u[o-1], True)
		return i if f else c(i)

	def s(r, f):
		n = False
		t = M(r, f, 0)
		for c in (1, e + 1 ,1):
			t = g(t)
			t = y(t)
			if e > c:t = k(t)
			t = M(t, f, c)
		return t

	def p(r, f):
		n = True
		t = M(r, f, e)
		for c in range(e - 1,-1,-1):
			t = y(t,n)
			t = g(t,n)
			t = M(t, f, c)
			if c > 0 : t = k(t,n)
		return t

	def g(e,n=True):#OK
		f = D if n else B; c = [0]*16
		for r in range(16):c[r] = f[e[r]]
		return c

	def y(e,n=True):
		f = []
		if n: c = [0, 13, 10, 7, 4, 1, 14, 11, 8, 5, 2, 15, 12, 9, 6, 3] 
		else:c =[0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11]
		for r in range(16):f.append(e[c[r]])
		return f

	def k(e,n=True):
		f = [0]*16
		if (n):
			for r in range(4):
				f[4 * r] = F[e[4 * r]] ^ R[e[1 + 4 * r]] ^ j[e[2 + 4 * r]] ^ z[e[3 + 4 * r]]
				f[1 + 4 * r] = z[e[4 * r]] ^ F[e[1 + 4 * r]] ^ R[e[2 + 4 * r]] ^ j[e[3 + 4 * r]]
				f[2 + 4 * r] = j[e[4 * r]] ^ z[e[1 + 4 * r]] ^ F[e[2 + 4 * r]] ^ R[e[3 + 4 * r]]
				f[3 + 4 * r] = R[e[4 * r]] ^ j[e[1 + 4 * r]] ^ z[e[2 + 4 * r]] ^ F[e[3 + 4 * r]]
		else:
			for r in range(4):
				f[4 * r] = E[e[4 * r]] ^ U[e[1 + 4 * r]] ^ e[2 + 4 * r] ^ e[3 + 4 * r]
				f[1 + 4 * r] = e[4 * r] ^ E[e[1 + 4 * r]] ^ U[e[2 + 4 * r]] ^ e[3 + 4 * r]
				f[2 + 4 * r] = e[4 * r] ^ e[1 + 4 * r] ^ E[e[2 + 4 * r]] ^ U[e[3 + 4 * r]]
				f[3 + 4 * r] = U[e[4 * r]] ^ e[1 + 4 * r] ^ e[2 + 4 * r] ^ E[e[3 + 4 * r]]
		return f	

	def M(e, r, n):#OK
		c = [0]*16
		for f in range(16):c[f] = e[f] ^ r[n][f]
		return c

	def x(e, r):
		f = [0]*16
		for n in  range(16):f[n] = e[n] ^ r[n]
		return f

	def S(n):#r=8;e=14
		o=[[n[4 * f + i] for i in range(4)] for f in range(r)]
		
		for f in range(r,4 * (e + 1)):
			d=[t for t in o[f-1]]
			if 0 == f % r:d = m(w(d)); d[0] ^= K[f / r - 1]
			elif r > 6 and 4 == f % r : d = m(d)
			o.append([o[f - r][t] ^ d[t] for t in range(4)])
		
		u = []
		for f in range(e + 1):
			u.append([])
			for a in range(4):u[f]+=o[4 * f + a]
		return u

	def m(e):
		return [B[e[r]] for r in range(4)]

	def w(e):
		e.insert(4,e[0])
		e.remove(e[4])
		return e

	def A(e, r):return [int(e[n:n+r], 16) for n in range(0,len(e),r)]

	def C(e):
		n=[0]*len(e)
		for r in range(len(e)):n[e[r]] = r
		return n

	def I(e, r):
		f=0
		for n in range(8):
			f = f ^ e if 1 == (1 & r) else f
			e = j2p(283 ^ e << 1) if e > 127 else j2p(e << 1)
			r >>= 1
		return f

	def O(e):
		n = [0]*256
		for r in range(256):n[r] = I(e, r)
		return n

	B = A("637c777bf26b6fc53001672bfed7ab76ca82c97dfa5947f0add4a2af9ca472c0b7fd9326363ff7cc34a5e5f171d8311504c723c31896059a071280e2eb27b27509832c1a1b6e5aa0523bd6b329e32f8453d100ed20fcb15b6acbbe394a4c58cfd0efaafb434d338545f9027f503c9fa851a3408f929d38f5bcb6da2110fff3d2cd0c13ec5f974417c4a77e3d645d197360814fdc222a908846eeb814de5e0bdbe0323a0a4906245cc2d3ac629195e479e7c8376d8dd54ea96c56f4ea657aae08ba78252e1ca6b4c6e8dd741f4bbd8b8a703eb5664803f60e613557b986c11d9ee1f8981169d98e949b1e87e9ce5528df8ca1890dbfe6426841992d0fb054bb16", 2)
	D = C(B)
	K = A("01020408102040801b366cd8ab4d9a2f5ebc63c697356ad4b37dfaefc591", 2)
	E = O(2)
	U = O(3)
	z = O(9)
	R = O(11)
	j = O(13)
	F = O(14)

	def G(e, r, n):
		c = b(8); t = h(u(r, n), c); a = t.key; o = t.iv; d = [83, 97, 108, 116, 101, 100, 95, 95]+c
		e = u(e, n)
		f = l(e, a, o)
		f = d+f
		return T.encode(f)

	def H(e, r, n=''):
		f = decode(e)
		c = f[8 : 16]
		t = h(u(r, n), c)
		a = t['key']
		o = t['iv']
		f = f[16 : len(f)]
		return v(f, a, o, n)

	def decode(r):#OK
		def indexOfchar(n):
			try:a=e.index(r[n])
			except:a=-1
			return a
		
		e="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
		r=r.replace('\n','');f=[];c=[0]*4
		for n in range(0,len(r),4):
			for i in range(len(c)):c[i]=indexOfchar(n+i)
			f.append(j2p(c[0]<<2|c[1]>>4))
			f.append(j2p((15&c[1])<<4|c[2]>>2))
			f.append(j2p((3&c[2])<<6|c[3]))
		return f[0:len(f)-len(f)%16]

	def L(e):
		def r(e, r):return j2p(e << r) | j2p(rshift(e, 32-r))

		def n(e, r):
			c = 2147483648 & e
			t = 2147483648 & r
			n = 1073741824 & e
			f = 1073741824 & r
			a = (1073741823 & e) + (1073741823 & r)
			i = 2147483648^a^c^t
			j = 3221225472^a^c^t
			k = 1073741824^a^c^t
			return j2p(i if n & f else ((j if 1073741824 & a else k) if n | f else a^c^t))		

		def f(e, r, n):return j2p(e & r) | j2p(~e & n)

		def c(e, r, n):return j2p(e & n) | j2p(r & ~n)

		def t(e, r, n):return e ^ r ^ n

		def a(e, r, n):return r ^ (e | ~n)

		def o(e, c, t, a, o, d, u):
			e = n(e, n(n(f(c, t, a), o), u))
			return n(r(e, d), c)

		def d(e, f, t, a, o, d, u):
			e = n(e, n(n(c(f, t, a), o), u))
			return n(r(e, d), f)

		def u(e, f, c, a, o, d, u):
				e = n(e, n(n(t(f, c, a), o), u))
				return n(r(e, d), f)

		def i(e, f, c, t, o, d, u):
			e = n(e, n(n(a(f, c, t), o), u))
			return n(r(e, d), f)

		def b(e):
			n=len(e); f = n + 8; c = (f - f % 64) / 64; t = 16 * (c + 1); a = [0]*t; o = 0
			for d in range(n):r = (d - d % 4) / 4; o = 8 * (d % 4);	a[r] = a[r] | j2p(e[d] << o)
			d+=1
			r = (d - d % 4) / 4
			o = 8 * (d % 4)
			a[r] = a[r] | j2p(128 << o)
			a[t - 2] = j2p(n << 3)
			a[t - 1] = j2p(rshift(n,29))
			return a

		def h(e):
			f = []
			for n in range(4):
				r = j2p(255 & rshift(e, 8 * n))
				f.append(r)
			return f

		m = A("67452301efcdab8998badcfe10325476d76aa478e8c7b756242070dbc1bdceeef57c0faf4787c62aa8304613fd469501698098d88b44f7afffff5bb1895cd7be6b901122fd987193a679438e49b40821f61e2562c040b340265e5a51e9b6c7aad62f105d02441453d8a1e681e7d3fbc821e1cde6c33707d6f4d50d87455a14eda9e3e905fcefa3f8676f02d98d2a4c8afffa39428771f6816d9d6122fde5380ca4beea444bdecfa9f6bb4b60bebfbc70289b7ec6eaa127fad4ef308504881d05d9d4d039e6db99e51fa27cf8c4ac5665f4292244432aff97ab9423a7fc93a039655b59c38f0ccc92ffeff47d85845dd16fa87e4ffe2ce6e0a30143144e0811a1f7537e82bd3af2352ad7d2bbeb86d391", 8)
		S = [];  S = b(e); y = m[0]; k = m[1]; M = m[2]; x = m[3]; l = 0
		for l in range(0,len(S),16):
			v = y
			s = k
			p = M
			g = x
			y = o(y, k, M, x, S[l + 0], 7, m[4])
			x = o(x, y, k, M, S[l + 1], 12, m[5])
			M = o(M, x, y, k, S[l + 2], 17, m[6])
			k = o(k, M, x, y, S[l + 3], 22, m[7])
			y = o(y, k, M, x, S[l + 4], 7, m[8])
			x = o(x, y, k, M, S[l + 5], 12, m[9])
			M = o(M, x, y, k, S[l + 6], 17, m[10])
			k = o(k, M, x, y, S[l + 7], 22, m[11])
			y = o(y, k, M, x, S[l + 8], 7, m[12])
			x = o(x, y, k, M, S[l + 9], 12, m[13])
			M = o(M, x, y, k, S[l + 10], 17, m[14])
			k = o(k, M, x, y, S[l + 11], 22, m[15])
			y = o(y, k, M, x, S[l + 12], 7, m[16])
			x = o(x, y, k, M, S[l + 13], 12, m[17])
			M = o(M, x, y, k, S[l + 14], 17, m[18])
			k = o(k, M, x, y, S[l + 15], 22, m[19])
			y = d(y, k, M, x, S[l + 1], 5, m[20])
			x = d(x, y, k, M, S[l + 6], 9, m[21])
			M = d(M, x, y, k, S[l + 11], 14, m[22])
			k = d(k, M, x, y, S[l + 0], 20, m[23])
			y = d(y, k, M, x, S[l + 5], 5, m[24])
			x = d(x, y, k, M, S[l + 10], 9, m[25])
			M = d(M, x, y, k, S[l + 15], 14, m[26])
			k = d(k, M, x, y, S[l + 4], 20, m[27])
			y = d(y, k, M, x, S[l + 9], 5, m[28])
			x = d(x, y, k, M, S[l + 14], 9, m[29])
			M = d(M, x, y, k, S[l + 3], 14, m[30])
			k = d(k, M, x, y, S[l + 8], 20, m[31])
			y = d(y, k, M, x, S[l + 13], 5, m[32])
			x = d(x, y, k, M, S[l + 2], 9, m[33])
			M = d(M, x, y, k, S[l + 7], 14, m[34])
			k = d(k, M, x, y, S[l + 12], 20, m[35])
			y = u(y, k, M, x, S[l + 5], 4, m[36])
			x = u(x, y, k, M, S[l + 8], 11, m[37])
			M = u(M, x, y, k, S[l + 11], 16, m[38])
			k = u(k, M, x, y, S[l + 14], 23, m[39])
			y = u(y, k, M, x, S[l + 1], 4, m[40])
			x = u(x, y, k, M, S[l + 4], 11, m[41])
			M = u(M, x, y, k, S[l + 7], 16, m[42])
			k = u(k, M, x, y, S[l + 10], 23, m[43])
			y = u(y, k, M, x, S[l + 13], 4, m[44])
			x = u(x, y, k, M, S[l + 0], 11, m[45])
			M = u(M, x, y, k, S[l + 3], 16, m[46])
			k = u(k, M, x, y, S[l + 6], 23, m[47])
			y = u(y, k, M, x, S[l + 9], 4, m[48])
			x = u(x, y, k, M, S[l + 12], 11, m[49])
			M = u(M, x, y, k, S[l + 15], 16, m[50])
			k = u(k, M, x, y, S[l + 2], 23, m[51])
			y = i(y, k, M, x, S[l + 0], 6, m[52])
			x = i(x, y, k, M, S[l + 7], 10, m[53])
			M = i(M, x, y, k, S[l + 14], 15, m[54])
			k = i(k, M, x, y, S[l + 5], 21, m[55])
			y = i(y, k, M, x, S[l + 12], 6, m[56])
			x = i(x, y, k, M, S[l + 3], 10, m[57])
			M = i(M, x, y, k, S[l + 10], 15, m[58])
			k = i(k, M, x, y, S[l + 1], 21, m[59])
			y = i(y, k, M, x, S[l + 8], 6, m[60])
			x = i(x, y, k, M, S[l + 15], 10, m[61])
			M = i(M, x, y, k, S[l + 6], 15, m[62])
			k = i(k, M, x, y, S[l + 13], 21, m[63])
			y = i(y, k, M, x, S[l + 4], 6, m[64])
			x = i(x, y, k, M, S[l + 11], 10, m[65])
			M = i(M, x, y, k, S[l + 2], 15, m[66])
			k = i(k, M, x, y, S[l + 9], 21, m[67])
			y = n(y, v)
			k = n(k, s)
			M = n(M, p)
			x = n(x, g)
		return h(y)+h(k)+h(M)+h(x)

		
	def recode(b):
		def getcode(s):
			w, i, s, e=s.split(',')
			a=b=c=0;d=[];f=[]
			while True:
				if a < 5:f.append(w[a])
				elif a < len(w):d.append(w[a])
				a+=1
				
				if  b < 5 :f.append(i[b])
				elif  b < len(i):d.append(i[b])
				b+=1
				
				if  c < 5:f.append(s[c])
				elif  c < len(s):d.append(s[c])
				c+=1
				
				if len(w) + len(i) + len(s) + len(e) == len(d) + len(f) + len(e):break

			k=''.join(s for s in d);m=''.join(s for s in f);b=0;o=[]
			for a in range(0,len(d),2):
				n = -1
				if ord(m[b]) % 2:n = 1
				o.append(chr(int(k[a:a+2], 36) - n))
				b+=1
				if b >= len(f):b = 0
			return ''.join(s for s in o)
		l=0
		while l<5 or 'decodeLink' not in b:
			try:b=getcode(xsearch("(\w{100,},\w+,\w+,\w+)",b.replace("'",'')));l+=1
			except:break
		return b
	
	return H(string, key) if key else recode(string)

class serversList:
	def __init__(self):
		self.servers=[('anime47.com', '37'), ('tvhay.org', '41'), ('hdviet.com', '22'), ('fptplay.net', '07'), ('hayhaytv.vn', '23'), ('bilutv.com', '36'), ('phimmoi.net', '24'), ('hdonline.vn', '30'), ('megabox.vn', '17'), ('phim3s.net', '32'), ('phim14.net', '39'), ('kenh88.com', '26'), ('phimdata.com', '27'), ('phimsot.com', '29'), ('phim47.com', '28'), ('phimbathu.com', '43'), ('kphim.tv', '33'), ('phimnhanh.com', '35'), ('dangcaphd.com', '18'), ('phim.media', '40'), ('hdsieunhanh.com', '44'), ('imovies.vn', '48'), ('vuahd.tv', '21'), ('pubvn.tv', '19'), ('vietsubhd.com', '54'), ('mphim.net', '55')]
		try:self.ordinal=[int(i) for i in xrw('free_servers.dat').split(',')]
		except:self.ordinal=[]
		l=len(self.servers);update=False
		for i in range(l):
			if i not in self.ordinal:self.ordinal.append(i);update=True
		for i in self.ordinal:
			if i >= l:self.ordinal.remove(i);update=True
		if update:xrw('free_servers.dat',','.join(str(i) for i in self.ordinal))
		
	def mylist(self):
		return [self.servers[i] for i in self.ordinal]

	def move(self,server,step):#sl:server location, ol: ordinal location, step:up=-1,down=+1
		sl=self.servers.index([i for i in self.servers if i[0]==server][0])
		ol=self.ordinal.index([i for i in self.ordinal if i==sl][0])
		temp=self.ordinal[ol+step];self.ordinal[ol+step]=sl;self.ordinal[ol]=temp
		xrw('free_servers.dat',','.join(str(i) for i in self.ordinal))

	def moveDown(self,server):
		sl=self.servers.index([i for i in self.servers if i[0]==server][0])
		ol=self.ordinal.index([i for i in self.ordinal if i==sl][0])
		temp=self.ordinal[ol+1];self.ordinal[ol+1]=sl;self.ordinal[ol]=temp
		xrw('free_servers.dat',','.join(str(i) for i in self.ordinal))

	def search(self,url):
		try:j=json.loads(xsearch('\((\{.+?\})\)',xread(url)))
		except:j={}
		if not j.get('results',{}):
			mess(u'Tìm gần đúng','i-max.vn')
			try:j=json.loads(xsearch('\((\{.+?\})\)',xread(url.replace('%22',''))))
			except:j={}
			if not j:return []
		
		def detail(l):
			title=l.get('titleNoFormatting','').encode('utf-8')
			href=l.get('unescapedUrl','').encode('utf-8')
			try:img=l['richSnippet']['cseImage']['src'].encode('utf-8')
			except:img=''
			return title,href,img
		l=[detail(i) for i in j.get('results',{}) if i.get('titleNoFormatting') and i.get('unescapedUrl')]
		
		cursor=j.get('cursor',{});currentPage=cursor.get('currentPageIndex',1000);pages=cursor.get('pages',{})
		start=''.join(i.get('start','') for i in pages if i.get('label',0)==cursor.get('currentPageIndex')+2)
		if start:
			title='[COLOR lime]Page next: %d[/COLOR]'%(cursor.get('currentPageIndex')+2)
			l.append((title,start,''))
		return l

class googlesearch:
	def __init__(self):
		self.url='https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&'
		self.url+='rsz=filtered_cse&num=20&hl=vi&prettyPrint=false&source=gcsc&gss=.com&googlehost=www.google.com&'
		self.url+='callback=google.search.Search.apiary19044&alt=json&cx=%s&start=%s&q=%s'
	
	def detail(self,i):
		title=i.get('titleNoFormatting','').encode('utf-8')
		href=i.get('unescapedUrl','').encode('utf-8')
		if not title or not href:return []
		if '...' in title:
			s=i.get('richSnippet',{}).get('metatags',{}).get('ogTitle')
			if s:title=s.encode('utf-8')
			elif i.get('contentNoFormatting'):
				s=title.replace('....','...').split('...')[-1]
				if s:
					title=i.get('contentNoFormatting').encode('utf-8')
					title=title.split(s)[0].replace('Thông tin tập tin. ','')+s
		try:img=i['richSnippet']['cseImage']['src'].encode('utf-8')
		except:img=''
		return title,href,img
	
	def content(self,cx,start,string):
		string='+'.join(string.split())
		try:d=json.loads(xsearch('\((\{.+?\})\)',xread(self.url%(cx,start,'%22'+string+'%22'))))
		except:d={}
		if not d.get('results',{}):
			mess(u'Tìm gần đúng ...','xshare')
			try:d=json.loads(xsearch('\((\{.+?\})\)',xread(self.url%(cx,start,string))))
			except:d={}
		items=[i for i in [self.detail(j) for j in d.get('results',{})] if i]
		
		cursor=d.get('cursor',{});currentPage=cursor.get('currentPageIndex',1000);pages=cursor.get('pages',{})
		start=''.join(i.get('start','') for i in pages if i.get('label',0)==currentPage+2).encode('utf-8')
		if start:
			title='[COLOR lime]Page next: %d[/COLOR]'%(currentPage+2)
			items.append((title,start,currentPage+2))
		return items

class fshare:#https://www.fshare.vn/home/Mục chia sẻ của thaitni/abc?pageIndex=1
    
	def __init__(self, username='', password='', id=''):
		self.url_id=id
		self.myFavourite_id=''
		self.token=''
		self.logged=None
		self.hd={'User-Agent':'Mozilla/5.0','x-requested-with':'XMLHttpRequest'}
		self.myAcc=username and password
		if self.myAcc:
			self.login(username,password)
			if self.logged=='success':
				myfolder=self.get_myFolder()
				self.myFavourite_id=''.join(xsearch('(\w{10,})',s[1]) for s in myfolder if s[0]=='xshare_favourite')
				if not self.myFavourite_id:
					self.myFavourite_id=self.add_folder(folder_name='xshare_favourite',in_dir_id='0')

	def fetch(self,url,data=None):
		try:response=urlfetch.fetch(url,headers=self.hd,data=data)
		except:response= None
		return response
	
	def login(self,username,password):
		response = self.fetch('https://www.fshare.vn/login')
		if not response or response.status!=200:mess('Connect to fshare.vn fails','Fshare.vn')
		else:
			fs_csrf=xsearch('value="(.+?)" name="fs_csrf"',response.body)
			data={"LoginForm[email]":username,"LoginForm[password]":password,"fs_csrf":fs_csrf}
			self.hd['Cookie']=response.cookiestring
			response = self.fetch('https://www.fshare.vn/login',data)
			if response and response.status==302:
				self.hd['Cookie']=response.cookiestring;self.logged='success';print self.hd
				mess(u'Login thành công','Fshare.vn')
			else:mess(u'Login không thành công!','Fshare.vn')
	
	def logout(self):
		if False:
		#if self.logged:
			response = self.fetch('https://www.fshare.vn/logout')
			if response and response.status==302:self.logged=None;mess(u'Logout thành công','Fshare.vn')
			else:mess(u'Logout không thành công!','Fshare.vn')
	
	def loginOK(self,u,p):
		try:
			b=urllib2.urlopen(urllib2.Request('http://www.fshare.vn'))
			cookie=b.headers.getheader('set-cookie')
			fs_csrf=xsearch('value="(.+?)" name="fs_csrf"',b.read())
		except:cookie=fs_csrf=''
		data=urllib.urlencode({"LoginForm[email]":u,"LoginForm[password]":p,"fs_csrf":fs_csrf})
		hd={'Cookie':cookie,'Content-Type':'application/x-www-form-urlencoded'}
		conn = urllib2.httplib.HTTPSConnection('www.fshare.vn')
		conn.request('POST', '/login',data,hd)
		try:
			response=conn.getresponse()
			if response.status==302:cookie=response.getheader('set-cookie')
			else:cookie=''
		except:cookie=''
		return cookie
	
	def get_maxlink(self,url):
		def aku(url):
			from StringIO import StringIO
			import gzip
			data='url_download=https%3A%2F%2Fwww.fshare.vn%2Ffile%2F'+url.rsplit('/',1)[1]
			try:
				buf = StringIO(xread('http://www.aku.vn/linksvip',data=data))
				f = gzip.GzipFile(fileobj=buf)
				link=xsearch('<a href=([^<]+?) target=_blank',f.read())
				if link:mess('[COLOR cyan]Thanks to Nhat Vo Van[/COLOR]','get link from aku.vn')
			except:link=''
			return link
		
		b=xget(url,self.hd)
		if not b:return 'fail'
		link=b.geturl()
		if link==url:
			b=b.read()
			if re.search('<title>.*Lỗi 404.*</title>|"index-404"',b):
				mess(u'Tập tin quý khách yêu cầu không tồn tại!','Fshare.vn');result='fail'
			elif 'sử dụng nhiều địa chỉ IP' in b:
				mess(u'Acc Quý khách sử dụng nhiều địa chỉ IP!','Fshare.vn',10000)
				result='fail'
			elif re.search('<i class="fa fa-star">',b):
				mess(u'Bạn đang sử dụng FREE Fshare acc','fshare.vn')
				return aku(url)
			elif not re.search('<a href="/logout">',b):
				mess(u'Thông tin Fshare acc chưa đủ hoặc sai','fshare.vn')
				return aku(url)
			
			fs_csrf=xsearch('value="(.+?)" name="fs_csrf"',b)
			downloadForm=xsearch('id="DownloadForm_linkcode" type="hidden" value="(.+?)"',b)
			data={'fs_csrf':fs_csrf,'DownloadForm[linkcode]':downloadForm,'ajax':'download-form'}
			if re.search('class="fa fa-lock"',b):
				data['DownloadForm[pwd]']=get_input(u'Hãy nhập: Mật khẩu tập tin')
			b=xread('https://www.fshare.vn/download/get',self.hd,urllib.urlencode(data))
			try:link=json.loads(b).get('url','')
			except:link='fail'
		return link
	
	def get_token(self,url='https://www.fshare.vn/home'):
		self.hd['x-pjax']='true'
		return xsearch('data-token="(.+?)"',xread('https://www.fshare.vn/home',self.hd))
	
	def get_folder(self,url):
		def fixTitleEPS(i):
			p=[xsearch('(Tập.?\d+)|(tập.?\d+)|(TẬP.?\d+)',i),xsearch('(\W[E|e].?.?\d+)',i),xsearch('(\A\d+)',i)]
			if p[0]:i=re.sub(p[0],'Tập '+format(int(xsearch('(\d+)',p[0])),'02d'),i)
			elif p[1]:i=re.sub(p[1],'.E'+format(int(xsearch('(\d+)',p[1])),'02d'),i)
			elif p[2]:i=re.sub(p[2],format(int(xsearch('(\d+)',p[2])),'02d'),i)
			return i
		
		items=[]
		result={'pagename':'','items':items}
		if '/file/' in url:return result
		b=xread(url,self.hd)
		if xsearch('(Số lượng: 0)',b):mess('Folder %s is empty'%url,'Fshare.vn');return result
		elif not b:mess('Folder %s find not found'%url,'Fshare.vn');return result
		
		pagename=xsearch('<title>(.+?)</title>',b).replace('Fshare - ','')
		list=[i for i in refas('(<li.+?/li>)',b) if 'date_modify' in i]
		for s in list:
			id=xsearch('data-id="(.+?)"',s)
			title=xsearch('title="(.+?)"',s).strip()
			size=xsearch('<div class="pull-left file_size align-right">(\d.+?)</div>',s)
			type=xsearch('data-type="(.+?)"',s)
			if type=='file':link='https://www.fshare.vn/file/%s'%id
			elif xsearch('(\A[0-9A-Z_]{12,20})',title):#MyFshare item name
				ID=xsearch('(\A[0-9A-Z_]{12,20})',title)
				title=title.split(' ',1)[-1].strip()
				if 'FOLDER' in ID:link='https://www.fshare.vn/folder/%s'%ID.replace('FOLDER','')
				elif 'FILE' in ID:link='https://www.fshare.vn/file/%s'%ID.replace('FILE','')
				elif xread('https://www.fshare.vn/folder/%s'%ID):link='https://www.fshare.vn/folder/%s'%ID
				else:link='https://www.fshare.vn/file/%s'%ID
			else:link='https://www.fshare.vn/folder/%s'%id
			date=xsearch('"pull-left file_date_modify align-right">(\d{2}/\d{2}/\d{4})</div>',s).strip()
			title=fixTitleEPS(title)
			items.append((title,link,id,size,date))
		return {'pagename':pagename,'items':items}
	
	def myFshare_add(self,url,name):
		if not self.url_id:mess(u'Hãy set "Thư mục chia sẻ của tôi trên Fshare!"','myFshare');return
		id=url.split('/')[4]
		if [s for s in self.get_folder('https://www.fshare.vn/folder/'+self.url_id)['items'] if id in s[0]]:
			mess(u'This item already in MyFshare!','Fshare.vn');return
		token=self.get_token();name=id+('FOLDER ' if 'folder' in url else 'FILE ')+name
		data='{"token":"%s","name":"%s","in_dir":"%s"}'%(token,name,self.url_id)
		response=self.fetch('https://www.fshare.vn/api/fileops/createFolder',data)
		if response and response.status==200:mess(u'Add a item to MyFshare success','Fshare.vn')
		else:mess(u'Add a item to MyFshare fail!','Fshare.vn')
	
	def myFshare_remove(self,url):
		id=[s[2] for s in self.get_folder('https://www.fshare.vn/folder/'+self.url_id)['items'] if url==s[1]]
		id=id[0] if id else '';data='{"token":"%s","items":["%s"]}'%(self.get_token(),id.strip())
		response=self.fetch('https://www.fshare.vn/api/fileops/delete',data)
		if response and response.status==200:result=True;mess(u'Remove a item from MyFshare success','Fshare.vn')
		else:result=False;mess(u'Remove a item from MyFshare fail!','Fshare.vn')
		return result
	
	def myFshare_rename(self,url,new_name):
		id=[s[2] for s in self.get_folder('https://www.fshare.vn/folder/'+self.url_id)['items'] if url==s[1]]
		id=id[0] if id else '';data='{"token":"%s","new_name":"%s","file":"%s"}'%(self.get_token(),new_name,id)
		response=self.fetch('https://www.fshare.vn/api/fileops/rename',data)
		if response and response.status==200:result=True;mess(u'Rename a item in MyFshare success','Fshare.vn')
		else:result=False;mess(u'Rename a item in MyFshare fail!','Fshare.vn')
		return result
	
	def myFshare_upload(self,name,size,content):
		response=self.fetch('https://www.fshare.vn/home');result=False
		if not response or response.status!=200:
			response=self.fetch('https://www.fshare.vn/home')
			if not response or response.status!=200:mess(u'Get home page fail!','Fshare.vn');return result
		token=xsearch('data-token="(.+?)"',response.body)
		path=xsearch('data-id="%s" path-origin = "" data-path="(.+?)"'%self.url_id,response.body)
		SESSID=xsearch('session_id=(.+?)\W',str(self.hd))
		data='{"SESSID":"%s","name":"%s","size":"%s","path":"%s","token":"%s","secured":1}'%(
			SESSID,name,size,path,token)#;print data
		response=self.fetch('https://www.fshare.vn/api/session/upload',data)
		if response and response.status==200:
			response=self.fetch(response.json['location'],content)
			if response and response.status==200:result=True;mess(u'Upload file to MyFshare success','Fshare.vn')
		if result is False:mess(u'Upload file to MyFshare fail!','Fshare.vn')#;print response.status
		return result
	
	def Favorite_add(self,url):
		data='{"token":"%s","link":"%s"}'%(self.get_token(),url)
		response=self.fetch('https://www.fshare.vn/api/fileops/AddFavorite',data)
		if response and response.status==200:
			result=True;mess(u'Add a item to MyFshare Favorite success','Fshare.vn')
		else:result=False;mess(u'Add a item to MyFshare Favorite fail!','Fshare.vn')
		return result
	
	def Favorite_remove(self,name):
		data='{"token":"%s","items":["%s"],"status":0}'%(self.get_token(),name)
		response=self.fetch('https://www.fshare.vn/api/fileops/ChangeFavorite',data)
		if response and response.status==200:
			result=True;mess(u'Remove a item from MyFshare Favorite success','Fshare.vn')
		else:result=False;mess(u'Remove a item from MyFshare Favorite fail!','Fshare.vn')
		return result
	
	def add_folder(self,folder_name,in_dir_id='0'):
		token=self.get_token()
		#{"token":"49e3b84c0e4f1353491fed40eb964f485d091574","name":"abc","in_dir":"8NDKF9NA7T9I"}
		data='{"token":"%s","name":"%s","in_dir":"%s"}'%(token,folder_name,in_dir_id)
		response=self.fetch('https://www.fshare.vn/api/fileops/createFolder',data)
		try:result=response.json;result_code=result.get('code')
		except:result_code=0
		if result_code==200:
			#mess(result.get('msg')+' - '+result.get('folder',{}).get('name'),'Fshare.vn')
			result=result.get('folder',{}).get('linkcode')
		else:mess(u'Add folder fail !','Fshare.vn');result=''
		return result #folder ID created, empty if fail
	
	def remove_folder(self,parent_folder,folder_id):
		data='{"token":"%s","items":["%s"]}'%(self.get_token(),folder_id)
		self.hd['Referer']='https://www.fshare.vn/home/xshare_favourite'
		response=self.fetch('https://www.fshare.vn/api/fileops/delete',data)
		try:result=response.json;result_code=result.get('code')
		except:result_code=0
		if result_code==200:result=result.get('msg')
		else:result=''
		return result
	
	def get_myFolder(self,folder_name='',page=0):
		self.hd['x-pjax']='true'
		if page>0 and folder_name=='xshare_favourite':
			url='https://www.fshare.vn/home/xshare_favourite?pageIndex=%d'%page
		else:url='https://www.fshare.vn/home/'+folder_name+'?_pjax=%23pjax_content'#;print url,self.hd
		response=self.fetch(url)
		if response and response.status==200:
			items=re.findall('dl="(.+?)".+?f-name= "(.+?)"',response.body)
			items=[(s[1],'https://www.fshare.vn'+s[0]) for s in items]
		else:items=[]
		return items #(folder name,public url)
	
	def upload_file(self,fn):#Chua xong
		size=os.path.getsize(fn);name=os.path.basename(fn);path='/'
		session_id=xsearch('session_id=(.+?)\W',str(self.hd))
		data='{"SESSID":"%s","name":"%s","path":"%s","secured":"1","size":"%d","token":"%s"}'%(session_id,name,path,size,self.get_token())
		response=self.fetch('https://www.fshare.vn/api/session/upload',data)
		
		if response and response.status==200:
			try:response=urlfetch.fetch(response.json['location'].replace('http:','https:'),headers=self.hd,data=data)
			except:response= None
			if response and response.status==200:
				result=True;mess(u'Upload file to MyFshare success','Fshare.vn')
		#print response.status

	def remove_file(self,id):
		data='{"token": "%s", "items":["%s"]}'%(self.get_token(),id)
		response=self.fetch('https://www.fshare.vn/api/fileops/delete',data)
		
	def myFavourites_add(self,s):
		result=[]
		if not self.myFavourite_id:mess('Your Fshare Favourite ID not found!')
		else:
			import time
			loop=True;prefix=int(time.time());count=0;s=urllib2.base64.urlsafe_b64encode(s)
			while loop:
				folder_name='%d.%d.'%(prefix,count)+s[:230]
				if len(s)>230:s=s[230:];count+=1
				else:loop=False
				i=self.add_folder(folder_name,self.myFavourite_id)
				if i:result.append(i)
				else:loop=False#Chua xu ly delete neu that bai
		return result # list of folders ID created
	
	def myFavourites_loads(self,page):
		#(folder name,public url)
		myFolder=self.get_myFolder('xshare_favourite',page)
		f=[i[0] for i in myFolder if re.search('\d{10,}',i[0])]
		s=sorted([i.split('.') for i in f], key=lambda m:(m[0],m[1]))
		k=[]
		for i in sorted(list(set([i[0] for i in s])),reverse=True):
			try:m=urllib2.base64.urlsafe_b64decode(''.join(j[2] for j in s if j[0]==i))
			except:m=''
			if m:k.append(m+','+'-'.join(xsearch('(\w{10,})',j[1]) for j in myFolder if i in j[0]))
		if len(myFolder)==100:k.append('Trang tiếp theo ...')
		return k
		
	def myFavourites_remove(self,ids):
		result=True
		for i in ids.split('-'):
			if not self.remove_folder('xshare_favourite',i):result=False
		return result
	
	def searchFollow(self,q):
		b=xread('https://www.fshare.vn/files/searchFollow?key=%s'%q,self.hd)
		items=[]
		for s in refas('(<li.+?/li>)',b):
			title=xsearch('title="(.+?)"',s)
			href=xsearch('href="(.+?)"',s)
			if not title or not href:continue
			href='https://www.fshare.vn'+href
			t=xsearch('list_item">(\d+)</div>',s)
			if t:title='%s [COLOR blue]%s (files)[/COLOR]'%(title,t)
			t=xsearch('data-int="\d+">(.+?)</div>',s)
			if t:title='%s [COLOR green]%s[/COLOR]'%(title,t)
			t=xsearch('data-int="">(\d+)</div>',s).strip()
			if t:t=int(t);title='%s [COLOR cyan]%d (follow)[/COLOR]'%(title,t)
			else:t=0
			followed='"hidden pull-right btn btn-danger following follow"' in s
			if followed:title='[COLOR orange]%s[/COLOR]'%title
			items.append((title,href,t))
		items=[(i[0],i[1]) for i in sorted(items, key=lambda k:k[2],reverse=True)]
		return items

class fptPlay:#from resources.lib.servers import fptPlay;fpt=fptPlay(c)
	def __init__(self):
		self.hd={'User_Agent':'Mozilla/5.0','X-Requested-With':'XMLHttpRequest'}
		self.hd['referer']='https://fptplay.net/fptplay/gioi-thieu'
		self.hd['Cookie']=xrw('fptplay.cookie') if filetime('fptplay.cookie')<30 else self.login()
		
	def login(self):
		phone_fptplay=get_setting('phone_fptplay');password=get_setting('pass_fptplay')
		conutry=re.sub('\(.+?\)','',get_setting('country_fptplay')).strip()
		if not phone_fptplay:#'MDkxODc3ODAxMzpoaWV1aGllbi52bg=='
			mess(u'Bạn đang sử dụng account Fptplay của hieuhien.vn')
			#phone_fptplay,password=urllib2.base64.b64decode('MDkxMzc2MTQ0NDphZGRvbnhzaGFyZQ==').split(':')
			phone_fptplay,password=urllib2.base64.b64decode('MDkxODc3ODAxMzpoaWV1aGllbi52bg==').split(':')
		data=urllib.urlencode({'phone':phone_fptplay,'password':password,'country_code':conutry})
		cookie=urllib2.HTTPCookieProcessor();opener=urllib2.build_opener(cookie);urllib2.install_opener(opener)
		#try:b=opener.open(self.hd['referer'])
		#except:pass
		opener.addheaders=self.hd.items();url='https://fptplay.net/user/login'
		req=urllib2.Request('https://fptplay.net/user/login',data)
		try:b=urllib2.urlopen(req,timeout=30)
		except:pass
		cookie=xcookie(cookie)
		if 'laravel_id' in cookie:mess(u'Login thành công','fptplay.net');xrw('fptplay.cookie',cookie)
		else:mess(u'Login không thành công!','fptplay.net')
		return cookie
	
	def detail(self,s):
		title=vnu(xsearch('title="([^"]+?)"',s))
		if not title:title=vnu(xsearch('alt="([^"]+?)"',s))
		label=' '.join(re.findall('<p[^<]*?>(.+?)</p>',s))+title
		dir=True if 'tập' in (title+label).lower() else False
		if xsearch('(\d+/\d+)',label):dir=True;title+=' [COLOR blue]%s[/COLOR]'%xsearch('(\d+/\d+)',label)
		if 'thuyếtminh' in (title+label).replace(' ','').lower():title='[COLOR blue]TM[/COLOR] '+title
		if 'phụđề' in (title+label).replace(' ','').lower():title='[COLOR green]PĐ[/COLOR] '+title
		href=xsearch('href="([^"]+?)"',s)
		if not href:href=xsearch('data-href="(.+?)"',s)
		if 'Đang diễn ra' in s:dir=None
		img=xsearch('src="([^"]+?\.jpg)',s)
		if not img:
			img=xsearch('data-original="([^"]+?\.jpg)',s)
			if not img:img=xsearch('data-original="([^"]+?\.png)',s)
		return title,href,img,dir
	
	def eps(self,url,page):
		data='film_id=%s&page=%d'%(xsearch('(\w{20,30})',url),page);items=[]
		b=xread('https://fptplay.net/show/episode',self.hd,data)
		for s in [i for i in re.findall('(<li.+?/li>)',b,re.S) if '"title_items"' in i]:
			title=xsearch('title="(.+?)"',s)
			epi=xsearch('<p class="title_items">.+? (\d+)',s)
			if epi:title=epi+'-'+title
			if 'phụđề' in title.replace(' ','').lower():title='[COLOR green]PĐ[/COLOR] '+title
			elif 'thuyếtminh' in title.replace(' ','').lower():title='[COLOR blue]TM[/COLOR] '+title
			href=xsearch('(\w{20,30})',xsearch('href="(.+?)"',s))+'?'+xsearch('id="episode_(\d{1,4})"',s)
			items.append((vnu(title),href))

		if '&rsaquo;&rsaquo;' in b:items.append(('[COLOR lime]Các tập tiếp theo ...[/COLOR]',''))
		return items
	
	def schedule(self):
		#b=xread('https://fptplay.net/show/schedule?channel=vtv6-hd&date=06-10-2016&channel_now=')
		if filetime('fptschedule.txt')>10:
			b=xread('https://fptplay.net/livetv')
			b='\n'.join(re.findall('(<ul class="mar-p menu-list-event".+?/ul>)',b,re.S))
			xrw('fptschedule.txt',b)
		b=xrw('fptschedule.txt')
		items=[('day',i) for i in re.findall('<li rel="(\d.+?)"',b)]
		return items+[i for i in re.findall('<li rel="(\D.+?)".+?>([^<]+?)</span>',b)]
	
	def liveChannels(self):
		b=xread('https://fptplay.net/livetv')
		xrw('fptschedule.txt','\n'.join(re.findall('(<ul class="mar-p menu-list-event".+?/ul>)',b,re.S)))
		items=[('Lịch Phát Sóng','','')]
		b=b.split('<div id="box_')
		for s in [i for i in b if ' class="livetv_header' in i]:
			i=xsearch('<span class="livetv_header Regular pull-left"[^>]*>(.+?)</span>',s)
			items.append((vnu(i),'sep',''))
			for title,href,img,dir in [self.detail(i) for i in re.findall('(<a class="tv_channel.+?/a>)',s,re.S)]:
				items.append((title,href,img))
		return items
		
	def liveLink(self,url):
		id=urllib2.os.path.basename(url)
		if not id:id='vtv3-hd'
		data='mobile=web&quality=3&type=newchannel&id=%s'%id
		b=xread('https://fptplay.net/show/getlinklivetv',self.hd,data)
		try:link=json.loads(b).get('stream')
		except:link=''
		if link:link
		return link+'|User-Agent=Mozilla'
	
	def fptNodes(self,url):
		b=xread(url)
		string=xsearch('(<items.+?/items>)',b,1,re.S)
		if not string:
			s=re.findall('<item>(.+?)</item>',b,re.S)
			string='<items>\n'+'\n'.join(['<item>'+i+'</item>' for i in s if '<item>' not in i])+'\n</items>'
		from xml.etree.ElementTree import fromstring as xmlnodes
		try:nodes=[i for i in xmlnodes(string.replace('&','&amp;')) if i.tag=='item']
		except:nodes=[]
		mylist=[m for m in [dict([(i.tag,i.text) for i in j if i.text]) for j in nodes] if len(m)>=3]
		return mylist

class ifile:
	def __init__(self,c):
		self.home='http://ifile.tv'
		self.hd={'User-Agent':'Mozilla/5.0'}
		self.c=c
	
	def detail(self,s):
		title=xsearch('<font[^<]+>(.+?)<',s).strip()
		tl=xsearch('<b>Thời lượng</b>:(.+?)<br>',s).strip()
		if tl:title+=' [COLOR gold]%s[/COLOR]'%tl
		tl=xsearch('<b>Ngày cập nhật</b>:(.+?)<br>',s).strip()
		if tl:title+=' [COLOR green]%s[/COLOR]'%tl
		href=self.home+xsearch('href="(.+?)"',s)
		img=self.home+xsearch('src="(.+?)"',s)
		epi=xsearch('<b> Số tập :</b>(.+?)<br/>',s).strip()
		return title,href,img,epi
	
	def page(self,content):
		s=[i for i in content.split('<div class="box-widget-grid fl-box">') if '<div class="details">' in i]
		items=[self.detail(i) for i in s]
		pn=xsearch('<a href="([^<]+?)" title="Next" > Next</a>',content)
		if pn:items.append(('Page next...',self.home+pn,'',''))
		return items
	
	def eps(self,url):
		b=xread(url)
		img=xsearch("<img src= '(.+?)'",b)
		return [(i,self.home+img) for i in re.findall("'(http://4share.vn[^']+)'",b)]

class hayhayvn:
	def __init__(self,c):
		self.hd={'User-Agent':'Mozilla/5.0','X-Requested-With':'XMLHttpRequest','Referer':'http://www.hayhaytv.vn'}
		self.c=c
		
	def getLink(self,url):
		tap=xsearch('-Tap-(\d+)-',url)
		if tap:tap='_'+tap
		if '/show-' in url:url='http://www.hayhaytv.vn/getsourceshow/%s'%(xsearch('-(\w+)\.html',url)+tap)
		else:url='http://www.hayhaytv.vn/getsource/%s'%(xsearch('-(\w+)\.html',url)+tap)
		b=xread(url,self.hd)
		try:items=ls([(i.get('file','').replace('\\',''),rsl(i.get('label',''))) for i in eval(b)])
		except:items=[]
		return items

	def getLink1(self,url):
		b=xread(url)
		link=xsearch('file.{,5}"(.+?)"',b);sub=''
		if link:sub=xsearch("var track.{,5}'(.+?)'",b)
		else:
			url='http://www.hayhaytv.vn/getsource/%s'%xsearch("FILM_KEY = '(.+?)'",b)
			b=xread(url,self.hd)
			try:links=[(i.get('file').replace('\\',''),i.get('label')) for i in eval(b)]
			except:links=[]
			for href,r in ls([(i[0],rsl(i[1])) for i in links]):
				g=xget(href)
				if g:link=g.geturl();break
		return link,sub

class phim3s_net:
	def __init__(self, username, password):
		self.session = urlfetch.Session(headers={'User_Agent':'Mozilla/5.0 (Android 4.4; Mobile; rv:42.0) Gecko/41.0 Firefox/42.0','X-Requested-With':'XMLHttpRequest','Cookie':''})
		self.login(username,password)
	
	def fetch(self, url, data=''):
		try:response = self.session.fetch(url, data=data)
		except:response = None
		return response
	
	def login(self, username, password):
		data={'username':username,'password':password}
		response=self.fetch('http://phim3s.net/member/login/', data=data)
		try:response=response.json
		except:response={}
		mess(u'%s'%response.get('message',['Login to phim3s.net fail !',''])[0],'Login to Phim3s.net')
	
	def get_bookmark(self):
		response=self.fetch('http://phim3s.net/ajax/member/get_bookmarks/')
		try:response=response.json
		except:response={}
		#print response
		self.fetch('http://phim3s.net/member/logout/')
		return response

	def action_bookmark(self, url,action):#add_bookmark/remove_bookmark
		id=xsearch('_(\d+?)/',url)
		if id:
			url='http://phim3s.net/ajax/member/%s/?film_id=%s'%(action,id)
			response=self.fetch(url)
			try:response=response.json
			except:response={}
			mess(u'%s'%response.get('message','%s thất bại !'%action),'Phim3s.net bookmark')
			self.fetch('http://phim3s.net/member/logout/')

class kPhim:
	def __init__(self,c):
		self.hd={'User-Agent':'Mozilla/5.0','Referer':'http://kphim.tv/dieu-khoan-chung.html'}
		self.c=c

	def detail(self,l):
		items=[]
		for s in l:
			href=xsearch('href="(.+?)"',s)
			img=xsearch('src="(.+?)"',s)
			title=xsearch('>(.+?)</h4>',s)
			t=re.search('>(.+?) <span style=".+?">(.+?)</span>',s)
			if t: title+=' - '+t.group(1)+' '+t.group(2)
			elif xsearch('>(.+?)</span>',s):title+=' - '+xsearch('>(.+?)</span>',s)
			items.append((title,href,img))
		return items
	
	def genre(self,url):
		items=[]
		for s in re.findall('(<li style.+?/li>)',xread(url),re.S):
			href=xsearch('href="(.+?)"',s)
			img=xsearch('src="(.+?)"',s)
			t=xsearch('>(.+?)-\d+?</span>',s)
			title=t+' - ' if t else ''
			title+=xsearch('"movie-name-1">(.+?)</h3>',s)+' - '+xsearch('"movie-name-2">(.+?)</h4>',s)
			t=xsearch('<strong> (.+?)</strong></p>',s)
			if t:title+= ' (%s)'%t
			items.append((title,href,img))
		return items
	
	def eps(self,url):
		b=xread(url)
		items=re.findall('<a class="btn btn-default" href="(.+?)"> (.+?) </a>',b)
		if not items:items=re.findall('<a class="label[^"]+?" href="(.+?)"> (.+?) </a>',b)
		return items
	
	def getLink(self,url):
		b=xread(url)
		servers=re.findall('poster.+?fid.+?title="video-(\d+?)".+?title="(.+?)">',b)
		if servers:video_id=servers[0][0]
		else:video_id=xsearch("fvid='(.+?)'",b)
		server_id=xsearch('loadNewPlayer\(fsvvideo, (\d.+?),',b)
		tk=urllib2.hashlib.md5(server_id+'func').hexdigest()[1:]#jquery.min.js?ver=14 mahoahkphim
		b=xread('http://kphim.tv/embed/%s/%s/%s'%(server_id,video_id,tk),self.hd)
		
		j=re.findall('src="([^<]+?)".+?res="([^<]+?)"',b);link=''
		for href,label in ls([(i[0],rsl(i[1])) for i in j]):
			try:link=urllib2.urlopen(href).geturl();break
			except:pass
		return link

class tvhay:
	def __init__(self, s):
		try:
			w, i, s, e=s.split(',')
			s=self.dec(w, i, s, e)
			b=xsearch("(\w{100,},\w+,\w+,\w+)",s.replace("'",''))
			w, i, s, e=b.split(',')
			s=self.dec(w, i, s, e)
			b=xsearch("(\w{100,},\w+,\w+,\w+)",s.replace("'",''))
			w, i, s, e=b.split(',')
			s=self.dec(w, i, s, e)
		except:s=''
		self.string=s
	
	def dec(self, w, i, s, e):
		a=b=c=0;d=[];f=[]
		while (True):
			if a<5:f.append(w[a])
			elif a<len(w):d.append(w[a])
			a+=1
			if b<5:f.append(i[b])
			elif b<len(i):d.append(i[b])
			b+=1
			if c<5:f.append(s[c])
			elif c<len(s):d.append(s[c])
			c+=1
			if len(w)+len(i)+len(s)+len(e)==len(d)+len(f)+len(e):break


		b=0;k=[];h=''.join(f);g=''.join(d)
		for a in range(0,len(d),2):
			m=1 if ord(h[b])%2 else -1
			k.append(chr(int(g[a:a+2],36)-m))
			b+=1
			if b>=len(f):b=0

		return ''.join(k)
	
	def dec_(self, w, i, s, e):
		for s in range(0,len(w),2):
			i+=chr(int(w[s:s+2],36))
		return i

class hdVietnamn:#from resources.lib.servers import hdvn;hdvn=hdvn()
	def __init__(self):
		self.urlhome='http://www.hdvietnam.com/'
		if filetime('hdvietnam.cookie')>1:
			data={'login':addon.getSetting('usernameh'),'password':addon.getSetting('usernameh')}
			try:
				cookie=urlfetch.post('http://www.hdvietnam.com/login/login',data=data).cookiestring
				xrw('hdvietnam.cookie',cookie)
			except:cookie=''
		else:cookie=xrw('hdvietnam.cookie')
		self.hd={'User-Agent':'Mozilla/5.0','Referer':'http://www.hdvietnam.com/forums/','Cookie':cookie}
		cookie=xread(self.urlhome+'threads/997745/page-200',self.hd)
		self.token=xsearch('"logout.._xfToken=(.+?)"',cookie)
		self.urlhome='http://www.hdvietnam.com/'
	
	def login(self):
		cookie=urllib2.HTTPCookieProcessor()
		opener=urllib2.build_opener(cookie)
		urllib2.install_opener(opener)
		opener.addheaders=[('User_Agent','Mozilla/5.0')]
		data='login=%s&register=0&password=%s&cookie_check=1'
		data=data%(addon.getSetting('usernameh'),addon.getSetting('passwordh'))
		b=opener.open('http://www.hdvietnam.com/login/login',data)
		content=b.read()
		if addon.getSetting('usernameh') in content:
			hdvncookie=';'.join('%s=%s'%(i.name,i.value) for i in cookie.cookiejar)
			self.hd['Cookie']=hdvncookie
			self.token=xsearch('"logout.._xfToken=(.+?)"',content)
			xrw('hdvietnam.cookie',hdvncookie)
		else:mess(u'Login không thành công!','hdvietnam.com')
	
	def data_refresh(self,data):
		return re.sub('securitytoken=[^&]+','securitytoken='+self.token,data)
	
	def getpage(self,url):
		content=xread(url,self.hd).split('"nodeList section sectionMain"')[-1]
		s=re.findall('<a href="(.+?)" data-description=".+?">(.+?)</a></h3>',content)
		items=[(self.urlhome+i,j) for i,j in s]
		return items
		
	def forums1(self,url):
		content=xread(url,self.hd)
		items=re.findall('data-previewUrl="(.+?)">(.+?)</a>',content)
		pn=xsearch('<a href="(.+?)" class="text">Ti.+ &gt;</a>',content)
		if pn:items.append((pn,'[COLOR lime]Trang tiếp theo: %s[/COLOR]'%xsearch('/page-(\d+)',pn)))
		return [(self.urlhome+i.replace('/preview',''),j) for i,j in items]
	
	def forums(self,url):
		def cleans(s):return ' '.join(re.sub('<[^<]+?>|\{[^\{]+\}|\[[^\[]+?\]|&#\w+;|amp;','',s).split())
		def detail(s):
			id=xsearch('id="thread-(.+?)"',s)
			timestring=xsearch('data-timestring="(.+?)"',s)
			if not timestring:
				datestring=xsearch('<a class="dateTime"><span class="DateTime" title="(.+?)"',s).replace('lúc ','')
				datestring='[COLOR gold]%s[/COLOR] '%datestring
			else:datestring='[COLOR gold]%s %s[/COLOR] '%(xsearch('data-datestring="(.+?)"',s),timestring)
			author='[COLOR blue]%s[/COLOR] '%xsearch('data-author="(.+?)"',s)+datestring
			title='data-previewUrl="(.+?)/preview">(.+?)</a>'
			href=self.urlhome+xsearch(title,s,1)
			title=xsearch(title,s,2)
			return id,author+cleans(title),href
		
		content=xread(url,self.hd).split('<div class="titleBar">')[-1]
		nodeList=re.findall('<h3 class="nodeTitle"><a href="([^"]+?)"[^<]+?>(.+?)</a></h3>',content)
		items=[('nodeList','[B]%s[/B]'%title,self.urlhome+href) for href,title in nodeList]
		for s in [i for i in re.findall('(<li id="thread.+?/li>)',content,re.S) if 'class="sticky"' not in i]:
			#img=xsearch('<img src="(.+?)"',content)
			items.append(detail(s))
		pn=xsearch('<a href="(.+?)" class="text">Ti.+ &gt;</a>',content)
		if pn:
			pn=self.urlhome+pn
			items.append(('pageNext','[COLOR lime]Trang tiếp theo: %s[/COLOR]'%xsearch('/page-(\d+)',pn),pn))
		return items
		
	def threads(self,url,refresh=''):
		def cleans(s):return ' '.join(re.sub('<[^<]+?>|\{[^\{]+\}|\[[^\[]+?\]|&#\w+;|amp;|<','',s).split())
		def srv(link):return [i for i in srvs if i in link]
		srvs=['fshare.vn','4share.vn','tenlua.vn','subscene.com','phudeviet.org','youtube.com']
		items=[];morethread=[]
		def getTitle(title,href,s):
			if refresh and 'fshare.vn' in href or '4share.vn' in href:return title
			t=title
			if [i for i in srvs if i in title] or not title:
				title=xsearch('<b>Ðề: (.+?)</b>',s)
				if not title:
					title=' '.join(xsearch('<div style="text-align: center".+?>(\w[^<]+?)<',s).split())
			elif 'download' in title.strip().lower():
				title=xsearch('class="internalLink">([^<]+?)<',s[s.find(href)-500:])
				if not title:title=xsearch('<title>(.+?)</title>',content)
			if not title:title=t
			title=cleans(title)
			return title
		
		content=xread(url,self.hd)
		for s in re.findall('(<li id="post-.+?/li>)',content,re.S):
			img=xsearch('<img src="([^"]+?)" class="',s,result=xsearch('<img src="(.+?jpg)"',s))
			i=s
			while 'header-' in img and 'ogo' not in img:
				i=i[i.find(img)+10:]
				img=xsearch('<img src="(.+?jpg)"',i)
			
			i=re.findall('<a href="([^"]+?)" target="_blank"[^<]+?>(.+?)/a>',s)
			i= [(getTitle(title,href,s),href,img) for href,title in i if srv(href)]
			if i:items+=i
			else:
				m=re.findall('(http[\w|:|/|\.|\?|=|&|-]+)',s.replace('amp;',''))
				items+=[('',i,img) for i in m if srv(i)]

			j=re.findall('<a href="(http://www.hdvietnam.com/[^"]+?)" class="internalLink">(.+>)',s)
			j= [(cleans(title),href,img) for href,title in j if 'chuyenlink' not in href and 'tags' not in href]
			if j:morethread+=j
		temp=[];list=[]
		for i in items+morethread:
			if i[1] not in temp:temp.append(i[1]);list.append(i)
		
		#if len([i for i in items if 'fshare.vn' in i[1]])<5:
		if refresh:
			def ftitle(title,href):
				if 'fshare.vn' in href or '4share.vn' in href:
					mess(href,'link checking ...')
					title=siteInfo(href)[0]
				return title
			items=[(ftitle(i[0],i[1]),i[1],i[2]) for i in list]
		
		list=[i for i in items if i[0] and i[1]]
		
		return list
		
	def getThanks(self,data):
		show_href='http://www.hdvietnam.com/diendan/showthread.php';s=[]
		thanks_href='http://www.hdvietnam.com/diendan/post_thanks.php'
		i=self.getpage(thanks_href,data,loop=True)
		data=self.data_refresh(data).replace('post_thanks_add','whatever')
		return self.getpage(show_href,data)

	def getlink(self,url,buian=''):
		srv=['fshare.vn','4share.vn','tenlua.vn','subscene.com','hdvietnam.com','phudeviet.org']
		def s1(s):return [j for j in srv if j in s.lower()]
		def s2(string,href,c):#get title
			if buian:
				c=' '.join(i for i in c.split('=*=') if href in i)#Lay session co href
				p=c.find(href);i=0;s=''
				pattern='<div style="text-align[^"]+"><b><font size="\d">([^<]+?)</font></b>'
				while len(s)<10 and (p-i)>0:
					i+=100;s=xsearch(pattern,c[p-i:p]).strip()
					if [j for j in ('nội dung ẩn','Trailer','Download') if j in s]:s=''
			else:
				s=' '.join(i for i in re.sub('<[^<]+>','',string).split())
				if not s or [j for j in ('nội dung ẩn','Trailer','Download','http') if j in s]:
					c=' '.join(i for i in c.split('=*=') if href in i)#Lay session co href
					p=c.find(href);i=0;s=''
					while len(s)<5 and (p-i)>0:
						i+=50;s=xsearch('>([^<]+)<',c[p-i:p]).strip()
						if [j for j in ('nội dung ẩn','Trailer','Download') if j in s]:s=''
			return s if s else href

		def s3(href,img,c):#get img
			c=' '.join(i for i in c.split('=*=') if href in i)#Lay session co href
			p=c.find(href);i=0;s=''
			while not s and (p-i)>0:
				i+=100;s=xsearch('src="([^"]+)"',c[p-i:p])
				if not 'attachment.php' in s:s=''
			if not s:s=img
			return s

		if '#post' in url:url=url.split('#post')[0]
		content=self.getpage(url,loop=True)
		
		label=' '.join(re.sub('\[[^\[]+\]','',xsearch('<title>(.+?)</title>',content)).split())
		img=xsearch('<img src="([^"]+?\.jpg)"',content)
		if not img:img=xsearch('<img src="([^"]{300,})"',content)
		chuyenmuc=xsearch('<div class="morethread">(.+?)class="postfoot"',content)
		s=[]
		for i in re.findall('(<div class="posthead">.+?class="report")',content):
			i=i.replace('\\t','').replace('\\r','').replace('\\n','').replace('amp;','').replace('&gt;','-')
			if 'id="hide_fieldset"' in i:
				thanks=xsearch('(do=post_thanks_add[^"]+?)"',i).replace('amp;','')
				if thanks:i=i.replace('id="hide_fieldset"','-*-'+self.getThanks(thanks)+'-*-')
			s.append(i)
		
		content='\n=*=\n'.join(' '.join(i.split()) for i in s);s=''
		temp=re.findall('<a href="([^"]+?)" target="_blank">(.+?)</a>',content)
		temp1=[i for i in temp if s1(i[0])];n=[i[0] for i in temp1]
		temp=[i for i in re.findall('>(http[^<]+?)<',content) if '...' not in i and s1(i)]
		temp1+=[(i,'') for i in temp if i not in n];n=[];temp=[]
		
		for i in temp1:
			if 'chuyenlink.php' not in i[0] and 'members' not in i[0] and i[0] not in n:
				temp.append(i);n.append(i[0])
			elif 'phudeviet.org' in i[0]:
				j=urllib.unquote(xsearch('(phudeviet.org.+)',i[0]))
				if j and 'http://'+j not in n:temp.append(('http://'+j,i[1]));n.append('http://'+j)
		
		items=[(s2(i[1],i[0],content),i[0],s3(i[0],img,content)) for i in temp]
		items=[i for i in items if 'point fshare' not in i[0].lower()]
		
		#CÁC CHỦ ĐỀ CÙNG CHUYÊN MỤC
		for title,href in re.findall('<a title="(.+?)" href="(.+?)">',chuyenmuc):
			items.append((title,href,"morethread"))
		return items#title,href,img

	def addRoom(self,url):
		roomid=xsearch('(\d{6,10})',url)
		url='http://www.hdvietnam.com/diendan/subscription.php?do=addsubscription&t='+roomid
		content=self.getpage(url);
		token=xsearch('name="securitytoken" value="(.+?)"',content)
		link=urllib.quote_plus(xsearch('name="url" value="(.+?)"',content))
		data='emailupdate=0&folderid=0&s=&securitytoken=%s&do=doaddsubscription&threadid=%s&url=%s'
		content=self.getpage('http://www.hdvietnam.com/diendan/subscription.php',data%(token,roomid,link))
		mess(xsearch('<p class="blockrow restore">(.+?)</p>',content).decode('utf-8'),'HDVietnam.com')
	
	def removeRoom(self,url):
		content=self.getpage(url);token=xsearch('name="securitytoken" value="(.+?)"',content)
		href=xsearch('href="(subscription.php\?do=removesubscription[^"]+?)"',content).replace('amp;','')
		if href:
			content=self.getpage('http://www.hdvietnam.com/diendan/'+href)
			mess(xsearch('<p class="blockrow restore">(.+?)</p>',content).decode('utf-8'),'HDVietnam.com')
			result=True
		else:result=False;mess('Link subscription remove not found!','HDVietnam.com')
		return result

class youtube:#https://www.youtube.com/watch?v=rZftpdEKzeY
	class signature:
		def __init__(self,json=1):
			if json==1:
				self.json = {'actions': [
				{'params': ['%SIG%'], 'func': 'list'}, {'params': ['%SIG%', 0, 3],'func': 'splice'}, 
				{'params': ['%SIG%', 2], 'func': 'swap'}, {'params': ['%SIG%', 0, 2],'func': 'splice'}, 
				{'params': ['%SIG%', 46], 'func': 'swap'}, {'params': ['%SIG%', 0, 1],'func': 'splice'}, 
				{'params': ['%SIG%', 31], 'func': 'swap'}, {'params': ['%SIG%', 27],'func': 'swap'}, 
				{'params': ['%SIG%'], 'func': 'join'}]}
			elif json==2:
				self.json={'actions': [
				{'params': ['%SIG%'], 'func': 'list'}, {'params': ['%SIG%', 0, 2], 'func': 'splice'},
				{'params': ['%SIG%'],'func': 'reverse'}, {'params': ['%SIG%', 0, 2], 'func': 'splice'}, 
				{'params': ['%SIG%', 31],'func': 'swap'}, {'params': ['%SIG%', 6], 'func': 'swap'}, 
				{'params': ['%SIG%'],'func': 'reverse'}, {'params': ['%SIG%', 0, 2], 'func': 'splice'}, 
				{'params': ['%SIG%'], 'func': 'join'}]}
			elif json==3:
				self.json={'actions': [
				{'params': ['%SIG%'], 'func': 'list'}, {'params': ['%SIG%', 19], 'func': 'swap'}, 
				{'params': ['%SIG%'], 'func': 'reverse'}, {'params': ['%SIG%', 0, 1], 'func': 'splice'}, 
				{'params': ['%SIG%'], 'func': 'reverse'}, {'params': ['%SIG%', 0, 1], 'func': 'splice'}, 
				{'params': ['%SIG%', 7], 'func': 'swap'}, {'params': ['%SIG%'], 'func': 'reverse'}, 
				{'params': ['%SIG%', 38], 'func': 'swap'}, {'params': ['%SIG%', 0, 3], 'func': 'splice'},
				{'params': ['%SIG%'], 'func': 'join'}]}
			else:
				self.json={'actions': [
				{'params': ['%SIG%'], 'func': 'list'}, {'params': ['%SIG%'], 'func': 'reverse'}, 
				{'params': ['%SIG%', 0, 3], 'func': 'splice'}, {'params': ['%SIG%'], 'func': 'reverse'}, 
				{'params': ['%SIG%', 20], 'func': 'swap'}, {'params': ['%SIG%', 0, 3], 'func': 'splice'}, 
				{'params': ['%SIG%'], 'func': 'reverse'}, {'params': ['%SIG%', 0, 2], 'func': 'splice'},
				{'params': ['%SIG%'], 'func': 'reverse'}, {'params': ['%SIG%'], 'func': 'join'}]}

		def makeSign(self, s):
			for action in self.json['actions']:
				func = '_'+action['func']
				params = action['params']
				if func == '_return':break

				for i in range(len(params)):
					param = params[i]
					if param == '%SIG%':
						param = s
						params[i] = param
						break

				method = getattr(self, func)
				if method:s = method(*params)
			return s

		def _join(self, s):return ''.join(s)
		def _list(self, s):return list(s)
		def _splice(self, s, a, b):del s[a:b];return s
		def _swap(self, s, b):c=s[0]; s[0]=s[b%len(s)]; s[b]=c; return s
		def _reverse(self, signature):return signature[::-1]
	
	def __init__(self):
		self.url='https://www.googleapis.com/youtube/v3/%s?regionCode=VN&hl=vi&maxResults=50&order=date&key=AIzaSyA-Y38JpoUKbdpQgFellPthOgcZTFJwkqY&%s'
		self.key='AIzaSyA-Y38JpoUKbdpQgFellPthOgcZTFJwkqY'
	
	def ytRead(self,url):
		try:j=json.loads(xread(url))
		except:j={}
		#xrw(r'd:\xoa.json',json.dumps(j,indent=2))
		return j
	
	def getNextPageURL(self,url,j):
		return re.sub('&pageToken=.*','',url)+'&pageToken='+j.get('nextPageToken') if j.has_key('nextPageToken') else ''
	
	def getItems(self,url,urlNextPage):
		def publishedDay(day):
			d=xsearch('-(\d+-\d+)',day)
			d='%s/%s'%(d.split('-')[1],d.split('-')[0])
			y=xsearch('(\d{4})',day)
			if y and y<year:d+='/%s'%y[2:]
			return d
		
		def duration(i):
			s=i.get('contentDetails',{}).get('duration','')
			t=int(xsearch('(\d*)H',s,result='0'))*3600
			t+=int(xsearch('(\d*)M',s,result='0'))*60
			t+=int(xsearch('(\d*)S',s,result='0'))
			return 'duration:'+str(t)
			
		year=urllib2.time.strftime("%Y")
		j=self.ytRead(url)
		items=[];publishedAt=''
		#print 'getItems:url=%s,  urlNextPage=%s'%(url,urlNextPage)
		for i in j.get('items',[]):
			kind=i.get('kind','').replace('youtube#','').encode('utf-8')
			img=i.get('snippet',{}).get('thumbnails',{}).get('high',{}).get('url','').encode('utf-8')
			if kind=='guideCategory':
				title=i.get('snippet',{}).get('title','').encode('utf-8')
				id=i.get('id','').encode('utf-8')
			elif kind=='channel':
				title=i.get('snippet',{}).get('localized',{}).get('title','').encode('utf-8')
				id='UU'+i.get('id','').encode('utf-8')[2:]
			elif kind=='playlist':
				title=i.get('snippet',{}).get('localized',{}).get('title','').encode('utf-8')
				id=i.get('id','').encode('utf-8')
				publishedAt=i.get('snippet',{}).get('publishedAt','').encode('utf-8')
				if title:title='[COLOR blue]%s[/COLOR] %s'%(publishedDay(publishedAt),title)
			elif kind=='video':
				title=i.get('snippet',{}).get('localized',{}).get('title','').encode('utf-8')
				id=i.get('id','').encode('utf-8')
				publishedAt=i.get('snippet',{}).get('publishedAt','').encode('utf-8')
				if title:title='[COLOR blue]%s[/COLOR] %s%s'%(publishedDay(publishedAt),title,duration(i))
			elif kind=='searchResult':
				title=i.get('snippet',{}).get('title','').encode('utf-8')
				if i.get('id',{}).get('kind','').replace('youtube#','')=='playlist':
					kind+='Playlist'
					id=i.get('id',{}).get('playlistId','').encode('utf-8')
				elif i.get('id',{}).get('kind','').replace('youtube#','')=='channel':
					kind+='Channel'
					id=i.get('id',{}).get('channelId','').encode('utf-8')
			
			if not title or not id or 'sex' in title:continue
			else:items.append((title,id,img,kind,publishedAt))
		
		items=[(i[0],i[1],i[2],i[3]) for i in sorted(items, key=lambda k: k[4],reverse=True)]
		if not urlNextPage:urlNextPage=self.getNextPageURL(url,j)
		if urlNextPage:items.append(('nextPage',urlNextPage,'',''))
		return items
			
	def getElements(self,id,kind):
		url=self.url
		urlNextPage=''
		href=id if id.startswith('https:') else ''
		if kind=='guideCategoryListResponse':url=url%('guideCategories','part=snippet')
		elif kind=='guideCategory':
			url=url%('channels','part=snippet%2Clocalizations%2CcontentDetails&categoryId='+id) if not href else href
		elif kind=='playlists':
			if not href:href=url%('playlists','part=snippet&channelId='+id)
			j=self.ytRead(href)
			urlNextPage=self.getNextPageURL(href,j)
			ids=','.join(i.get('id').encode('utf-8') for i in j.get('items',[]))
			url=url%('playlists','part=snippet%2CcontentDetails&'+urllib.urlencode({'id':ids}))
		elif kind=='playlist':
			if not href:href=url%('playlistItems','part=snippet&playlistId='+id)
			j=self.ytRead(href)
			urlNextPage=self.getNextPageURL(href,j)
			ids=','.join(i.get('snippet',{}).get('resourceId',{}).get('videoId','').encode('utf-8') for i in j.get('items',[]))
			url=url%('videos','part=snippet%2CcontentDetails&'+urllib.urlencode({'id':ids}))
		elif kind=='channel':
			if not href:href=href=url%('playlistItems','part=snippet&playlistId='+id)
			j=self.ytRead(href)
			urlNextPage=self.getNextPageURL(href,j)
			ids=','.join(i.get('snippet',{}).get('resourceId',{}).get('videoId','').encode('utf-8') for i in j.get('items',[]))
			url=url%('videos','part=snippet%2CcontentDetails&'+urllib.urlencode({'id':ids}))
		elif kind=='searchListResponse':#type=video/channel/playlist
			if not href:href=url%('search','type=video&part=snippet&q='+urllib.quote_plus(id))#id:stringsearch
			j=self.ytRead(href)
			urlNextPage=self.getNextPageURL(href,j)
			ids=','.join(i.get('id',{}).get('videoId','').encode('utf-8') for i in j.get('items',[]))
			url=url%('videos','part=snippet%2CcontentDetails&'+urllib.urlencode({'id':ids}))
		elif kind=='searchPlayLists':
			url=url%('search','type=playlist&part=snippet&q='+urllib.quote_plus(id)) if not href else href
		elif kind=='searchChannels':
			url=url%('search','type=channel&part=snippet&q='+urllib.quote_plus(id)) if not href else href
		elif kind=='channelOfSearch':
			if not href:href=url%('playlists','part=snippet&channelId='+id)
			j=self.ytRead(href)
			urlNextPage=self.getNextPageURL(href,j)
			id=[i.get('id').encode('utf-8') for i in j.get('items',[])][0]
			url=url%('playlistItems','snippet&playlistId='+id)#urllib.urlencode({'id':ids}))
		elif kind=='channels':
			url=url%('channels','part=snippet%2Clocalizations%2CcontentDetails&categoryId='+id) if not href else href
		return self.getItems(url,urlNextPage)
	
	def getDL(self,url,map):
		def ytCheckLink(l):
			if not l:link='Video not found!'
			else:
				link=''
				for href,label in l:
					link=xcheck(href)#;print href,label
					if link:break
			return link
		
		def getData1(id):
			b=xread('https://www.youtube.com/watch?v='+id)
			s=xsearch('"url_encoded_fmt_stream_map":"(.+?)"',b).replace('\\u0026', '&').split(',')
		def getData(id):
			url='https://www.youtube.com/watch?v=%s&spf=navigate-back'%id
			try:data=json.loads(xread(url))
			except:data=[]
			items=[];link=''
			if data:
				fmts=''
				for i in data:
					fmts=i.get('data',{}).get('swfcfg',{}).get('args',{}).get(map,'')
					if fmts:break
				if fmts:
					qsl=urllib2.urlparse.parse_qsl
					l=[dict(qsl(i)) for i in fmts.split(',')]
					q='quality' if l[0].has_key('quality') else 'quality_label'
					def makeItems(d,sig):
						try:
							sign=self.signature(sig)
							r=d.get('url','')+'&signature='+sign.makeSign(d.get('s','')),rsl(d.get(q,''))
						except:r='',''
						return r
					sig=1
					while sig<5:
						link=ytCheckLink(ls([makeItems(i,sig) for i in l]))
						if link:break
						else:sig+=1
			return link
	
		id=xsearch('([\w|-]{10,20})',url)
		b=xread('https://www.youtube.com/get_video_info?video_id=%s'%id)
		qsl=urllib2.urlparse.parse_qsl;items=[]
		try:p=dict(qsl(b))
		except:p={}
		l=[dict(qsl(i)) for i in p.get(map,'').split(',')]
		q='quality' if l[0].has_key('quality') else 'quality_label'
		link=ytCheckLink(ls([(i.get('url',''),rsl(i.get(q,''))) for i in l]))
		if not link or link=='Video not found!':link=getData(id)
		return link

class imovies:
	def __init__(self,c):
		self.hd={'User-Agent':'Mozilla/5.0','Cookie':''}
		self.c=c
	
	def maxLink(self,url):
		id=xsearch('im(\d+)',url);epi=xsearch('-(\d+)\.html',url)
		url='http://imovies.vn/Movie/Play'
		try:j=json.loads(xread(url,data='movieId=%s&partId=%s'%(id,epi))).get('Sources')
		except:j=[]
		link=googleItems(j,'file','label')
		sub=''
		for i in [k for k in j if k.get('tracks')]:
			for m in i.get('tracks'):
				if m.get('kind','')=='captions' and 'vi' in m.get('label',''):
					sub=m.get('file','')
					break
		return link,sub
	
	def getElement(self,s):
		title=xsearch('title="(.+?)"',s,result=xsearch('alt="(.+?)"',s)).replace('Xem phim ','')
		href=xsearch('href="(.+?)"',s)
		if not title or not href:return ''
		title=s2c(title);dir=False
		result=' '.join(re.sub('<.+?>','',xsearch('Năm Sản Xuất:(.+?)</div>',s,1,re.S)).split())
		label=' '.join(re.sub('<.+?>','',xsearch('<label>Năm:(.+?)</span>',s,result=result)).split())
		if label and 'Đang' not in label:title+=' [COLOR orangered]%s[/COLOR]'%label
		result=xsearch('"label-part"><span>(.+?)</span>',s)
		label=xsearch('"st">(.+?)</span>',s,result=xsearch('"part-mv">(.+?)</span>',s,result=result))
		if label:title=namecolor(title,self.c)+' [COLOR cyan]%s[/COLOR]'%label;dir=True
		result=xsearch('Lượt Xem :</span>(.+?)</div>',s)
		label=' '.join(re.sub('<.+?>','',xsearch('<label>Lượt xem:(.+?)</span>',s,result=result)).split())
		if label and 'Đang' not in label:title+=' [COLOR lime]%s[/COLOR]'%label
		label=' '.join(re.sub('<.+?>','',xsearch('imdb">(.+?)</span>',s)))
		if label and 'Đang' not in label:title+=' [COLOR green]%s[/COLOR]'%''.join(label.split())
		if 'http' not in href:href='http://imovies.vn'+href
		img=xsearch('src="(.+?)"',s)
		if img and 'http' not in img:img='http://imovies.vn'+img
		fanart=xsearch('data-src="(.+?)"',s)
		if 'imovies.vn' not in href:href='http://imovies.vn'+href
		return title,href,img,fanart,dir
	
	def htmlPage(self,url,mode=0):
		b=xread(url);items=[]
		if 'Ooops.Đã Có lỗi xảy ra!' in b:mess(u'Ooops.Đã Có lỗi xảy ra!','imovies.vn')
		elif mode==1:
			for s in ['<abc>'+i for i in b.split('<h2 class="prl-d">') if 'class="mvli"' in i]:
				i=xsearch('<abc>(.+?)</h2>',s,1,re.S)
				title=' '.join(re.sub('<.+?>','',i).split())
				items.append((title,'','','','add_sep_item'))
				href=xsearch('href="(.+?)"',i)
				if href:
					title=namecolor(xsearch('title="(.+?)"',i),'orangered')
					items.append((title,'http://imovies.vn'+href,'','','page'))
				
				for i in re.findall('(<div class="mt".+?/a>)',s,re.S):
					items.append((self.getElement(i)))

		elif mode==2:
			for s in [i for i in b.split('<div class="item-content ">') if '"item-tite-movie"' in i]:
				items.append((self.getElement(s)))
		
		current=pageNext=hrefNext=''
		for s in re.findall('(<li.+?/li>)',xsearch('(<ul class="pagination".+?/ul>)',b,1,re.S),re.S):
			if 'class="active"' in s:current=xsearch('>(\d+)</a>',s)
			elif current:
				pageNext=xsearch('title="(.+?)"',s)
				hrefNext=xsearch('href="(.+?)"',s).replace('&amp;','&')
				break
		if pageNext and hrefNext:
			title='[COLOR lime]Trang tiếp ...%s[/COLOR]'%pageNext
			items.append((title,'http://imovies.vn'+hrefNext,'','',True))
		return items
	
	def ajaxPage(self,url,sort=''):
		try:j=json.loads(xread(url))
		except:j={}
		def geti(i,s):return i.get(s,'').encode('utf-8') if i.get(s,'') else ''
		keys=[('Daily','hôm nay'),('Weekly','trong tuần'),('Monthly','tháng')] if sort=='Hit' else [('Data','')]
		items=[]
		for key in keys:
			if len(keys)>1:
				cat='lẻ' if 'id=1' in url else 'bộ'
				title='Phim %s hot nhất '%cat+key[1]
				items.append((title,'','','','add_sep_item'))
			d=sorted(j.get(key[0]), key=lambda k: k.get(sort),reverse=True) if sort else j.get(key[0])
			for i in d:
				title='%s %s'%(geti(i,'Title'),geti(i,'Name'));dir=False
				if i.get('Year'):title+=' [COLOR orangered]%s[/COLOR]'%i.get('Year')
				if geti(i,'State'):
					title=namecolor(title,self.c)+' [COLOR cyan]%s[/COLOR]'%geti(i,'State');dir=True
				if i.get('Hit'):title+=' [COLOR lime]%s[/COLOR]'%i.get('Hit')
				if i.get('Imdb'):title+=' [COLOR green]%s[/COLOR]'%i.get('Imdb')
				href='http://imovies.vn/abc/abc/im%d.html'%i.get('Id',0)
				img='http://static.imovies.vn/'+geti(i,'Avatar')
				fanart='http://static.imovies.vn/'+geti(i,'Poster')
				items.append((title,href,img,fanart,dir))
		
		PageIndex=j.get('PageIndex',0)
		if PageIndex*25 < j.get('TotalRecord',0):
			href=re.sub('pageIndex=\d+','pageIndex=%d'%(PageIndex+1),url)
			title='[COLOR lime]Page next: ...%d[/COLOR]'%(PageIndex+1)
			items.append((title,href,'','',True))
		return items

class iMax:#;f=open(r'd:\xoa1.html','w');f.write(b);f.close()
	def __init__(self,c):
		self.hd={'User-Agent':'Mozilla/5.0','Cookie':''}
		self.c=c
		
	def dmOK(self,s):
		return [i for i in ('fshare.vn','4share.vn','subscene.com') if i in s.lower()]
	
	def thread(self,url):
		b=xread(url)
		items=[('',i,'') for i in re.findall('>(http[^<]+?)<',b) if self.dmOK(i)]
		
		items.append(('','','Bài viết nổi bật'))
		s=xsearch('(Featured Articles.+?/table>)',b,1,re.S)
		s=re.findall('href="([^"]+?)" title="[^<]+?"><img alt="([^"]+?)" src="([^"]+?)"',s)
		items+=[(i[1],i[0],i[2]) for i in s]
		
		items.append(('','','Các chủ đề khác'))
		s=xsearch('(<tbody id="collapseobj_similarthreads".+?/tbody>)',b,1,re.S)
		for s in re.findall('(<tr.+?/tr>)',s,re.S):
			label=re.search('>([^<]+?)<a href="([^"]+?)" title="([^"]+?\.jpg)',s)
			title=xsearch('>([^<]+?)</a>',s)
			if not label or not title:continue
			mem=xsearch('>([^<]+?)</span>',s)
			if mem:title='[COLOR gold]%s[/COLOR] [COLOR blue]%s[/COLOR] '%(label.group(1).strip(),mem)+title
			else:title='[COLOR gold]%s[/COLOR] '%label.group(1).strip()+title
			href='http://i-max.vn/forum/'+label.group(2).replace('amp;','')
			img=label.group(3)
			items.append((title,href,img))

		return items
	
	def pageDetail(self,s):
		title=xsearch('alt="([^"]+?)"',s).replace('amp;','')
		if not title:title=xsearch('<a href="[^"]+?">([^<]+?)</a>',s).strip()
		label=xsearch('>([^<]+?)<a href="http://i-max.vn/forum/showthread.php[^"]+?"',s).strip()
		if not label:label=xsearch('>\s*(\w[^<]+?)<a href="showthread\.php',s,1,re.S).strip()
		if label:title='[COLOR gold]%s[/COLOR] '%label.strip()+title
		member=xsearch('(\w+ \d\d).+?<a href="http://i-max.vn/forum/member.php[^"]+">(.+?)</a>',s)
		member+=' '+xsearch('\w.+?<a href="http://i-max.vn/forum/member.php[^"]+">(.+?)</a>',s)
		if not member.strip():
			member=xsearch('<span class="smallfont">\s*(\d\d.\d\d)',s,1,re.S).strip()
			member+=' %s'%xsearch('<a href="member\.php[^"]+?">(.+?)</a>',s).strip()
		title='[COLOR blue]%s[/COLOR] '%(' '.join(member.split()))+title
		href=xsearch('href="(http://i-max.vn/forum/showthread.php[^"]+?)"',s).replace('amp;','')
		if not href:
			href='http://i-max.vn/forum/'+xsearch('href="(showthread.php[^"]+?)"',s).replace('amp;','')
		img=xsearch('<div align="center"><img src="([^"]+)"',s).replace('amp;','')
		if not img:img=xsearch('<img src="([^"]+)"',s).replace('amp;','')
		return title,href,img
		
	def category(self,url):
		b=xread(url);items=[]
		s=xsearch('(<tbody id="threadbits_forum_.+?/tbody>)',b,1,re.S)
		#f=open(r'd:\xoa1.html','w');f.write(s);f.close()
		for s in s.split('</table>'):items.append((self.pageDetail(s)))
			
		pn=xsearch('<a rel="next" class="smallfont" href="([^"]+?)"',b).replace('amp;','')
		if pn:
			pn='http://i-max.vn/forum/'+pn.replace('amp;','')
			pages=xsearch('href="[^"]+?page=(\d+)" title="Trang Cuối',b)
			title='[COLOR lime]Page next: %s/%s[/COLOR]'%(xsearch('page=(\d+)',pn),pages)
			items.append((title,pn,'pagenext'))
			
		return items
	
	def search(self,url):
		b=xread(url)
		try:j=json.loads(xsearch('\((\{.+?\})\)',b))
		except:j={}
		if not j.get('results',{}):
			url=url.replace('%22','');mess(u'Tìm gần đúng','i-max.vn')
			try:j=json.loads(xsearch('\((\{.+?\})\)',xread(url)))
			except:j={}
			if not j:return []
		l=[]
		for i in j.get('results',{}):
			title=i.get('titleNoFormatting')
			href=i.get('unescapedUrl')
			t=xsearch('t=(\d+)',href);f=xsearch('f=(\d+)',href);p=xsearch('p=(\d+)',href)
			if t:href='http://i-max.vn/forum/showthread.php?t='+t;q='thread'
			elif f:href='http://i-max.vn/forum/forumdisplay.php?f='+f;q='category'
			elif p:href='http://i-max.vn/forum/showthread.php?p='+p;q='thread'
			else:print '------------------'+href;continue
			try:img=i['richSnippet']['cseImage']['src']
			except:img=''
			if href not in [m[1] for m in l]:l.append((title,href,img,q))
		
		cursor=j.get('cursor',{});currentPage=cursor.get('currentPageIndex',1000);pages=cursor.get('pages',{})
		start=''.join(i.get('start','') for i in pages if i.get('label',0)==cursor.get('currentPageIndex')+2)
		if start:
			title='[COLOR lime]Page next: %d[/COLOR]'%(cursor.get('currentPageIndex')+2)
			l.append((title,start,'',''))
		return l

class taiphim:
	def __init__(self,c):
		self.hd={'User-Agent':'Mozilla/5.0','Cookie':xrw('taiphimhd.cookie')}
		self.token=''
		self.c=c
	
	def login(self):
		data=urllib2.base64.b64decode('bG9naW49eHNoYXJlJTQwdGhhbmh0aGFpLm5ldCZyZWdpc3Rlcj0wJnBhc3N3b3JkPXhzaGFyZSZjb29raWVfY2hlY2s9MSZyZWRpcmVjdD0lMkYmX3hmVG9rZW49');url='http://taiphimhd.com/login/login';hd={'User-Agent':'Mozilla/5.0'}
		try:
			a=self.fetch(url,hd);hd['Cookie']=a.cookiestring;a=self.fetch(url,hd,data);self.hd['Cookie']=a.cookiestring
			if a.status==303:
				xrw('taiphimhd.cookie',self.hd['Cookie'])
				print '---------------------------- Login OK'
		except:pass
	
	def fetch(self,url,headers=None,data=None):
		if not headers:headers=self.hd
		try:response=urlfetch.fetch(url,headers=headers,data=data)
		except:response=None
		
		return response
	
	def getThanks(self,s):
		id=xsearch('href="posts/(\d+)/like"',s)
		if id:
			mess('Thanked to %s'%xsearch('data-author="(.+?)"',s).strip())
			url='http://taiphimhd.com/posts/%s/like'%id
			b=self.fetch(url,data={'_xfToken':self.token,'_xfNoRedirect':'1','_xfResponseType':'json'})
			url='http://taiphimhd.com/posts/%s/like-hide-check'%id
			b=self.fetch(url,data={'_xfToken':self.token,'_xfNoRedirect':'1','_xfResponseType':'json'})
			try:s=b.body.replace('amp;','').replace('\\','')
			except:pass
		
		return s
	
	def getLink(self,b):
		def srvs(i):
			srv=['fshare.vn','4share.vn','tenlua.vn','subscene.com','taiphimhd.com','phudeviet.org']
			return [j for j in srv if j in i]
		def i_l(i,l): return i[0] not in [j[0] for j in l]
		l=[];loop=False
		for s in re.findall('(<li id="post.+?/li>)',b,re.DOTALL):
			if 'click nút Like để lấy link' in s:s=self.getThanks(s);loop=True
			if loop:l=[];continue
			else:
				img=xsearch('img src="(.+?)"',s);p='<a href="(.+?)" target="_blank"[^<]+?>(.+>)'
				l+=[(i[0],re.sub('<[^<]+>','',i[1]),img) for i in re.findall(p,s) if srvs(i[0])]
				p='href="([^"]+?)"[^<]+?><[^<]+?>([^<]+?)<'
				l+=[(i[0],i[1],'') for i in re.findall(p,s) if srvs(i[0]) and i[0] not in [j[0] for j in l]]
				l+=[(i,i,img) for i in re.findall('(http[^<]+?)<',s) if srvs(i) and i not in [j[0] for j in l]]
		
		n=[]
		for href,title,img in l:
			if re.search('"|,|\'|\?',href) or href in [j[0] for j in n]:continue
			s=b[b.find(href)-1000:b.find(href)]
			if xsearch('"(http[^"]+\.jpg)"',s):img=xsearch('"(http[^"]+\.jpg)"',s)
			if 'fshare.vn' in href or '4share.vn' in href:title=siteInfo(href)[0]
			elif title in href or href in title:
				i='';fs=30
				while not i and fs>10:
					i=xsearch('style="font-size:.{,3}%d.{,5}">([^<]+)<'%fs,s);fs-=1
				if i:title=' '.join(i.split())
			if href and title.strip():n.append((href,' '.join(title.split()),img))
		
		return n#href,title,img
	
	def search(self,s):
		url='https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=20&hl=en&prettyPrint=false&source=gcsc&gss=.com&cx=006272920913781838063:kzk6oinlbd0&googlehost=www.google.com&callback=google.search.Search.apiary17955&q='+s
		a=self.fetch(url,headers={'User-Agent':'Mozilla/5.0'})
		try:j=json.loads(xsearch('\((\{.+?\})\)',a.body)).get('results')
		except:j=[]
		if not j:return []
		l=[]
		for i in j:
			title=i.get('title')
			href=re.sub('page-\d+','',i.get('url'))
			try:img=i['richSnippet']['cseImage']['src']
			except:img=''
			if href not in [m[1] for m in l]:l.append((title,href,img))
		
		return l
		
	def search1(self,s):
		url='http://taiphimhd.com/search/search'
		b=self.getContent(url)
		data={'keywords':urllib.quote_plus(s),'users':'','date':'','_xfToken':self.token}
		b=self.fetch(url,data=data)
		try:b=self.fetch(b.headers.get('location')).body
		except:b=''
		
		return b
	
	def xfetch(self,url,headers=None,data=None):
		b=xread(url,self.hd)
		try:response=urlfetch.fetch(url,headers=headers,data=data)
		except:response=None
		
		return response
	
	def getContent(self,url):
		b=xread(url,self.hd)
		if not xsearch('href="(logout[^"]+?)"',b):self.login();b=xread(url,self.hd)
		else:print '---------------------------- cookie OK'

		self.token=urllib.unquote(xsearch('name="_xfToken" value="(.+?)"',b))
		
		return b
	
	def getPage(self,url):
		b=self.getContent(url);items=[('name','','')]
		i=self.getLink(b);urlhome='http://taiphimhd.com/'
		if not i:i=self.getLink(self.getContent(url))
		for href,title,img in i:
			if 'http' not in img:img=urlhome+img
			if 'http://taiphimhd.com/' in href:title=namecolor(title,self.c)
			items.append((title,href,img))
		
		items.append(('--Có thể bạn muốn xem--','',''))
		for s in [i for i in re.findall('(<li id="thread.+?/li>)',b,re.DOTALL) if 'data-author' in i]:
			href=xsearch('href="(threads/.+?)"',s)
			if 'http' not in href:href=urlhome+href
			img=xsearch('src="(.+?)"',s)
			if 'http' not in img:img=urlhome+img
			title=xsearch('data-previewUrl=".+?">(.+?)</a>',s)
			items.append((namecolor(title,self.c),href,img))
		
		return items

	def getLists(self,url):
		if '/find-new/' in url:b=xread(url);items=[]
		else:b=self.getContent(url);items=[]
		for href,title in re.findall('<h3 class="nodeTitle"><a href="([^"]+?)"[^<]+?">(.+?)</a></h3>',b):
			title=namecolor('[B]Mục %s[/B]'%title.replace('amp;',''),self.c)
			items.append((title,'http://taiphimhd.com/'+href,'ico'))

		for s in re.findall('(<li id="thread.+?/li>)',b,re.DOTALL):
			href=xsearch('href="(.+?)"',s)
			if 'http' not in href:href='http://taiphimhd.com/'+href
			img=xsearch('src="(.+?)"',s)
			if 'http' not in img:img='http://taiphimhd.com/'+img
			author=xsearch('data-author="(.+?)"',s)
			title='[COLOR gold]%s[/COLOR] '%author+xsearch('data-previewUrl=".+?">(.+?)</a>',s)
			items.append((namecolor(title,self.c),href,img))
		
		s=xsearch('(PageNavNext.+?/nav>)',b,1,re.DOTALL)
		if s:
			href='http://taiphimhd.com/'+xsearch('href="(.+?)" class="text">Tiếp',s)
			pages=xsearch('href="[^"]+?" class="">(\d+)</a>',s)
			items.append((pages,href,'next'))
		
		return items
		
	def getRSS(self,url):
		b=self.getContent(url);items=[]
		for s in [i for i in b.split('<item>') if '<author>' in i]:
			author=xsearch('<author>(.+?)</author>',s)
			title=xsearch('<title>(.+?)</title>',s)
			href=xsearch('href="(http://taiphimhd.com/threads/[^"]+?)"',s)
			img=xsearch('src="([^"]+?jpg)"',s)
			items.append((title,href,img))
			
		return items

class sieunhanh:
	def __init__(self):
		self.hd={'User-Agent':'Mozilla/5.0'}
		self.urlhome='http://hdsieunhanh.com/'
		self.color='orangered'

	def eps(self,url):
		content=xread(url);items=[]
		s=xsearch('(<ul class="list_episode".+?/ul>)',content,1,re.DOTALL)
		return re.findall('href="(.+?)">(.+?)</a>',s)

	def item(self,s):
		title=xsearch('alt="(.+?)"',s)
		href=xsearch('href="(.+?)"',s)
		if 'html' not in href:href=self.urlhome+href
		img=xsearch('src="(.+?)"',s)
		rate=xsearch('"rate">([^<]+?)</span>',s)
		if rate:title='%s [COLOR green]%s[/COLOR]'%(title,rate)
		eps=' '.join(re.sub('<[^<]+?>','',xsearch('(<span class="label-range">.+?<strong>\d+?</strong>)',s)).split())
		if eps:title='%s [COLOR gold](%s)[/COLOR]'%(namecolor(title,self.color),eps);dir=True
		else:dir=False
		return (title,href,img,dir)
		
	def page(self,url):
		content=xread(url);items=[]
		for s in [i for i in content.split('<div class="block-base movie">') if 'data-id' in i]:items.append(self.item(s))
			
		pn=xsearch('<a href="([^"]+?)">Sau</a>',content)
		if pn:
			pn=self.urlhome+pn.replace('amp;','')
			pages=xsearch('=(\d+)">Cuối</a></li></ul>',content)
			title='[COLOR lime]Page next: page/%s[/COLOR]'%pages
			items.append((title,pn,'image',True))
		return items#title,href,img

	def search(self,s):
		url='http://hdsieunhanh.com/tim-kiem.html?term='+urllib.quote_plus(s)
		self.hd['X-Requested-With']='XMLHttpRequest';items=[];b=xread(url,self.hd)
		if not b:mess('Get search fail','hdsieunhanh.com');return items
		try:j=json.loads(b)
		except:j={}
		for s in ('director','phim','actor','show'):
			for i in j.get(s,[]):
				title=i.get('name').encode('utf-8')+' - '+i.get('extension').encode('utf-8')
				href=i.get('link')
				img=i.get('image')
				eps=(i.get('last_episode')+'/'+i.get('total_episode')) if i.get('total_episode')>'1' else ''
				eps=eps.encode('utf-8')
				if not eps:dir=False
				else:title='%s [COLOR blue]%s[/COLOR]'%(namecolor(title,self.color),eps);dir=True
				items.append((title,href,img,dir))
		if not items:mess(u'Không tìm thấy dữ liệu vui lòng thử lại!','hdsieunhanh.com')
		return items
	
	def maxLink(self,url):
		tap=xsearch('-Tap-(\d+)-',url)
		if tap:tap='_'+tap
		hd=self.hd;hd['Referer']=self.urlhome
		url='http://hdsieunhanh.com/getsource/%s'%(xsearch('-(\w+)\.html',url)+tap)
		try:items=ls([(i.get('file'),rsl(i.get('label'))) for i in json.loads(xread(url,hd))])
		except:items=[]
		return items
		
	def maxLink1(self,url):
		content=xread(url);link=''
		s=re.findall("file[^']+?'([^']+?)'[^']+?label:'([^']+?)'",content)
		if get_setting('resolut')=='Max':
			items=sorted(list(set([(i[0],rsl(i[1])) for i in s])), key=lambda k: int(k[1]),reverse=True)
		else:items=sorted(list(set([(i[0],rsl(i[1])) for i in s])), key=lambda k: int(k[1]))
		return items

class chiaseNhac:
	def __init__(self,username,password):
		self.session = urlfetch.Session(headers={'User_Agent':'Mozilla/5.0 (Android 4.4; Mobile; rv:42.0) Gecko/41.0 Firefox/42.0','Cookie':'vq=i%3A1080%3B; mq=i%3A500%3B'})
		self.urlhome='http://chiasenhac.vn/'
		self.login(username,password)
	
	def fetch(self, url, data=''):
		try:response = self.session.fetch(url, data=data)
		except:response = None
		return response
	
	def login(self,username,password):
		data={'username':username,'password':password,'login':'Dang Nhap'}
		response=self.fetch('http://chiasenhac.vn/login.php', data=data)
		if not response or response.status!=302:mess(u'Login Không thành công!','chiasenhac.com')

	def logout(self):
		self.fetch('http://chiasenhac.vn/login.php?logout=true')

	def favourite(self, url,action='add'):
		href='http://chiasenhac.vn/mp3/favourite/'+os.path.basename(url).replace('.','_%s.'%action)
		a=self.fetch(href);mess('%s success'%action)
	
	def get_favourite(self):
		response = self.fetch('http://chiasenhac.vn/mp3/favourite')
		if response and response.status==200:body=response.body
		else:body=''
		return body

class nhaccuatui:
	def __init__(self):
		self.url='http://www.nhaccuatui.com/'
		self.mh='http://www.nhaccuatui.com/mh/auto/'
		self.vh='http://www.nhaccuatui.com/vh/auto/'
		self.urlsearch='http://www.nhaccuatui.com/tim-kiem?q='
		self.speedsearch='http://www.nhaccuatui.com/ajax/search?q='
		self.cookie='NCT_AUTH=977cc927d3fa32554d0f19a6a080f69062a11d2cd2c94858decd6164af58e95a;NCT_LastLogin=1464771952377'
		self.headers={'User-Agent':'Mozilla/5.0','Cookie':self.cookie}
	
	def login(self):
		hd={'User-Agent':'Mozilla/5.0'}
		cookie=urllib2.HTTPCookieProcessor()
		opener=urllib2.build_opener(cookie)
		urllib2.install_opener(opener)
		username=get_setting('nct_u');password=get_setting('nct_p')
		if not username and not password:
			username,password=urllib2.base64.b64decode('eHNoYXJlLHRoYWl0bmk=').split(',')
		su='http://www.nhaccuatui.com/ajax/user?type=login'
		url='https://sso.nct.vn/auth/login?method=xlogin'
		data={'uname':username,'password':password,'appName':'nhaccuatui','su':su}
		req=urllib2.Request(url,urllib.urlencode(data),hd)
		res=urllib2.urlopen(req)
		self.headers['Cookie']=';'.join('%s=%s'%(i.name,i.value) for i in cookie.cookiejar)
	
	def getData(self,s,key):
		data=xsearch('\[([^\[]+?)\]\]',xsearch('<%s>(.+?)</%s>'%(key,key),s,1,re.DOTALL))
		if not data and key=='locationHQ':
			data=xsearch('\[([^\[]+?)\]\]',xsearch('<location>(.+?)</location>',s,1,re.DOTALL))
		return data
	
	def getLink(self,id,url=''):
		url=self.vh if url else self.mh
		xmlURL=xsearch('xmlURL.{,10}"(.+?)"',xread(url+id))
		xml=xread(xmlURL,self.headers)
		return self.getData(xml,'locationHQ')

	def home(self):
		b=xread(self.url)
		s=[i for i in re.findall('(<li.+?/li>)',b,re.DOTALL) if  '<a rel="follow"' in i]
		items=re.findall('<a rel="follow" href="([^"]+?)"[^<]+?>([^<]+?)</a>',b)
		
		return items
	
	def search(self,s,url):
		items=[]
		if s!='search-in':
			try:j=json.loads(xread(self.speedsearch+s)).get('data',dict())
			except:j={}
			if not j:return items
			for k in [j.get(i,dict()) for i in ['singer','video','playlist','song']]:
				for m in k:
					title=m.get('name').encode('utf-8')
					singer=','.join(m.get('singer',[])[n]['name'].encode('utf-8') for n in range(len(m.get('singer',[]))))
					if singer:title+=' [COLOR green]%s[/COLOR]'%singer
					items.append(('0',title,m.get('url'),m.get('img','')))
		
		b=xread(self.urlsearch+s) if s!='search-in' else xread(url)
		counter_sg=self.getCounter_sg(b)
		counter_pl=self.getCounter_pl(b)
		#f=open(r'd:\xoa.html','w');f.write(b);f.close()
		s=xsearch('(<ul class="search_returns_list">.+?/ul>)',b,1,re.DOTALL)
		for s in [i for i in s.split('<h2>') if '<li class=' in i]:
			title=' '.join(re.sub('<[^<]+?>','',s[:s.find('</a></h2>')]).split())
			href=xsearch('<a href="(.+?)"',s)
			if title:items.append(('1',title,href,''))
			for i in re.findall('(<li.+?/li>)',s,re.DOTALL):
				if 'class="list_song"' in i:
					title,href,img=self.getDetail_sg(i,counter_sg)
					items.append(('2',title,href,img))
				elif 'class="list_album"' in i:
					title,href,img=self.getDetail_sg(i,counter_pl)
					items.append(('2',title,href,img))
				elif 'class="list_video"' in i:
					title,href,img=self.getDetail_sg(i,counter_sg,'video')
					items.append(('2',title,href,img))
		
		i=self.pageControl(b)
		if i:title,href,img=i;items.append(('4',title,href,img))
		
		return items
	
	def pageControl(self,b):
		pageview=xsearch('(<div class="box_pageview">.+?</div>)',b,1,re.DOTALL)
		pn=xsearch('class="active">\d+</a><a href="([^"]+?)" rel="next"',pageview)
		if pn:
			pages=xsearch('\.(\d+)\.html" rel="Trang cuối"',pageview)
			if not pages:pages=xsearch('page=(\d+)" rel="Trang cuối"',pageview)
			title='[COLOR lime]Page next: page/%s[/COLOR]'%pages
			items=title,pn,'page'
		else:items=[]
			
		return items
	
	def getCounter_sg(self,s):
		ids=urllib.quote(','.join(re.findall('id="NCTCounter_sg_(\d+)"',s)))
		href='http://www.nhaccuatui.com/interaction/api/counter?listSongIds='+ids
		try:counter=json.loads(xread(href)).get('data')['songs']
		except:counter={}
		return counter
		
	def getDetail_sg(self,s,counter,sg=''):
		title=xsearch('class="name_song">(.+?)</a>',s)
		if not title:title=xsearch('class="name_song" title="[^"]+?">(.+?)<',s)
		if not title:title=xsearch('title="(.+?")',s)
		cs=', '.join(re.findall('target="_blank">([^<]+?)</a>',s))
		title=title+' - '+'[COLOR green]%s[/COLOR]'%cs
		count=counter.get(xsearch('id="NCTCounter_sg_(\d+)"',s))
		if count:title+=' [COLOR gold](%s)[/COLOR]'%fmn(count)
		href=xsearch('href="(.+?)"',s)
		img=xsearch('src="(.+?)"',s) if not sg else xsearch('data-src="(.+?)"',s)
		return title,href,img
		
	def getPage_sg(self,url):
		b=xread(url);items=[]
		counter=self.getCounter_sg(b)
		
		for s in [i for i in re.findall('(<li.+?/li>)',b,re.DOTALL) if '"item_content"' in i]:
			items.append((self.getDetail_sg(s,counter)))
			
		pageview=xsearch('(<div class="box_pageview">.+?</div>)',b,1,re.DOTALL)
		pn=xsearch('class="active">\d+</a><a href="([^"]+?)" rel="next"',pageview)
		if pn:
			pages=xsearch('\.(\d+)\.html" rel="Trang cuối"',pageview)
			title='[COLOR lime]Page next: page/%s[/COLOR]'%pages
			items.append((title,pn,''))
		
		return items
	
	def getCounter_pl(self,s):
		ids=urllib.quote(','.join(re.findall('id="NCTCounter_pl_(\d+)"',s)))
		href='http://www.nhaccuatui.com/interaction/api/counter?listPlaylistIds='+ids
		try:counter=json.loads(xread(href)).get('data')['playlists']
		except:counter={}
		return counter
		
	def getDetail_pl(self,s,counter):
		title=xsearch('class="name_song">(.+?)</a>',s)
		if not title:title=xsearch('title="(.+?)"',s)
		cs=xsearch('target="_blank">(.+?)</a>',s)
		if cs:title=title+' - '+'[COLOR green]%s[/COLOR]'%cs
		count=counter.get(xsearch('id="NCTCounter_pl_(\d+)"',s))
		if count:title+=' [COLOR gold](%s)[/COLOR]'%fmn(count)
		href=xsearch('href="(.+?)"',s)
		img=xsearch('data-src="(.+?)"',s)
		if not img:img=xsearch('src="(.+?)"',s)
		return title,href,img
	
	def getDetail_pl1(self,s,counter):
		title=xsearch('class="name_song">(.+?)</a>',s)
		cs=xsearch('target="_blank">(.+?)</a>',s)
		title=title+' - '+'[COLOR green]%s[/COLOR]'%cs
		count=counter.get(xsearch('id="NCTCounter_pl_(\d+)"',s))
		if count:title+=' [COLOR gold](%s)[/COLOR]'%'{0:,}'.format(int(count)).replace(',','.')
		href=xsearch('href="(.+?)"',s)
		img=xsearch('data-src="(.+?)"',s)
		return title,href,img
		
	def getPage_pl(self,url):
		b=xread(url);items=[]
		if '<div class="box_cata_control">' in b:b=b[b.find('<div class="box_cata_control">'):]
		counter=self.getCounter_pl(b)
		
		for s in [i for i in re.findall('(<li.+?/li>)',b,re.DOTALL) if '<div class="info_album">' in i]:
			items.append((self.getDetail_pl(s,counter)))
			
		i=self.pageControl(b)
		if i:items.append((i))

		return items
	
	def getPlayList(self,url):
		b=xread(url);items=[]
		counter=self.getCounter_sg(b)
		
		xml=[i for i in xread(xsearch('xmlURL.{,10}"(.+?)"',b),self.headers).split('<track>') if '<title>' in i]
		for i in xml:
			title=self.getData(i,'title')
			creator=self.getData(i,'creator')
			if creator:title=title+' - '+'[COLOR green]%s[/COLOR]'%creator
			href=self.getData(i,'locationHQ')
			count=counter.get(xsearch('-(\d+)\.',href))
			if count:title+=' [COLOR gold](%s)[/COLOR]'%fmn(count)
			img=self.getData(i,'avatar')
			items.append((title,href,img))
		
		s=xsearch('(begin div list_album.+?end div list_album)',b,1,re.DOTALL)
		s=xsearch('<a title="(.+?)"',s)
		if s:items.append(('[COLOR lime]----%s----[/COLOR]'%s,'',''))
		for s in [i for i in re.findall('(<li.+?/li>)',b,re.DOTALL) if '<div class="info_album">' in i]:
			items.append((self.getDetail_pl(s,counter)))
		
		i=self.pageControl(b)
		if i:items.append((i))
		
		return items	
		
	def getSukien(self,url):
		b=xread(url);items=[]
		for s in re.findall('(<li class="event".+?/li>)',b,re.DOTALL):
			title=xsearch('class="name_event">(.+?)<',s)
			href=xsearch('href="(.+?)"',s)
			img=xsearch('src="(.+?)"',s)
			fanart=xsearch('title="%s" src="(.+?)"'%title,b)
			items.append((title,href,img,fanart))
		
		return items
	
	def listSukien(self,url):
		b=xread(url);items=[]
		for s in re.findall('(<div class="ti\w{,3}_box.+?/ul>)',b,re.DOTALL):
			for s in re.findall('(<li.+?/li>)',s,re.DOTALL):
				title=xsearch('alt="(.+?)"',s)
				label=xsearch('"name_singer">([^<]+?)<',s)
				if label:title+=' [COLOR blue]%s[/COLOR]'%label
				label=xsearch('"icon_time_video">([^<]+?)<',s)
				if label:title+=' [COLOR green]%s[/COLOR]'%label
				label=xsearch('"icon_view">([^<]+?)<',s)
				if label:title+=' [COLOR gold]%s[/COLOR]'%label
				href=xsearch('href="(.+?)"',s)
				img=xsearch('src="(.+?)"',s)
				items.append((title,href,img))
		
		return items
	
	def getNghesi(self,url):
		b=xread(url);items=[]
		
		s=xsearch('(<ul class="list-singer-item">.+?<div class="tevi_iframe">)',b,1,re.DOTALL)
		for s in re.findall('(<li.+?/li>)',s,re.DOTALL):
			title=xsearch('title="(.+?)"',s)
			href=xsearch('href="(.+?)"',s).replace('.html','.bai-hat.html')
			img=xsearch('data-src="(.+?)"',s)
			items.append((title,href,img))
		
		return items
	
	def getBXH(self,url):
		b=xread(url);counter=self.getCounter_sg(b);items=[]
		items.append(('[COLOR lime]----%s----[/COLOR]'%xsearch('<title>(.+?)</title>',b),url,''))
		for s in [i for i in re.findall('(<li.+?/li>)',b,re.DOTALL) if '<div class="box_info_field">' in i]:
			items.append((self.getDetail_sg(s,counter)))
		return items
			
	def getPage_video(self,url):
		b=xread(url);counter=self.getCounter_sg(b);items=[]
		for s in [i for i in b.split('"title_of_box_video"') if '"btn_view_select"' in i]:
			title=xsearch('title="(.+?)"',s);href=xsearch('href="(.+?)"',s)
			if title and href:items.append(('[COLOR lime]%s[/COLOR]'%title,href,'link'))
			for s in [i for i in re.findall('(<li.+?/li>)',s,re.DOTALL) if 'class="box_absolute"' in i]:
				items.append((self.getDetail_sg(s,counter,'video')))

		i=self.pageControl(b)
		if i:items.append((i))
		
		return items
	
	def getPage_hero(self,url):
		b=xread(url);counter=self.getCounter_pl(b);items=[]
	def getPage_hero(self,url):
		b=xread(url);counter=self.getCounter_pl(b);items=[]
		s=xsearch('(<div class="list_album".+?/ul>)',b,1,re.DOTALL)
		for s in [i for i in re.findall('(<li.+?/li>)',b,re.DOTALL) if '<div class="info_album">' in i]:
			items.append((self.getDetail_pl(s,counter)))
			
		i=self.pageControl(b)
		if i:items.append((i))
			
		return items
		
	def getPage_hero_10(self,url):
		b=xread(url);counter=self.getCounter_pl(b);items=[]
		for s in [i for i in b.split('class="box_absolute"') if '"label_week"' in i]:
			for s in re.findall('(<li.+?/li>)',xsearch('(<ul.+?/ul>)',s,1,re.DOTALL),re.DOTALL):
				title=xsearch('title="(.+?)"',s)
				href=xsearch('href="(.+?)"',s)
				img=xsearch('src="(.+?)"',s)
				items.append((title,href,img))
		
		return items

class vietsubhd:
	def __init__(self,c):
		self.hd={'User-Agent':'Mozilla/5.0','Cookie':''}
		self.c=c
	
	def detail(self,s):
		title=xsearch('title="(.+?)"',s)
		label=xsearch('"status">(.+?)<',s)
		if label:title+=' [COLOR blue]%s[/COLOR]'%label
		label=xsearch('<div class="eps">(.+?)</div>',s)
		if label:title+=' [COLOR yellow]%s[/COLOR]'%label
		year=xsearch('<dfn>(\d+?)<',s)
		if year:title+=' [COLOR gold]%s[/COLOR]'%year
		views=xsearch('"play-icon">(\d+?)<',s)
		if views:title+=' [COLOR green]%s[/COLOR]'%views
		time=xsearch('"video-time">(.+?)<',s)
		if time:title+=' [COLOR yellow]%s[/COLOR]'%time
		href=xsearch('href="(.+?)"',s)
		img=xsearch('src="(.+?)"',s)
		if not img:img=xsearch('(http[^<]+jpg)',s).replace('w35-h35','w180-h200').replace('Poster.','')
			
		return title,href,img
	
	def eps(self,url):
		b=xread(url);items=[]
		for s in [i for i in b.split('<i class="fa fa-database">') if 'class="episodes' in i]:
			label=xsearch('</i>(.+?)</div>',s).strip()
			if label:label='[COLOR gold]%s[/COLOR] '%label
			items+=[(label+i[1],i[0],i[2]) for i in re.findall('href="([^"]+?)" title="([^"]+?)" id="(\d+?)"',s)]
		items=[(i[0],xsearch('-(\d+?)/',i[1])+'-'+i[2]) for i in items]
		
		if not items:
			b=xread(url.replace('xem-phim.html',''));yt=xsearch('"([^"]+youtube.com[^"]+)"',b)
			if yt:items=[('[COLOR gold]Bản Trailer[/COLOR]',yt)]
			
		return items
	
	def page(self,url):
		b=xread(url);items=[]
		if '/videos' in url:
			for s in [i for i in b.split('<div class="column medium-4') if '<div class="box">' in i]:
				items.append((self.detail(s)))
		else:
			for s in re.findall('(<a class="poster".+?/div>)',b):items.append((self.detail(s)))
				
		pn=xsearch('class="current".+?<a href="([^"]+?)"[^<]*?>\d+<',b)
		if pn:
			pages=xsearch('-(\d+)\.html" title="Trang cuối">',b)
			title='[COLOR lime]Page next: page/%s[/COLOR]'%pages
			items.append((title,pn,''))

		return items

	def uncode(self,s):
		k="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
		s=urllib.unquote(s);l=len(s);i=0;result=""
		while i < l:
			x9 = k.index(s[i]);i+=1
			xa = k.index(s[i]);i+=1
			xb = k.index(s[i]);i+=1
			xc = k.index(s[i]);i+=1
			x6 = ((x9 & 0x3F)<< 2) | ((xa >> 4) & 0x3)
			x7 = ((xa & 0xF ) << 4) | ((xb >> 2) & 0xF)
			x8 = ((xb & 0x3 ) << 6) | (xc & 0x3F)
			result += chr(x6) + (chr(x7) if x7 else '') + (chr(x8) if x8 else '')
		
		return result
	
	def decode(self,s):
		s=self.uncode(s);xf="VSHDKeyRandom30042016";result=""
		for i in range(len(s)):
			x10=s[i];x11=xf[i%len(xf)-1];x12=ord(x10[0]);x13=ord(x11[0]);x14=x12-x13;x10=chr(x14);result+=x10
		
		return result
		
	def maxLink(self,url):
		if 'id=' in url:filmID,episodeID=url.replace('id=','').split('-')
		else:
			b=xread(url)
			filmID=xsearch("filmInfo.filmID = parseInt\('(.+?)'\)",b)
			episodeID=xsearch("filmInfo.episodeID = parseInt\('(.+?)'\)",b)
		s=xread('http://www.vietsubhd.com/ajaxload',data='NextEpisode=1&EpisodeID=%s&filmID=%s'%(episodeID,filmID))
		#link=xsearch('link:"(.+?)"',self.decode(s))
		link=xsearch('link:"(.+?)"',s)
		b=xread('http://www.vietsubhd.com/gkphp/plugins/gkpluginsphp.php',data='link=%s'%link);items=[]
		
		try:j=json.loads(b)#;print j
		except:j={}
		if j.get('link'):
			if type(j.get('link'))==unicode:items=[(j.get('link'),'720')]
			else:items=[(i.get('link'),rsl(i.get('label'))) for i in j.get('link')]
		elif j.get('list'):
			for j in j.get('list',[]):
				for i in j.get('link'):items.append((i.get('link'),rsl(i.get('label'))))
		r=True if get_setting('resolut')=='Max' else False
		items=sorted(items, key=lambda k: int(k[1]),reverse=r)
		link=''
		for href,label in items:
			link=xcheck(href)
			if link:break
		return link
	
class hdonline:
	def __init__(self,c):
		self.c=c;self.home='http://hdonline.vn'
		cookie=xrw('hdonline.cookie')
		self.userID=xsearch('userID=(\d+)',cookie)
		self.hd={'User-Agent':'Mozilla/5.0','Accept': 'json','Cookie':cookie,'Referer': self.home}
	
	def page(self,url):
		b=xread(url) if len(url)<100 else url
		items=[self.getDetail(s) for s in re.findall('(<aside.+?</div>)',b,re.S)]
		
		p=xsearch('(<a class="btn btn-alt waves-button waves-effect".+?</div>)',b)
		if p and '"btn btn-flat btn-alt waves-button waves-effect"' in p:
			pn=xsearch('btn btn-alt waves.+?href=.+?href="([^"]+?)">',p)
			pages=xsearch('>(\d+?)</a></p>',p)
			title='[COLOR lime]Trang tiep theo...trang page/%s[/COLOR]'%pages
			items.append((title,pn,'','',''))
		return items

	def getDetail(self,s):
		href=xsearch('href="(.+?)"',s)
		img=xsearch('src="(.+?)"',s)
		title=xsearch('href="[^"]+?" title="[^"]+?">([^"]+?)</a>',s)
		eng=xsearch('<em[^<]+?>(.+?)</em>',s)
		if eng:title=title+' '+eng
		if not title:title=xsearch('<p class="name-en">(.+?)</p>',s)+' '+xsearch('<p class="name-vi">(.+?)</p>',s)
		if re.search('.huyết .inh',title):title='[COLOR blue]TM[/COLOR] '+title
		if re.search('.hụ .ề .iệt',title):title='[COLOR blue]PĐV[/COLOR] '+title
		temp=xsearch('<span title="Chất lượng HD (.+?)"',s)
		if temp:title+=' [COLOR blue]%s[/COLOR]'%temp
		temp=xsearch('<p>Số Tập:(.+?)</p>',s)
		if temp:title+=' [COLOR gold]%s[/COLOR]'%temp
		temp=xsearch('<p>Năm sản xuất:(.+?)</p>',s)
		if temp:title+=' [COLOR yellow]%s[/COLOR]'%temp
		eps=xsearch('class="fa fa-bolt"[^"]+?(\d+?/\d+)',s)
		if eps:title=namecolor(title+' - [COLOR gold]%s[/COLOR]'%eps,self.c);q='eps';dir=True
		else:href=href.replace('m.hdonline','hdonline');q='play';dir=False
		
		return title,href,img,q,dir
	
	def eps(self,id,page):
		b=xread('http://hdonline.vn/episode/ajax?film=%s&episode=&page=%d&search='%(id,page))
		items=[('http://hdonline.vn'+j[0],j[1]) for j in re.findall('href="(.+?)"[^>]+>(\d+)</a>',b)]
		
		pn=xsearch('<a class="active"[^<]+>\d+</a><[^<]+>(\d+)</a>',b)
		if pn:items.append(('[COLOR lime]Các tập tiếp theo...[/COLOR]',pn))
		return items
		
	def like_film(self,url):
		b=xread(url,self.hd)
		try:m=json.loads(b).get('msg');mess(u'%s'%m[:m.find('.')])
		except:pass
	
	def maxLink(self,url):
		items=[];sub=''
		try:
			j=json.loads(xread(url,self.hd))#;print json.dumps(j,indent=2),j.get('subtitle')
			if j.get("audiodub"):mess(u'Phim này có 2 audio','HDonline.vn',10000)
			if j.get('level'):items=ls([(i.get('file'),rsl(i.get('label'))) for i in j.get('level')])
			elif j.get('file'):items=j.get('file')
			
			if j.get('subtitle'):
				for i in j.get('subtitle'):
					if i.get('code').encode('utf-8')=='vi':sub=i.get('file');break
		except:pass
		return items,sub
	
	def getLink(self,url,ep='1'):
		b=xread(url,self.hd)#;xrw('xoa.html',b)
		url='http://hdonline.vn/frontend/episode/xmlplay?ep=%s&fid=%s&token=%s-%s&format=json'
		id=xsearch('-(\d+)\.',url)
		token=xsearch('\|(\w{80,100})\|',b)#+'=='
		rand=xsearch('\|(\d{10,12})\|',b)#;print token,rand
		url=url%(ep,id,token,rand)
		chonserver=addon.getSetting('chonserver')
		if chonserver=='Thuyết minh':url+='&tm=1'
		
		try:j=json.loads(xread(url,self.hd))#;print json.dumps(j,indent=2)
		except:j={}
		items=[];sub=''
		if j.get("audiodub"):mess(u'Phim này có 2 audio','HDonline.vn',10000)
		if j.get('level'):items=ls([(i.get('file'),rsl(i.get('label'))) for i in j.get('level')])
		elif j.get('file'):items=j.get('file')
		
		if j.get('subtitle'):
			for i in j.get('subtitle'):
				if i.get('code').encode('utf-8')=='vi':sub=i.get('file');break
		return items,sub,j.get('image','')

class phimBatHu:
	def __init__(self):
		self.home='http://phimbathu.com'
	
	def getDirectLink(self,url):
		def getLink(s,key):#chonserver values="Thuyết minh|VietSub|Không"
			try:j=json.loads(xsearch('"sources":(\[[^\]]+?\])',s))
			except:j={}
			for i in j:
				try:i['file']=urllib.unquote(gibberishAES(i.get('file',''),key))
				except:pass
			link=googleItems(j,'file','label')
			return link
		
		b=xread(url)
		key="phimbathu.com4590481877"+xsearch("'film_id':'(.+?)'",b)
		chonserver=addon.getSetting('chonserver')
		servers=re.findall('(<a.+?/a>)',xsearch('<ul class="choose-server">(.+?)</ul>',b,1,re.S))
		
		
		playOn=''
		if not servers or chonserver=='Không':
			link=getLink(b,key)
			playOn=xsearch('>([^<]+?)</a>',str([i for i in servers if '"playing"' in i]))
			if not playOn:playOn='Default Server'
			servers=[i for i in servers if '"playing"' not in i]#Loai bo server default trong servers
		else:
			for s in servers:
				title=xsearch('>([^<]+?)</a>',s).upper();found=False
				if 'T MINH' not in title and 'VIETSUB' not in title:found=True;break
				elif chonserver=='Thuyết minh' and 'T MINH' in title:found=True;break
				elif chonserver=='VietSub' and 'VIETSUB' in title:found=True;break
			
			if found:servers=[i for i in servers if i!=s]#Loai bo server hien tai trong servers

			if '"playing"' not in s:url=self.home+xsearch('href="(.+?)"',s);b=xread(url)
			playOn=xsearch('>([^<]+?)</a>',s)
			link=getLink(b,key)

		if not link:
			mess('get next servers','phimbathu.com') 
			for s in servers:
				link=getLink(xread(self.home+xsearch('href="(.+?)"',s)),key)
				playOn=xsearch('>([^<]+?)</a>',s)
				if link:break
		
		if not link:
			playOn='Backup Server'
			mess('get bakup servers','phimbathu.com') 
			s=xsearch('<ul class="server-backup"(.+?)</ul>',b,1,re.S)
			strings=re.findall('link="([^"]+?)"',s)
			for s in strings:
				href=self.home+urllib.unquote(gibberishAES(s,key));print 'ccc',href
				b=xread(href)
				try:link=googleItems(json.loads(b),'file','label')
				except:pass
				if link:break
				
		if link:
			try:mess(u'Play on: '+playOn.decode('utf-8'))
			except:pass
		else:mess('File invalid or deleted!','phimbathu.com')
		
		return link
		
class mphim:
	def __init__(self,c):
		self.c=c;self.home='http://mphim.net'
		cookie=xrw('mphim.cookie')
		self.userID=xsearch('userID=(\d+)',cookie)
		self.hd={'User-Agent':'Mozilla/5.0','Accept': 'json','Cookie':cookie,'Referer': self.home}
	
	def detail(self,i):
		title=xsearch('<span class="title">(.+?)</span>',i)
		t=xsearch('<span class="moreinfo">(.+?)</span>',i)
		if t:title+=' [COLOR blue]%s/[/COLOR]'%t
		tl=xsearch('>Thời lượng: </span>(.+?)</p>',i);dir=False
		if 'phút' not in tl.lower() or 'tập' in tl.replace(' ','').lower():
			title+='[COLOR blue]%s[/COLOR]'%tl;dir=True
		elif tl:title+=' [COLOR blue]%s[/COLOR]'%tl
		likes=xsearch('<p class="like"><span>(.+?) likes</span>',i)
		if likes:title+=' [COLOR green]%s[/COLOR]'%likes
		href=xsearch('href="(.+?)"',i)
		if not href:href=xsearch('title="(.+?)"',i)
		if 'http' not in href:href='http://mphim.net'+href
		img=xsearch('data-original="(.+?)"',i)
		
		return title,href,img,dir
		
	def page(self,url):
		b=xread(url);s=xsearch('(<ul class="list_m".+?/ul>)',b,1,re.S)
		items=[self.detail(i) for i in re.findall('(<li.+?/li>)',s,re.S)]
		
		s=xsearch('(<div class="paging".+?/div>)',b,1,re.S);found=False;pn='';pages=''
		for i in s.splitlines():
			if 'class="current"' in i:found=True
			elif found and not pn:
				pn=xsearch('href="(.+?)"',i)
				if pn and 'http' not in pn:pn='http://mphim.net'+pn
			elif found:
				j=xsearch('<a href=".+?">(\d+)</a>',i)
				if j :pages=j
		if pn:
			title='[COLOR lime]Page next: page/%s[/COLOR]'%pages
			items.append((title,pn,'',''))

		return items

	def eps(self,url):
		b=xread(url.replace('/phim/','/xem-phim/'))
		s=xsearch('(<p class="epi".+?/p>)',b,1,re.S)
		l=re.findall('href="([^"]+?)" title="([^"]+?)">(\d+)</a>',s)
		return [(i[2]+'-'+i[1],'http://mphim.net'+i[0]) for i in l]
	
	def maxLink(self,url):
		items=[]
		try:
			b=xread(url.replace('/phim/','/xem-phim/'))
			s=xsearch('setup\((\{.+?\})\)',b,1,re.S).replace('\n','').replace('sources','"sources"')
			s=eval(s.replace('file','"file"').replace('label','"label"').replace('type','"type"'))
			items=ls([(i.get('file'),rsl(i.get('label'))) for i in s.get('sources')])
		except:mess('Get maxLink error !')
		return items

class phim47com:
	def __init__(self,c):
		self.hd={'User-Agent':'Mozilla/5.0'}
		self.urlhome='http://phim47.com/'

	def maxLink(self,url):
		b=xread(url);j=refa('<jwplayer:source (.+?)/>',b)
		l=ls([(xsearch('file="(.+?)"',i),rsl(xsearch('label="(.+?)"',i))) for i in j])
		sub=xsearch('file="([^"]+?)" label="Tiếng Việt"',b)
		return l,sub
	
	def getEPS(self,url):
		b=xread(url)
		#for s in refa('id="xemphimus" href="(http://phim47.com.+?)"',b):
		#	
	def getLink(self,url):
		link=sub='';b=xread(url)
		for s in refa("playlist':.?'(.+?)'",b):
			s=xread(s)
			sub=xsearch('track file="(.+?)" label="Tiếng Việt"',s)
			j=refa('<jwplayer:source (.+?)/>',s)
			for href,r in ls([(xsearch('file="(.+?)"',i),rsl(xsearch('label="(.+?)"',i))) for i in j]):
				g=xget(href.replace('amp;',''))
				if g:link=g.geturl();break
		if not link:link=xsearch('iframe.+?src="(http.?://www.youtube.com.+?)"',b)
		return link,sub
	
	def getDetail(self,s):
		tm=xsearch('(<span class="thuyetminh">)',s) or xsearch('(title="Audio Việt")',s)
		series=xsearch('class="bo[^"]*?">(.*?)</span>',s)
		views=xsearch('>(\d+)</span>',s)
		href=xsearch('<a href="(.+?)"',s)
		title=xsearch('alt="(.+?)"',s)
		img=xsearch('(http://img.phim47.com/[^"]+?\.jpg)',s)
		if tm:title=title+' [COLOR gold]TM[/COLOR]'
		if series:title+='[COLOR gold]%s[/COLOR]'%series
		if views:title+=' [COLOR blue]%s[/COLOR] '%views
		if 'http://' not in href:href=self.urlhome+href 
		return title,href,img
	
	def getItems(self,s):
		items=[]
		for i in [j for j in refa('(<li>.+?</li>)',s,re.S) if "menuTitle" in j]:
			items.append(self.getDetail(i))
		return items
			
	def xemnhieu(self,s):
		items=[]
		for i in refa('<div class="l_episode">(.+?)</span>',s,re.S):
			title=xsearch('title="(.+?)"',i)
			href=xsearch('href="(.+?)"',i)
			img=xsearch('src="(.+?)"',i)
			items.append((title,href,img))
		return items	

class vtvgovn:
	def __init__(self,c):
		self.hd={'User-Agent':'Mozilla/5.0','Cookie':xrw('vtvgo.cookie')}
		self.urlhome='http://vtvgo.vn/'

	def liveGoList(self,url):
		def e(i):return i.get('name').encode('utf-8'),i.get('id').encode('utf-8'),i.get('thumbnailUrl').encode('utf-8')
		b=xread(url,self.hd)
		try:j=json.loads(b)
		except:j=[{},[]]
		return [e(i) for i in j[1]]
	
	def cat02(self,url):
		b=xread(url);items=[]
		for s in ['<h3 class="'+i for i in b.split('<h3 class="') if xsearch('>([^<]+?)</a></h3>',i)]:
			items.append((xsearch('>([^<]+?)</a></h3>',s),'sep',''))
			for s in [i for i in s.split('<div class="item">') if '"icon-play"' in i]:items.append(self.detail(s))
		return items
	
	def cat03(self,url):
		b=xread(url);items=[]
		for s in ['<h3 class="'+i for i in b.split('<h3 class="') if '</h3>'in i]:
			items.append((xsearch('<h3 class="s_title">([^<]+?)</h3>',s),'sep',''))
			for s in [i for i in s.split('<div class="item">') if '"icon-play"' in i]:items.append(self.detail(s))
		return items
	
	def vodList(self,url):
		def e(i):return i.get('name').encode('utf-8'),i.get('downloadUrl').encode('utf-8'),i.get('thumbnailUrl').encode('utf-8')
		b=xread(url,self.hd)
		try:j=json.loads(b)
		except:j=[{},[]]
		return [e(i) for i in j[1]]
	
	def liveList(self):
		def detail(s):return xsearch('title="(.+?)"',s),xsearch('href="(.+?)"',s),xsearch('src="(.+?)"',s)
		b=xget(self.urlhome)
		if b and b.getcode()==200:
			xrw('vtvgo.cookie',b.headers.get('Set-Cookie'));b=b.read()
			if xsearch("else window.location.href = '(.+?)'",b):
				b=xread(xsearch("else window.location.href = '(.+?)'",b))
		else:b=''
		
		title=xsearch('title content="(.+?)"',b)
		href=xsearch('url content="(.+?)"',b)
		img=xsearch('image content="(.+?)"',b)
		items=[self.detail(i) for i in b.split('class="item"') if 'class="play-icon"' in i]
		if href!="http://vtvgo.vn/" and href not in items:items.append((title,href,img))
		return sorted(items, key=lambda k: k[1])
	
	def cat41(self,url):
		url='http://cdnapi.kaltura.com/api_v3/index.php?service=multirequest&apiVersion=3.1&expiry=86400&clientTag=kwidget%3Av2.44&format=1&ignoreNull=1&action=null&1:service=session&1:action=startWidgetSession&1:widgetId=_2111921&2:ks=%7B1%3Aresult%3Aks%7D&2:service=playlist&2:action=execute&2:id=1_by8rxnyv&kalsig=ad9291d0921fec4bcf6bc406a5d0c752'
		return self.liveGoList(url)
	
	def live(self,id):
		url='http://vtvgo.vn/get-program-channel?epg_id=%s&type=1'%id
		try:link=json.loads(xread(url,self.hd)).get('data','')
		except:link=''
		print link
		return link

	def detail(self,s):
		title=xsearch('title="(.+?)"',s)
		if not title:title=xsearch('alt="(.+?)"',s)
		href=xsearch('href="(.+?)"',s)
		img=xsearch("data-bg='(.+?)'",s)
		if not img:img=xsearch('src="(.+?)"',s)
		return title,href,img
	
	def news(self,url,page):
		items=[]
		b='\n'.join([xread(url%i,self.hd) for i in range(page,page+5)])
		for s in [i for i in b.split('<div class="box-img') if '"icon-play"' in i]:
			items.append(self.detail(s))
		return items

	def gameshows(self,url):
		b=xread(url,self.hd)
		
		
	def category(self,url):
		def detail(s):return xsearch('"title">(.+?)<',s),xsearch('href="(.+?)"',s),xsearch('src="(.+?)"',s)
		def filter(s):return '"slider_shadow"' in s or 'class="icon-play"' in s
		b=xread(url,self.hd);items=[]
		for s in [i for i in b.split('row fix-row label-news-page') if '<h2>' in i]:
			items.append((xsearch('<h2>(.+?)</h2>',s),'sep',''))
			items+=[detail(i) for i in s.split('<div class="item ') if filter(i)]
		return items
	
	def vodLink(self,url):
		return xsearch('(http.+?m3u8)',xread(url,self.hd))
	
	def golive(self,url,l='04'):
		c='VTV6' if url=='1_rhex2pfs' else 'VTV3'
		b=xread('https://drive.google.com/folderview?id=0B5y3DO2sHt1LWnJSTDBBRkZNZEU')
		url=xread(urllib2.base64.b64decode(xsearch('<title>(.+?)</title>',b).split(' ')[1])%url)
		try:url=json.loads(url).get('flavors')[0].get('url')
		except:url=''
		
		t=xsearch('(\w{40,50})',url)
		d1='http://vtvgoeuroobj.b5695cde.cdnviet.com'
		d2='Content/HLS/Live/Channel(%s)/Stream(%s)/index.m3u8'
		s=['#EXTM3U\n#EXT-X-VERSION:4\n#EXT-X-ALLOW-CACHE:YES\n']
		s+='#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio",NAME="und",DEFAULT=YES,AUTOSELECT=YES,'
		s+='URI="%s/%s/%s"\n'%(d1,t,d2%(c,'05'))
		if l=='01':r='640x360';b='680243'
		elif l=='02':r='854x480';b='1497634'
		elif l=='03':r='1024x576';b='1906330'
		else:r='1280x720';b='2315025'
		
		s+='#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=%s,RESOLUTION=%s,AUDIO="audio"\n'%(b,r)
		s+='%s/%s/%s\n'%(d1,t,d2%(c,l))
		url=xrw('vtv.m3u8',''.join(s))
		return url
		
	def golive6(self,url):
		b=xread('https://drive.google.com/folderview?id=0B5y3DO2sHt1LWnJSTDBBRkZNZEU')
		url=xread(urllib2.base64.b64decode(xsearch('<title>(.+?)</title>',b).split(' ')[1])%url)
		try:
			url=xget(json.loads(url).get('flavors')[0].get('url')).geturl()
			s='\n'.join(l for l in xread(url).replace('Stream',urllib2.os.path.dirname(url)+'/Stream').splitlines() if l)
			url=xrw('vtv.m3u8',s)
		except:url=''
		return url
		
	def golive0(self,url):
		b=xread('https://drive.google.com/folderview?id=0B5y3DO2sHt1LWnJSTDBBRkZNZEU')
		url=xread(urllib2.base64.b64decode(xsearch('<title>(.+?)</title>',b).split(' ')[1])%url)
		try:url=xget(json.loads(url).get('flavors')[0].get('url')).geturl()
		except:url=''
		return url
		base=urllib2.os.path.dirname(url)
		for i in xread(url).splitlines():
			if link in i:link='OK';continue
			elif i and link=='OK':link=i;break
		link=base+'/'+link
		
	def golive1(self,url):
		url='http://cdnapi.kaltura.com/p/2111921/sp/211192100/playManifest/entryId/'+url
		url+='/format/applehttp/protocol/http/uiConfId/35084022/index.m3u8?referrer=aHR0cDovL3Z0dmdvLnZu&'
		url+='playSessionId=&responseFormat=%s&callback='
		try:
			base=urllib2.os.path.dirname(json.loads(xread(url%'json')).get('flavors')[0].get('url'))
			b=xread(url%'xml');link='1024'
			for i in b.splitlines():
				if link in i:link='OK';continue
				elif i and link=='OK':link=i;break
			link=base+'/'+link
		except:link=''
		return link
		
	def golive1(self,url):
		#b=xread('https://drive.google.com/folderview?id=0B5y3DO2sHt1LajFDalU2U05GX28')
		#b=xread(urllib2.base64.b64decode(xsearch('<title>(.+?)</title>',b))%url)
		b='http://cdnapi.kaltura.com/p/2111921/sp/211192100/playManifest/entryId/%s/format/applehttp/protocol/http/uiConfId/35084022/index.m3u8?referrer=aHR0cDovL3Z0dmdvLnZu&playSessionId=236fb9c2-70c2-50c1-e15d-a812189598b8&responseFormat=jsonp&callback=jQuery111109580692829438424_1465981277141&mediaType=201'
		b=xread(b%url)
		try:
			b=xget(json.loads(xsearch('\((\{.+?\})\)',b)).get('flavors')[0].get('url'))#;print b
			if b and b.getcode()==200:
				href=b.geturl()#;print href
				b=xread(href);link='854'
				for i in b.splitlines():
					if link in i:link='OK';continue
					if link=='OK' and i:link=i;break
				link=urllib2.os.path.dirname(href)+'/'+link
			else:link=''
		except:link=''
		return link
	
	def golive_f4m(self,url='1_rhex2pfs'):
		url=json.loads(xread('http://cdnapi.kaltura.com/p/2111921/sp/211192100/playManifest/entryId/%s/format/hdnetworkmanifest/protocol/http/uiConfId/35084022/?referrer=aHR0cDovL3Z0dmdvLnZu&responseFormat=json'%url)).get('flavors')[0]['url']
		
		#url='http://vtvgoeuroobj.04477775.sabai.vn/64aa5d03694d469b23382af99d4746621466325887/Content/HDS/Live/Channel(VTV6)/manifest.f4m'
		b=urllib2.urlopen(url)
		url=b.geturl().replace('.f4m','')
		#return 'http://vtvgoeuroobj.b5695cde.cdnviet.com/a9b5697eb19288806f6ceb661f7fdc6b1466332250/Content/HDS/Live/Channel(VTV6)/Stream(manifest_1200)/manifest.bootstrap?g=WBPGLZKANOKW&hdcore=3.1.0&plugin=aasp-3.1.0.43.124?swfUrl=http://vtvgo.vn/public/js/plugin/jwplayer/jwplayer.flash.swf&pageUrl=http://vtvgo.vn/euro2016/live.html'
		#return 'rtmp://vtvgoeuroobj.b5695cde.cdnviet.com/Content/HDS/Live/Channel(VTV6)/manifest.f4m?ks=djJ8MjExMTkyMXwaLOyQmTgyudBssKQJeLOIJYT5VmR40jQx7FPKd_msL5HQKwOLvPuopVF3CjiLspwzyX_gidcnALuP99F6m_luYv3hpM2ZqilaO5PXiqFaKw=='+ ' swfUrl=http://vtvgo.vn/public/js/plugin/jwplayer/jwplayer.flash.swf pageUrl=http://vtvgo.vn/euro2016/live.html'
		#return 'http://vtvgoeuroobj.b5695cde.cdnviet.com/a46eda7b32a7bc4b801b5d153b51029a1466429037/Content/HDS/Live/Channel(VTV6)/Stream(manifest_400)/manifest.bootstrap?g=UWOYDGHGGRPW&hdcore=3.1.0&plugin=aasp-3.1.0.43.124 '+ ' swfUrl=http://vtvgo.vn/public/js/plugin/jwplayer/jwplayer.flash.swf pageUrl=http://vtvgo.vn/euro2016/live.html'
		return url
		
	def temp(self):
		u='http://cdnapi.kaltura.com/p/2111921/sp/211192100/playManifest/entryId/1_rhex2pfs/format/applehttp/protocol/http/uiConfId/35084022?referrer=aHR0cDovL3Z0dmdvLnZu&responseFormat=jsonp&callback='


		u='http://cdnapi.kaltura.com/api_v3/index.php?service=multirequest&apiVersion=3.1&expiry=86400&clientTag=kwidget%3Av2.44&format=1&ignoreNull=1&action=null&1:service=session&1:action=startWidgetSession&1:widgetId=_2111921&2:ks=%7B1%3Aresult%3Aks%7D&2:service=playlist&2:action=execute&2:id=1_by8rxnyv&kalsig=ad9291d0921fec4bcf6bc406a5d0c752'
		
		play='http://cdnapi.kaltura.com/html5/html5lib/v2.6.3/mwEmbedFrame.php/p/2111921/uiconf_id/35084022/entry_id/1_rhex2pfs?wid=_2111921&iframeembed=true&playerId=kaltura_player_1411138624&entry_id=1_rhex2pfs&flashvars'

class phimMedia:
	def maxLink(self,url):
		body=xread(url)
		s=xsearch('sources: (\[[^\[]+?\])',body)
		for i in re.findall('(\w+):.?"',s):s=s.replace("%s:"%i,'"%s":'%i)
		try:items=ls([(i.get('file',''),rsl(i.get('label',''))) for i in eval(s)])
		except:items=[]
		return items

class k88com:
	def __init__(self,c):
		self.hd={'User-Agent':'Mozilla/5.0'}
		self.urlhome='http://www.kenh88.com/'
		
	def getDetail(self,s):
		tap=xsearch('class="process_r">([^<]+?)</span>',s)
		res=xsearch('class="status">([^<]+?)</span>',s)
		href='%sxem-phim-online/%s'%(self.urlhome,os.path.basename(xsearch('href="/([^"]+?)"',s)))
		title=xsearch('href="[^"]+?">([^<].+?)</a>',s)+'-'+xsearch('href="[^"]+?">[^<]+?</a>([^<]+?)</h2>',s)
		title=' '.join(title.split())
		if res:title+='[COLOR blue]-%s[/COLOR]'%res
		if tap:title+='[COLOR gold]-%s[/COLOR]'%tap
		img=self.urlhome+urllib2.quote(xsearch('src="/([^"]+?)"',s))
		return tap,href,title,img
	
	def episode(self,url):
		b=xread(url.replace('/phim/','/xem-phim-online/'));d={};count=0
		items=refa('(class="server".+?</ul>)',b,re.S)
		if items:
			for s in items:
				count+=1
				i=xsearch('</i>(.+?)</div>',s).replace(':','')
				i='No name' if not i else '%d-%s'%(count,i)
				d[i]=[(self.urlhome+j[0],'Tập '+j[1]) for j in refa('<a href="/(.+?)"\s.+?>([^<]+?)</a>',s)]
		else:
			d['No name']=[]
			for s in refa("(<div class=''.+?<h2>.+?</div>)",b,re.S):
				tap,href,title,img=self.getDetail(s)
				d['No name'].append((tap,href))
		
		href=xsearch('class="next" href="/(.+?)\?',b)
		if href:
			pages=xsearch('>(\d{,4})</a></li><li><span>',b)
			#title=namecolor(name,c)+color['trangtiep']+' Trang tiep theo...trang %d/%s[/COLOR]'%(page+1,pages)
			#addir_info(title,urlhome+href,ico,'',mode,page+1,query,True)
		return d
	
	def getPage(self,url):
		b=xread(url)
		s=refa("<div class='(.+?)</div>\s",b,re.S)
		items=[self.getDetail(i.replace('\n','')) for i in s]

		pn=xsearch('class="next" href="/(.+?)\?',b)
		if pn:
			pages=xsearch('>(\d{,4})</a></li><li><span>',b)
			items.append((pages,self.urlhome+pn.replace('/page/','?page='),'pageNext',''))
		return items
	
	def getLink(self,url):
		response=xread(url);link=''
		href=xsearch('\{link:.*"(.+?)"\}',response)
		if len(href)>20:
			data=urllib.urlencode({'link':href});label=0
			jp=xread('http://www.kenh88.com/gkphp/plugins/gkpluginsphp.php',data=data)
			try:j=json.loads(jp).get('link')
			except:j={}
			if isinstance(j,unicode):items=[(j,'')]
			else:items=ls([(i.get('link'),rsl(i.get('label'))) for i in j])
			for href,r in items:
				link=xcheck(href.replace('amp;',''))
				if link:break
		
		elif xsearch('src="(.+?docid=.+?)"',response):
			docid=xsearch('docid=(.+?)&',response)
			if docid:
				link='https://docs.google.com/get_video_info?authuser=&eurl=%s&docid=%s'
				link=link%(urllib.quote_plus(url),docid)
				response=xread(link)
				link=xsearch('url_encoded_fmt_stream_map(.+?)\Z',response)
				link=xsearch('url=(.+?)&type=',urllib.unquote(urllib.unquote(link)))
		
		elif xsearch('iframe src="(.+?)"',response):
			b=xread(xsearch('iframe src="(.+?)"',response))
			l=re.findall('file: "([^"]+?)"[^"]+label: "([^"]+?)"',b,re.S)
			for href,r in ls([(i[0],rsl(i[1])) for i in l]):
				link=xcheck(href.replace('amp;',''))
				if link:break
		return link

class fcinenet:
	def __init__(self):
		self.hd={'User-Agent':'Mozilla/5.0','X-Requested-With':'XMLHttpRequest'}
		self.cookie=xrw('fcine.cookie')
		if not self.cookie or filetime('fcine.cookie')>1:self.cookie=self.login()
	
	def login(self):
		auth=addon.getSetting('fcine_user');pw=addon.getSetting('fcine_pass')
		headers={'Cookie':'ips4_IPSSessionFront=xshare'}
		url='http://fcine.net/login/'
		try:cookie=urllib2.urlopen(urllib2.Request(url,'',headers)).read()
		except:cookie=''
		csrfKey=xsearch('name="csrfKey" value="(.+?)"',cookie)
		data={'csrfKey':csrfKey,'auth':auth,'password':pw,
			  'login__standard_submitted':'1','remember_me':'0','remember_me_checkbox':'1'}
		cookie=urllib2.HTTPCookieProcessor()
		opener=urllib2.build_opener(cookie)
		urllib2.install_opener(opener)
		opener.addheaders=headers.items()
		try:opener.open(url,urllib.urlencode(data))
		except:pass
		cookie=';'.join('%s=%s'%(i.name,i.value) for i in cookie.cookiejar if 'ips4' in i.name)
		if 'ips4_pass_hash' in cookie:
			mess(u'Login thành công','fcine.net')
			xrw('fcine.cookie',cookie)
		else:mess(u'Login không thành công!','fcine.net')
		return cookie
	
	def lisItem(self,s):
		S=re.findall('(<div class="esnList_item".+?/ul>)',s,re.S)
		if not S:S=re.findall('(<li.+?/li>)',s,re.S)
		items=[]
		for s in S:
			title=xsearch("title='(.+?)'",s,result=xsearch('title="(.+?)"',s)).replace('&#039;',"'")
			href=xsearch('href="(.+?)"',s)
			if not title or not href:continue
			if 'HDRip.png' in s:title+=' [COLOR orange]HDRip[/COLOR]'
			elif 'Bluray.png' in s:title+=' [COLOR orange]Bluray[/COLOR]'
			elif 'WEBrip.png' in s:title+=' [COLOR orange]WEBrip[/COLOR]'
			elif 'WEB-DL.png' in s:title+=' [COLOR orange]WEB-DL[/COLOR]'
			img=xsearch('src="(.+?)"',s)
			items.append((title,href,img))
		return items
	
	def pageItems(self,url):
		b=xread(url,self.hd).replace('\\n','').replace('\\t','').replace('\\r','')
		try:j=json.loads(b)
		except:j={}
		items=self.lisItem(j.get('rows','').encode('utf-8'))
		
		pagination=j.get('pagination','').replace('&amp;','&').encode('utf-8')
		p=xsearch("data-page='(\d+)' data-ipsTooltip title='Next page'",pagination)
		if p:
			href=xsearch("href='([^']+?)' data-page='%s'"%p,pagination)
			title='[COLOR lime]Page next: %s[/COLOR]'%p
			if href:items.append((title,href+'&listResort=1',''))
		return items
	
	def getFshare(self,url):
		url='http://fcine.net/?controller=view&do=toggleFields&id=%s'%xsearch('/view/(\d+)-',url)
		b=xread(url,{'Cookie':self.cookie,'X-Requested-With':'XMLHttpRequest'})
		try:j=json.loads(b.replace('\\n','').replace('\\t','').replace('\\r',''))
		except:j={}
		s=j.get('html','').encode('utf-8')
		def check(s):return '<strong>Phụ đề:</strong>' in s or '<strong>Tải phim:</strong>' in s
		s=''.join(i for i in s.split('<li class="ipsDataItem">') if check(i))
		items=[i for i in re.findall('href="(.+?)"[^<]*?>.+?>(.+?)</',s) if i[0] and i[1]]
		items=[(i[0],' '.join(re.sub('<.+?>','',i[1]).split())) for i in items ]
		return items
	
	def getLink(self,url):
		b=xread(url+'?area=online',{'Cookie':self.cookie})
		items=[]
		for s in re.findall('(<ul class="ipsButton_split".+?/ul)',b,re.S):
			server=xsearch('<li.+?>(.+?)</li>',s)
			href=xsearch('href="(.+?)"',s).replace('&amp;','&')
			if not server or not href:continue
			default='ipsButton_important' in s
			items.append((server,href,default))
		
		chonserver=addon.getSetting('chonserver')#"Thuyết minh|VietSub|Không"
		if len(items)<2:pass
		elif len(items)>1 and chonserver=="Không":
			serverChoice=xselect("Chọn server bạn muốn xem phim này",[i[0] for i in items])
			if serverChoice>=0 and not items[serverChoice][2]:
				b=xread(items[serverChoice][1],{'Cookie':self.cookie})
		elif len(items)>1 and chonserver=="Thuyết minh":
			chon=[i for i in items if 'T MINH' in i[0].upper() and not i[2]]
			if len(chon)==1:b=xread(chon[0][1],{'Cookie':self.cookie})
		elif len(items)>1 and chonserver=="VietSub":
			chon=[i for i in items if 'T MINH' not in i[0].upper() and not i[2]]
			if len(chon)==1:b=xread(chon[0][1],{'Cookie':self.cookie})
		
		sub=xsearch('kind="captions" src="(.+?)"',b)
		s=xsearch('(<video.+?/video>)',b.replace('&amp;','&'),1,re.S)
		link=xcheck(ls(re.findall('src="(.+?)".+?data-res="(.+?)"',s)))
		if not link:mess(u'Get Link không thành công! Hãy thử lại','fcine.net')
		return link,sub

class taiphimhdnet:
	def __init__(self):
		self.cookie=xrw('taiphimhdnet.cookie')
		if not self.cookie or 'DRUPAL_UID=' not in self.cookie or filetime('taiphimhdnet.cookie')>10:
			self.cookie=self.login()
		self.hd={'User-Agent':'Mozilla/5.0','Cookie':self.cookie}#,'X-Requested-With':'XMLHttpRequest'}
		self.home='http://taiphimhd.net'
	
	def trueLink(self,link):
		if self.home not in link:link=self.home+link
		return link.replace('&amp;','&')
	
	def login(self):
		name=addon.getSetting('taiphimhdnet_user');pw=addon.getSetting('taiphimhdnet_pass')
		data=urllib.urlencode({'name':name,'pass':pw,'form_id':'user_login'});print data
		url='http://taiphimhd.net/user?destination=http://taiphimhd.net'
		cookie=urllib2.HTTPCookieProcessor()
		opener=urllib2.build_opener(cookie)
		urllib2.install_opener(opener)
		try:
			res=urllib2.urlopen(urllib2.Request(url,data,{'User-Agent': 'xshare'}))
			cookie=';'.join('%s=%s'%(i.name,i.value) for i in cookie.cookiejar)
		except:cookie=''
		if 'DRUPAL_UID=' in cookie:
			xrw('taiphimhdnet.cookie',cookie)
			mess(u'Login thành công','taiphimhd.net')
		else:cookie='';mess(u'Login không thành công!','taiphimhd.net')
		return cookie
	
	def getLinks(self,url):
		b=xread(url,self.hd)
		items=[]
		for s in re.findall('(<div class="dlphimhdvip".+?/ul>)',b,re.S):
			if '>FSHARE<' in s:
				p='http://taiphimhd.net/get-link.html#'
				for m in ['<li>'+i for i in s.split('<li>') if 'href="' in i]:
					title=xsearch('<li>(.+?)<a',m).replace(':','').strip()
					href=xsearch('href="(.+?)"',m).replace(p,'').strip()
					if title and href:
						label=re.sub('<.+?>|\|','',xsearch('<b>(.+?)</b>',m)).strip()
						if label:title=label
						items.append((title,href))
			else:
				for href,title in re.findall('href="(.+?)">(.+?)</a>',s):
					items.append(('[COLOR lime]Phụ đề:[/COLOR] '+title,href))
		
		for href in list(set(re.findall('(https?://subscene.com/[\w|/|-]+)',b))):
			items.append(('[COLOR lime]Phụ đề[/COLOR] ',href))
		return items

	def getDetail(self,b):
		items=[]
		s=xsearch('(<div class="search_solr".+?class="pager")',b,1,re.S)
		for s in s.split('<div class="search_solr"'):
			title=xsearch('<a class="search_title"[^<]+>(.+?)</a>',s,1,re.S).strip()
			href=xsearch('href="(.+?)"',s)
			if not title or not href:continue
			i=xsearch('(<span>Chia sẻ bởi.+?</span>)',s)
			if i:
				j='[COLOR gold]%s[/COLOR]'%xsearch('class="sb_date">(.+?)<',i)
				j+='-[COLOR orange]%s[/COLOR] '%xsearch('>([^<]+?)</a>',i)
				title=j+title
			img=xsearch('src="(.+?)"',s)
			items.append((s2c(title),self.trueLink(href),img))
		return items
	
	def pageNext(self,b,p):
		href=xsearch('<li class="pager-next"><a href="([^"]+?)"',b)
		if href:
			href=self.trueLink(href)
			item=('[COLOR lime]Trang tiếp theo ...%d[/COLOR]'%(p+1),href)
		else:item=''
		return item
	
	def detail(self,s):
		title=xsearch('title="([^"]+?)"',s,result=xsearch('<a href="[^"]+?">([^>]+?)</a>',s))
		href=xsearch('href="(.+?)"',s)
		img=xsearch('src="(.+?)"',s)
		if title and href:
			i=xsearch('<div class="left">([^<]+?)</div>',s)
			if i:title='[COLOR gold]%s[/COLOR] '%i+title
			i=xsearch('Lượt xem.+>([\d|,]+)</',s).replace(',','.')
			if i:title+=' [COLOR gold]%s[/COLOR]'%i
			if self.home not in href:href=self.home+href
			result=s2c(title),href,img
		else:result=''
		return result
	
	def xemnhieu(self,l,d,p):
		l='_phimbo' if l=='phimbo' else ''
		url='http://taiphimhd.net/views/ajax?js=1&view_display_id=block_1&view_path=home&view_base_path='
		url+='phim-xem-nhieu-%s.html&view_name=view_phim_xemnhieu_%s%s&page=%d'%(d,d,l,p-1)
		b=xread(url)
		try:s=eval(re.sub('"status".+?,','',b)).get('display')
		except:s=''
		a='<div class="field-content">'
		items=[i for i in [self.detail(i) for i in s.split('"item-list"')[0].split(a)] if i]
		
		pn=xsearch('<li class="pager-next"><a href="(.+?)"',s).replace('&amp;','&')
		if pn:items.append(('[COLOR lime]Trang tiếp theo (%s)...%d[/COLOR]'%(d,p+1),self.trueLink(pn),''))
		return items
	
	def download(self,url):
		try:res=urllib2.urlopen(urllib2.Request(url,headers=self.hd))
		except:res=''
		if res:b=res.read(500*1024)
		else:b=''
		return b
