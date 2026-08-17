from playwright.sync_api import sync_playwright
from datetime import datetime

# ---------------------------------------------------------------------------
# AUTOMAÇÃO FGTS - Emissão de Guias e Relatórios
# ---------------------------------------------------------------------------
# 
# CONFIGURAÇÕES DISPONÍVEIS (edite conforme necessário):
#
# 1. COMPETENCIA: Mês/Ano a processar (ex: "07/2026")
# 2. VENCIMENTO_DESEJADO: Específica qual data de vencimento baixar
#    - None (padrão) = baixa TODAS as datas disponíveis
#    - "18/08/2026" = baixa APENAS guias com esse vencimento
# 3. BAIXAR_TODOS_VENCIMENTOS: True = ignora VENCIMENTO_DESEJADO e baixa tudo
#
# EXEMPLOS DE USO:
# - Baixar TODAS as guias da competência: deixe BAIXAR_TODOS_VENCIMENTOS = True
# - Baixar APENAS vencimento 20/08/2026: defina VENCIMENTO_DESEJADO = "20/08/2026"
# - Processar competência diferente: altere COMPETENCIA = "08/2026"
#
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# LOG - registra tudo em arquivo alem de mostrar no cmd, pra revisar depois
# ---------------------------------------------------------------------------

def registrar(mensagem):
    print(mensagem)
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            hora = datetime.now().strftime("%H:%M:%S")
            f.write(f"[{hora}] {mensagem}\n")
    except Exception:
        pass  # se der erro ao gravar o log, so segue sem travar o script

# ---------------------------------------------------------------------------
# CONFIGURAÇÕES
# ---------------------------------------------------------------------------

CNPJS_EMPRESAS = {
    "00.000.000/00001/00": "NOME DA EMPRESA 1",
    "00.000.000/00001/00": "NOME DA EMPRESA 2", #colocar todos nesse formato, sejam quantas empresas for
}

COMPETENCIA = "07/2026"
PASTA_DOWNLOAD = r"C:\Users\RH Intersoft\Desktop\GuiasFGTS"
LOG_PATH = r"C:\Users\RH Intersoft\Desktop\GuiasFGTS\log_execucao.txt"

# OPÇÕES DE FILTRAGEM
VENCIMENTO_DESEJADO = None  # None = baixa TODAS as guias, ou especifique "18/08/2026" para uma específica
BAIXAR_TODOS_VENCIMENTOS = True  # True = baixa todos os vencimentos disponíveis


# ---------------------------------------------------------------------------
# FUNÇÕES DE AUTOMAÇÃO
# ---------------------------------------------------------------------------

def desmarcar_rescisorio(page, nome_empresa):
    """Desmarca a checkbox de Rescisório após selecionar competência.
    Retorna True se conseguiu desmarcar, False caso contrário."""
    try:
        checkbox_rescisorio = page.locator("#h-checkbox-2")
        if checkbox_rescisorio.count() > 0:
            if checkbox_rescisorio.is_checked(timeout=1000):
                checkbox_rescisorio.click(force=True)
                page.wait_for_timeout(500)
                registrar(f"  ✓ Rescisório desmarcado")
                return True
        else:
            registrar(f"  ⚠️ Checkbox rescisório não encontrado")
            return False
    except Exception as e:
        registrar(f"  ⚠️ Erro ao desmarcar rescisório: {str(e)}")
        return False


def listar_vencimentos_disponiveis(page):
    """Lista todas as datas de vencimento ÚNICAS disponíveis na página após pesquisar.
    Retorna uma lista com as datas encontradas (ex: ["18/08/2026", "20/08/2026"])."""
    vencimentos_unicos = set()  # Usa set para garantir unicidade
    try:
        # Procura por todos os elementos com padrão "Mensal - Vencimento da Guia: DD/MM/YYYY"
        titulos = page.locator("text=/Mensal.*Vencimento da Guia:/").all()
        
        for titulo in titulos:
            try:
                texto = titulo.text_content()
                if "Vencimento da Guia:" in texto:
                    data = texto.split("Vencimento da Guia:")[1].strip()
                    vencimentos_unicos.add(data)  # Adiciona ao set (automáticamente evita duplicatas)
            except Exception:
                continue
        
        # Converte de volta para lista e ordena
        vencimentos = sorted(list(vencimentos_unicos))
        for data in vencimentos:
            registrar(f"  → Vencimento encontrado: {data}")
                
    except Exception as e:
        registrar(f"  ⚠️ Erro ao listar vencimentos: {str(e)}")
        vencimentos = []
    
    return vencimentos


