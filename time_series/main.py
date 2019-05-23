import numpy as np

if __name__ == '__main__':
    with open('sim_2_Y3.txt') as f:
        data = f.readlines()
        sim_2_Y3 = np.array([float(x) for x in data]).reshape((1, 100))

    rand = np.random.rand(1, 100)
    randn = np.random.randn(1, 100)

    y1 = np.array(sim_2_Y3, copy=True)
    print(y1)
    y1[:, 1:] = 0.3 * y1[:, :-1] + 0.7 * y1[:, 1:] + randn[:, 1:]
    print(y1)
