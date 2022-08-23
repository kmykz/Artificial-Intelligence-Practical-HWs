import math
import os
import statistics

import scipy.stats as st
import numpy as np
import matplotlib.pyplot as plt
def pdf_1(x):
    return 3/10*st.norm.pdf(x, loc=4, scale= math.sqrt(2)) + 3/10*st.norm.pdf(x,loc = 3, scale= math.sqrt(2)) + 4/10*st.expon.pdf(x, loc=0, scale=100)
def pdf_2(x):
    return 2/10*st.norm.pdf(x, loc=0, scale= math.sqrt(10)) + 2/10*st.norm.pdf(x,loc = 20, scale= math.sqrt(15)) + 3/10*st.norm.pdf(x,loc = -10, scale= math.sqrt(8)) + 3/10*st.norm.pdf(x,loc = 50, scale= 5)
def pmf_3(x):
    return 2/10*st.geom.pmf(x, 0.1) + 2/10*st.geom.pmf(x, 0.5) + 2/10*st.geom.pmf(x, 0.3) + 4/10*st.geom.pmf(x, 0.04)
def rejection_sampling(pdf, x_min, x_max, n):
    samples = []
    while len(samples) < n:
        x = np.random.uniform(x_min, x_max)
        u = np.random.uniform(0, 1)
        if u <= pdf(x):
            samples.append(x)
    return samples
def rejection_sampling_for_pmf(pmf, x_min, x_max, n):
    samples = []
    while len(samples) < n:
        x = np.random.randint(x_min, x_max)
        u = np.random.uniform(0, 1)
        if u <= pmf(x):
            samples.append(x)
    return samples
Xs = np.linspace(-10, 20, 100)
Xs2 = np.linspace(-30, 100, 1000)
Xs3 = np.linspace(1, 100, 100)
Ys = [pdf_1(x) for x in Xs]
Ys1 = [pdf_2(x) for x in Xs2]
Ys2 = [pmf_3(x) for x in Xs3]
current_path = os.getcwd()
destination_path =os.path.join(current_path, 'part1')
if not os.path.exists(destination_path):
    os.makedirs(destination_path)
plt.plot(Xs, Ys)
plt.savefig('part1/pdf1.png')
plt.show()
plt.plot(Xs2, Ys1)
plt.savefig('part1/pdf2.png')
plt.show()
plt.plot(Xs3, Ys2)
plt.savefig('part1/pdf3.png')
plt.show()
Sample1 = rejection_sampling(pdf_1, -10, 20, 500)
bins = np.arange(-10, 20, 1)
plt.hist(Sample1, bins=bins, density=True)
plt.savefig('part1/pdf1_sample.png')
plt.show()
Sample2 = rejection_sampling(pdf_2, -30, 100, 500)
bins = np.arange(-30, 100, 1)
plt.hist(Sample2, bins=bins, density=True)
plt.savefig('part1/pdf2_sample.png')
plt.show()
Sample3 = rejection_sampling_for_pmf(pmf_3, 0, 100, 500)
bins = np.arange(0, 100, 1)
plt.hist(Sample3, bins=bins, density=True)
plt.savefig('part1/pdf3_sample.png')
plt.show()
file = open('part1/log.txt', 'w')
file.write('1 ' + str(round(statistics.mean(Sample1),4)) + ' ' + str(round(statistics.stdev(Sample1),4)) + '\n')
file.write('2 ' + str(round(statistics.mean(Sample2),4)) + ' ' + str(round(statistics.stdev(Sample2),4)) + '\n')
file.write('3 ' + str(round(statistics.mean(Sample3),4)) + ' ' + str(round(statistics.stdev(Sample3),4)) + '\n')
file.close()


