
import numpy as np
import pandas as pd
import random
import math
import matplotlib.pyplot as plt
import statistics 

#Läs in data från life_table.txt och interest.txt
data = pd.read_csv('life_table.txt')
interest_df = pd.read_csv('interest.txt')

#Klipp ut relevant data från båda tabellerna:
#-Interest
interest_df = interest_df[interest_df['t'] < 26]
rt = interest_df['rt'].tolist()
#-Life Table
new_data = data[data['Ages']>=65]
new_data = new_data[new_data['Ages']<90]

#Skapa en DataFrame som ska innehålla simulerade kontrakt
simulation_df = pd.DataFrame()

#Funktion för att simulera ett kontrakt:
def simulate():
    out = []
    for i in range(25):
        random_number = random.uniform(0,1)
        if random_number < (new_data['qx1000'].iloc[i])/1000: 
            out.append(0)
            break
        else:
            out.append(1)
    while len(out)<25:
        out.append(0)
#Output är en lista med längd 25, där varje element motsvarar 1 om individen lever och 0 om individen är död
    return out

#Vi gör detta för 5000 kontrakt: (Avkommentera för att göra hela simuleringen)
#n = 5000
#for i in range(1, n+1):
#    simulation_df[str(i)] = simulate()
#simulation_df.to_csv('simulation_df2.csv', index=False)

#Läs in från redan simulerad tabell:

#Vi har redan gjort simuleringen och läser därför in den versionen från 'simulation_df.csv'
simulation_df = pd.read_csv('simulation_df.csv')


alive = [5000]
for i in range(25):
    alive.append(sum(simulation_df.iloc[i]))

#One-year death probability, simulated
death_prob = []
for i in range(1,26):
    death_prob.append((alive[i-1]-alive[i])/alive[i-1])


#Diskontering
dt = []
for i in range(25):
    dt.append(math.exp(-(i+1)*rt[i]))

#P(T_x > t) Simulated
simulated_death = []
for i in range(25):
	a = 1
	while i >= 0:
		a = a * (1-death_prob[i])
		i -= 1
	simulated_death.append(1-a)

#Simulerat väntevärde
sim_expected = []
for i in range(25):
    sim_expected.append(dt[i] * (1-simulated_death[i]))

print('Simulerat väntevärde', sum(sim_expected), '\n') 
print('Sim,Väntevärde i olika tidsperioder:', np.array(sim_expected).round(2))



#P(T_x > t) Theoretical
theoretical_death = []
for i in range(25):
	a = 1
	while i >= 0:
		a = a * (1-new_data['qx1000'].tolist()[i]/1000)
		i -= 1
	theoretical_death.append(1-a)

#Teoretiskt väntevärde
teo_expected = []
for i in range(25):
    teo_expected.append(dt[i] * (1-theoretical_death[i]))
    
print('Teo,Väntevärde i olika tidsperioder:', np.array(teo_expected).round(2))
print('Teoretiskt väntevärde', sum(teo_expected), '\n')



#PLOT DOUBLE-BAR PLOT FOR EXPECTED CASH FLOW IN DIFFERENT TIME PERIODS:
plt.figure(4)
# set width of bar
barWidth = 0.25
 
# set height of bar
bars1 = sim_expected
bars2 = teo_expected
#bars3 = [29, 3, 24, 25, 17]
 
# Set position of bar on X axis
r0 = np.arange(len(bars1))
r1 = [x - barWidth/2 for x in r0]
r2 = [x + barWidth/2 for x in r0]
#r3 = [x + barWidth for x in r2]
 
# Make the plot
plt.bar(r1, bars1, color='#7f6d5f', width=barWidth, edgecolor='white', label='Simulerat Väntevärde')
plt.bar(r2, bars2, color='#557f2d', width=barWidth, edgecolor='white', label='Teoretiskt Väntevärde')
#plt.bar(r3, bars3, color='#2d7f5e', width=barWidth, edgecolor='white', label='var3')
 
# Add xticks on the middle of the group bars
plt.xlabel('t')
plt.ylabel('Väntevärde')
plt.title('Stapeldiagram')
plt.xticks([r for r in range(len(bars1))], range(1,26))
 
# Create legend & Show graphic
plt.legend()
#plt.savefig('cashflow_periods.png', dpi=1000)


#print('Simulated Death Prob',np.array(death_prob))
#print('Theoretical Death Prob',np.array(new_data['qx1000'].tolist())/1000)

def diskontering(x):
	k = x.sum()
	return sum(dt[:k])

