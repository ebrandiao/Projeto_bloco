import pygame
import sys
import psutil
import socket
import cpuinfo

# CORES
PRETO = (0, 0, 0)
AZUL = (242, 174, 114)
BRANCO = (88, 140, 126)
VERMELHO = (179, 64, 51)
AMARELO = (242, 227, 148)

# Fontes
pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 20)
body_font = pygame.font.SysFont(None, 18)

# Iniciando a janela principal
largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Eduardo Brandiao - TP04")
pygame.display.init()

# Menu superior
# Textos
cabecalho = ["CPU", "MEMÓRY", "DISK", "IP", "INFORMATION"]

# Posição inicial do marcador
circulo = 10
# Lista das posições do marcador
marcador = [10, 80, 160, 240, 320]

# Cria relógio
clock = pygame.time.Clock()

# Criação das telas
tela_cpu = pygame.surface.Surface((largura_tela, altura_tela - 20))
tela_mem = pygame.surface.Surface((largura_tela, altura_tela - 20))
tela_disco = pygame.surface.Surface((largura_tela, altura_tela - 20))
tela_ip = pygame.surface.Surface((largura_tela, altura_tela - 20))
tela_resumo = pygame.surface.Surface((largura_tela, altura_tela - 20))

# Lista das telas
telas = [tela_cpu, tela_mem, tela_disco, tela_ip, tela_resumo]
# Define a tela inicial
view = telas[0]

n = 0
info_cpu = cpuinfo.get_cpu_info()


# Mostrar uso de CPU
def mostra_uso_cpu(s, l_cpu_percent):
    s.fill(PRETO)
    num_cpu = len(l_cpu_percent)
    x = 10
    y = 20
    desl = 10
    alt = s.get_height() // 2 - 2 * y
    larg = (s.get_width() - 2 * y - (num_cpu + 1) * desl) / num_cpu
    d = x + desl
    for i in l_cpu_percent:
        pygame.draw.rect(s, VERMELHO, (d, y, larg, alt))
        pygame.draw.rect(s, AZUL, (d, y, larg, (1 - i / 100) * alt))
        d = d + larg + desl


def mostra_info_cpu():
    mostra_texto(tela_cpu, "Nome:", "brand_raw", 310)
    mostra_texto(tela_cpu, "Arquitetura:", "arch", 340)
    mostra_texto(tela_cpu, "Palavra (bits):", "bits", 370)
    mostra_texto(tela_cpu, "Frequência (MHz):", "freq", 400)
    mostra_texto(tela_cpu, "Núcleos (físicos):", "nucleos", 430)


# Mostra texto de acordo com uma chave:
def mostra_texto(s1, nome, chave, pos_y):
    text1 = font.render(nome, True, BRANCO)
    s1.blit(text1, (20, pos_y))
    if chave == "freq":
        s = f"{round(psutil.cpu_freq().current, 2)} (atual) | {psutil.cpu_freq().max} (máx.)"
    elif chave == "nucleos":
        s = str(psutil.cpu_count())
        s = s + " (" + str(psutil.cpu_count(logical=False)) + ")"
    else:
        s = str(info_cpu[chave])
    text2 = font.render(s, True, AMARELO)
    s1.blit(text2, (text1.get_width() + 30, pos_y))


# Mostar uso de memória
def mostra_uso_memoria():
    tela_mem.fill(PRETO)
    mem = psutil.virtual_memory()
    larg = largura_tela - 2 * 20
    pygame.draw.rect(tela_mem, AZUL, (20, 70, larg, 70))
    larg = larg * mem.percent / 100
    pygame.draw.rect(tela_mem, VERMELHO, (20, 70, larg, 70))
    total = round(mem.total / (1024 * 1024 * 1024), 2)
    texto_barra = "Uso da Memória (Total: " + str(total) + "GB):"
    text = font.render(texto_barra, True, BRANCO)
    tela_mem.blit(text, (20, 30))


