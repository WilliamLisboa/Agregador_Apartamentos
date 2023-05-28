import pandas as pd

def requisicao_buscador():
    import requests as re
    from bs4 import BeautifulSoup

    info_cidades = {
        'Sao_Paulo': {
            'cidade': 'sao-paulo',
            'onde': ',S%C3%A3o%20Paulo,S%C3%A3o%20Paulo,,,,,city,BR%3ESao%20Paulo%3ENULL%3ESao%20Paulo,-23.555771,-46.639557,%2Fvenda%2Fapartamentos%2Fsp%2Bsao-paulo%2F'
        },
        'Jundiai': {
            'cidade':'jundiai',
            'onde': ',São Paulo,Jundiaí,,,,,city,BR>Sao Paulo>NULL>Jundiai,-23.185653,-46.889222,%2Fvenda%2Fimoveis%2Fsp%2Bjundiai%2F'
        }
    }

    for cidade in ['Sao_Paulo', 'Jundiai']:
        pagina = '1'
        domain = 'https://www.zapimoveis.com.br'
        path = '/venda/apartamentos/sp+' + info_cidades[cidade]['cidade']
        df_apartamentos = ''

        payload = {
            'onde':info_cidades[cidade]['onde'],
            'transacao':'Venda',
            'tipo':'Im%C3%B3vel%20usado',
            'tipos':'apartamento_residencial',
            'pagina': pagina
        }

        headers={
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0',
            'Connection':'keep-alive',
            'Keep-Alive': "'timeout':30, 'max':1000",
            'Alt-Used':'www.zapimoveis.com.br',
            'DNT':'1',
            'Host':'www.zapimoveis.com.br',
            'Sec-Fetch-Dest':'document',
            'Sec-Fetch-Mode':'navigate',
            'Sec-Fetch-Site': 'none'
        }

        request = re.get(domain+path, params=payload, headers=headers)
        if request.status_code == 200:
            soup = BeautifulSoup(request.text, 'lxml')
            quantidade_paginas = retorno_paginas(soup)
            print(quantidade_paginas)
            print(request.status_code)
            df = retorno_elementos_por_pagina(soup)
            for elemento in range(2, quantidade_paginas):
                pagina = str(elemento)
                request = re.get(domain + path, params=payload, headers=headers)
                soup = BeautifulSoup(request.text, 'lxml')
                try:
                    df_new = retorno_elementos_por_pagina(soup)
                    frames = [df_apartamentos, df_new]
                    df_apartamentos = pd.concat(frames)
                except:
                    pass
                if elemento > 250:
                    break

    return df_apartamentos

def retorno_paginas(soup):
    numero_resultados_por_pagina = 100
    section_soup = soup.find("section", class_="results__section")
    section_wrapper = section_soup.find("div", class_="results__wrapper")
    section_result_list = section_wrapper.find("div", class_="results__list js-results")
    header_section_result_list = section_result_list.find("header", class_="results__summary")
    summary_header_section_result_list = header_section_result_list.find("div", class_="summary__header")
    h1_summary_header_section_result_list = summary_header_section_result_list.find("h1",
        class_="summary__title js-summary-title heading-regular heading-regular__bold align-left text-margin-zero results__title")
    strong_h1_summary_header_section_result_list = h1_summary_header_section_result_list.find("strong")
    quantidade_resultados = int(strong_h1_summary_header_section_result_list.text.split(sep=" ")[0].replace(".", ""))
    quantidade_de_paginas = int(quantidade_resultados / numero_resultados_por_pagina)
    return quantidade_de_paginas