payments = []
for i in range(1,5001):
	payments.append(diskontering(simulation_df[str(i)]))
total_payments = sum(payments)
exp_payment = total_payments/5000

tot_variance = []
for i in range(1,5001):
	tot_variance.append((diskontering(simulation_df[str(i)])-exp_payment)**2)

variance = sum(tot_variance)/5000
print('exp_payment:', exp_payment)
print('variance:', variance)


#95% konf.intervall 
konf_est = []
for i in range(25):
	konf_est.append(death_prob[i]-(1.96*(math.sqrt(5000*death_prob[i]*(1-death_prob[i]))))/5000)

konf_est_upper = []
for i in range(25):
	konf_est.append(death_prob[i]-(1.96*(math.sqrt(5000*death_prob[i]*(1-death_prob[i]))))/5000)

#print(konf_est)

#P(T_x > t) konf_intervall
konf_death = []
for i in range(25):
	a = 1
	while i >= 0:
		a = a * (1-konf_est[i])
		i -= 1
	konf_death.append(1-a)

#Simulerat konf_intervall väntevärde
konf_expected = []
for i in range(25):
    konf_expected.append(dt[i] * (1-konf_death[i]))

print('\nkonf_exp1:', sum(konf_expected))

#simulate payments through konf.interval 95% death probabilities
new_sim_konf = [5000]
for i in range(25):
	new_sim_konf.append(new_sim_konf[i] - new_sim_konf[i]*konf_est[i])
new_sim_konf = new_sim_konf[1:]


test = []
for i in range(25):
	test.append((dt[i]*new_sim_konf[i]))
print('konf_exp2:', sum(test)/5000)

print('Full betalning:', sum(dt))

#Analyse the simulated distribution of total future payments w.r.t. variance, quantiles:
#Variance: Done above
#Quantiles:
#List of payments for every contract, discounted is the variable = payments
#Sort the list:
payments.sort()
#print('Mean:', statistics.mean(payments))
#90%-kvantil:
#print('90%-kvantil:', payments[4500-1])

#50%-kvantil / median:
#print('50%-kvantil / Median:', payments[2100-1])
#print(payments.count(payments[-1]))
print('5%-kvantil:', payments[250-1])
print('Första kvartilen:', payments[1250-1])

fig1 = plt.figure(1)

x = payments 

new_dt = dt
for i in range(1,len(dt)):
	new_dt[i] += new_dt[-1]

x = []
for i in range(1,5001):
	x.append(sum(simulation_df[str(i)]))
x.sort()

print(x.count(x[-1])/len(x))
print(x.count(x[-1]))
print(alive[-1])

plt.hist(x, bins = 26)
plt.xlabel('Antal utbetalningar')
plt.ylabel('Frekvens')
plt.title('Histogram')
#plt.xticks([r for r in range(len(bars1))], range(1,26))
#plt.show()
#plt.savefig('test1.png', dpi=1000)

##############################
####ONE YEAR DEATH PROBABILITY
##############################

#print(np.array(death_prob))
#print(np.array(new_data['qx1000'].tolist())/1000)16.27152082121823

#Nelson-Aalen estimator
nelson_aalen = []
for i in range(25):
	counter = 0
	while i>=0:
		counter += death_prob[i]
		i-=1
	nelson_aalen.append(counter)

#print(np.array(nelson_aalen))


#Make-Ham function
mh = []
def make_ham(t):
	a = 0.001
	b = 0.000012
	c = 0.044
	return a+b*10**(c*(t-6))

for t in range(65,90):
	mh.append(make_ham(t))

#Integrated Make-Ham function

mh_integrated  = []
for i in range(25):
	counter = 0
	while i>=0:
		counter += mh[i]
		i-=1
	mh_integrated.append(counter)

#print(np.array(mh_integrated))
 

plt.figure(2)
# set width of bar
barWidth = 0.25
 
# set height of bar
bars1 = nelson_aalen
bars2 = mh_integrated
#bars3 = [29, 3, 24, 25, 17]
 
# Set position of bar on X axis
r0 = np.arange(len(bars1))
r1 = [x - barWidth/2 for x in r0]
r2 = [x + barWidth/2 for x in r0]
#r3 = [x + barWidth for x in r2]
 
# Make the plot
plt.bar(r1, bars1, color='#7f6d5f', width=barWidth, edgecolor='white', label='Nelson-Aalen')
plt.bar(r2, bars2, color='#557f2d', width=barWidth, edgecolor='white', label='Makeham')
#plt.bar(r3, bars3, color='#2d7f5e', width=barWidth, edgecolor='white', label='var3')
 
