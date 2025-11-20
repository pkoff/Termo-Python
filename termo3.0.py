from colorama import Fore, Back, Style, init, Style
from unidecode import unidecode
import random
import pandas as pd

def restart(resultado):
    global palavraEscolhidaDecodada, winStreak, historico

    print("-"*6 + "="*6 + "-"*6)
    historico = []

    if resultado == "derrota":
        print(f'acabaram as tentativas, guerreiro, a palavra era {palavraEscolhidaDecodada}')
        winStreak = 0
    else:
        winStreak += 1

    r3 = input(f"vai escolher a bluepill para reiniciar e continuar no jogo, ou a redpill que vai te tirar do jogo? O termo foi feito em {totalTentativa} tentativas(Blue ou Red?(b/r)):").lower()
    if r3 == "b":
        palavraEscolhida = random.choice(totalpalavras_list)
        palavraEscolhidaDecodada = unidecode(palavraEscolhida)
    elif r3 == "r":
        print(f"voce saiu da matrix do termo com {totalTentativa} tentativas")
        quit()
    else:
        print("comando inválido, voce será retirado da matrix automaticamente")
        quit()

df = pd.read_csv('https://raw.githubusercontent.com/fserb/pt-br/refs/heads/master/icf', 
                 
                 header=None, 
                 names=['palavra', 'icf'] )

df2 = pd.read_csv('https://raw.githubusercontent.com/fserb/pt-br/refs/heads/master/lexico', 
                 
                 header=None, 
                 names=['palavra'] )

df3 = pd.read_csv('https://raw.githubusercontent.com/fserb/pt-br/refs/heads/master/conjuga%C3%A7%C3%B5es', 
                 
                 header=None, 
                 names=['palavra'] )

respostasPossiveis = pd.concat([
    df[df['palavra'].str.len() == 5]['palavra'],
    df2[df2['palavra'].str.len() == 5]['palavra'],
    df3[df3['palavra'].str.len() == 5]['palavra']
]).drop_duplicates().reset_index(drop=True)

totalpalavras = pd.concat([df.loc[(df['palavra'].str.len() == 5) & (df['icf'] < 15),'palavra'],
                            df2.loc[df2['palavra'].str.len() == 5,'palavra'],
                              df3.loc[df3['palavra'].str.len() == 5,'palavra']
                              ]).drop_duplicates().reset_index(drop=True)

historico = []
winStreak = 0

init(autoreset = True)

alfabeto = "abcdefghijklmnopqrstuvxwyz"
totalpalavras_list = [unidecode(palavra) for palavra in totalpalavras.tolist()]
respostasPossiveis_list = respostasPossiveis.tolist()

palavraEscolhida = random.choice(totalpalavras_list)
palavraEscolhidaDecodada = unidecode(palavraEscolhida)

while True:
    print("-"*6 + "="*6 + "-"*6)
    r = unidecode(input("Termo:").lower())

    if (len(r) != 5) or (r not in respostasPossiveis_list):
        print("palavra inválida, digite apenas palavras com cinco letras que compoem o léxico brasileiro")
        continue

    if not any(char in alfabeto for char in r):
        print("palavra inválida, escreva apenas letras do alfabeto")

    resultado_temp = [""] * 5
    restantes = {}

    for i, char in enumerate(palavraEscolhidaDecodada):
        if r[i] != char:
            restantes[char] = restantes.get(char, 0) + 1

    for i, char in enumerate(r):
        if char == palavraEscolhidaDecodada[i]:
            resultado_temp[i] = Back.GREEN + Fore.BLACK + char + Style.RESET_ALL + " "

    for i, char in enumerate(r):
        if resultado_temp[i] != "":
            continue

        if char in restantes and restantes[char] > 0:
            resultado_temp[i] = Back.YELLOW + Fore.BLACK + char + Style.RESET_ALL + " "
            restantes[char] -= 1
        else:
            resultado_temp[i] = Back.WHITE + Fore.BLACK + char + Style.RESET_ALL + " "

    resultado = "".join(resultado_temp)

    historico.append(resultado)

    totalTentativa = len(historico)

    print("\nhistórico da partida :)")
    for i, tentativa in enumerate(historico, start=1):
        print(f"{i}  {tentativa}")

    if winStreak > 1:
        print(f"win streak = {winStreak}")

    if totalTentativa >= 6:
        restart("derrota")

    if r == palavraEscolhidaDecodada:
        restart("vitória")