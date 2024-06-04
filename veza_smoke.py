import streamlit as st
import pandas as pd
import re
import io
import datetime
import random
import ssl
import certifi
context = ssl.create_default_context(cafile=certifi.where())
suffi = (sum(list(map(int, datetime.datetime.now().strftime("%d%m%Y"))))*random.randint(10000, 99999))%random.randint(100,999)+random.randint(1,random.randint(10,137))
st.set_page_config(layout="wide")
MU = 0.64
PHI = 0.4
ETHA = 0.9
ALPHA = 0.012
CP = 1.09
G = 9.81
def rasschet_mosh(first_window_data, moshnost):
    fwd = list(map(float, first_window_data))
    Qk = (1 - PHI) * float(moshnost)
    h0 = 0.166 * (Qk**0.4)
    Gk = 0.071*(Qk**(1/3))*(fwd[3]**(5/3)) + 0.0018*Qk if h0 < fwd[3] else 0.032*fwd[3]*(Qk**0.6)
    Gy = Gk
    Tv = fwd[4] + 273
    Tn = fwd[5] + 273
    Tpg = (Qk / (CP*Gy + ALPHA*(fwd[0] + fwd[1]*(fwd[2] - fwd[3])))) + Tv
    ron = 353/Tn
    ropg = 353/Tpg
    DELTAPrasp = G*(ron-ropg)*(fwd[2]-fwd[3])
    Fy = Gy / (MU*((2*ropg*DELTAPrasp)**0.5))
    Ly = (3600 * Gy)/ropg
    Gpr = Gy
    Fpr = Gpr / (MU*((2*ron*DELTAPrasp)**0.5))
    Lpr = (3600 * Gpr)/ron
    v = Lpr / (3600 * Fpr)
    results = [round(Fy, 3), round(Ly, 3), round(Fpr, 3), round(Lpr, 3), round(v, 3)]
    return results
def rasschet_plosh(first_window_data, ploshvars):
    fwd = list(map(float, first_window_data))
    Qp = 1000 * float(ploshvars[1])
    PSIud = float(ploshvars[2]) / 60
    Qk = (1-PHI) * ETHA * Qp * PSIud * float(ploshvars[0])
    h0 = 0.166 * (Qk**0.4)
    Gk = 0.071*(Qk**(1/3))*(fwd[3]**(5/3)) + 0.0018*Qk if h0 < fwd[3] else 0.032*fwd[3]*(Qk**0.6)
    Gy = Gk
    Tv = fwd[4] + 273
    Tn = fwd[5] + 273
    Tpg = (Qk / (CP*Gy + ALPHA*(fwd[0] + fwd[1]*(fwd[2] - fwd[3])))) + Tv
    ron = 353/Tn
    ropg = 353/Tpg
    DELTAPrasp = G*(ron-ropg)*(fwd[2]-fwd[3])
    Fy = Gy / (MU*((2*ropg*DELTAPrasp)**0.5))
    Ly = (3600 * Gy)/ropg
    Gpr = Gy
    Fpr = Gpr / (MU*((2*ron*DELTAPrasp)**0.5))
    Lpr = (3600 * Gpr)/ron
    v = Lpr / (3600 * Fpr)
    results = [round(Fy, 3), round(Ly, 3), round(Fpr, 3), round(Lpr, 3), round(v, 3)]
    return results
def usilie_privoda(dymozor, sneg):
    dymozor = int(dymozor[-3:])
    if dymozor == 300:
        return 40
    else:
        if (dymozor in [100,200,500] and sneg in ["I", "II"]) or (dymozor == 600 and sneg in ["I", "II", "III"]):
            return 1600
        else:
            return 3000
def picture_url(dymozor, kryshka):
    ds = {100:{"У": "https://i.postimg.cc/D0fzTtfT/image.png", "П": "https://i.postimg.cc/zB8zC9gg/image.png", "А": "https://i.postimg.cc/y8q1N4WH/image.png", "Р":"https://i.postimg.cc/jjgWkb01/100-1.png"}, 200:{"У": "https://i.postimg.cc/0y6wTqF1/image.png", "П": "https://i.postimg.cc/yNgyyRs9/image.png", "А": "https://i.postimg.cc/0jqnQNgS/image.png", "Р":"https://i.postimg.cc/4NQxSgp1/200-1.png"},300:{"У": "https://i.postimg.cc/KYzHS4Fv/image.png", "Р":"https://i.postimg.cc/nrn6s6MH/300-1.png"}, 500:{"У": "https://i.postimg.cc/FzT2J6yN/image.png", "П": "https://i.postimg.cc/qRxfpqgt/image.png", "А": "https://i.postimg.cc/CLy83KkC/image.png", "Р":"https://i.postimg.cc/3NrcrmbN/500-1.png"}, 600:{"У": "https://i.postimg.cc/g2RvwWDq/image.png", "Р":"https://i.postimg.cc/DzK5y1Sh/600-1.png"}}
    return ds[int(dymozor[-3:])][kryshka[0].upper()]
