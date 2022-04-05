import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from pandas.plotting import table
import random
import math
import statistics


sim_n = 1000

def simulate(x, sim_n):
	out = { x:0 for x in range(1,101) }

	# claim_triangle = pd.DataFrame()
	# for i in range(1,6):
	# 	dev_I = 6-i
	# 	claim_triangle[i] = simulate(dev_I, sim_n).values()

	# claim_triangle.index += 1
	# claim_triangle = claim_triangle.transpose().round(2)
	counter = 0
	#Simulate x development years.
	for i in range(1, x+1):
		#Simulate 1000 contracts every year.
		for k in range(sim_n):
		
			#Simulate claims for each contract for every year according to Poi(0.1)
			if i == 1:
				claims = np.random.poisson(0.1)
				while claims>0:
				#Simulate delay of Exp(1/3):
					year = np.floor(np.random.exponential(3))
					out[i + year] += claims
					counter += year
					claims -= 1

	#Return accumulated payments/claims:
	for i in range(1, len(out)):
		out[i+1] = out[i+1]+out[i]

	#out[6] = counter
	#qq = list(out.values())[-1]
	#out[7] = qq

	return out

####################################################
#UNCOMMENT TO DO NEW SIMULATION:
####################################################
claim_triangle = pd.DataFrame()
for i in range(1,6):
	dev_I = 6-i
	claim_triangle[i] = simulate(dev_I, sim_n).values()

claim_triangle.index += 1
claim_triangle = claim_triangle.transpose().round(2)

claim_triangle.to_csv('sim_iv2.csv', index = 0)

####################################################
#UNCOMMENT TO READ SAVED SIMULATION FROM FILE:
####################################################
claim_triangle = pd.read_csv('sim_iv2.csv')
claim_triangle.index += 1
####################################################

l = len(claim_triangle['1'])
for i in range(1,l+1):
 	for j in range(l-i+2, l+1):
 		claim_triangle.loc[i,str(j)] = 0

###################################################
l = len(claim_triangle['1'])

print('Claimstriangle:')
print(claim_triangle[['1','2','3','4','5']])

############################

def incr_list(x):
	out = []
	for i in range(len(x)):
		if i==0:
			out.append(x[i])
		elif (x[i]-x[i-1])>0:
			out.append(x[i]-x[i-1])
	return out

def return_time(x):
	out = 0
	for i in range(len(x)):
		out += (1+i)*x[i]
	return out
############################

print('Estimate Exp(lambda):')
#Return time spent, sum over j*claims_ij in the triangle:
r=0
for i in range(1,6):
	row = incr_list(claim_triangle.loc[i].tolist()[:5])
	r += return_time(row)
#claim_triangle.loc[i,str(j)]*(j-1)
r_1=r
for i in range(1,6):
	r += (l-i+1)*(claim_triangle.loc[i].tolist()[-1]-claim_triangle.loc[i,str(l-i+1)])




totala_claims = 0
for i in range(1,6):
	totala_claims += claim_triangle.loc[i, str(l-i+1)]

totala_claims_tot = 0
for i in range(1,6):
	totala_claims_tot += claim_triangle.loc[i].tolist()[-1]

print('totala claims i triangeln:', totala_claims)
print('total claims:', totala_claims_tot) #Oviktig
print('Total tid r:', r)
print('Total tid r_1', r_1)
d = totala_claims
#d= totala_claims_tot
r = r
print('*1:',d/r)  	#uppgift(iv) punkt 1
print('*2:',d/r_1)	#uppgift(iv) punkt 2

np.random.seed(seed=1991)

def sim(n,f):
    out = []
    po = np.random.poisson(0.1*n,1000)
    for t in po:
        if f == 'g':
            out.append(sum(np.random.gamma(25,1/25,t)))
        elif f == 'p':
            out.append(sum((np.random.pareto(1+26**0.5,t)+1)*(26/25-26**0.5/25)))
    return(out)

g1 = sim(100,'g')
p1 = sim(100,'p')
g2 = sim(1000,'g')
p2 = sim(1000,'p')
g3 = sim(5000,'g')
p3 = sim(5000,'p')


# teoretiskt väntevärde är 10, 100, resp 500
print(sum(g1)/1000,sum(g2)/1000,sum(g3)/1000)
print(sum(p1)/1000,sum(p2)/1000,sum(p3)/1000)

def var(l):
    c = 0
    for i in l:
        c += (i-sum(l)/1000)**2
    return c/999

# teoretisk varians är 10.4, 104 och 520
print(var(g1),var(g2),var(g3))
print(var(p1),var(p2),var(p3))

# 99% och 90% kvantiler 
def quant(l):
    j = l.copy()
    i = 0
    while i < 10:
        j.remove(max(j))
        i += 1
    ad = j.copy()
    while i < 100:
        j.remove(max(j))
        i += 1
    return max(ad), max(j)

print(quant(g1),quant(g2),quant(g3))
print(quant(p1),quant(p2),quant(p3))

def sim1(n,f):
    out = []
    po = np.random.poisson(0.1*n,1000)
    for t in po:
        if f == 'g':
            out.append(sum(np.random.gamma(4,1/4,t)))
        elif f == 'p':
            out.append(sum((np.random.pareto(1+5**0.5,t)+1)*(5/4-5**0.5/4)))
    return(out)

y1 = sim1(100,'g')
u1 = sim1(100,'p')
y2 = sim1(1000,'g')
u2 = sim1(1000,'p')
y3 = sim1(5000,'g')
u3 = sim1(5000,'p')

# teoretiskt väntevärde är samma på 10, 100, 500. 
print(sum(y1)/1000,sum(y2)/1000,sum(y3)/1000)
print(sum(u1)/1000,sum(u2)/1000,sum(u3)/1000)

# teoretisk varians är nu 12.5, 125, 625
print(var(y1),var(y2),var(y3))
print(var(u1),var(u2),var(u3))

print(quant(y1),quant(y2),quant(y3))
print(quant(u1),quant(u2),quant(u3))

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def m(n,f):
    i = 0
    means, quants = [], []
    while i < 1000:
        mean = []
        sim1 = np.random.poisson(0.1,n)
        sim2 = [int(v) for v in sim1]
        sim2.sort()
        if 1 in sim2:
            sim3 = sim2[sim2.index(1)-1:]
        else:
            sim3 = sim2
        for t in sim3:
            if f == 'g':
                mean.append(sum(np.random.gamma(25,1/25,t)))
            elif f == 'p':
                mean.append(sum(np.random.pareto(1+26**0.5,t)+1)*(26/25-26**0.5/25))
        means.append(sum(mean)/n)
        mean.sort()
        for z in range(int(n/100)):
            mean.pop()
        quants.append(mean[-1])
        i += 1
    return(means+quants)