FROM ubuntu:22.04

RUN apt-get update && apt-get install -y openssh-server sudo vim && \
    mkdir /var/run/sshd

# Low-privilege service account — this is what players log into
RUN useradd -m -s /bin/bash backupsvc && \
    echo "backupsvc:Backup123!" | chpasswd

# The misconfiguration: backupsvc can run vim as root with no password
RUN echo "backupsvc ALL=(ALL) NOPASSWD: /usr/bin/vim" > /etc/sudoers.d/backup-svc && \
    chmod 440 /etc/sudoers.d/backup-svc

# The flag, only readable by root
RUN echo "ROGUE{s0_th4ts_h0w_h3_did_it}" > /root/vault_access.flag && \
    chmod 600 /root/vault_access.flag

RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
