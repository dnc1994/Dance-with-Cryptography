import DES

def write_to_file(filename, data):
    with open(filename, 'w') as f:
        f.write(data + '\n')

key = DES.gen_bits(64)
des = DES.DES(key=key)

write_to_file('test/KEY.txt', key)

pt_len_list = [56, 64, 120, 128, 800]

for pt_len in pt_len_list:
    pt = DES.gen_bits(pt_len)
    ct = des.encrypt(pt)
    
    write_to_file('test/PT-%d.txt' % pt_len, pt)
    write_to_file('test/CT-%d.txt' % pt_len, ct)