def retorno_elementos_por_pagina(soup):

    section_soup = soup.find("section", class_="results__section")
    section_wrapper = section_soup.find("div", class_="results__wrapper")
    section_listing_wrapper = section_wrapper.find("div", class_="listings__wrapper")
    section_listing_container = section_listing_wrapper.find("div", class_="listings__container")
    card_container = section_listing_container.find_all("div", class_="card-container js-listing-card")
    lista_ids_apartamentos = [elemento['data-id'] for elemento in card_container]
    card_container_listing = [element_soup_0.find("div", class_="card-listing simple-card") for element_soup_0 in card_container]
    lista_status_construcao = retorno_status_dos_apartamentos(card_container_listing)
    lista_precos_apartamentos = retorno_precos_dos_apartamentos(card_container_listing)
    lista_enderecos_apartamentos, lista_areas_apartamentos, lista_qtd_quartos_apartamentos, lista_qtd_banheiros_apartamentos, lista_qtd_vagas_carros_apartamentos = retorno_caracteristicas_dos_apartamentos(card_container_listing)
    lista_bairros_apartamentos = [elemento.split(',')[1].strip() if elemento.split(',')[1].strip() != 'São Paulo' else elemento.split(',')[0].strip() for elemento in lista_enderecos_apartamentos]
    lista_urls_apartamentos = gerar_url_apartamento(lista_enderecos_apartamentos, lista_areas_apartamentos, lista_ids_apartamentos, lista_qtd_quartos_apartamentos)

    print(lista_ids_apartamentos, len(lista_ids_apartamentos))
    print(lista_urls_apartamentos)
    print(lista_status_construcao)
    print(lista_precos_apartamentos)
    print(lista_enderecos_apartamentos)
    print(lista_bairros_apartamentos)
    print(lista_areas_apartamentos, len(lista_areas_apartamentos))
    print(lista_qtd_quartos_apartamentos, len(lista_qtd_quartos_apartamentos))
    print(lista_qtd_banheiros_apartamentos, len(lista_qtd_banheiros_apartamentos))
    print(lista_qtd_vagas_carros_apartamentos, len(lista_qtd_vagas_carros_apartamentos))

    df = pd.DataFrame(zip(lista_ids_apartamentos, lista_status_construcao, lista_precos_apartamentos, lista_enderecos_apartamentos,
                          lista_bairros_apartamentos, lista_areas_apartamentos, lista_qtd_quartos_apartamentos,
                          lista_qtd_banheiros_apartamentos, lista_qtd_vagas_carros_apartamentos, lista_urls_apartamentos),
                                                                                                columns=['ID', 'STATUS', 'PRECO', 'ENDERECO', 'BAIRRO', 'AREA', 'QTD_QUARTOS',
                                                                                                        'QTD_BANHEIROS', 'QTS_VAGAS_CARROS', 'URLS'])
    return df
def retorno_status_dos_apartamentos(soup_container_card):
    card_container_listing_status_simple_card = [element_soup_2.find("div", class_="simple-card__highligths") if element_soup_2 is not None else None for
                                                 element_soup_2 in soup_container_card]
    card_container_listing_status_simple_card_strong = [element_soup_3.find("strong") if element_soup_3 is not None else None for element_soup_3 in
                                                        card_container_listing_status_simple_card]
    print(len(card_container_listing_status_simple_card_strong))
    lista_status_construcao = [element.text if element is not None else None for element in
                               card_container_listing_status_simple_card_strong]
    return lista_status_construcao

def retorno_precos_dos_apartamentos(soup_container_card):
    card_container_listing_card_box = [element_soup_1.find("div", class_="simple-card__box") for element_soup_1 in
                                       soup_container_card]
    card_container_listing_card_box_listing = [
        element_soup_2.find("div", class_="simple-card__listing-prices simple-card__prices") for element_soup_2 in
        card_container_listing_card_box]
    card_container_listing_card_box_listing_price_p_strong = [
        element_soup_4.find("strong") if element_soup_4 is not None else None for element_soup_4 in
        card_container_listing_card_box_listing]
    lista_precos_apartamentos = [
        int(element.text.replace('\n', '').strip().replace('R$ ', '').replace('.', '')) if element is not None else None
        for element in card_container_listing_card_box_listing_price_p_strong]

    return lista_precos_apartamentos