def opis_dimozor(model):
    slovar = {100:'ДЫМОЗОР®-100 предназначен для монтажа на плоскую кровлю здания либо с углом ската до 14 градусов и использования в системах противодымной вентиляции с естественным побуждением тяги. Рекомендуется для установки на одноэтажные здания большой площади. Кроме основного назначения – удаления продуктов горения, может быть использован для проветривания помещения. В варианте с прозрачной крышкой имеет функцию дополнительного естественного освещения помещения.',200:'ДЫМОЗОР®-200 предназначен для монтажа на плоскую кровлю здания либо с углом ската до 14 градусов и использования в системах противодымной вентиляции с естественным побуждением тяги. Рекомендуется для установки на одноэтажные здания большой площади. В варианте с прозрачными крышками имеет функцию дополнительного естественного освещения помещения. Кроме основного назначения – удаления продуктов горения, может быть использован для проветривания помещения.',300:'ДЫМОЗОР®-300 предназначен для монтажа в стену здания и использования в системах вытяжной противодымной вентиляции с естественным побуждением тяги. Кроме основного назначения – удаления продуктов горения, может быть использован для проветривания помещения, а также в системах приточной противодымной вентиляции с естественным побуждением тяги.',500:'ДЫМОЗОР®-500 предназначен для монтажа на кровлю здания с любым углом ската и использования в системах противодымной вентиляции с естественным побуждением тяги. В варианте с прозрачной крышкой имеет функцию дополнительного естественного освещения помещения. Кроме основного назначения – удаление продуктов горения, может быть использован для проветривания.',600:'ДЫМОЗОР®-600 предназначен для монтажа на плоскую кровлю здания либо с углом ската до 14 градусов и использования в системах противодымной вентиляции с естественным побуждением тяги. Рекомендуется для эксплуатации на зданиях, расположенных в районах с большим весом снегового покрова.'}
    return slovar[int(model)]
def nap_pit_dimozor(model):
    return {100:['24'],200:['24'],300:['24','220'],500:['24'],600:['24'],100:['24']}[int(model)]
def tip_krsh_dimozor(model):
    return {100:["У","П","А","АА","ААА"],200:["У","П","А","АА","ААА"],300:["У"],500:["У","П","А","АА","ААА"],600:["У"]}[int(model)]
def opis_krsh_dimozor(tip):
    slovar = {"У":'У – Утепленная непрозрачная. Наполнитель – самозатухающий пенопласт S = 50 мм (для серии 300 – минеральная вата). Сопротивление теплопередаче Rо = 1,29 м2×°С/Вт.',"П":'П – Прозрачная однослойная. Материал крышки – сотовый поликарбонат S = 16 мм. Сопротивление теплопередаче Rо = 0,45 м2×°С/Вт.',"А":'А – Архитектурная прозрачная с однослойным куполом. Материал крышки – монолитный поликарбонат. Сопротивление теплопередаче Rо = 0,24 м2×°С/Вт. Коэффициент направленногопропускания света 0,85',"АА":'АА – Архитектурная прозрачная с двухслойным куполом. Материал крышки – монолитный поликарбонат. Сопротивление теплопередаче Rо = 0,35 м2×°С/Вт. Коэффициент направленногопропускания света 0,81',"ААА":'ААА – Архитектурная прозрачная с трехслойным куполом. Материал крышки – монолитный поликарбонат. Сопротивление теплопередаче Rо = 0,52 м2×°С/Вт. Коэффициент направленногопропускания света 0,73'}
    return slovar[str(tip).upper()]
def choise_option_dimozor(model):
    return {100:['0','Решетка'],200:['0','Решетка'],300:['0','Экран'],500:['0','Решетка'],600:['0','Решетка']}[int(model)]
def opis_option_dimozor(tip):
    tip = str(tip).lower()
    slovar = {'0':'Не комплектуется','р':'защитная решетка. Служит для защиты от падения человека или иных предметов в проем люка.','решетка':'защитная решетка. Служит для защиты от падения человека или иных предметов в проем люка.','э':'Экран. Защищает проходное сечение открытого люка от фронтальных ветровых нагрузок.','экран':'Экран. Защищает проходное сечение открытого люка от фронтальных ветровых нагрузок.'}
    return slovar[tip]
