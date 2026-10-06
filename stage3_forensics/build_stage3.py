from scapy.all import IP, TCP, Raw, wrpcap

client_ip = "10.10.10.45"   # Marcus's workstation
server_ip = "10.10.50.15"   # internal staging server
client_port = 51322
server_port = 21

packets = []
seq_c = 1000
seq_s = 5000

def data_pkt(src, dst, sport, dport, seq, ack, data):
    return IP(src=src, dst=dst)/TCP(sport=sport, dport=dport, flags="PA", seq=seq, ack=ack)/Raw(load=data)

def ack_pkt(src, dst, sport, dport, seq, ack):
    return IP(src=src, dst=dst)/TCP(sport=sport, dport=dport, flags="A", seq=seq, ack=ack)

packets.append(IP(src=client_ip, dst=server_ip)/TCP(sport=client_port, dport=server_port, flags="S", seq=seq_c))
seq_c += 1
packets.append(IP(src=server_ip, dst=client_ip)/TCP(sport=server_port, dport=client_port, flags="SA", seq=seq_s, ack=seq_c))
seq_s += 1
packets.append(ack_pkt(client_ip, server_ip, client_port, server_port, seq_c, seq_s))

def server_says(msg):
    global seq_s
    packets.append(data_pkt(server_ip, client_ip, server_port, client_port, seq_s, seq_c, msg))
    seq_s += len(msg)
    packets.append(ack_pkt(client_ip, server_ip, client_port, server_port, seq_c, seq_s))

def client_says(msg):
    global seq_c
    packets.append(data_pkt(client_ip, server_ip, client_port, server_port, seq_c, seq_s, msg))
    seq_c += len(msg)
    packets.append(ack_pkt(server_ip, client_ip, server_port, client_port, seq_s, seq_c))

server_says(b"220 Aegis-Staging FTP server ready.\r\n")
client_says(b"USER mreyes.backup\r\n")
server_says(b"331 Password required.\r\n")
client_says(b"PASS Backup123!\r\n")
server_says(b"230 User logged in.\r\n")
client_says(b"STOR ml_model_v3.enc\r\n")
server_says(b"150 Opening data connection.\r\n226 Transfer complete.\r\n")
client_says(b"STOR financial_projections_q4.zip\r\n")
server_says(b"150 Opening data connection.\r\n226 Transfer complete.\r\n")
client_says(b"QUIT\r\n")
server_says(b"221 Goodbye.\r\n")

packets.append(IP(src=client_ip,dst=server_ip)/TCP(sport=client_port,dport=server_port,flags="FA",seq=seq_c,ack=seq_s))
seq_c += 1
packets.append(IP(src=server_ip,dst=client_ip)/TCP(sport=server_port,dport=client_port,flags="A",seq=seq_s,ack=seq_c))
packets.append(IP(src=server_ip,dst=client_ip)/TCP(sport=server_port,dport=client_port,flags="FA",seq=seq_s,ack=seq_c))
seq_s += 1
packets.append(IP(src=client_ip,dst=server_ip)/TCP(sport=client_port,dport=server_port,flags="A",seq=seq_c,ack=seq_s))

wrpcap("stage3.pcap", packets)
print("Wrote", len(packets), "packets")
