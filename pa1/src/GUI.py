import os
import DES
import Tkinter
import Tkconstants
import tkFileDialog
import tkMessageBox

DEBUG = 0

class CryptUI(object):
    E = 0
    D = 1

    def __init__(self):
        self.ui_init()
        self.logic_init()

    def ui_init(self):    
        self.root = Tkinter.Tk()
        self.root.title('DES encrypt/decrypt [by Linghao Zhang]')
        
        # Data Input        
        Tkinter.Label(self.root, text='Plain Text / Cipher Text').grid(row=0, column=0, sticky=Tkinter.W)
        self.data_text = Tkinter.Text(self.root, height=5)
        self.data_text.grid(row=0, column=1, columnspan=3)
        Tkinter.Button(self.root, text='Open', command=self.open_input_file).grid(row=0, column=4)
        
        # Key Input                     
        Tkinter.Label(self.root, text='Key').grid(row=1, column=0, sticky=Tkinter.W)
        self.key_text = Tkinter.Text(self.root, height=5)
        self.key_text.grid(row=1, column=1, columnspan=3)
        Tkinter.Button(self.root, text='Open', command=self.open_key_file).grid(row=1, column=4)
        
        # Output     
        Tkinter.Label(self.root, text='Result').grid(row=2, column=0, sticky=Tkinter.W)
        self.output_text = Tkinter.Text(self.root, height=5)
        self.output_text.grid(row=2, column=1, columnspan=3)  
        Tkinter.Button(self.root, text='Save', command=self.save_to_file).grid(row=2, column=4)
        
        # Control           
        Tkinter.Button(self.root, text='Encrypt', command=self.encrypt).grid(row=3, column=1)
        Tkinter.Button(self.root, text='Decrypt', command=self.decrypt).grid(row=3, column=2)
        Tkinter.Button(self.root, text='Reset', command=self.reset).grid(row=3, column=3)            
      
    def logic_init(self):
        self.open_opt = {}
        self.open_opt['defaultextension'] = '.txt'
        self.open_opt['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        self.open_opt['initialdir'] = os.getcwd()
        self.open_opt['parent'] = self.root
        self.save_opt = self.open_opt.copy()
        self.save_opt.update({'initialfile': 'result.txt'})
    
    def init_crypter(self):
        try:
            del self.des
        except:
            pass
        try:
            assert(self.key)
        except AttributeError, AssertionError:
            tkMessageBox.showwarning('Error', 'Key not loaded.')
            return False
        
        self.des = DES.DES(key=self.key)
        return True
    
    def update_text(self, target, data):
        target.delete(1.0, Tkinter.END)
        target.insert(1.0, data)
    
    def crypt(self, crypt_type):
        if not self.init_crypter():
            return
        try:
            assert(self.input_data)
        except AttributeError, AssertionError:
            tkMessageBox.showwarning('Error', 'Data not loaded.')
            return
            
        crypt_func = {0: self.des.encrypt, 1: self.des.encrypt}[crypt_type]
        self.output_data = crypt_func(self.input_data)
        self.update_text(self.output_text, self.output_data)
    
    def encrypt(self):
        self.crypt(CryptUI.E)
    
    def decrypt(self):
        self.crypt(CryptUI.D)
    
    def reset(self):
        self.input_data = ''
        self.key = ''
        self.output_data = ''
        self.update_text(self.data_text, '')
        self.update_text(self.key_text, '')
        self.update_text(self.output_text, '')
    
    def save_to_file(self):
        file = tkFileDialog.asksaveasfile(mode='w', **self.save_opt)
        try:
            assert self.output_data
        except AttributeError, AssertionError:
            tkMessageBox.showwarning('Error', 'No result to save.')
            return
        
        file.write(self.output_data + '\n')
    
    def read_from_file(self):
        file = tkFileDialog.askopenfile(mode='r', **self.open_opt)
        try:
            lines = file.readlines()
        except:
            tkMessageBox.showwarning('Error', 'Read file failed.')
            return None
            
        return lines[0].strip()
        
    def open_input_file(self):
        data = self.read_from_file()
        if not data:
            return
        try:
            assert all(map(lambda ch: ch in ['0', '1'], data))
        except AssertionError:
            tkMessageBox.showwarning('Error', 'Input must be a binary string.')
            return
            
        self.input_data = data
        self.update_text(self.data_text, self.input_data)
        
    def open_key_file(self):
        data = self.read_from_file()
        if not data:
            return
        try:
            assert all(map(lambda ch: ch in ['0', '1'], data))
        except AssertionError:
            tkMessageBox.showwarning('Error', 'Key must be a binary string.')
        try:
            assert len(data) == 64
        except AssertionError:
            tkMessageBox.showwarning('Error', 'The length of Key must be a multiple of 8.')
            return
        
        self.key = data
        self.update_text(self.key_text, self.key)

ui = CryptUI()        
        
ui.root.mainloop()