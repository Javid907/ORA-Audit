This is a application that will help find tables where there are sensitive data.


# Installation Guide for Linux

Prepare your host

    cd /opt
    git clone https://github.com/Javid907/ORA-Audit.git
    mv ORA-Audit ora-audit
    cd ora-audit/

You need to change path for your config/template.yaml
    
    vi module/config.py 


You need to add your data in following files

    vi config/template.yaml
    vi config/key.csv
    vi config/exclude_key.csv
    vi config/db.csv


Then run these commands:

      sh -c "echo  /opt/ora-audit/lib/linux/instantclient_19_12 > /etc/ld.so.conf.d/oracle-instantclient.conf"
      ldconfig
      export LD_LIBRARY_PATH=/opt/ora-audit/lib/linux/instantclient_19_12:$LD_LIBRARY_PATH

      pip3.6 install -r ./requirements.txt
      pip3.6 install --user -U ./
      python3.6 ~/.local/bin/run.py



# CRONTAB
### ORA-Audit
     0 3 * * * PYTHONPATH=/root/.local/lib/python3.6/site-packages /usr/bin/python3.6 /root/.local/bin/run.py