# Add xticks on the middle of the group bars
plt.xlabel('t')
plt.ylabel('Sannolikhet')
plt.title('Stapeldiagram')
plt.xticks([r for r in range(len(bars1))], range(1,26))
 
# Create legend & Show graphic
plt.legend()
#plt.show()
#plt.savefig('nelsonaalen_makeham.png', dpi=1000)


##################################################
##################################################
#Set bars for death probability
##################################################
##################################################

plt.figure(3)

life_table = np.array(new_data['qx1000'].tolist())/1000

# set height of bar
bars1 = death_prob
bars2 = life_table.tolist()
#bars3 = [29, 3, 24, 25, 17]
 
# Set position of bar on X axis
r0 = np.arange(len(bars1))
r1 = [x - barWidth/2 for x in r0]
r2 = [x + barWidth/2 for x in r0]
#r3 = [x + barWidth for x in r2]
 
# Make the plot
plt.bar(r1, bars1, color='#7f6d5f', width=barWidth, edgecolor='white', label='Simulerad Dödssannolikhet')
plt.bar(r2, bars2, color='#557f2d', width=barWidth, edgecolor='white', label='Teoretisk Dödssannolikhet')
#plt.bar(r3, bars3, color='#2d7f5e', width=barWidth, edgecolor='white', label='var3')
 
# Add xticks on the middle of the group bars
plt.xlabel('t')
plt.ylabel('Sannolikhet')
plt.title('Stapeldiagram')
plt.xticks([r for r in range(len(bars1))], range(1,26))
 
# Create legend & Show graphic
plt.legend()
#plt.show()
#plt.savefig('simulate_teor_deathprob.png', dpi=1000)


print(death_prob)
print(life_table.tolist())

###################################

plt.figure(5)

#Integrated Make-Ham function
life_table = np.array(new_data['qx1000'].tolist())/1000
lifetable_integrated  = []
for i in range(25):
	counter = 0
	while i>=0:
		counter += life_table[i]
		i-=1
	lifetable_integrated.append(counter)
print('\nlife_table:', lifetable_integrated)
print('nelson-aalen:', nelson_aalen)




# set height of bar
bars1 = lifetable_integrated
bars2 = nelson_aalen
#bars3 = mh_integrated
 
# Set position of bar on X axis
r0 = np.arange(len(bars1))
r1 = [x - barWidth/2 for x in r0]
r2 = [x + barWidth/2 for x in r0]
#r3 = [x + barWidth for x in r2]
 
# Make the plot
plt.bar(r1, bars1, color='#7f6d5f', width=barWidth, edgecolor='white', label='Life Table')
plt.bar(r2, bars2, color='#557f2d', width=barWidth, edgecolor='white', label='Nelson-Aalen')
#plt.bar(r3, bars3, color='#2d7f5e', width=barWidth, edgecolor='white', label='var3')
 
# Add xticks on the middle of the group bars
plt.xlabel('t')
plt.ylabel('Sannolikhet')
plt.title('Stapeldiagram')
plt.xticks([r for r in range(len(bars1))], range(1,26))
 
# Create legend & Show graphic
plt.legend()
#plt.show()
#plt.savefig('nelson_aalen_lifetable', dpi=1000)

##########################################################
##########################################################

data = pd.read_csv('life_table.txt')
new_data = data[data['Ages']>=65]
relevant = (new_data.head(25))
qx1000 = relevant['qx1000'].tolist()
qx = [qx1000[i]/1000 for i in range(25)]

interest_df = pd.read_csv('interest.txt')
interest_df = interest_df[interest_df['t'] < 26]
rt = interest_df['rt'].tolist()

interest = []
for i in range(25):
    interest.append(math.exp(-(i+1)*rt[i]))

px = [1-qx[i] for i in range(25)]

qx_trend = []
for i in range(25):
    qx_trend.append(1-px[i]**(0.99)**(i+1))

px_trend = [1-qx_trend[i] for i in range(25)]

px_cu = []
asse = 5000
for i in range(25):
    asse = asse*px_trend[i]
    px_cu.append(asse)
    

np.random.seed(seed=191)
n = 5000
ag = 0
num_alive = []
while ag < 25:
    s = np.random.binomial(n,qx_trend[ag],1)
    n = n-s
    num_alive.append(n)
    ag += 1

alive_pp = [num_alive[i]/5000 for i in range(25)]

el = []
for i in range(25):
    count7 = alive_pp[i]*interest[i]
    el.append(count7)

