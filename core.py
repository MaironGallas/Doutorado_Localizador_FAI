import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize._lsq import least_squares
from scipy.interpolate import interp1d


def avaliar_componentes_fortescue(fase_a, fase_b, fase_c):
    isp_1, isn_1, isz_1 = fase2simetrico(fase_a, fase_b, fase_c)
    isp_3, isn_3, isz_3 = fase2simetrico(fase_a, fase_b, fase_c, harmonica=3)

    # Sequencias Positiva, Negativa e Zero -> Modulos
    fig = plt.figure()
    plt.subplot(3, 2, 1)
    plt.plot(isp_1[0], color='red', label='Modulo Sequencia Positiva')
    plt.plot(isn_1[0], color='green', label='Modulo Sequencia Negativa')
    plt.plot(isz_1[0], color='blue', label='Modulo Sequencia Zero')
    plt.title('Modulos das Componentes de Sequencia para 1ª Harmonica')
    plt.legend()

    plt.subplot(3, 2, 2)
    plt.plot(isp_3[0], color='red', label='Modulo Sequencia Positiva')
    plt.plot(isn_3[0], color='green', label='Modulo Sequencia Negativa')
    plt.plot(isz_3[0], color='blue', label='Modulo Sequencia Zero')
    plt.title('Modulos das Componentes de Sequencia para 3ª Harmonica')
    plt.legend()

    # Sequencias Positiva, Negativa e Zero -> Angulos
    plt.subplot(3, 2, 3)
    plt.plot(isp_1[1], color='red', label='Angulo Sequencia Positiva')
    plt.plot(isn_1[1], color='green', label='Angulo Sequencia Negativa')
    plt.plot(isz_1[1], color='blue', label='Angulo Sequencia Zero')
    plt.title('Angulos das Componentes de Sequencia para 1ª Harmonica')
    plt.legend()

    plt.subplot(3, 2, 4)
    plt.plot(isp_3[1], color='red', label='Angulo Sequencia Positiva')
    plt.plot(isn_3[1], color='green', label='Angulo Sequencia Negativa')
    plt.plot(isz_3[1], color='blue', label='Angulo Sequencia Zero')
    plt.title('Angulos das Componentes de Sequencia para 3ª Harmonica')
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(fase_a.sinal, color='red', label='Fase A')
    plt.plot(fase_b.sinal, color='green', label='Fase B')
    plt.plot(fase_c.sinal, color='blue', label='Fase C')
    plt.title('Sinal Instantaneo nas Fases')
    plt.legend()

    plt.show()


def pol2cart(theta, rho):
    """
    Transforme as coordenadas polares em cartesianas.
    :param theta: graus
    :param rho: float
    :return x, y:
    """
    x = rho * np.cos(theta)
    y = rho * np.sin(theta)
    return x, y


def cart2pol(x, y):
    """
    Transforme as coordenadas cartesianas em polares.
    :param x: float
    :param y: float
    :return theta, rho:
    """
    theta = np.arctan2(y, x)
    rho = np.hypot(x, y)
    return theta, rho


def my_fft(sinal, frequencia_amostragem):
    """
    Função para realizar a Transformada de Fourier de um Sinal e executar a plotagem no dominio da frequencia.
    :param sinal:
    :param taxa_amostragem:
    :return:
    """
    tamanho = len(sinal)
    periodo = tamanho / frequencia_amostragem
    values = np.arange(tamanho)

    frequencias = values / periodo
    frequencias = frequencias[range(int(tamanho / 2))]

    fourier_transform = np.fft.fft(sinal) / tamanho  # FFT normalizada do vetor sinal sobre tamanho
    fourier_transform = fourier_transform[range(int(tamanho / 2))]  # Ajusta o eixo do sinal

    #plt.plot(frequencias, 2*abs(fourier_transform))
    #plt.show()

    return fourier_transform, frequencias


def simetrico2fase():
    pass