def list_of_variants(lukeType:str, intersection:float, gabars=[10**100, 10**100]):
    mingab, maxgab = min(gabars), max(gabars)
    if "600" in lukeType:
        variants = {
            0.93 :  [[1000, 1000]],
            1.14 :  [[1100, 1100]],
            1.36 :  [[1200, 1200]],
            1.6 :   [[1300, 1300]],
            1.87 :  [[1400, 1400]],
            2.15 :  [[1500, 1500]]
        }
        correct_variants = {key: variants[key] for key in list(variants.keys()) if ((key > intersection))}
        for key in list(correct_variants.keys()):
            t_s = []
            term_s = correct_variants[key]
            for s in term_s:
                if (min(s) + 200 <= mingab) and (max(s) + 200 <= maxgab):
                    t_s.append(s)
            correct_variants[key] = t_s
        correct_variants = {key_: correct_variants[key_] for key_ in list(correct_variants.keys()) if len(correct_variants[key_]) != 0}
        return correct_variants
    if "500" in lukeType or "100" in lukeType:
        variants = {}
        A = [500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000] # 1 строка
        B = [600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800] # Столбец А
        inters = [[0.26, 0.32, 0.38, 0.44, 0.5, 0.56, 0.62, 0.68, 0.74, 0.8, 0.86, 0.92, 0.98, 1.04, 1.1, 1.16], [0.3, 0.37, 0.44, 0.51, 0.58, 0.65, 0.72, 0.79, 0.86, 0.93, 1.0, 1.07, 1.14, 1.21, 1.28, 1.35], [0.34, 0.42, 0.5, 0.58, 0.66, 0.74, 0.82, 0.9, 0.98, 1.06, 1.14, 1.22, 1.3, 1.38, 1.46, 1.54], [0.39, 0.48, 0.57, 0.66, 0.75, 0.84, 0.93, 1.02, 1.11, 1.2, 1.29, 1.38, 1.47, 1.56, 1.65, 1.74], [0.43, 0.53, 0.63, 0.73, 0.83, 0.93, 1.03, 1.13, 1.23, 1.33, 1.43, 1.53, 1.63, 1.73, 1.83, 1.93], [0.48, 0.59, 0.7, 0.81, 0.92, 1.03, 1.14, 1.25, 1.36, 1.47, 1.58, 1.69, 1.8, 1.91, 2.02, 2.13], [0.52, 0.64, 0.76, 0.88, 1.0, 1.12, 1.24, 1.36, 1.48, 1.6, 1.72, 1.84, 1.96, 2.08, 2.2, 2.32], [0.56, 0.69, 0.82, 0.95, 1.08, 1.21, 1.34, 1.47, 1.6, 1.73, 1.86, 1.99, 2.12, 2.25], [0.61, 0.75, 0.89, 1.03, 1.17, 1.31, 1.45, 1.59, 1.73, 1.87, 2.01, 2.15], [0.65, 0.8, 0.95, 1.1, 1.25, 1.4, 1.55, 1.7, 1.85, 2.0, 2.15], [0.7, 0.86, 1.02, 1.18, 1.34, 1.5, 1.66, 1.82, 1.98, 2.14], [0.74, 0.91, 1.08, 1.25, 1.42, 1.59, 1.76, 1.93, 2.1], [0.78, 0.96, 1.14, 1.33, 1.5, 1.68, 1.86, 2.04, 2.22]]
        for i in range(len(inters)):
            for j in range(len(inters[i])):
                variants[inters[i][j]] = []
        for i in range(len(inters)):
            for j in range(len(inters[i])):
                variants[inters[i][j]].append([A[j], B[i]])
        correct_variants = {key: variants[key] for key in list(variants.keys()) if ((key > intersection))}
        for key in list(correct_variants.keys()):
            t_s = []
            term_s = correct_variants[key]
            for s in term_s:
                if (min(s) + 200 <= mingab) and (max(s) + 200 <= maxgab):
                    t_s.append(s)
            correct_variants[key] = t_s
        correct_variants = {key_: correct_variants[key_] for key_ in list(correct_variants.keys()) if len(correct_variants[key_]) != 0}
        return correct_variants
    if "200" in lukeType:
        variants = {}
        A = [500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000]
        B = [1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 3200, 3300]
        inters = [[0.52, 0.64, 0.76, 0.88, 1.0, 1.12, 1.24, 1.36, 1.48, 1.6, 1.72, 1.84, 1.96, 2.08, 2.2, 2.32], [0.56, 0.69, 0.82, 0.95, 1.08, 1.21, 1.34, 1.47, 1.6, 1.73, 1.86, 1.99, 2.12, 2.25, 2.38, 2.51], [0.61, 0.75, 0.89, 1.03, 1.17, 1.31, 1.45, 1.59, 1.73, 1.87, 2.01, 2.15, 2.29, 2.43, 2.57, 2.71], [0.65, 0.8, 0.95, 1.1, 1.25, 1.4, 1.55, 1.7, 1.85, 2.0, 2.15, 2.3, 2.45, 2.6, 2.75, 2.9], [0.69, 0.85, 1.01, 1.17, 1.33, 1.49, 1.65, 1.81, 1.97, 2.13, 2.29, 2.45, 2.61, 2.77, 2.93, 3.09], [0.74, 0.91, 1.05, 1.25, 1.42, 1.59, 1.76, 1.93, 2.1, 2.27, 2.44, 2.61, 2.78, 2.95, 3.12, 3.29], [0.78, 0.96, 1.14, 1.32, 1.5, 1.68, 1.86, 2.04, 2.22, 2.4, 2.58, 2.76, 2.94, 3.12, 3.3, 3.48], [0.83, 1.02, 1.21, 1.4, 1.59, 1.78, 1.97, 2.16, 2.35, 2.54, 2.73, 2.92, 3.11, 3.3, 3.49, 3.68], [0.87, 1.07, 1.27, 1.47, 1.67, 1.87, 2.07, 2.27, 2.47, 2.67, 2.87, 3.07, 3.27, 3.47, 3.67], [0.91, 1.12, 1.33, 1.54, 1.75, 1.96, 2.17, 2.38, 2.59, 2.8, 3.01, 3.22, 3.43, 3.64], [0.96, 1.18, 1.4, 1.62, 1.84, 2.06, 2.28, 2.5, 2.72, 2.94, 3.16, 3.38, 3.6], [1.0, 1.23, 1.46, 1.69, 1.92, 2.15, 2.38, 2.61, 2.84, 3.07, 3.3, 3.53, 3.76], [1.05, 1.29, 1.53, 1.77, 2.01, 2.25, 2.49, 2.73, 2.97, 3.21, 3.45, 3.69], [1.09, 1.34, 1.59, 1.84, 2.09, 2.34, 2.59, 2.84, 3.09, 3.34, 3.59, 3.84], [1.13, 1.39, 1.65, 1.91, 2.17, 2.43, 2.69, 2.95, 3.21, 3.47, 3.73], [1.18, 1.45, 1.72, 1.99, 2.26, 2.53, 2.8, 3.07, 3.34, 3.61, 3.88], [1.22, 1.5, 1.78, 2.06, 2.34, 2.62, 2.9, 3.18, 3.46, 3.74, 4.02], [1.27, 1.56, 1.85, 2.14, 2.43, 2.72, 3.01, 3.3, 3.59, 3.88], [1.31, 1.61, 1.91, 2.21, 2.51, 2.81, 3.11, 3.41, 3.71, 4.01], [1.35, 1.66, 1.97, 2.28, 2.59, 2.9, 3.21, 3.52, 3.83, 4.14], [1.72, 2.04, 2.36, 2.68, 3.0, 3.32, 3.64, 3.96, 4.28], [1.77, 2.1, 2.43, 2.76, 3.09, 3.42, 3.75, 4.08]]
        for i in range(len(inters)):
            for j in range(len(inters[i])):
                variants[inters[i][j]] = []
        for i in range(len(inters)):
            for j in range(len(inters[i])):
                variants[inters[i][j]].append([A[j], B[i]])
        correct_variants = {key: variants[key] for key in list(variants.keys()) if ((key > intersection))}
        for key in list(correct_variants.keys()):
            t_s = []
            term_s = correct_variants[key]
            for s in term_s:
                if (min(s) + 200 <= mingab) and (max(s) + 200 <= maxgab):
                    t_s.append(s)
            correct_variants[key] = t_s
        correct_variants = {key_: correct_variants[key_] for key_ in list(correct_variants.keys()) if len(correct_variants[key_]) != 0}
        return correct_variants
    if "300" in lukeType:
        variants = {}
        A = [500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800]
        B = [500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000]
        inters = [[0.07, 0.09, 0.11, 0.13, 0.15, 0.16, 0.18, 0.2, 0.22, 0.24, 0.26, 0.28, 0.3, 0.32], [0.12, 0.15, 0.18, 0.22, 0.25, 0.28, 0.31, 0.34, 0.38, 0.41, 0.44, 0.47, 0.5, 0.53], [0.12, 0.15, 0.18, 0.22, 0.25, 0.28, 0.31, 0.34, 0.38, 0.41, 0.44, 0.47, 0.5, 0.53], [0.17, 0.22, 0.26, 0.31, 0.35, 0.4, 0.44, 0.49, 0.53, 0.57, 0.62, 0.66, 0.71, 0.75], [0.22, 0.28, 0.34, 0.4, 0.45, 0.51, 0.57, 0.63, 0.68, 0.74, 0.8, 0.86, 0.91, 0.97], [0.22, 0.28, 0.34, 0.4, 0.45, 0.51, 0.57, 0.63, 0.68, 0.74, 0.8, 0.86, 0.91, 0.97], [0.27, 0.35, 0.42, 0.49, 0.56, 0.63, 0.7, 0.77, 0.84, 0.91, 0.98, 1.05, 1.12, 1.19], [0.33, 0.41, 0.49, 0.58, 0.66, 0.74, 0.83, 0.91, 0.99, 1.08, 1.16, 1.24, 1.33, 1.41], [0.33, 0.41, 0.49, 0.58, 0.66, 0.74, 0.83, 0.91, 0.99, 1.08, 1.16, 1.24, 1.33, 1.41], [0.38, 0.47, 0.57, 0.67, 0.76, 0.86, 0.96, 1.05, 1.15, 1.24, 1.34, 1.44, 1.53, 1.63], [0.43, 0.54, 0.65, 0.76, 0.87, 0.97, 1.08, 1.19, 1.3, 1.41, 1.52, 1.63, 1.74, 1.85], [0.43, 0.54, 0.65, 0.76, 0.87, 0.97, 1.08, 1.19, 1.3, 1.41, 1.52, 1.63, 1.74, 1.85], [0.48, 0.6, 0.72, 0.85, 0.97, 1.09, 1.21, 1.33, 1.46, 1.58, 1.7, 1.82, 1.94, 2.07], [0.53, 0.67, 0.8, 0.94, 1.07, 1.21, 1.34, 1.48, 1.61, 1.75, 1.88, 2.02, 2.15, 2.29], [0.53, 0.67, 0.8, 0.94, 1.07, 1.21, 1.34, 1.48, 1.61, 1.75, 1.88, 2.02, 2.15, 2.29], [0.58, 0.73, 0.88, 1.03, 1.17, 1.32, 1.47, 1.62, 1.77, 1.91, 2.06, 2.21, 2.36, 2.5]]
        for i in range(len(inters)):
            for j in range(len(inters[i])):
                variants[inters[i][j]] = []
        for i in range(len(inters)):
            for j in range(len(inters[i])):
                variants[inters[i][j]].append([A[j], B[i]])
        correct_variants = {key: variants[key] for key in list(variants.keys()) if ((key > intersection) and (key < (intersection * 1.15)))}
        for key in list(correct_variants.keys()):
            t_s = []
            term_s = correct_variants[key]
            for s in term_s:
                if (min(s) + 100 <= mingab) and (max(s) + 100 <= maxgab):
                    t_s.append(s)
            correct_variants[key] = t_s
        correct_variants = {key_: correct_variants[key_] for key_ in list(correct_variants.keys()) if len(correct_variants[key_]) != 0}
        return correct_variants