def retorno_caracteristicas_dos_apartamentos(card_container_listing):
    card_container_listing_actions = [element_soup_1.find("div", class_="simple-card__actions") for element_soup_1 in
                                      card_container_listing]
    lista_enderecos_apartamentos = [element_soup_2.find("h2").text.replace("\n", "").strip() for element_soup_2 in
                                    card_container_listing_actions]
    card_container_listing_actions_list = [element_soup_3.find("ul") for element_soup_3 in
                                           card_container_listing_actions]
    card_container_listing_actions_list_elements = [element_soup_4.find_all("li") for element_soup_4 in
                                                    card_container_listing_actions_list]
    lista_propriedades_apartamento = [
        {elemento.find_all("span")[0].find("i").text.strip(): elemento.find_all("span")[1].text.replace('\n',
                                                                                                        '').strip() for
         elemento in elementos}
        for elementos in card_container_listing_actions_list_elements
    ]
    lista_areas_apartamentos, lista_qtd_quartos_apartamentos, lista_qtd_banheiros_apartamentos, lista_qtd_vagas_carros_apartamentos = [], [], [], []
    for i, elementos in enumerate(lista_propriedades_apartamento):
        for key, value in elementos.items():
            if key == 'area':
                lista_areas_apartamentos.append(value)
            elif key == 'bedroom':
                lista_qtd_quartos_apartamentos.append(value)
            elif key == 'bathroom':
                lista_qtd_banheiros_apartamentos.append(value)
            elif key == 'parking':
                lista_qtd_vagas_carros_apartamentos.append(value)
        if len(lista_areas_apartamentos) != i + 1:
            lista_areas_apartamentos.append('Sem informação')
        elif len(lista_qtd_quartos_apartamentos) != i + 1:
            lista_qtd_quartos_apartamentos.append('Sem informação')
        elif len(lista_qtd_banheiros_apartamentos) != i + 1:
            lista_qtd_banheiros_apartamentos.append('Sem informação')
        elif len(lista_qtd_vagas_carros_apartamentos) != i + 1:
            lista_qtd_vagas_carros_apartamentos.append('Sem informalção')

    return lista_enderecos_apartamentos, lista_areas_apartamentos, lista_qtd_quartos_apartamentos, lista_qtd_banheiros_apartamentos, lista_qtd_vagas_carros_apartamentos

def gerar_url_apartamento(lista_enderecos, lista_areas, lista_ids, lista_qtd_quartos):
    base_url_apartamento = 'https://www.zapimoveis.com.br/imovel/venda-apartamento-'
    lista_urls_apartamentos = []
    for i in range(0, len(lista_ids)):
        base_url = base_url_apartamento + lista_qtd_quartos[i][-1] + '-quartos-' + \
                   corrigir_enderecos(lista_enderecos[i]) + '-' + \
                   lista_areas[i].split(" ")[0] + 'm2-id-' + lista_ids[i]
        lista_urls_apartamentos.append(base_url)
    return lista_urls_apartamentos

def corrigir_enderecos(endereco):

    # Retirando a ",", e substituindo os espaços em branco por "-"
    endereco = endereco.replace(",", "").replace(" ", "-").lower()

    # Substituindo os caracteres especiais por seus equivalentes
    endereco_list = list(endereco)
    for i, elemento in enumerate(endereco_list):
        if elemento in ('á', 'à', 'ã', 'â'):
            endereco_list[i] = 'a'
        elif elemento in ('ó', 'ô', 'õ'):
            endereco_list[i] = 'o'
        elif elemento == 'ú':
            endereco_list[i] = 'u'
        elif elemento == 'í':
            endereco_list[i] = 'i'
        elif elemento in ('é', 'ê'):
            endereco_list[i] = 'e'
        elif elemento == 'ç':
            endereco_list[i] = 'c'

    # Adicionando sufixo caso necessário
    if endereco_list[-1] == 'sp':
        pass
    elif (endereco_list[-1] == 'paulo') | (endereco_list[-2] == 'paulo'):
        endereco_list.append('-sp')
    elif endereco_list[-1] != 'paulo':
        endereco_list.append('-sao-paulo-sp')

    endereco = ''.join(endereco_list)

    return endereco
