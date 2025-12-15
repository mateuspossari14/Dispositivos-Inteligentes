import os
import cv2
import time
import serial
from tkinter import * 
from tkinter import messagebox
from simple_facerec import SimpleFacerec

class MyMessage:
    def __init__(self):
        self.principal_window = Tk()
        self.principal_window.title = 'DISPOSITIVOS INTELIGENTES INTEGRADOS COM ARDUÍNO, EM PROL DA SEGURANÇA EM MÁQUINAS E EQUIPAMENTOS'

        self.button = Button(self.principal_window, text='Detectar funcionário', command=self.detect_face)
        self.button_registerPerson = Button(self.principal_window, text='Registrar funcionário', command=self.register_person)
        self.button_quit = Button(self.principal_window, text='Sair', command=self.principal_window.destroy)
        
        self.principal_window.geometry("400x200")

        self.button.pack()
        self.button_registerPerson.pack()
        self.button_quit.pack()
        self.register_window = None  # Inicializar como None
        mainloop()

    def detect_face(self):
        capture = cv2.VideoCapture(0)
        sfr = SimpleFacerec()
        
        # Variáveis para controle da comunicação serial
        arduino_connection = None
        last_detected_name = None
        frame_count = 0

        if len(os.listdir('assets/img/')) != 0:
            sfr.load_encoding_images('assets/img/')
            
            # Tentar conectar com Arduino uma única vez
            try:
                arduino_connection = serial.Serial("COM3", 9600, timeout=1)
                time.sleep(2)  # Aguardar Arduino inicializar
                print('Conexão com Arduino estabelecida:', arduino_connection.portstr)
            except serial.SerialException as e:
                print(f"Erro ao conectar com Arduino: {e}")
                arduino_connection = None

            while True:
                status, video = capture.read()
                video = cv2.flip(video, 1)
                response = arduino_connection.readline().decode('utf-8').strip()
                print(response)
                
                # Processar detecção a cada 5 frames para melhor performance
                video_grayScale = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)
                face_locations, face_names = sfr.detect_known_faces(video_grayScale)
                
                # Verificar se algum rosto conhecido foi detectado
                current_detected_name = None
                for name in face_names:
                    if name != "Unknown":
                        current_detected_name = name
                        break
                
                # Enviar sinal para Arduino apenas se o estado mudou
                if current_detected_name != last_detected_name and arduino_connection:
                    try:
                        if current_detected_name:
                            # Rosto conhecido detectado
                            
                            arduino_connection.write('1'.encode('utf-8'))
                            print(f'Acesso liberado para: {current_detected_name}')
                            time.sleep(30)
                        else:
                            # Nenhum rosto conhecido detectado
                            arduino_connection.write('0'.encode('utf-8'))
                            print('Acesso negado')
                        
                        
                        
                            
                    except serial.SerialException as e:
                        print(f"Erro na comunicação serial: {e}")
                
                last_detected_name = current_detected_name
                
                # Desenhar interface visual
                face_locations, face_names = sfr.detect_known_faces(cv2.cvtColor(video, cv2.COLOR_BGR2GRAY))
                for face_loc, name in zip(face_locations, face_names):
                    top, right, bottom, left = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
                    
                    # Cor baseada no reconhecimento
                    color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                    
                    cv2.putText(video, name, (right, top - 10), fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, 
                                fontScale=1, color=color, thickness=2)
                    cv2.rectangle(video, (right, top), (left, bottom), color, 2)
                
                cv2.imshow('My video', video)

                if cv2.waitKey(1) == ord('q'):
                    cv2.destroyAllWindows()
                    break
            
            # Fechar conexão Arduino ao final
            if arduino_connection:
                arduino_connection.close()
                print('Conexão com Arduino fechada')
                
        else:
            print('The folder is empty!')
        capture.release()

    def show_message(self):
        name_input = self.input_entry.get()
        name_person = {'value': ''}  # Usando dicionário para permitir modificação na função interna

        if name_input:
            name_person['value'] = name_input
            print(f"Nome cadastrado: {name_person['value']}")
            self.register_window.destroy()
            self.register_window = None  # Resetar para None após fechar 
            
            capture = cv2.VideoCapture(0)
            sfr = SimpleFacerec()
            if name_person['value']:
                status, frame = capture.read()

                if status:
                    frame = cv2.flip(frame, 1)
                    try:
                        if len(os.listdir('assets/img/')) == 0:
                            cv2.imwrite(f'./assets/img/{name_person["value"]}.jpg', frame)
                            messagebox.showinfo(title='Salvamento de Imagem',
                                                message=f'Imagem salva com sucesso como {name_person["value"]}.jpg!')
                        else:
                            sfr.load_encoding_images('assets/img/')
                            face_locations, face_names = sfr.detect_known_faces(frame)
                            
                            if len(face_locations) == 0:
                                messagebox.showwarning(title='Nenhum rosto detectado', 
                                                     message='Nenhum rosto foi detectado na foto. Posicione-se melhor em frente à câmera.')
                            else:
                                face_already_exists = False
                                for face_name in face_names:
                                    if face_name != "Unknown":  
                                        face_already_exists = True
                                        messagebox.showwarning(title='Rosto já cadastrado', 
                                                             message=f'Este rosto já está cadastrado como "{face_name}". Foto não foi salva.')
                                        break
                                if not face_already_exists:
                                    cv2.imwrite(f'./assets/img/{name_person["value"]}.jpg', frame)
                                    messagebox.showinfo(title='Salvamento de Imagem',
                                                        message=f'Imagem salva com sucesso como {name_person["value"]}.jpg!')
                    except Exception as e:
                        messagebox.showerror(title='Erro', message=f'Erro ao processar imagem: {str(e)}')
                else:
                    messagebox.showerror(title='Erro de salvamento', message='A foto não foi capturada!')
            capture.release()
        else:
            messagebox.showinfo(title='Lembrete', message='Digite algum nome')

    def register_person(self):
        if self.register_window is not None:
            try:
                self.register_window.lift()
                self.register_window.focus()
                return
            except:
                self.register_window = None
        
        self.register_window = Tk()
        self.register_window.geometry('500x300')
        self.register_window.title('Registrando o funcionário')

        label = Label(self.register_window, text="Digite o seu nome:")
        label.grid(row=0, column=0, padx=10, pady=2)

        self.input_entry = Entry(self.register_window)
        self.input_entry.grid(row=0, column=1, padx=2, pady=2)

        button = Button(self.register_window, text='Cadastrar', command=self.show_message)
        button.grid(row=1, column=0, padx=10, pady=1)

        buttonCancel = Button(self.register_window, text='Cancelar', command=self.register_window.destroy)
        buttonCancel.grid(row=1, column=1, padx=10, pady=1)

        self.register_window.mainloop()
MyMessage()