def filtrar_vencimento(vencimentos_disponiveis, vencimento_selecionado):
    """Filtra os vencimentos baseado na seleção do usuário.
    Se BAIXAR_TODOS_VENCIMENTOS=True, retorna todos.
    Se vencimento_selecionado especificado, retorna apenas esse."""
    if BAIXAR_TODOS_VENCIMENTOS:
        return vencimentos_disponiveis
    elif vencimento_selecionado and vencimento_selecionado in vencimentos_disponiveis:
        return [vencimento_selecionado]
    elif vencimento_selecionado:
        registrar(f"  ⚠️ Vencimento {vencimento_selecionado} não encontrado. Baixando todos...")
        return vencimentos_disponiveis
    else:
        return vencimentos_disponiveis


def obter_card_guia_por_vencimento(page, vencimento):
    """Localiza o card específico de uma guia pelo seu vencimento.
    Retorna o card (locator) se encontrado, None caso contrário."""
    try:
        # Procura pelo padrão exato "Vencimento da Guia: DD/MM/YYYY" dentro de um container
        card = page.locator(f"div:has-text('Vencimento da Guia: {vencimento}')").first
        if card.count() > 0:
            return card
    except Exception:
        pass
    return None


def abrir_selecionar_procurador(page):
    """Volta para a home (onde 'Trocar Perfil' fica disponivel), abre o modal
    e seleciona a opcao 'Procurador'. Deixa pronto pro CNPJ ser digitado."""
    try:
        page.goto(
            "https://fgtsdigital.sistema.gov.br/portal/servicos",
            wait_until="domcontentloaded",
            timeout=15000,
        )
    except Exception:
        pass  # segue mesmo se a navegacao "travar" - a pagina ja deve ter mudado
    page.wait_for_timeout(1500)
    page.get_by_role("button", name="Trocar Perfil").click()
    page.wait_for_timeout(500)
    page.locator("input[role='combobox']:visible").first.click()
    page.get_by_text("Procurador", exact=True).click()
    page.wait_for_timeout(300)


def tentar_selecionar_cnpj(page, cnpj):
    """Preenche o CNPJ no modal ja aberto e clica em Selecionar.
    Retorna True se o modal fechou (deu certo).
    Retorna False se o modal continuar aberto (ex: sem procuracao para o CNPJ) -
    nesse caso o campo fica pronto pra tentar o proximo CNPJ direto, sem
    precisar reabrir 'Trocar Perfil'."""
    campo_cnpj = page.get_by_placeholder("Informe CNPJ ou CPF")
    campo_cnpj.fill("")
    campo_cnpj.fill(cnpj)
    page.get_by_role("button", name="Selecionar").click()
    page.wait_for_timeout(1500)

    # Se o botao "Selecionar" ainda estiver visivel, o modal nao fechou -
    # sinal de erro (ex: CNPJ sem procuracao configurada)
    modal_ainda_aberto = page.get_by_role("button", name="Selecionar").is_visible()
    return not modal_ainda_aberto


