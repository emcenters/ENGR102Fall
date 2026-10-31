import matplotlib.pyplot as plt
import math

t = [0, 0.45, 1.1, 1.75, 2.25, 2.7] 
y = [0, 0.23, 0.4, 0.18, 0.07, 0.01]

def solve_function_one(t):
    return t**2*math.exp(-t**2)

def solve_function_two(t):
    return t**4*math.exp(-t**2)

solved_list_of_nums = {1:[], 2:[]}
x_list = []
for i in range(60):
    x_list.append(i/20)
    solved_list_of_nums[1] += [(solve_function_one(i/20))]
    solved_list_of_nums[2] += [(solve_function_two(i/20))]

win = plt.figure()
plt.subplot(2, 1, 1)
plt.scatter(t, y, color='black', label = 'data')
plt.xlim(0.0)
plt.ylim(-0.05, top = 1.05)
plt.yticks([0.00, 0.25, 0.50, 0.75, 1.00] )
plt.plot(x_list, solved_list_of_nums[1], color = 'red', label = 't^2*exp(–t^2)')
plt.plot(x_list, solved_list_of_nums[2], color = 'blue', label = 't^4*exp(–t^2)')
plt.xlabel('time')
plt.ylabel('y')
plt.title('Data and two curves vs. time')
plt.legend()

plt.subplot(2, 1, 2)
plt.scatter(t, y, color='y', label = 'data', marker = '^')
plt.plot(t, y, color='y')
plt.xlim(1.00, 2.00)
plt.ylim(0.0, 0.5)
plt.plot(x_list, solved_list_of_nums[1], color = 'blue', label = 't^2*exp(–t^2)')
plt.xlabel('time')
plt.ylabel('y')
plt.title('Data interpolation and Curve 1')
plt.legend()
plt.tight_layout()
plt.annotate("It's closest here!", xy=[1.4, 0.275], xytext=[1.3, 0.12], fontsize = 8, arrowprops = dict(facecolor = 'black', shrink = 0.1, width = 0.5, headwidth = 5, headlength = 5))
win.canvas.manager.set_window_title('Frodo likes this.')
plt.show()

# plt.plot(x, y)