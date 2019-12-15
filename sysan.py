import numpy as np
from pprint import pprint
from collections import defaultdict

init_prob_1 = [.6, .3, .2]
init_prob_2 = [.4, .5, .3, .7, .05, .1, .05, .05]
init_prob_3 = [.3, .8]

corr_12 = np.array([
    [.3, .3, .3, .3, 0, 0, 0, 0],
    [.3, 0, 0, 0, 0, .1, .3, 0],
    [.3, .3, .3, .3, 0, .3, 0, 0],
]) + 1

corr_13 = np.array([
    [0, 0],
    [-.3, 0],
    [-.5, 0],
]) + 1

corr_23 = np.array([
    [0, .1],
    [0, .3],
    [0, .3],
    [.5, .3],
    [0, .3],
    [0, .3],
    [0, .1],
    [0, 0],
]) + 1

corr_14 = np.array([
    [0, 0, 0, 0, 0, .3],
    [0, 0, .3, .3, 0, .5],
    [-.3, 0, 0, 0, -.3, 0]
]) + 1

corr_24 = np.array([
    [.5, 0, .3, .3, .3, .1],
    [0, 0, .1, .1, .3, .3],
    [0, 0, .3, .1, .3, .3],
    [.3, .5, .5, -.3, 0, .1],
    [0, 0, .3, 0, 0, .3],
    [.3, 0, 0, .3, .3, .1],
    [.3, 0, .3, .3, .3, 0],
    [0, 0, 0, 0, 0, 0],
]) + 1

corr_34 = np.array([
    [.5, .3, .3, .3, .1, -.5],
    [0, .5, .7, .5, 0, .5],
]) + 1

prob_1 = [v / sum(init_prob_1) for v in init_prob_1]
prob_2 = [v / sum(init_prob_2) for v in init_prob_2]
prob_3 = [v / sum(init_prob_3) for v in init_prob_3]

pprint(prob_1)
pprint(prob_2)
pprint(prob_3)
data = {}
ps = np.zeros((len(prob_1), len(prob_2), len(prob_3)))
for a, pa in enumerate(prob_1):
    for b, pb in enumerate(prob_2):
        for c, pc in enumerate(prob_3):
            prob = pa * pb * pc
            corr_coeff = corr_12[a][b] * corr_13[a][c] * corr_23[b][c]
            prob_corr = prob * corr_coeff
            if a not in data:
                data[a] = {}

            if b not in data[a]:
                data[a][b] = {}

            data[a][b][c] = {
                'prob': pa * pb * pc,
                'corr_coeff': corr_coeff,
                'prob_corr': prob_corr,
            }
            ps[a][b][c] = prob_corr

total_a = np.sum(ps, axis=(1, 2))
total_b = np.sum(ps, axis=(0, 2))
total_c = np.sum(ps, axis=(0, 1))
total = np.sum(ps)

pprint(total_a)
pprint(total_b)
pprint(total_c)
pprint(total)
for a in range(len(prob_1)):
    for b in range(len(prob_2)):
        for c in range(len(prob_3)):
            prob = data[a][b][c]['prob']
            corr_coeff = data[a][b][c]['corr_coeff']
            prob_corr = data[a][b][c]['prob_corr']
            adj_prob = data[a][b][c]['prob_corr'] / total
            data[a][b][c]['adj_prob'] = adj_prob
            print(",".join([f"{x:.4f}" for x in [a+1, b+1, c+1, prob, corr_coeff, prob_corr, adj_prob]]))

len_r = len(corr_14[0])
data_r = {}
for a in range(len(prob_1)):
    for b in range(len(prob_2)):
        for c in range(len(prob_3)):
            r_sum = 0
            for r in range(len_r):
                if a not in data_r:
                    data_r[a] = {}

                if b not in data_r[a]:
                    data_r[a][b] = {}

                if c not in data_r[a][b]:
                    data_r[a][b][c] = {}

                ps_abc = data[a][b][c]['adj_prob']
                r_coeff = corr_14[a][r] * corr_24[b][r] * corr_34[c][r]
                r_sum += r_coeff
                data_r[a][b][c][r] = {
                    'ps_abc': ps_abc,
                    'r_coeff': r_coeff,
                }

            for r in range(len_r):
                data_r[a][b][c][r]['r_coeff_norm'] = data_r[a][b][c][r]['r_coeff'] / r_sum
                data_r[a][b][c][r]['r_ps'] = data_r[a][b][c][r]['r_coeff_norm'] * data_r[a][b][c][r]['ps_abc']

            r_coeffs = [x['r_coeff'] for x in data_r[a][b][c].values()]
            r_coeff_norms = [x['r_coeff_norm'] for x in data_r[a][b][c].values()]
            r_pss = [x['r_ps'] for x in data_r[a][b][c].values()]

            print(','.join([f"{x:.4f}" for x in [a + 1, b + 1, c + 1, *r_coeffs, *r_coeff_norms, *r_pss]]))

sums = [0 for _ in range(len_r)]
for a in range(len(prob_1)):
    for b in range(len(prob_2)):
        for c in range(len(prob_3)):
            r_sum = 0
            for r in range(len_r):
                sums[r] += data_r[a][b][c][r]['r_ps']

pprint(sums)
