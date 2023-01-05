import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://www.bolsadesantiago.com/'

XPATH_LINK_TO_ARTICLE = '//div[@class="col-lg-4"]/a/@href'
XPATH_TITLE = '//h1[@class="text-uppercase font-weight-bold ng-binding"]/text()'
XPATH_SUMMARY = '//p[@class="f-18 ng-binding"]/text()'



def parse_notice(link, today):
    try:
        response=requests.get(link)
        #Valido si tengo un status correcto
        if response.status_code == 200:
            #Tranforma contenido a formato utf-8 (como esta funcion se itera, trabaja con cada noticia)
            notice = response.content.decode('utf-8')
            #Guarda contenido html que tengo en home, y transforma en un documento manejable para hacer spam
            parsed = html.fromstring(notice)

            try:
                #Se usa 0 por que el resultado de utilizar xpath en un archivo html devuelve una lista, sabiendo que title es uno solo
                #Es un string
                title = parsed.xpath(XPATH_TITLE)[0]

                #Se usa para evitar que titulo venga con comillas
                title = title.replace('\"', '')

                #Se usa 0 por que el resultado de utilizar xpath en un archivo html devuelve una lista, sabiendo que summary es uno solo
                summary = parsed.xpath(XPATH_SUMMARY)[0]
     
                #No se pone 0 por que se usara toda la lista de body (cada uno es un parrafo de la noticia)
                #body = parsed.xpath(XPATH_BODY)
            #Ante error, salgo de la funcion (pueden haber noticias que no tienen summary, por lo que salgo de la funcion)                
            except IndexError:
                return  
            #Permite, si script se cierra de manera inesperada, mantiene todo seguro
            #Abro carpeta creada en metodo mas abajo, t creo archivo {title}.txt, se abre en modo escritura 'w' y encoding
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:   
                #Escribo archivo con data    
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                #for p in body:
                 #   f.write(p)
                  #  f.write('\n')

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:    
        print(ve)



def parse_home():
    try:
        response = requests.get(HOME_URL)
        
        #Valido si tengo un status correcto
        if response.status_code == 200:
            #Tranforma contenido a formato utf-8
            home = response.content.decode('utf-8')
            print(home)
            #Guarda contenido html que tengo en home, y transforma en un documento manejable para hacer spam
            parsed = html.fromstring(home)
            #Obtengo lista de links
            links_to_notice = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            print(links_to_notice)
            #print(links_to_notice)

            #Obtengo fecha actual
            today = datetime.date.today().strftime('%d-%m-%Y')
            #Trae boleano, Si no existe carpeta con nombre de fecha actual, la creo con os.mkdir(today)
            if not os.path.isdir(today):
                os.mkdir(today)
            #Itero, y llamo a funcion prebiamente creada, para que guarde archivo con cada notocia del dia    
            for link in links_to_notice:
                parse_notice(link, today)    
        else:
            raise ValueError(f'Error: {response.status_code}')    
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__=='__main__':
    run()   