def list_of_lukes(lukeType:str, intersection:float, kryshka, usilie, napryazhenie, opcia, l):
    glintersection = intersection
    intersection /= l
    vars = {}
    dzors = []
    cvars = list_of_variants(lukeType, intersection)
    for key in cvars:
        if not key in vars.keys():
            vars[key] = [cvars[key] + [l]]
        else:
            vars[key]+=[cvars[key] + [l]]
    for v in vars.keys():
        for item in vars[v][0][:-1]:
            d = f'ДЫМОЗОР-{lukeType[-3:]}-{item[0]}*{item[1]}-{kryshka}-{usilie}-{napryazhenie}-{opcia[:1]}-С'
            A = f"{item[0]}"
            B = f"{item[1]}"
            kolvo = vars[v][0][-1]
            zapas = round(round((((v*kolvo) - glintersection)/glintersection), 3)*100, 1)
            dzors.append([d, kolvo, round(zapas,1), A, B])
    return dzors
def two_excel(df, HEADER=False, START=1):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, header=HEADER,startrow=START, startcol=START, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    for idx, col in enumerate(df):
        series = df[col]
        max_len = max((series.astype(str).map(len).max(), len(str(series.name)))) + 4
        worksheet.set_column(idx,idx,max_len)
    url1 = picture_url(st.session_state["ДЫМОЗОР серия"], st.session_state["Тип крышки"])
    url2 = picture_url(st.session_state["ТИП ЛЮКА КОМПЕНСАЦИИ"], st.session_state["Тип крышки на компенсации"])
    import urllib.request
    data1 = urllib.request.urlopen(url1, context=context).read()
    file1 = open(f"{suffi}image1.jpg", "wb")
    file1.write(data1)
    file1.close()
    data2 = urllib.request.urlopen(url2, context=context).read()
    file2 = open(f"{suffi}image2.jpg", "wb")
    file2.write(data2)
    file2.close()
    worksheet.insert_image('A5', f"{suffi}image1.jpg")
    worksheet.insert_image('B5', f"{suffi}image2.jpg")
    writer.close()
    import os
    os.remove(f"{suffi}image1.jpg")
    os.remove(f"{suffi}image2.jpg")
    return output.getvalue()
