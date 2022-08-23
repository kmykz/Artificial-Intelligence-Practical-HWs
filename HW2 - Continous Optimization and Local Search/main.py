import math
import random

import numpy as np
import matplotlib.pyplot as plt

def f1(x):
    return (x**4 * math.exp(x) - math.sin(x))/2
def f2(x):
    return 5*math.log10(math.sin(5*x)+math.sqrt(x))
def f3(x):
    return math.cos(5*math.log10(x))-(x**3)/10
def show_plot(f,l,r):
    x = np.arange(l,r,0.01)
    y = [f(i) for i in x]
    plt.plot(x,y)
    plt.show()
# plots:
show_plot(f1,-2,1)
show_plot(f2,2,6)
show_plot(f3,0.5,2)

# Part 2 & 3:
def second_derivative(f, x, h=0.001):
    return (f(x + h) - 2 * f(x) + f(x - h)) / h ** 2

def derivative(f, x, h=0.001):
    return (f(x + h) - f(x)) / h


def next_step_gradient_descent(f, x, learningRate):
    return x - learningRate * derivative(f, x)

def next_step_newton(f, x):
    return x - derivative(f, x) / second_derivative(f, x)



def find_min_gradient_descent(f, l, r, learningRate, numberOfSteps):
    steps = 0
    x = random.uniform(l, r)
    while True:
        x = next_step_gradient_descent(f, x, learningRate)
        if x < l:
            x = l
        if x > r:
            x = r
        steps += 1
        if steps > numberOfSteps:
            break
    return f(x)

def find_min_newton(f, l, r, numberOfSteps):
    steps = 0
    x = random.uniform(l, r)
    while True:
        x = next_step_newton(f, x)
        if x < l:
            x = l
        if x > r:
            x = r
        steps += 1
        if steps > numberOfSteps:
            break
    return f(x)


def isValidMinimumForF2(x):
    return abs(x + 1.591) < 0.1
#Output for Part 2:
print("the minimum of f1 with learning rate = 0.1 is: %f" % (find_min_gradient_descent(f1,-2,1,0.1,100)))
print("the minimum of f1 with learning rate = 0.4 is: %f" % (find_min_gradient_descent(f1,-2,1,0.4,100)))
print("the minimum of f1 with learning rate = 0.6 is: %f" % (find_min_gradient_descent(f1,-2,1,0.6,100)))
print("the minimum of f1 with learning rate = 0.9 is: %f" % (find_min_gradient_descent(f1,-2,1,0.9,100)))


res1 = res2 = res3 = res4 = res5 = 0
for i in range(1000):
    if isValidMinimumForF2(find_min_gradient_descent(f2, 2, 6, 0.1, 100)):
        res1 = res1 + 1
    if isValidMinimumForF2(find_min_gradient_descent(f2, 2, 6, 0.4, 100)):
        res2 = res2 + 1
    if isValidMinimumForF2(find_min_gradient_descent(f2, 2, 6, 0.6, 100)):
        res3 = res3 + 1
    if isValidMinimumForF2(find_min_gradient_descent(f2, 2, 6, 0.9, 100)):
        res4 = res4 + 1
print("success rate with learning rate = %f is %f%%"% (0.1, res1/10))
print("success rate with learning rate = %f is %f%%"% (0.4, res2/10))
print("success rate with learning rate = %f is %f%%"% (0.6, res3/10))
print("success rate with learning rate = %f is %f%%"% (0.9, res4/10))
#Output for Part 3:
print("the minimum of f1 using newton's method is: %f" % find_min_newton(f1, -2, 1, 100))

for i in range(1000):
    if isValidMinimumForF2(find_min_newton(f2, 2, 6, 100)):
        res5 = res5 + 1
print("success rate with newton's method  is %f%%" % (res5/10))
#Part 4:

