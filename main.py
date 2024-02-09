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
                with open(os.path.join(os.getcwd(), 'login.html'), 'r', encoding='utf-8') as login_file:
                    content = login_file.read()# le o contedo do arquivo login 
                
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode('utf-8')) # escreve o conteudo da página

            # Caso dê erro
            except FileNotFoundError:
                pass
        
        elif self.path == '/login_failed':
            #responde ao cliente com a mensagem de login/senha incorreta 
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            #le o conteud da página login.html
            with open(os.path.join(os.getcwd(), 'login.html'), 'r', encoding='utf-8') as login_file:
                content = login_file.read()
            
            #Adiciona a mensagem de erro no conrúdo da página
                mensagem = 'Login e/ou senha incorretos. Tente novamente'
                content = content.replace('<!--Mensagem de erro inserida aqui-->', f'<div class="error-message">{mensagem}</div>' )

            #Envia o conteudo modificado para o cliente 
            self.wfile.write(content.encode('utf-8'))
                
            
        
        else:
            #Se não for a rota "/login", continua com o comportamento padrão
            super().do_GET()

    def usuario_existente(self, login, senha):
        #verifica se o login já existe no arquivo
        with open ('dados_login.txt', 'r', encoding='utf-8') as file:
            for line in file:
                stored_login, stored_senha = line.strip().split(';')
                if login == stored_login:
                    return senha == stored_senha
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

            #verificar se o usuáro já existe:
            login = form_data.get('email',[''])[0]
            senha = form_data.get('senha',[''])[0]

            if self.usuario_existente(login, senha):
                #Responde ao cliente indicando que usuário já consta nos registros
                with open(os.path.join(os.getcwd(), 'usuario_existente.html'), 'r', encoding='utf-8') as usuario_existente_file:
                    content = usuario_existente_file.read() # le o contedo do arquivo login 

                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))

            else:

                if any(line.startswith(f'{login};') for line in open('dados_login.txt', 'r', encoding='utf-8')):
                    #redireciona o cliente para a rota '/login_failed'
                    self.send_response(302)
                    self.send_header('Location', '/login_failed')
                    self.end_headers()
                    return #Adicionando um return para evitar a execução do restante do código

                else:
                    #Armazena os dados num arquivo txt
                    with open('dados_login.txt', 'a') as file:
                        login = form_data.get('email', [''])[0]
                        senha = form_data.get('senha', [''])[0]
                        file.write(f'{login};{senha}\n')

                    with open(os.path.join(os.getcwd(), 'resposta.html'), 'r', encoding='utf-8') as resposta_file:
                            content = resposta_file.read() # le o contedo do arquivo login 

                    #Responde ao cliente indicando que os dados foram recebidos e armazenados com sucesso
                    self.send_response(200)
                    self.send_header("Content-type", "text/html; charset=utf-8")
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