def emitir_guia_e_relatorio(page, nome_empresa):
    page.get_by_text("Gestão de Guias", exact=True).click()
    page.wait_for_timeout(1000)
    page.get_by_text("Emissão de Guia Rápida", exact=True).click()
    page.wait_for_timeout(1500)

    # 1. Clica para abrir a lista de competências
    page.locator("ng-select").first.click()
    page.wait_for_timeout(500)

    # 2. Localiza a competência desejada
    opcao_competencia = page.locator("div.ng-option").filter(has_text=COMPETENCIA).first

    # CHECAGEM 1: A competência existe no menu suspenso?
    if not opcao_competencia.is_visible(timeout=3000):
        registrar(f"⚠️ AVISO: A competência {COMPETENCIA} não existe para {nome_empresa}. Pulando...")
        page.keyboard.press("Escape")
        return

    opcao_competencia.click(force=True)
    page.wait_for_timeout(1000)

    # DESMARCAR RESCISÓRIO
    desmarcar_rescisorio(page, nome_empresa)

    page.get_by_role("button", name="Pesquisar").click()
    page.wait_for_timeout(2000)

    # CHECAGEM 2: apareceu o alerta "Não há débitos de interesse"?
    alerta_sem_debito = page.locator("#alert-content .title").filter(has_text="Não há débitos de interesse")
    if alerta_sem_debito.is_visible(timeout=2000):
        registrar(f"ℹ️ SEM DÉBITOS DE INTERESSE: {nome_empresa} não possui guia na competência {COMPETENCIA}. Pulando...")
        return

    # LISTAR VENCIMENTOS DISPONÍVEIS
    registrar(f"  📋 Buscando vencimentos disponíveis...")
    vencimentos_disponiveis = listar_vencimentos_disponiveis(page)
    if not vencimentos_disponiveis:
        registrar(f"ℹ️ Nenhuma guia encontrada após pesquisa para {nome_empresa}. Pulando...")
        return

    vencimentos_para_processar = filtrar_vencimento(vencimentos_disponiveis, VENCIMENTO_DESEJADO)
    registrar(f"  → Processando {len(vencimentos_para_processar)} vencimento(s): {', '.join(vencimentos_para_processar)}")

    total_guias_processadas = 0

    # Processar cada vencimento específico encontrado
    for idx, vencimento_data in enumerate(vencimentos_para_processar):
        try:
            # Localizar o card específico DESTE vencimento
            card = obter_card_guia_por_vencimento(page, vencimento_data)
            if card is None:
                registrar(f"  ⚠️ Card não encontrado para vencimento {vencimento_data}. Pulando...")
                continue

            data_vencimento = vencimento_data.replace("/", "-")
            registrar(f"  → Processando guia #{idx + 1} com vencimento: {vencimento_data}")

            # Emissão da guia com tratamento do modal de confirmação, se houver
            btn_emitir_local = card.get_by_role("button", name="Emitir guia").first
            if btn_emitir_local.count() == 0:
                registrar(f"  ⚠️ Botão 'Emitir guia' não encontrado no card de {vencimento_data}. Pulando...")
                continue

            with page.expect_download(timeout=20000) as download_info:
                btn_emitir_local.click()
                page.wait_for_timeout(1000)
                btn_confirmar = page.get_by_role("button", name="Confirmar")
                if btn_confirmar.count() > 0:
                    registrar(f"    → Modal de confirmação detectado, clicando em Confirmar...")
                    btn_confirmar.click()
                    page.wait_for_timeout(1000)

            nome_arquivo_guia = f"{nome_empresa} - Guia - {data_vencimento}.pdf"
            download_info.value.save_as(f"{PASTA_DOWNLOAD}\\{nome_arquivo_guia}")
            registrar(f"    ✓ Guia baixada: {nome_arquivo_guia}")

            page.wait_for_timeout(2000)

            # Baixar relatório: procurar no card OU na página em geral
            try:
                btn_relatorio_local = None
                
                # Primeiro tenta no card específico
                try:
                    btn_relatorio_local = card.locator("i.fa-file-pdf").first
                    if btn_relatorio_local.count() == 0:
                        btn_relatorio_local = None
                except Exception:
                    btn_relatorio_local = None
                
                # Se não achou no card, procura na página inteira (pode ter mudado após emissão)
                if btn_relatorio_local is None:
                    registrar(f"    ℹ️ Procurando relatório na página...")
                    btn_relatorio_local = page.locator("i.fa-file-pdf").first
                    if btn_relatorio_local.count() == 0:
                        raise Exception("Botão PDF não encontrado nem no card nem na página")
                
                with page.expect_download(timeout=15000) as download_info2:
                    btn_relatorio_local.click(force=True, timeout=5000)

                nome_arquivo_relatorio = f"{nome_empresa} - Relatorio - {data_vencimento}.pdf"
                download_info2.value.save_as(f"{PASTA_DOWNLOAD}\\{nome_arquivo_relatorio}")
                registrar(f"    ✓ Relatório baixado: {nome_arquivo_relatorio}")
            except Exception as erro:
                registrar(f"    ⚠️ AVISO ao baixar relatório para {vencimento_data}: {str(erro)}")

            page.wait_for_timeout(1500)
            total_guias_processadas += 1

        except Exception as erro:
            registrar(f"  ❌ ERRO ao processar guia com vencimento {vencimento_data}: {str(erro)}")
            continue

    if total_guias_processadas > 0:
        registrar(f"OK - {nome_empresa}: {total_guias_processadas} guia(s) e relatório(s) concluído(s).")
        return True
    else:
        registrar(f"⚠️ AVISO: Nenhuma guia foi processada para {nome_empresa}.")
        return False