A_tab = {"Бумага в рулонах"  : [13.4, 0.48],"Бумага во взрыхленном состоянии" : [13.4, 0.48],"Древесина"  : [13.85, 0.9],"Карболитовые изделия" : [26, 0.38],"Каучук натуральный"  : [42, 0.8],"Корд": [14, .25],"Пакет подвешенных тканей с расстоянием 0,2 м"  : [13.9, 1],"Пенополиуретан": [31.8, .92],"Полистирол (изделия)" : [42, .89],"РТИ": [33.6, .7],"Текстолит": [21, .53],"Угары в свободной укладке" : [13.9, .25, 6, 1.2],"Хлопок в плотной упаковке" : [16.8, .25],"Хлопок во взрыхленном состоянии" : [16.8, .25],"Шпательное волокно в рулонах" : [13.9, .4],"Шпательное волокно во взрыхленном состоянии"   : [13.9, .4],"Ацетон" : [29, 2.83],"Бензин" : [42, 3.3],"Бензол"  : [42, 2.3],"Дизельное топливо"  : [42, 2.5],"Диэтиловый эфир" : [33.6, 3.6],"Керосин": [43.7, 2.9],"Мазут" : [40, 2.1],"Метиловый спирт"  : [24, 0.96],"Нефть": [42, 1.4],"Толуол" : [42.7, 2.3]}
K_tab = tuple(sorted(A_tab.keys()))
mats = tuple(sorted([item for item in A_tab.keys()]))
col={}
st.header("Рекомендации по выбору дымовых люков")
st.session_state["Данные рассчёта"] = []
col[0] = st.columns(4)
with col[0][0]:
    st.write("#### Тип выбора ###")
    st.markdown("---")
    st.session_state["Вариант подбора дымового люка"] = col[0][0].radio("Вариант подбора дымового люка", options=("По тепловой мощности пожара", "По площади возгорания"))
    st.write("#### Параметры помещения ###")
    st.markdown("---")
    st.session_state["Высота помещения до места выброса продуктов горения, м"] = float(col[0][1].text_input("Высота помещения до места выброса продуктов горения, м", value='0').replace(",",'.'))
    st.session_state["Требуемая высота незадымленной зоны, м"] = float(col[0][1].text_input("Требуемая высота незадымленной зоны, м", value='0').replace(",",'.'))
    if st.session_state["Высота помещения до места выброса продуктов горения, м"] <= st.session_state["Требуемая высота незадымленной зоны, м"]:
        st.markdown(":red[Высота незадымленной зоны должна быть меньше высоты помещения до места выброса продуктов горения!]")
    st.markdown("---")
    st.session_state["Температура внутреннего воздуха, °C"] = float(col[0][1].text_input("Температура внутреннего воздуха, °C", value='0').replace(",",'.'))
    st.session_state["Температура наружнего воздуха, °C"] = float(col[0][1].text_input("Температура наружнего воздуха, °C", value='0').replace(",",'.'))
with col[0][0]:
    st.session_state["Площадь зоны дымоудаления, м²"] = float(col[0][0].text_input("Площадь зоны дымоудаления, м²", value='0').replace(",",'.'))
    st.session_state["Периметр ограждающих конструкций, м²"] = float(col[0][0].text_input("Периметр ограждающих конструкций, м", value='0').replace(",",'.'))
    if st.session_state["Вариант подбора дымового люка"] == "По тепловой мощности пожара":
        st.session_state["Тепловая мощность пожара, кВт"] = float(col[0][0].text_input("Тепловая мощность пожара, кВт", value='0').replace(",",'.'))
        try:
            first_window = [st.session_state[key] for key in ["Площадь зоны дымоудаления, м²", "Периметр ограждающих конструкций, м²", "Высота помещения до места выброса продуктов горения, м", "Требуемая высота незадымленной зоны, м", "Температура внутреннего воздуха, °C", "Температура наружнего воздуха, °C"]]
            st.session_state["Данные рассчёта"] = rasschet_mosh(first_window, st.session_state["Тепловая мощность пожара, кВт"])
        except:
            st.session_state["Данные рассчёта"] = []
    else:
        st.session_state["Площадь возгорания, м²"] = float(col[0][0].text_input("Площадь возгорания, м²", value='0').replace(",",'.'))
        st.session_state["Выбор материала"] = col[0][0].selectbox("Выбор материала", options=mats)
        try:
            first_window = [st.session_state[key] for key in ["Площадь зоны дымоудаления, м²", "Периметр ограждающих конструкций, м²", "Высота помещения до места выброса продуктов горения, м", "Требуемая высота незадымленной зоны, м", "Температура внутреннего воздуха, °C", "Температура наружнего воздуха, °C"]]
            ploshi = [st.session_state["Площадь возгорания, м²"], A_tab[st.session_state["Выбор материала"]][0], A_tab[st.session_state["Выбор материала"]][1]]
            st.session_state["Данные рассчёта"] = rasschet_plosh(first_window, ploshi)
        except:
            st.session_state["Данные рассчёта"] = []
