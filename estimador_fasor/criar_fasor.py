import math
import numpy as np

from core import pol2cart


class Fourier():
    def __init__(self, amostragem, frequencia):
        self.cfc_lista = []
        self.cfs_lista = []
        self.frequencia = frequencia
        self.taxa_amostragem = amostragem
        self.janela_de_amostras = np.arange(0, self.taxa_amostragem, 1)
        self.cria_coef_sin_cos()

    def cria_referencia_matlab(self, time):
        angle = (2 * np.pi * self.frequencia) * time
        self.ref = np.sin(angle)

    def seleciona_referencia(self, sinal):
        self.ref = sinal

    def cria_coef_sin_cos(self):
        for harmonica in range(0, 8, 1):
            angle = (2 * np.pi * harmonica / self.taxa_amostragem) * self.janela_de_amostras
            cfc = np.cos(angle)
            cfs = - np.sin(angle)
            self.cfc_lista.append(np.copy(cfc))
            self.cfs_lista.append(np.copy(cfs))



class Fasor():
    def __init__(self, fft):
        self.fft = fft
        self.modulo = []
        self.fase = []
        self.complexo = []

    def estimar(self, sinal):
        modulo = np.zeros((len(sinal) - self.fft.taxa_amostragem, 1))
        fase = np.zeros((len(sinal) - self.fft.taxa_amostragem, 1))

        CONSTANTE = (2 / self.fft.taxa_amostragem)

        for harmonica in range(0, 8, 1):
            for i in range(self.fft.taxa_amostragem, len(sinal), 1):
                fftr = (np.sum(sinal[i - self.fft.taxa_amostragem:i] * self.fft.cfc_lista[harmonica])) * CONSTANTE
                ffti = (np.sum(sinal[i - self.fft.taxa_amostragem:i] * self.fft.cfs_lista[harmonica])) * CONSTANTE

                fftr_ref = (np.sum(self.fft.ref[i - self.fft.taxa_amostragem:i] * self.fft.cfc_lista[1])) * CONSTANTE
                ffti_ref = (np.sum(self.fft.ref[i - self.fft.taxa_amostragem:i] * self.fft.cfs_lista[1])) * CONSTANTE

                ffta = math.atan2(ffti, fftr) * 57.295779
                ffta_ref = math.atan2(ffti_ref, fftr_ref) * 57.295779

                modulo[i - self.fft.taxa_amostragem] = np.sqrt(fftr * fftr + (ffti * ffti))
                fase[i - self.fft.taxa_amostragem] = self.calcular_angulo(ffta, ffta_ref, harmonica)


            self.modulo.append(np.copy(modulo))
            self.fase.append(np.copy(fase))


    def calcular_angulo(self, ffta, ref_angulo, harmonica):
        x = ffta - 90
        if x <= -180:
            x = x + 360

        xref = ref_angulo - 90
        if xref <= -180:
            xref = xref + 360

        xref = xref * harmonica

        while xref <= -180:
            xref = xref + 360

        while xref >= 180:
            xref = xref - 360

        angulo = x - xref

        if angulo >= 180:
            angulo = angulo - 360
        if angulo <= -180:
            angulo = angulo + 360
        if (angulo >= -0.0001) and (angulo <= 0.0001):
            angulo = 0

        return angulo

    def complex(self, harmonicas=[0, 1, 2, 3]):
        for harmonica in harmonicas:
            x, y = pol2cart(self.fase[harmonica] * np.pi / 180, self.modulo[harmonica])
            complexo = x + 1j * y
            self.complexo.append(np.copy(complexo))
