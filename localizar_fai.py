import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat

from carregar_simulacoes.loading_simulations import Simulacao
from estimador_fasor.criar_fasor import Fourier
from estimador_fasor.criar_sinal import Sinal
from core import *
from cabo.criar_cabo import Cabo


def metodo_novo():
    matriz_correntes = np.array([[ia.fasor.complexo[1]], [ib.fasor.complexo[1]], [ic.fasor.complexo[1]]]).reshape(3, len(ia.fasor.complexo[1]))
    matriz_m = cabo.impedancia.dot(matriz_correntes)

    # Condiciona Variaveis
    v_sub = va.fasor.complexo[1][sync:].flatten()
    i_falta = ifalta_real.fasor.complexo[1][sync:].flatten()
    #matriz_m_falta = matriz_m[0][sync:]  # --> Fase A
    matriz_m_falta = vlinha_a.fasor.complexo[1][sync:].flatten()/2500
    estimar_distancia_mmq(v_sub, i_falta, matriz_m)

    """# Estimador em Loop
    parametros = []
    for i in range(0, len(v_sub)-8):
        v_sub_janela = v_sub[i:i+8]
        i_falta_janela = i_falta[i:i+8]
        matriz_m_falta_janela = matriz_m_falta[i:i+8]
        parametros_x = estimar_distancia_lm(v_sub_janela, i_falta_janela, matriz_m_falta_janela)
        print(parametros_x.x[2])
        parametros.append(parametros_x.x)

    print("Acabou")"""


if __name__ == '__main__':
    AMOSTRAGEM = 256
    FREQUENCIA_REDE = 60
    TEMPO = 2.5

    # Carregando Simulacao
    file_path = r"C:\Users\Mairon\PycharmProjects\Doutorado_Localizador_FAI\simulacoes\sim_256sam_2500m.mat"
    sinais = loadmat(file_path)

    # simulacao = Simulacao(r'D:\Mairon\Algoritimo Localizador de Falta\Simulacoes_Python\SI_FAIResistencia_N5261_S0_FA_T2.mat')
    # sinais = simulacao.loading()

    # Sinais Simulações
    """va = Sinal(sinais['Va'], AMOSTRAGEM, FREQUENCIA_REDE)
    vb = Sinal(sinais['Vb'], AMOSTRAGEM, FREQUENCIA_REDE)
    vc = Sinal(sinais['Vc'], AMOSTRAGEM, FREQUENCIA_REDE)
    ia = Sinal(sinais['Ia'], AMOSTRAGEM, FREQUENCIA_REDE)
    ib = Sinal(sinais['Ib'], AMOSTRAGEM, FREQUENCIA_REDE)
    ic = Sinal(sinais['Ic'], AMOSTRAGEM, FREQUENCIA_REDE)
    ineutro = Sinal(sinais['Ineutro'], AMOSTRAGEM, FREQUENCIA_REDE)
    ifalta_real = Sinal(sinais['Ifalta_fonte'], AMOSTRAGEM, FREQUENCIA_REDE)
    vfalta_real = Sinal(sinais['Vfalta_fonte'], AMOSTRAGEM, FREQUENCIA_REDE)"""

    va = Sinal(sinais['vX0003a'].flatten(), AMOSTRAGEM, FREQUENCIA_REDE)
    vb = Sinal(sinais['vX0003b'].flatten(), AMOSTRAGEM, FREQUENCIA_REDE)
    vc = Sinal(sinais['vX0003c'].flatten(), AMOSTRAGEM, FREQUENCIA_REDE)
    ia = Sinal(sinais['iX0036aX0003a'].flatten(), AMOSTRAGEM, FREQUENCIA_REDE)
    ib = Sinal(sinais['iX0036bX0003b'].flatten(), AMOSTRAGEM, FREQUENCIA_REDE)
    ic = Sinal(sinais['iX0036cX0003c'].flatten(), AMOSTRAGEM, FREQUENCIA_REDE)
    ineutro = Sinal(sinais['iTerraXx0014'].flatten(), AMOSTRAGEM, FREQUENCIA_REDE)
    ifalta_real = Sinal(sinais['iXx0021Xx0026'].flatten(), AMOSTRAGEM, FREQUENCIA_REDE)
    vfalta_real = Sinal(sinais['vX0002a'].flatten(), AMOSTRAGEM, FREQUENCIA_REDE)
    vlinha_a = Sinal(sinais['vX0003aX0002a'].flatten(), AMOSTRAGEM, FREQUENCIA_REDE)
    vlinha_b = Sinal(sinais['vX0003bX0002b'].flatten(), AMOSTRAGEM, FREQUENCIA_REDE)
    vlinha_c = Sinal(sinais['vX0003cX0002c'].flatten(), AMOSTRAGEM, FREQUENCIA_REDE)

    # Escolhe Referencia para Fourier
    cfg_fft = Fourier(AMOSTRAGEM, FREQUENCIA_REDE)
    cfg_fft.seleciona_referencia(va.sinal)  # Utilizado Tensão na Fase A -> va

    # Estima Fasores de 1º a 7º Harmonica
    va.estimar(cfg_fft)
    vb.estimar(cfg_fft)
    vc.estimar(cfg_fft)
    ia.estimar(cfg_fft)
    ib.estimar(cfg_fft)
    ic.estimar(cfg_fft)
    ifalta_real.estimar(cfg_fft)
    vlinha_a.estimar(cfg_fft)

    # Calcular Matriz M
    cabo = Cabo("P-150")

    # Encontra Indice do Tempo
    #sync = find_indice_tempo(va.tempo, TEMPO)