st.session_state["Данные рассчёта"]
st.markdown("---")
with col[0][2]:
    if not len(st.session_state["Данные рассчёта"]):
        pass
    else:
        st.write("#### Выбор параметров люка ###")
        st.markdown("---")
        st.session_state["Расположение люка"] = st.radio("Выбор расположения дымового люка", options=("На крыше", "В стене"), horizontal=True)
        if st.session_state["Расположение люка"] == "В стене":
            st.session_state["ДЫМОЗОР серия"] = st.radio("Серия дымового люка", options=("ДЫМОЗОР®-300", "ДЫМОЗОР®-500"), horizontal=True)
            with st.expander(f'Краткое описание {st.session_state["ДЫМОЗОР серия"]}'):
                st.write(opis_dimozor(st.session_state["ДЫМОЗОР серия"][-3:]))
            st.session_state["ДЫМОЗОР напряжение привода"] = st.radio("Напряжение привода, В", options=('24','220') if st.session_state["ДЫМОЗОР серия"] == "ДЫМОЗОР®-300" else ('24',), horizontal=True)
        else:
            st.session_state['ДЫМОЗОР угол ската кровли'] = st.radio("Угол ската кровли", options=("до 14°", "более 14°"), horizontal=True)
            if st.session_state['ДЫМОЗОР угол ската кровли'] == "более 14°":
                st.session_state['ДЫМОЗОР регион снеговой нагрузки'] = st.radio("Регион снеговой нагрузки", options=("I","II","III","IV","V"), horizontal=True)
                st.session_state["ДЫМОЗОР серия"] = st.radio("Серия дымового люка", options=("ДЫМОЗОР®-500",), horizontal=True)
                with st.expander(f'Краткое описание {st.session_state["ДЫМОЗОР серия"]}'):
                    st.write(opis_dimozor(st.session_state["ДЫМОЗОР серия"][-3:]))
            else:
                st.session_state['ДЫМОЗОР регион снеговой нагрузки'] = st.radio("Регион снеговой нагрузки", options=("I","II","III","IV","V","VI"), horizontal=True)
                if st.session_state['ДЫМОЗОР регион снеговой нагрузки'] == "VI":
                    st.session_state["ДЫМОЗОР серия"] = st.radio("Серия дымового люка", options=("ДЫМОЗОР®-600",), horizontal=True)
                    with st.expander(f'Краткое описание {st.session_state["ДЫМОЗОР серия"]}'):
                        st.write(opis_dimozor(st.session_state["ДЫМОЗОР серия"][-3:]))
                else:
                    st.session_state["ДЫМОЗОР серия"] = st.radio("Серия дымового люка", options=("ДЫМОЗОР®-100", "ДЫМОЗОР®-200", "ДЫМОЗОР®-500", "ДЫМОЗОР®-600"), horizontal=True)
                    with st.expander(f'Краткое описание {st.session_state["ДЫМОЗОР серия"]}'):
                        st.write(opis_dimozor(st.session_state["ДЫМОЗОР серия"][-3:]))
        if not "3" in st.session_state["ДЫМОЗОР серия"]:
            st.session_state['ДЫМОЗОР напряжение привода'] = '24'
        if st.session_state["ДЫМОЗОР серия"] in ["ДЫМОЗОР®-100", "ДЫМОЗОР®-200", "ДЫМОЗОР®-500"]:
            st.session_state["Тип крышки"] = st.radio("Тип крышки", options=('У', 'П', 'ААА'), horizontal=True)
            with st.expander(f'Описание крышки {st.session_state["Тип крышки"]}'):
                st.write(opis_krsh_dimozor(st.session_state["Тип крышки"]))
        elif st.session_state["ДЫМОЗОР серия"] in ["ДЫМОЗОР®-300", "ДЫМОЗОР®-600"]:
            st.session_state["Тип крышки"] = st.radio("Тип крышки", options=('У',), horizontal=True)
            with st.expander(f'Описание крышки {st.session_state["Тип крышки"]}'):
                st.write(opis_krsh_dimozor(st.session_state["Тип крышки"]))
        st.session_state["ДЫМОЗОР опция"] = st.radio("Oпция", tuple(choise_option_dimozor(st.session_state["ДЫМОЗОР серия"][-3:])), horizontal=True)
        with st.expander(f'Опция {st.session_state["ДЫМОЗОР опция"]}'):
            st.write(opis_option_dimozor(st.session_state["ДЫМОЗОР опция"]))
try:
    st.session_state["Усилие привода"] = usilie_privoda(st.session_state["ДЫМОЗОР серия"], st.session_state['ДЫМОЗОР регион снеговой нагрузки'])
except:
    pass
try:
    spisok = ["Площадь проёма дымоудаления", "Расход удаляемых продуктов горения", "Площадь проёма компенсации", "Расход приточного воздуха", "Скорость потока в проёме компенсации"]
    raschdic = {"Расчётные данные":{spisok[i]:st.session_state["Данные рассчёта"][i] for i in range(len(spisok))}}
    # st.write(raschdic)
except:
    pass
with col[0][3]:
    if not len(st.session_state["Данные рассчёта"]):
        pass
    else:
        st.write("#### Схема ###")
        st.markdown("---")
        try:
            st.write(f'#### {st.session_state["ДЫМОЗОР серия"]} ###')
            st.image(picture_url(st.session_state["ДЫМОЗОР серия"], st.session_state["Тип крышки"]))
        except:
            pass
