import os
import random
import Tkinter
import Tkconstants
import tkFileDialog
import tkMessageBox
import DES
import RSA


def gen_primes(n):
    return filter(lambda x: all(map(lambda p: x % p != 0, range(2, x))), range(2, n))

def num_to_binstr(num):
    num = bin(num)[2:]
    return '0' * (max(0, 128 - len(num))) + num

def binstr_to_num(binstr):
    return int('0b' + binstr, 2)


class UI(object):
    def __init__(self):
        self.ui_init()
        self.logic_init()

    def ui_init(self):
        self.root = Tkinter.Tk()
        self.root.title('DES+RSA Messaging System [by Linghao Zhang]')

        # Row 0

        Tkinter.Button(self.root, text='Generate RSA Keys', command=self.gen_rsa_key).grid(row=0, column=0, columnspan=8)
        Tkinter.Label(self.root, text='Public Key').grid(row=1, column=0, columnspan=4)
        Tkinter.Label(self.root, text='Private Key').grid(row=1, column=4, columnspan=4)
        self.rsa_pubkey_text = Tkinter.Text(self.root, width=45, height=3)
        self.rsa_pubkey_text.grid(row=2, column=0, columnspan=4)
        self.rsa_prikey_text = Tkinter.Text(self.root, width=45, height=3)
        self.rsa_prikey_text.grid(row=2, column=4, columnspan=4)

        # Row 1

        # Plain Text
        Tkinter.Label(self.root, text='Plain Text').grid(row=3, column=0)
        Tkinter.Button(self.root, text='Load', command=self.load_pt).grid(row=3, column=1)
        self.pt_text = Tkinter.Text(self.root, width=30, height=10)
        self.pt_text.grid(row=4, column=0, columnspan=2)

        # Cipher Text
        Tkinter.Label(self.root, text='Cipher Text').grid(row=3, column=3, columnspan=2)
        self.ct_text = Tkinter.Text(self.root, width=30, height=10)
        self.ct_text.grid(row=4, column=3, columnspan=2)

        # Decrypted Text
        Tkinter.Label(self.root, text='Decrypted Text').grid(row=3, column=6)
        Tkinter.Button(self.root, text='Save', command=self.save_dt).grid(row=3, column=7)
        self.dt_text = Tkinter.Text(self.root, width=30, height=10)
        self.dt_text.grid(row=4, column=6, columnspan=2)

        # Row 2

        # DES Key
        Tkinter.Label(self.root, text='DES Key').grid(row=6, column=0, columnspan=2)
        self.des_key_text = Tkinter.Text(self.root, width=30, height=10)
        self.des_key_text.grid(row=7, column=0, columnspan=2)

        # Encrypted DES Key
        Tkinter.Label(self.root, text='Encrypted DES Key').grid(row=6, column=3, columnspan=2)
        self.enc_des_key_text = Tkinter.Text(self.root, width=30, height=10)
        self.enc_des_key_text.grid(row=7, column=3, columnspan=2)

        # Decrypted DES Key
        Tkinter.Label(self.root, text='Decrypted DES Key').grid(row=6, column=6, columnspan=2)
        self.dec_des_key_text = Tkinter.Text(self.root, width=30, height=10)
        self.dec_des_key_text.grid(row=7, column=6, columnspan=2)

        # Row 3

        # Controls
        Tkinter.Button(self.root, text='Generate DES Key', command=self.gen_des_key).grid(row=9, column=0, columnspan=2)
        Tkinter.Button(self.root, text='Send Message', command=self.send_msg).grid(row=9, column=3, columnspan=2)
        Tkinter.Button(self.root, text='Decrypt Message', command=self.decrypt_msg).grid(row=9, column=6, columnspan=2)

        # Row 4

        # Instructions
        instructions = """
        Instructions:
        1. Press 'Generate RSA Keys'
        2. Press 'Generate DES Key'
        3. Load plain text file (MUST BE BINARY STRING)
        4. Press 'Send'
        5. Press 'Decrypt Message'
        6. You can save the decrypted message to file
        """
        Tkinter.Label(self.root, text=instructions).grid(row=10, column=0, columnspan=8)

    def logic_init(self):
        self.open_opt = {}
        self.open_opt['defaultextension'] = '.txt'
        self.open_opt['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        self.open_opt['initialdir'] = os.getcwd()
        self.open_opt['parent'] = self.root
        self.save_opt = self.open_opt.copy()
        self.save_opt.update({'initialfile': 'message.txt'})

    def read_from_file(self):
        file = tkFileDialog.askopenfile(mode='r', **self.open_opt)
        try:
            lines = file.readlines()
        except:
            return None

        return lines[0].strip()

    def write_to_file(self, data):
        file = tkFileDialog.asksaveasfile(mode='w', **self.save_opt)
        try:
            file.write(data + '\n')
        except:
            return None

    def update_display(self, target, text):
        target.delete(1.0, Tkinter.END)
        target.insert(1.0, text)

    def error(self, text):
        tkMessageBox.showwarning('Error', text)

    def load_pt(self):
        pt = self.read_from_file()
        if not pt:
            return
        try:
            assert all(map(lambda ch: ch in ['0', '1'], pt))
        except AssertionError:
            self.error('Input must be a binary string.')
            return

        self.pt = pt
        self.update_display(self.pt_text, self.pt)

    def save_dt(self):
        try:
            assert self.dt
        except:
            self.error('Nothing to save.')
            return

        self.write_to_file(self.dt)

    def init_rsa(self):
        self.rsa = RSA.RSA()
        return True

    def gen_rsa_key(self):
        if not self.init_rsa():
            self.error('RSA init failed.')
            return
        self.modulus, self.e = self.rsa.get_public_key()
        self.modulus, self.d = self.rsa.get_private_key()

        pubkey_str = 'e = ' + str(int('0b'+self.e, 2)) + '\n' + 'n = ' + str(int('0b'+self.modulus, 2))
        prikey_str = 'd = ' + str(int('0b'+self.d, 2)) + '\n' + 'n = ' + str(int('0b'+self.modulus, 2))
        self.update_display(self.rsa_pubkey_text, pubkey_str)
        self.update_display(self.rsa_prikey_text, prikey_str)

    def init_des(self, key):
        self.des = DES.DES(key=key)
        return True

    def gen_des_key(self):
        self.des_key = num_to_binstr(random.getrandbits(64))
        self.init_des(self.des_key)
        self.update_display(self.des_key_text, self.des_key)

    def send_msg(self):
        try:
            assert self.pt
        except:
            self.error('Plain Text not loaded.')
            return
        try:
            assert self.rsa_pubkey_text
        except:
            self.error('RSA Public Key not found.')
            return

        self.enc_des_key = self.rsa.encrypt(self.des_key, self.rsa.get_public_key())
        self.update_display(self.enc_des_key_text, self.enc_des_key)
        self.ct = self.des.encrypt(self.pt)
        self.update_display(self.ct_text, self.ct)

    def decrypt_msg(self):
        try:
            assert self.ct
        except:
            self.error('Cipher Text not found.')
            return
        try:
            assert self.enc_des_key
        except:
            self.error('Encrypted DES Key not found.')
            return

        self.dec_des_key = self.rsa.decrypt(self.enc_des_key, self.rsa.get_private_key())
        self.update_display(self.dec_des_key_text, self.dec_des_key)
        self.dt = self.des.decrypt(self.ct)
        self.update_display(self.dt_text, self.dt)


if __name__ == '__main__':
    ui = UI()
    ui.root.mainloop()