# ---------------------------------------------------------------------------
# EXECUÇÃO PRINCIPAL
# ---------------------------------------------------------------------------

def main():
    with sync_playwright() as p:
        print("Conectando ao Chrome aberto na porta 9222...")
        try:
            # Conecta ao navegador que você abriu manualmente pelo CMD
           browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        except Exception as e:
            print("\nERRO: Não foi possível conectar ao Chrome.")
            print("Certifique-se de que fechou o Chrome e abriu usando o comando --remote-debugging-port=9222")
            return

        # Pega o contexto e a aba que já está aberta com o FGTS
        context = browser.contexts[0]
        page = context.pages[0]

        registrar("\n" + "=" * 70)
        registrar("Conectado com sucesso ao seu Chrome!")
        registrar("Certifique-se de que você JÁ FEZ O LOGIN na aba do FGTS Digital.")
        registrar("=" * 70)
        input("\n>>> Aperte ENTER aqui no terminal para começar a automação: ")

        registrar(f"\n--- Iniciando execução: {len(CNPJS_EMPRESAS)} empresas ---")

        # Abre o modal e seleciona "Procurador" uma vez, antes do loop
        abrir_selecionar_procurador(page)

        for cnpj, nome_empresa in CNPJS_EMPRESAS.items():
            registrar(f"\nProcessando: {nome_empresa} ({cnpj})...")
            try:
                sucesso = tentar_selecionar_cnpj(page, cnpj)

                if not sucesso:
                    # Modal continua aberto (provavelmente sem procuração para
                    # esse CNPJ) - so segue pro proximo CNPJ direto, sem reabrir
                    registrar(f"⚠️ SEM PROCURAÇÃO (ou erro ao selecionar): {nome_empresa} ({cnpj}). Pulando...")
                    continue

                # Selecionou com sucesso -> emite guia e relatorio
                emitir_guia_e_relatorio(page, nome_empresa)
                registrar(f"OK - {nome_empresa} concluído.")

                # Reabre o modal pra proxima empresa
                abrir_selecionar_procurador(page)

            except Exception as e:
                registrar(f"ERRO inesperado ao processar {nome_empresa} ({cnpj}): {e}")
                registrar("Tentando se recuperar e continuar com a próxima empresa...")
                try:
                    # Se algo travou no meio do fluxo, tenta reabrir o modal do
                    # zero pra nao perder o resto da lista
                    abrir_selecionar_procurador(page)
                except Exception as e2:
                    registrar(f"Falha ao tentar se recuperar: {e2}. Pulando mesmo assim...")
                continue

        registrar("\n--- Execução concluída! Verifique a pasta de downloads e o log. ---")
        browser.close()


if __name__ == "__main__":
    main()