try:
    aplaceholder = st.session_state['ДЫМОЗОР напряжение привода']
except:
    st.session_state['ДЫМОЗОР напряжение привода'] = '24'
try:
    phmd = st.session_state["ДЫМОЗОР серия"]
    st.write("#### Выберите из списка ###")
    st.image(picture_url(st.session_state["ДЫМОЗОР серия"], "Р"))
    if "300" in st.session_state["ДЫМОЗОР серия"]:
        st.markdown(":red[Размер проема для Дымозор-300 должен быть на 20 мм больше номинального размера люка.]")
    ss_ = st.columns(3)
    st.session_state["Число люков"] = ss_[0].select_slider("Выберите число дымовых люков", options=[i for i in range(1,31) if len(list_of_lukes(st.session_state["ДЫМОЗОР серия"], st.session_state["Данные рассчёта"][0], st.session_state['Тип крышки'], st.session_state['Усилие привода'], st.session_state['ДЫМОЗОР напряжение привода'], st.session_state['ДЫМОЗОР опция'], i))])
    spisok_lukov = sorted(list_of_lukes(st.session_state["ДЫМОЗОР серия"], st.session_state["Данные рассчёта"][0], st.session_state['Тип крышки'], st.session_state['Усилие привода'], st.session_state['ДЫМОЗОР напряжение привода'], st.session_state['ДЫМОЗОР опция'], st.session_state["Число люков"]), key=lambda x:x[2])
    spisok_lukov = sorted(spisok_lukov, key=lambda x: int(re.findall(r"-(\d+)\*",x[0])[0]) * int(re.findall(r"\*(\d+)-", x[0])[0]))
    spisok_lukov = sorted(spisok_lukov, key=lambda x: int(re.findall(r"\*(\d+)-", x[0])[0]))
    spisok_lukov = sorted(spisok_lukov, key=lambda x: int(re.findall(r"-(\d+)\*",x[0])[0]))
    spisok_lukov = sorted(spisok_lukov, key=lambda x: x[2])
    spisok_lukov = spisok_lukov if len(spisok_lukov)<=10 else spisok_lukov[:10]
    colu = st.columns((2,1,1,1,4), gap="small")
    luk = ((item[0] for item in spisok_lukov))
    kol_luk = "<br>".join([str(item[1]) for item in spisok_lukov])
    zap_luk = "<br>".join([str(item[2]) for item in spisok_lukov])
    A_luk =   "<br>".join([str(item[3]) for item in spisok_lukov])
    B_luk =   "<br>".join([str(item[4]) for item in spisok_lukov])
    colu[0].write("Выбор дымового люка")
    st.session_state["Выбранный люк"] = colu[0].radio("Выбор дымового люка", options=luk, label_visibility="collapsed")
    colu[1].write("Запас площади, %")
    colu[1].write(zap_luk, unsafe_allow_html=True)
    colu[2].write("A, мм")
    colu[2].write(A_luk, unsafe_allow_html=True)
    if not "600" in st.session_state["ДЫМОЗОР серия"]:
        colu[3].write("B, мм")
        colu[3].write(B_luk, unsafe_allow_html=True)
    st.markdown("---")
    st.write("#### Люк компенсации ###")
    st.session_state["ТИП ЛЮКА КОМПЕНСАЦИИ"] = st.radio("Выберите люк компесации", options=("ДЫМОЗОР®-300", "ДЫМОЗОР®-500") if st.session_state['ДЫМОЗОР напряжение привода']=="24" else ("ДЫМОЗОР®-300",), horizontal=True)
    if "5" in st.session_state["ТИП ЛЮКА КОМПЕНСАЦИИ"]:
        st.session_state["Тип крышки на компенсации"] = st.radio("Выберите крышку люка компесации", options=('У', 'П', 'ААА'), horizontal=True)
    else:
        st.session_state["Тип крышки на компенсации"] = "У"
    st.image(picture_url(st.session_state["ТИП ЛЮКА КОМПЕНСАЦИИ"], "Р"))
    if "3" in st.session_state["ТИП ЛЮКА КОМПЕНСАЦИИ"]:
        st.markdown(":red[Размер проема для Дымозор-300 должен быть на 20 мм больше номинального размера люка.]")
    ss_u = st.columns(3)
    st.session_state["ОПЦИЯ ПРИТОКА"] = st.radio("Выберите опцию для люка компенсации", options=("0", "Экран") if "3" in st.session_state["ТИП ЛЮКА КОМПЕНСАЦИИ"] else ("0", "Решетка"), horizontal=True)
    st.session_state["Число люков компенсации"] = ss_u[0].select_slider("Выберите число люков компенсации", options=[lil for lil in range(1,31) if len(list_of_lukes(st.session_state["ТИП ЛЮКА КОМПЕНСАЦИИ"], st.session_state["Данные рассчёта"][2], "У", usilie_privoda(st.session_state["ТИП ЛЮКА КОМПЕНСАЦИИ"], st.session_state['ДЫМОЗОР регион снеговой нагрузки']), st.session_state['ДЫМОЗОР напряжение привода'], st.session_state["ОПЦИЯ ПРИТОКА"], lil))])
    spisok_lukov_p = sorted(list_of_lukes(st.session_state["ТИП ЛЮКА КОМПЕНСАЦИИ"], st.session_state["Данные рассчёта"][2], st.session_state["Тип крышки на компенсации"], usilie_privoda(st.session_state["ТИП ЛЮКА КОМПЕНСАЦИИ"], st.session_state['ДЫМОЗОР регион снеговой нагрузки']), st.session_state['ДЫМОЗОР напряжение привода'], st.session_state["ОПЦИЯ ПРИТОКА"], st.session_state["Число люков компенсации"]), key=lambda x:x[2])
    spisok_lukov_p = sorted(spisok_lukov_p, key=lambda x: int(re.findall(r"-(\d+)\*",x[0])[0]) * int(re.findall(r"\*(\d+)-", x[0])[0]))
    spisok_lukov_p = sorted(spisok_lukov_p, key=lambda x: int(re.findall(r"\*(\d+)-", x[0])[0]))
    spisok_lukov_p = sorted(spisok_lukov_p, key=lambda x: int(re.findall(r"-(\d+)\*",x[0])[0]))
    spisok_lukov_p = sorted(spisok_lukov_p, key=lambda x: x[2])
    spisok_lukov_p = spisok_lukov_p if len(spisok_lukov_p)<=10 else spisok_lukov_p[:10]
    coluk = st.columns((2,1,1,1,4), gap="small")
    luk_p = ((item[0] for item in spisok_lukov_p))
    kol_luk_p = "<br>".join([str(item[1]) for item in spisok_lukov_p])
    zap_luk_p = "<br>".join([str(item[2]) for item in spisok_lukov_p])
    A_luk_p =   "<br>".join([str(item[3]) for item in spisok_lukov_p])
    B_luk_p =   "<br>".join([str(item[4]) for item in spisok_lukov_p])
    coluk[0].write("Выбор люка компенсации")
    st.session_state["Выбранный люк компенсации"] = coluk[0].radio("Выбор люка компенсации", options=luk_p, label_visibility="collapsed")
    coluk[1].write("Запас площади, %")
    coluk[1].write(zap_luk_p, unsafe_allow_html=True)
    coluk[2].write("A, мм")
    coluk[2].write(A_luk_p, unsafe_allow_html=True)
    coluk[3].write("B, мм")
    coluk[3].write(B_luk_p, unsafe_allow_html=True)
    st.markdown("---")
    st.session_state['Подобрано'] = [[st.session_state["Выбранный люк"], str(st.session_state["Число люков"]), st.session_state["Выбранный люк компенсации"], str(st.session_state["Число люков компенсации"])]]
    picol = st.columns((1,6,1))
    with picol[1]:
        st.write("#### Подобранные варианты ###")
        st.table(pd.DataFrame(st.session_state['Подобрано'], columns=["Дымовой люк","Количество дымовых люков, шт.", "Люк компенсации", "Количество люков компенсации, шт."]).assign(hack='').set_index('hack').style)
    picol_p = st.columns((1,3,3,1))
    with picol_p[1]:
        st.image(picture_url(st.session_state["ДЫМОЗОР серия"], st.session_state["Тип крышки"]))
        st.write(f"#### {st.session_state['ДЫМОЗОР серия']} ###")
    with picol_p[2]:
        st.image(picture_url(st.session_state["ТИП ЛЮКА КОМПЕНСАЦИИ"], st.session_state["Тип крышки на компенсации"]))
        st.write(f"#### {st.session_state['ТИП ЛЮКА КОМПЕНСАЦИИ']} ###")
    ppic = st.columns(3)
    with ppic[1]:
        st.download_button(label='💾 Скачать файл с выбранными люками',data=two_excel(pd.DataFrame({st.session_state["Выбранный люк"]: [str(st.session_state["Число люков"]) + " шт.", "На вытяжке", "", "", "", "", "", ""], st.session_state["Выбранный люк компенсации"]:[str(st.session_state["Число люков компенсации"])+" шт.", "Компенсация", "", "", "", "", "", ""], "":["","", "", "", "", "", "", ""], "Параметры подбора":["Вариант подбора","Тепловая мощность пожара" if st.session_state["Вариант подбора дымового люка"]=="По тепловой мощности пожара" else "Площадь возгорания | Горючий материал", "Площадь зоны дымоудаления, м²", "Периметр ограждающих конструкций, м", "Высота помещения до места выброса продуктов горения, м", "Требуемая высота незадымленной зоны, м", "Температура внутреннего воздуха, °C", "Температура наружнего воздуха, °C"], "Значения":[st.session_state["Вариант подбора дымового люка"], str(st.session_state["Тепловая мощность пожара, кВт"]) if st.session_state["Вариант подбора дымового люка"]=="По тепловой мощности пожара" else str(st.session_state["Площадь возгорания, м²"])+" | "+(st.session_state["Выбор материала"]), str(st.session_state["Площадь зоны дымоудаления, м²"]), str(st.session_state["Периметр ограждающих конструкций, м²"]), str(st.session_state["Высота помещения до места выброса продуктов горения, м"]), str(st.session_state["Требуемая высота незадымленной зоны, м"]), str(st.session_state["Температура внутреннего воздуха, °C"]), str(st.session_state["Температура наружнего воздуха, °C"])], "Параметры дымового люка":["Расположение","Угол ската кровли", "Регион снеговой нагрузки" if st.session_state["ДЫМОЗОР серия"][-3:]!="300" else "Напряжение привода", "Тип крышки", "Опция", "Опция люка компенсации", "", ""], "Выбранные значения":[st.session_state["Расположение люка"],st.session_state['ДЫМОЗОР угол ската кровли'], st.session_state['ДЫМОЗОР регион снеговой нагрузки'] if st.session_state["ДЫМОЗОР серия"][-3:]!="300" else st.session_state['ДЫМОЗОР напряжение привода'], st.session_state["Тип крышки"], st.session_state["ДЫМОЗОР опция"], st.session_state["ОПЦИЯ ПРИТОКА"], "", ""]}), HEADER=True, START=0) ,file_name= f'дымовые_люки{suffi}.xlsx')
except:
    pass
