import matplotlib.pyplot as plt
import numpy as np


# Apsibrėžiame pradinį tašką bei žingsnius bei kitą pagalbinę informaciją
u0 = [0]
step1 = 0.1
step2 = 0.05
interval = [0, 1]
a = b = 1

stepMsg = '\u03C4 ='
rungeKuttoMsg = '4-pakopis Rungės-Kuto'
secondOrderMsg = 'Dvipakopis, kai \u03C3=0,5'
title1 = '4-pakopis Rungės-Kuto grafikas su skirtingais žingsniais'
title2 = 'Dvipakopio metodo, kai \u03C3=0,5, grafikas su skirtingais žingsniais'
title3 = 'Skirtingų metodų grafikai, kai \u03C4 = '


# Apsibrėžiame pradinę funkciją
def func(x, u):
    return np.exp(x) * np.sin(u + x)


# Apsibrėžiame dvipakopį metodą.
def simetricalOilersMethod(f, u0, x, step):
    u = np.zeros(len(x))
    u[0] = u0
    for i in range(0, len(x) - 1):
        k1 = f(x[i], u[i])
        k2 = f((x[i] + step * a), (u[i] + step * b * k1))
        u[i + 1] = u[i] + 0.5 * step * (k1 + k2)
    return u


# Apsibrėžiame Rungės-Kuto metodą.
def rungeKuttaMethod(f, u0, x, step):
    u = np.zeros(len(x))
    u[0] = u0
    for i in range(0, len(x) - 1):
        f1 = step * f(x[i], u[i])
        f2 = step * f((x[i] + step/2), (u[i] + f1/2))
        f3 = step * f((x[i] + step/2), (u[i] + f2/2))
        f4 = step * f((x[i] + step), (u[i] + f3))
        u[i + 1] = u[i] + 1/6*(f1 + 2*f2 + 2*f3 + f4)
    return u


# Apsibrėžiame paklaidos skaičiavimo funkcijas
def error(u_2tau, u_tau, p):
    return np.abs(u_2tau - u_tau) / (2**p - 1)


def calculate_errors(u_2tau, u_tau, p):
    errors = {}
    for i in range(0, len(u_tau) - 1):
        errors[i] = error(u_2tau[i * 2], u_tau[i], p)

    return errors[max(errors, key=errors.get)]


# Brėžimo funkcijos
def drawFunctions(results1, results2, step1_t, message1, title, step2_t=None, message2=None, step=None):
    plt.figure(num=1, dpi=150, figsize=(7, 5))
    plt.rcParams["font.family"] = "serif"
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['savefig.facecolor'] = 'white'
    plt.xlabel("$x$")
    plt.ylabel("$u$")

    # Jei step2_t yra None tada piešiama ta pati funkcija su skirtingais žingsniais
    # Jei step2_t nėra None tada piešiamos abi funkcijos su tuo pačiu žingsniu
    if step2_t is not None:
        plt.plot(step1_t, results1, label=(message1 + str(step1)))
        plt.plot(step2_t, results2, label=(message1 + str(step2)))
        plt.title(title)
    else:
        plt.plot(step1_t, results1, label=message1)
        plt.plot(step1_t, results2, label=message2)
        plt.title(title + str(step))

    plt.grid(True, color='lightgray')
    plt.legend()
    plt.show()


# Suskirstome intervalą, kad būtų patogiau skaičiuoti
step1_t_eval = np.linspace(interval[0], interval[1], int(interval[1] / step1))
step2_t_eval = np.linspace(interval[0], interval[1], int(interval[1] / step2))

# Apskaičiuojame visus reikiamus rezultatus
rungeKuttoRez1 = rungeKuttaMethod(func, u0[0], step1_t_eval, step1)
rungeKuttoRez2 = rungeKuttaMethod(func, u0[0], step2_t_eval, step2)
secondOrderRez1 = simetricalOilersMethod(func, u0[0], step1_t_eval, step1)
secondOrderRez2 = simetricalOilersMethod(func, u0[0], step2_t_eval, step2)

# Piešiame grafikus
drawFunctions(rungeKuttoRez1, rungeKuttoRez2, step1_t_eval, stepMsg, title1, step2_t_eval)
drawFunctions(secondOrderRez1, secondOrderRez2, step1_t_eval, stepMsg, title2, step2_t_eval)

drawFunctions(rungeKuttoRez1, secondOrderRez1, step1_t_eval, rungeKuttoMsg, title3, message2=secondOrderMsg, step=step1)
drawFunctions(rungeKuttoRez2, secondOrderRez2, step2_t_eval, rungeKuttoMsg, title3, message2=secondOrderMsg, step=step2)


# Skaičiuojam paklaidas
print('4-pakopio Rungės-Kuto metodo paklaida yra lygi ', calculate_errors(rungeKuttoRez2, rungeKuttoRez1, 4))
print('Dvipakopio metodo, kai \u03C3=0,5, paklaida yra lygi ', calculate_errors(secondOrderRez2, secondOrderRez1, 2))