def draw_points(func, x_1_sequence, x_2_sequence,name):
    fig = plt.figure(figsize=plt.figaspect(0.5))
    X1, X2 = np.meshgrid(np.linspace(-15.0, 15.0, 1000), np.linspace(-15.0, 15.0, 1000))
    Y = func(X1, X2)
    f_sequence = [func(x_1_sequence[i], x_2_sequence[i]) for i in range(len(x_1_sequence))]

    # First subplot
    ax = fig.add_subplot(1, 2, 1)

    cp = ax.contour(X1, X2, Y, colors='black', linestyles='dashed', linewidths=1)
    ax.clabel(cp, inline=1, fontsize=10)
    cp = ax.contourf(X1, X2, Y, )
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.scatter(x_1_sequence, x_2_sequence, s=10, c="y")

    # Second subplot
    ax = fig.add_subplot(1, 2, 2, projection='3d')

    ax.contour3D(X1, X2, Y, 50, cmap="Blues")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.scatter3D(x_1_sequence, x_2_sequence, f_sequence, s=10, c="r")
    plt.savefig(name)
    plt.show()

def derivative_with_respect_to_x(f, x, y, h=0.001):
    return (f(x + h, y) - f(x, y)) / h


def derivative_with_respect_to_y(f, x, y, h=0.001):
    return (f(x, y + h) - f(x, y)) / h


def gradient(f, x, y):
    return (derivative_with_respect_to_x(f, x, y), derivative_with_respect_to_y(f, x, y))


def gradient_descent(func, l, r, learning_rate, max_iterations=100):
    x = random.uniform(l, r)
    y = random.uniform(l,r)
    X1 = []
    X2 = []
    X1.append(x)
    X2.append(y)
    for i in range(max_iterations):
        x_grad, y_grad = gradient(func, x, y)
        x -= learning_rate * x_grad
        y -= learning_rate * y_grad
        if x < l:
            x = l
        if x > r:
            x = r
        if y < l:
            y = l
        if y > r:
            y = r
        X1.append(x)
        X2.append(y)
    return (x, y, X1, X2)

def f(x, y):
    return 2**x/10000 + math.exp(y)/20000 + x**2 + 4 * (y**2) - 2 * x - 3 * y
func = np.vectorize(f)
t1 = gradient_descent(f, -15, 15, 0.01)
t2 = gradient_descent(f, -15, 15, 0.1)
t3 = gradient_descent(f, -15, 15, 0.18)
t4 = gradient_descent(f, -15, 15, 0.25)
print(t1[0],t1[1],f(t1[0],t1[1]))
print(t2[0],t2[1],f(t2[0],t2[1]))
print(t3[0],t3[1],f(t3[0],t3[1]))
print(t4[0],t4[1],f(t4[0],t4[1]))

draw_points(func,t1[2],t1[3],"1.png")
draw_points(func,t2[2],t2[3],"2.png")
draw_points(func,t3[2],t3[3],"3.png")
draw_points(func,t4[2],t4[3],"4.png")

#Part 5:
def next_T(T, gamma):
    return T * gamma

def cost(f,x):
    return -f(x)

def simulated_annealing(f, l, r, T_ititial, T_min, max_iterations, alpha, gamma):
    x = random.uniform(l, r)
    steps = 0
    T = T_ititial
    while T > T_min:
        if steps > max_iterations:
            break
        T = next_T(T, gamma)
        if T < T_min:
            break
        x1 = random.uniform(max(x - alpha,l),min(x + alpha,r))
        if f(x1) < f(x):
            x = x1
        elif random.uniform(0,1) < math.exp((cost(f,x1)-cost(f,x))/T):
            x = x1
        steps += 1
    return x



def success_calculator(alpha):
    res = 0
    for i in range(1000):
        if abs(2.18 - simulated_annealing(f2, 2, 6, 170, 0.01, 100, 0.4, 0.9)) < 0.2:
            res += 1
    print("success rate with alpha = %f is %f%%" % (alpha,res / 1000 * 100))

alphas = np.arange(0,1.1,0.1)
for alpha in alphas:
    success_calculator(alpha)

