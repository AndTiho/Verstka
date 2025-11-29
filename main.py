# Импорт встроенной библиотеки для работы веб-сервера
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

# Для начала определим настройки запуска
hostName = "localhost" # Адрес для доступа по сети
serverPort = 8080 # Порт для доступа по сети

class MyServer(BaseHTTPRequestHandler):
    """
        Специальный класс, который отвечает за
        обработку входящих запросов от клиентов
    """
    def do_GET(self):
        """Метод обработки входящих GET-запросов"""
        if self.path == '/':
            # Если запрос на корень, открываем contact.html
            self.path = '/contacts.html'

        if self.path.endswith('.html'):
            # Обслуживаем HTML-страницу
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open(os.path.join('.', self.path.lstrip('/')), 'r', encoding='utf-8') as file:
                html_content = file.read()
            self.wfile.write(bytes(html_content, "utf-8"))
        elif self.path.startswith('/static/css/'):
            # Обслуживаем CSS-файлы
            file_path = os.path.join('.', self.path.lstrip('/'))
            try:
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
                self.end_headers()
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.wfile.write(bytes(file.read(), "utf-8"))
            except FileNotFoundError:
                self.send_error(404, "File Not Found")
        elif self.path.startswith('/js/'):
            # Обслуживаем JavaScript-файлы
            file_path = os.path.join('.', self.path.lstrip('/'))
            try:
                self.send_response(200)
                self.send_header('Content-type', 'text/javascript')
                self.end_headers()
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.wfile.write(bytes(file.read(), "utf-8"))
            except FileNotFoundError:
                self.send_error(404, "File Not Found")
        elif self.path.startswith('/brand/'):
            # Обслуживаем изображения (включая SVG)
            file_path = os.path.join('.', self.path.lstrip('/'))
            try:
                self.send_response(200)
                if self.path.endswith('.svg'):
                    self.send_header('Content-type', 'image/svg+xml')
                else:
                    self.send_header('Content-type', 'image/png')  # Предположим, что изображения в формате PNG
                self.end_headers()
                with open(file_path, 'rb') as file:
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_error(404, "File Not Found")
        else:
            # Обрабатываем другие типы файлов (например, изображения или JavaScript)
            self.send_error(404, "Not Found")

    def do_POST(self):
        """Метод обработки входящих POST-запросов"""
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        print(body)
        self.send_response(200)
        self.end_headers()


if __name__ == "__main__":
    # Инициализация веб-сервера, который будет по заданным параметрах в сети
    # принимать запросы и отправлять их на обработку специальному классу, который был описан выше
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")