from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Progressbar
from payments_analysis import analyze
from threading import Thread

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.title('Analizador de Pagos')
        self.pack(fill=BOTH, expand=1)
        self.out_filename = 'generado.csv'

        # widgets
        self.chooseNamesFileLbl = Label(self, text='Escoger archivo de nombres: ')
        self.chooseNamesFileLbl.grid(row=0, column=0)
        
        self.chooseNamesFileBtn = Button(self, text='Escoger', highlightbackground='#3E4149', command=self.choose_names_file)
        self.chooseNamesFileBtn.grid(row=0, column=1)
        
        self.choosePaymentsFileLbl = Label(self, text='Escoger archivo de pagos: ')
        self.choosePaymentsFileLbl.grid(row=1, column=0)
        
        self.choosePaymentsFileBtn = Button(self, text='Escoger', highlightbackground='#3E4149', command=self.choose_payments_file)
        self.choosePaymentsFileBtn.grid(row=1, column=1)

        self.out_filename_lbl = Label(self, text='Nombre de archivo generado:')
        self.out_filename_lbl.grid(row=2, column=0)

        self.out_filename_entry = Entry(self)
        self.out_filename_entry.grid(row=2, column=1)

        self.analyzeBtn = Button(self, text='Analizar', highlightbackground='#3E4149', command=self.analyze_file)
        self.analyzeBtn.grid(row=3, column=1)

        self.progressBar = Progressbar(self, mode='indeterminate', takefocus=True, orient=HORIZONTAL)
    
    def choose_names_file(self):
        self.names_filename = filedialog.askopenfilename()
        if self.names_filename:
            parts = self.names_filename.split('/')
            clean_name = parts[len(parts) - 1]
        else:
            clean_name = ''
        self.names_file_lbl = Label(self, text=clean_name)
        self.names_file_lbl.grid(row=0, column=3)

    def choose_payments_file(self):
        self.payments_filename = filedialog.askopenfilename()
        if self.payments_filename:
            parts = self.payments_filename.split('/')
            clean_name = parts[len(parts) - 1]
        else:
            clean_name = ''
        self.payments_file_lbl = Label(self, text=clean_name)
        self.payments_file_lbl.grid(row=1, column=3)

    def analyze_file(self):
        self.out_filename = self.out_filename_entry.get()
        if self.out_filename:
            self.chooseNamesFileLbl.grid_forget()
            self.chooseNamesFileBtn.grid_forget()
            self.names_file_lbl.grid_forget()
            self.choosePaymentsFileLbl.grid_forget()
            self.choosePaymentsFileBtn.grid_forget()
            self.payments_file_lbl.grid_forget()
            self.analyzeBtn.grid_forget()
            self.out_filename_lbl.grid_forget()
            self.out_filename_entry.grid_forget()
            
            self.progressBar.grid(row=2, column=2)
            self.progressBar.start()
            
            t = Thread(target=analyze, args=(self.names_filename, self.payments_filename, self.out_filename+'.csv'))
            t.start()
            t.join()

            self.progressBar.stop()
            self.progressBar.grid_forget()

            self.chooseNamesFileLbl.grid(row=0, column=0)
            self.chooseNamesFileBtn.grid(row=0, column=1)
            self.names_file_lbl.grid(row=0, column=3)
            self.choosePaymentsFileLbl.grid(row=1, column=0)
            self.choosePaymentsFileBtn.grid(row=1, column=1)
            self.payments_file_lbl.grid(row=1, column=3)
            self.out_filename_lbl.grid(row=2, column=0)
            self.out_filename_entry.grid(row=2, column=1)
            self.analyzeBtn.grid(row=3, column=1)


root = Tk()
root.geometry('600x400')
app = Window(root)
root.mainloop()