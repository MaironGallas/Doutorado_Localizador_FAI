import numpy as np

from estimador_fasor.criar_fasor import Fasor


class Sinal():
    def __init__(self, sinal, taxa_amostragem, frequencia_rede):
        self.sinal = sinal
        self.frequencia = frequencia_rede
        self.taxa_amostragem = taxa_amostragem
        self.step = 1 / frequencia_rede / taxa_amostragem
        self.tempo = np.arange(1/60, len(self.sinal) * self.step, self.step)

    def estimar(self, cfg_fft):
        self.fasor = Fasor(cfg_fft)
        self.fasor.estimar(self.sinal)
        self.fasor.complex()
        #elf.criar_sinal_3harmonica()

    """def criar_sinal_3harmonica(self):
        sinal_3h = np.zeros(len(self.sinal))
        for i in range(self.taxa_amostragem, len(sinal_3h), 1):
            sinal_3h[i] = self.fasor.modulo[3][i - self.taxa_amostragem] * np.sin(
                2 * np.pi * 180 * self.tempo[i] + (self.fasor.fase[3][i - self.taxa_amostragem] * (np.pi / 180)))

        self.sinal_3h = sinal_3h
        self.sinal_3h_interpolado, self.tempo_interpolado, self.step_interpolado = interpolar(sinal_3h, self.tempo)
        self.taxa_amostragem_interpolado = round(1 / self.frequencia / self.step_interpolado)"""