# Mostrar o uso de disco local
def mostra_uso_disco():
    tela_disco.fill(PRETO)
    disco = psutil.disk_usage('.')
    larg = largura_tela - 2 * 20
    pygame.draw.rect(tela_disco, AZUL, (20, 70, larg, 70))
    larg = larg * disco.percent / 100
    pygame.draw.rect(tela_disco, VERMELHO, (20, 70, larg, 70))
    total = round(disco.total / (1024 * 1024 * 1024), 2)
    texto_barra = "Uso do Disco: (Total: " + str(total) + "GB):"
    text = font.render(texto_barra, True, BRANCO)
    tela_disco.blit(text, (20, 30))


# Obter endereços IP
def obter_endereco_ip(family):
    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family == family:
                yield interface, snic.address


# Função que itera a lista de IPs
def imprime_ip(lista, surface):
    y = 60
    for address in lista:
        texto = body_font.render(f"{address}", True, AMARELO)
        surface.blit(texto, (20, y))
        y += 20


# Mostrar endereços IP
def mostra_ip():
    tela_ip.fill(PRETO)
    ipv4s = list(obter_endereco_ip(socket.AF_INET))
    texto_barra = font.render("IP: ", True, BRANCO)
    tela_ip.blit(texto_barra, (20, 30))
    imprime_ip(ipv4s, tela_ip)


def mostra_resumo():
    tela_resumo.fill(PRETO)
    cpu_name = info_cpu['brand_raw']
    texto_cpu = font.render(f"Processador: {cpu_name}", True, AMARELO)
    disco = psutil.disk_usage('.')
    texto_disco = font.render(
        f"Disco: {round(disco.used / (1024 * 1024 * 1024), 2)} de {round(disco.total / (1024 * 1024 * 1024), 2)}GB usados",
        True, AMARELO)
    mem = psutil.virtual_memory()
    texto_memoria = font.render(
        f"Memória: {round(mem.used / (1024 * 1024 * 1024), 2)} de {round(mem.total / (1024 * 1024 * 1024), 2)}GB usados",
        True, AMARELO)
    tela_resumo.blit(texto_cpu, (20, 30))
    tela_resumo.blit(texto_disco, (20, 70))
    tela_resumo.blit(texto_memoria, (20, 110))


cont = 60

while True:
    # Checar os eventos aqui:
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if n < len(telas) - 1:
                    n += 1
                else:
                    n = 0
                view = telas[n]
                circulo = marcador[n]
            if event.key == pygame.K_LEFT:
                if n > 0:
                    n -= 1
                else:
                    n = len(telas) - 1
                view = telas[n]
                circulo = marcador[n]
            if event.key == pygame.K_SPACE:
                n = len(telas) - 1
                view = telas[-1]
                circulo = marcador[-1]

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    tela.fill(PRETO)

    # Chamadas das funções
    if cont == 60:
        mostra_uso_memoria()
        mostra_uso_disco()
        mostra_uso_cpu(tela_cpu, psutil.cpu_percent(percpu=True))
        mostra_info_cpu()
        mostra_ip()
        mostra_resumo()
        cont = 0

    # Posiciona menu superior
    tela.blit(body_font.render(cabecalho[0], True, BRANCO), (20, 5))
    tela.blit(body_font.render(cabecalho[1], True, BRANCO), (5 + largura_tela // 10, 5))
    tela.blit(body_font.render(cabecalho[2], True, BRANCO), (5 + 2 * largura_tela // 10, 5))
    tela.blit(body_font.render(cabecalho[3], True, BRANCO), (5 + 3 * largura_tela // 10, 5))
    tela.blit(body_font.render(cabecalho[4], True, BRANCO), (5 + 4 * largura_tela // 10, 5))

    # Atualiza a view
    tela.blit(view, (0, 20))
    # Cursor da tela selecionada
    pygame.draw.circle(tela, VERMELHO, (circulo, 12), 5)

    # Atualiza o desenho na tela
    pygame.display.update()

    # 60 frames por segundo
    clock.tick(60)
    cont += 1