def fase2simetrico(fase_a, fase_b, fase_c, harmonica=1):
    """
    Função para transformar fasores em componentes de fase para compenentes de sequencia
    utilizando a transformada de Fortescue.
    :param ia: Fasor
    :param ib: Fasor
    :param ic: Fasor
    :return: sqp, sqn, sqz
    """
    x, y = pol2cart(120 * np.pi / 180, 1)
    a2fq = x + 1j * y
    x, y = pol2cart(-120 * np.pi / 180, 1)
    a1fq = x + 1j * y

    x, y = pol2cart(fase_a.fasor.fase[harmonica] * np.pi / 180, fase_a.fasor.modulo[harmonica])
    fase_a_simetrico = x + 1j * y
    x, y = pol2cart(fase_b.fasor.fase[harmonica] * np.pi / 180, fase_b.fasor.modulo[harmonica])
    fase_b_simetrico = x + 1j * y
    x, y = pol2cart(fase_c.fasor.fase[harmonica] * np.pi / 180, fase_c.fasor.modulo[harmonica])
    fase_c_simetrico = x + 1j * y

    sqn = (fase_a_simetrico + a1fq * fase_b_simetrico + a2fq * fase_c_simetrico) / 3
    sqp = (fase_a_simetrico + a2fq * fase_b_simetrico + a1fq * fase_c_simetrico) / 3
    sqz = (fase_a_simetrico + fase_b_simetrico + fase_c_simetrico) / 3

    i1r = np.real(sqp)
    i1i = np.imag(sqp)
    i1a, i1m = cart2pol(i1r, i1i)
    i1a = i1a * 180 / np.pi

    i2r = np.real(sqn)
    i2i = np.imag(sqn)
    i2a, i2m = cart2pol(i2r, i2i)
    i2a = i2a * 180 / np.pi

    i0r = np.real(sqz)
    i0i = np.imag(sqz)
    i0a, i0m = cart2pol(i0r, i0i)
    i0a = i0a * 180 / np.pi

    return (i1m, i1a), (i2m, i2a), (i0m, i0a)


def find_indice_tempo(tempo, inicio):
    for i in range(0, len(tempo), 1):
        if tempo[i] > inicio:
            indice = i
            break
    return indice


def queda_tensao_por_km_fasor(ia, ib, ic, cabo, harmonica=1):
    x, y = pol2cart(ia.fasor.fase[harmonica] * np.pi / 180, ia.fasor.modulo[harmonica])
    ia_complexo = x + 1j * y
    x, y = pol2cart(ib.fasor.fase[harmonica] * np.pi / 180, ib.fasor.modulo[harmonica])
    ib_complexo = x + 1j * y
    x, y = pol2cart(ic.fasor.fase[harmonica] * np.pi / 180, ic.fasor.modulo[harmonica])
    ic_complexo = x + 1j * y

    matriz_correntes = np.array([[ia_complexo], [ib_complexo], [ic_complexo]]).reshape(3, len(ia_complexo))

    matriz_queda_tensao_linha = matriz_correntes * cabo.impedancia

    print(matriz_queda_tensao_linha)
    return matriz_queda_tensao_linha


def queda_tensao_por_km_sinal():
    pass


def func_modelo(x, v_sub, i_falta, matriz_m):  # x1 = R, x2 = X, x3 = Distancia
    eq1 = (i_falta.real * x[0] - i_falta.real * x[1] + matriz_m.real * x[2]) - v_sub.real
    eq2 = (i_falta.imag * x[0] + i_falta.imag * x[1] + matriz_m.imag * x[2]) - v_sub.imag
    return np.append(eq1, eq2)


def estimar_distancia_lm(v_sub, i_falta, matriz_m):
    x0 = [0, 0, 0]
    x1 = least_squares(func_modelo, x0, args=(v_sub, i_falta, matriz_m))
    return x1


def teste_minimos_quadrados():
    x = np.arange(1, 5.01, 0.1)
    n = len(x)
    y = (x-3)*(x-1)*(x-4)*(x-4.5)*(x+1) + 8*np.cos(x) + 5*np.random.random_sample(n)
    A = np.array([np.power(x, 5), np.power(x, 4), np.power(x, 3), np.power(x, 2), np.power(x, 1), np.power(x, 0), np.cos(x)]).T
    th = np.linalg.inv((A.T).dot(A)).dot(A.T).dot(y)
    print('Acabou')


def estimar_distancia_mmq(v_sub, i_falta, matriz_m):
    ifalta = np.append(i_falta.real, i_falta.imag)
    m = np.append(matriz_m.real, matriz_m.imag)
    y = np.append(v_sub.real, v_sub.imag)

    #A = np.array([np.power(inputs, 1), np.power(inputs, 1), np.power(inputs, 1)])
    #coefs = np.linalg.inv((A.T).dot(A)).dot(A.T).dot(y)


def func_distancia(x, v_linha_filter, v_sub_filter, v_falta_estimada_filter):
    return x[0]*v_linha_filter + v_falta_estimada_filter - v_sub_filter


def calcular_distancia_lm(queda_tensao_linha_vetor, vsub, vestimado):
    x0 = [10000]
    x1 = least_squares(func_distancia, x0, args=(queda_tensao_linha_vetor, vsub, vestimado))
    return x1.x


def interpolar(sinal, tempo):
    step_min = 1E-6
    tempo_interpolado = np.arange(tempo[0], tempo[-1]-step_min, step_min)
    step_interpolado = tempo_interpolado[1] - tempo_interpolado[0]

    cubic_interp = interp1d(tempo, sinal, kind='cubic')
    sinal_interpolado = cubic_interp(tempo_interpolado)

    return sinal_interpolado, step_interpolado, tempo_interpolado

if __name__ == '__main__':
    teste_minimos_quadrados()