import numpy as np


class Cabo():
    def __init__(self, cabo_nome):
        self.resistencia = None
        self.indutancia = None
        self.nome = cabo_nome
        self.cabos_imp = {"A-336": [0.18933, 0.38122, 0.36571, 2.14928], "S-336": [0.18933, 0.37518, 0.36571, 2.14324],
                          # r1,x1,r0,x0 ohm/km
                          "P-185": [0.184, 0.27137, 0.36043, 2.33866], "A-40": [0.30139, 0.40356, 0.47777, 2.17163],
                          "S-40": [0.29940, 0.39782, 0.47577, 2.16588], "P-150": [0.23100, 0.28034, 0.40743, 2.34763],
                          "A-10": [0.60420, 0.42983, 0.78057, 2.19790], "P-120": [0.28400, 0.28697, 0.46043, 2.35426],
                          "A-02": [0.96312, 0.44754, 1.13950, 2.21552], "S-02": [0.95712, 0.44158, 1.13350, 2.20965],
                          "A-04": [1.53008, 0.46489, 1.70645, 2.23295], "S-04": [1.51808, 0.45897, 1.69445, 2.22704],
                          "P-35": [0.97300, 0.33340, 1.14943, 2.40068], "S-10": [0.60020, 0.42402, 0.77657, 2.19209],
                          "P-50": [0.71799, 0.31930, 0.94593, 2.38659]}
        self.seq2fase()

    def tabela_seq(self):
        r1 = self.cabos_imp[self.nome][0] / 1000
        x1 = self.cabos_imp[self.nome][1] / 1000
        r0 = self.cabos_imp[self.nome][2] / 1000
        x0 = self.cabos_imp[self.nome][3] / 1000
        return r1, x1, r0, x0

    def seq2fase(self):
        r1, x1, r0, x0 = self.tabela_seq()

        w = 2 * np.pi * 60
        T = np.array([[1, 1, 1],
                      [1, np.exp(1j * 240 * np.pi / 180), np.exp(1j * 240 * np.pi / 360)],
                      [1, np.exp(1j * 240 * np.pi / 360), np.exp(1j * 240 * np.pi / 180)]])

        z0 = (r0 + 1j * x0)
        z1 = (r1 + 1j * x1)

        z012 = np.array([[z0, 0, 0], [0, z1, 0], [0, 0, z1]])

        zabc = T.dot(z012).dot(np.linalg.inv(T))

        self.resistencia = np.real(zabc)
        self.indutancia = np.imag(zabc) / w
        self.impedancia = zabc

    def set_rl(self, r, l):
        self.resistencia = r
        self.indutancia = l