contract = []
val = 0
for i in range(25):
    contract.append(val)
    val += interest[i]
contract.append(val)
    
var_el = []
for i in range(25):
    if i == 0:
        diff = 5000-num_alive[i]
    else:
        diff = num_alive[i-1]-num_alive[i]
    ade = ((contract[i]-sum(el))**2)*diff
    var_el.append(ade)
var_el.append(((contract[25]-sum(el))**2)*num_alive[24])


print('simulerat väntevärde för ett kontrakt:', sum(el))
print('varians för ett kontrakt:', sum(var_el)/4999)


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

qx_trend = []
for i in range(25):
    qx_trend.append(1-px[i]**(0.895))

px_trend = [1-qx_trend[i] for i in range(25)]


n = 5000
ag = 0
num_alive = []
while ag < 25:
    s = np.random.binomial(n,qx_trend[ag],1)
    n = n-s
    num_alive.append(n)
    ag += 1

alive_pp = [num_alive[i]/5000 for i in range(25)]

el = []
for i in range(25):
    count7 = alive_pp[i]*interest[i]
    el.append(count7)

px_cu = []
asse = 5000
for i in range(25):
    asse = asse*px_trend[i]
    px_cu.append(asse)

contract = []
val = 0
for i in range(25):
    contract.append(val)
    val += interest[i]
contract.append(val)
    
var_el = []
for i in range(25):
    if i == 0:
        diff = 5000-num_alive[i]
    else:
        diff = num_alive[i-1]-num_alive[i]
    ade = ((contract[i]-sum(el))**2)*diff
    var_el.append(ade)
var_el.append(((contract[25]-sum(el))**2)*num_alive[24])



print('')
print('s väljs till 10.5%')
print('simulerat väntevärde för ett kontrakt:', sum(el))
print('varians för ett kontrakt:', sum(var_el)/4999)


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

interest = []
for i in range(25):
    interest.append(math.exp(-(i+1)*rt[i]*0.9364))


np.random.seed(seed=19990)
n = 5000
ag = 0
num_alive = []
while ag < 25:
    s = np.random.binomial(n,qx[ag],1)
    n = n-s
    num_alive.append(n)
    ag += 1

alive_pp = [num_alive[i]/5000 for i in range(25)]

el = []
for i in range(25):
    count7 = alive_pp[i]*interest[i]
    el.append(count7)

px_cu = []
asse = 5000
for i in range(25):
    asse = asse*px[i]
    px_cu.append(asse)

contract = []
val = 0
for i in range(25):
    contract.append(val)
    val += interest[i]
contract.append(val)
    
var_el = []
for i in range(25):
    if i == 0:
        diff = 5000-num_alive[i]
    else:
        diff = num_alive[i-1]-num_alive[i]
    ade = ((contract[i]-sum(el))**2)*diff
    var_el.append(ade)
var_el.append(((contract[25]-sum(el))**2)*num_alive[24])


print('')
print('s väljs till 6.36%')
print('simulerat väntevärde för ett kontrakt:', sum(el))
print('varians för ett kontrakt:', sum(var_el)/4999)

#################################################################
#################################################################
interest_df = pd.read_csv('interest.txt')
interest_df = interest_df[interest_df['t'] < 26]
rt = interest_df['rt'].tolist()
interest = []
for i in range(25):
    interest.append(math.exp(-(i+1)*rt[i]))

c = 0.84

np.random.seed(seed=1990)
k = 0
dv = []
while k < 5000:
    n = 500
    ag = 0
    w = 0
    while ag < 25:
        s = np.random.binomial(n,qx[ag],1)
        n = n-s
        w += n*interest[ag]
        ag += 1
    k += 1
    dv.append(w)

var = 0
el = sum(dv)/5000
for i in dv:
    var += (i-el)**2
var = var/4999
sd = var**0.5
var1 = var/500
sd1 = var1**0.5
el1 = el/500

k = 0
dv = []
while k < 5000:
    n = 5000
    ag = 0
    w = 0
    while ag < 25:
        s = np.random.binomial(n,qx[ag],1)
        n = n-s
        w += n*interest[ag]
        ag += 1
    k += 1
    dv.append(w)

var = 0
el = sum(dv)/5000
for i in dv:
    var += (i-el)**2
var = var/4999
sd = var**0.5
var1 = var/5000
sd1 = var1**0.5
el1 = el/5000

################################################################
################################################################

print(nelson_aalen[-1])
k=1
for i in range(25):
	k = k*(1-life_table[i])
print(k)