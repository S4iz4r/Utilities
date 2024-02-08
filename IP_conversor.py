import re

while True:
    ip_input = input("\nIntroduzca IP con el subnet ( IP/24 por ejemplo ): ")
    if re.match("^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\/([0-9]{1,2})$", ip_input) and int(ip_input.split('/')[1]) <= 32 and int(ip_input.split('/')[1]) >= 1:
        try:
            IP, CIDR = ip_input.split('/')
            for octet in IP.split('.'):
                if int(octet) > 255:
                    raise Exception()
            break
        except:
            pass
    print("\nDebes introducir un formato correcto! 192.168.1.66/24 por ejemplo.\n")

CIDR = int(CIDR)
bin_ip_octets = []
for octet in IP.split('.'):
    octet = '{0:08b}'.format(int(octet))
    bin_ip_octets.append(octet)

print(f"\nIP_ADDRESS        -> {IP}       ->  {'.'.join(bin_ip_octets)}")

bin_net_masc = []
net_octet = []
net_masc = []
step = 0
for i in range(4):
    for j in range(8):
        if step < CIDR:
            net_octet.append('1')
        else:
            net_octet.append('0')
        step += 1
    bin_net_masc.append(''.join(net_octet))
    net_octet = []
for octet in bin_net_masc:
    net_masc.append(str(int(octet, 2)))

print(
    f'NETWORK_MASC      -> {".".join(net_masc)}      ->  {".".join(bin_net_masc)}')


bin_id_octet = []
id_octet = []
net_id = []

for i in range(4):
    for j in range(8):
        if bin_ip_octets[i][j] == '1' and bin_net_masc[i][j] == '1':
            id_octet.append('1')
        else:
            id_octet.append('0')

    bin_id_octet.append(''.join(id_octet))
    id_octet = []

for octet in bin_id_octet:
    net_id.append(str(int(octet, 2)))

print(
    f'NETWORK_ID        -> {".".join(net_id)}         ->  {".".join(bin_id_octet)}')


bin_br_add = []
add_octet = []
br_add = []
step = 0
for i in range(4):
    for j in range(8):
        if step < CIDR:
            add_octet.append(bin_ip_octets[i][j])
        else:
            add_octet.append('1')
        step += 1
    bin_br_add.append(''.join(add_octet))
    add_octet = []
for octet in bin_br_add:
    br_add.append(str(int(octet, 2)))

print(
    f'BROADCAST ADDRESS -> {".".join(br_add)}     ->  {".".join(bin_br_add)}')
