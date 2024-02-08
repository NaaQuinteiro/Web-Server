# Navega no diretorio
import os
# Manipula e Cria um servidir (sem framework)
from http.server import SimpleHTTPRequestHandler
# Gerencia a comunicação com o cliente
import socketserver

from urllib.parse import parse_qs

# Criação de Classe com artificio de HTTP
class MyHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        # Tenta o Código abaixo
        try:
            # Abre o arquivo index.html
            with open(os.path.join(path, 'index.html'), 'r', encoding='utf-8') as f:
                # Envia o cabeçalho HTTP
                # Se existir, envia o conteudo do arquivo
                # Envia para o Cliente o Código de Sucesso
                self.send_response(200)
                 # Forma de Tratmento
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()

                # Lê e envia o conteúdo do arquivo
                content = f.read()
                # Leitura do HTML
                self.wfile.write(content.encode('utf-8'))
                # Finaliza para não contnuar o carregamento
                f.close
                return 
            
        # Caso dê erro  
        except FileNotFoundError:
            pass

        return super().list_directory(path)
    

    
    def do_GET(self):
        if self.path == '/login':
            #Tentar abrir o arquivo login
            try:
                with open(os.path.join(os.getcwd(), 'login.html'), 'r') as login_file:
                    content = login_file.read() # le o contedo do arquivo login 
                
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content.encode('utf-8')) # escreve o conteudo da página

            # Caso dê erro
            except FileNotFoundError:
                pass
        
        else:
            #Se não for a rota "/login", continua com o comportamento padrão
            super().do_GET()

    def usuario_existente(self, login):
        #verifica se o login já existe no arquivo
        with open ('dados_login.txt', 'r') as file:
            for line in file:
                stored_login, _ = line.strip().split(';')
                if login == stored_login:
                    return True
        return False

    def do_POST(self):
        #verifica se a rota é "/enviar_login" (isso tem que estar no action do formulario )
        if self.path == '/enviar_login':
            #Obtém o comprimento do corpo da requisição
            content_length = int(self.headers['content-length'])

            #Lê o corpo de requisição
            body = self.rfile.read(content_length).decode('utf-8')

            #Parseia os dados do formulário 
            form_data = parse_qs(body)

            #Exibe os dados no terminal 
            print("Dados Formulário:")
            print("Email:", form_data.get('email', [''][0]))
            print("Senha:", form_data.get('email', [''][0]))

            with open('dados_login.txt', 'a') as file:
                login = form_data.get('email', [''])[0]
                senha = form_data.get('senha', [''])[0]
                file.write(f'{login};{senha}\n')

            #verificar se o usuáro já existe:
            login = form_data.get('email',[''])[0]
            if self.usuario_existente(login):
                #Responde ao cliente indicando que usuário já consta nos registros
                with open(os.path.join(os.getcwd(), 'usuario_existente.html'), 'r') as usuario_existente_file:
                    content = usuario_existente_file.read() # le o contedo do arquivo login 

                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))

            else:
                #Armazena os dados num arquivo txt
                with open(os.path.join(os.getcwd(), 'resposta.html'), 'r') as resposta_file:
                        content = resposta_file.read() # le o contedo do arquivo login 

                #Responde ao cliente indicando que os dados foram recebidos e armazenados com sucesso
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content.encode('utf-8')) # escreve o conteudo da página

        else:
            #Se não for a rota definifa, conrinua com o comportamento padrão
            super(MyHandler, self).do_POST()

endereco_ip = "0.0.0.0"
porta = 8000

with socketserver.TCPServer((endereco_ip, porta), MyHandler) as httpd:
    print(f"Servidor iniciando em {endereco_ip}:{porta}")
    httpd.serve_forever()

