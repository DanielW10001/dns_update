# dns_update

Periodically Update DDNS to Local Public IP

- Only support `park-your-domain.com` and Windows now
- Usage
    - `poetry install`
    - Edit `./dns_update.xml`
        - Use `%BASE%` for parent dir of `dns_update.xml`
        - Set `<executable>` to project's python executable path
        - Set `<arguments>` to `%BASE%/dns_update.py HOST DOMAIN PASSWORD PROXY`
    - `./dns_update.exe COMMAND`: `install|uninstall|start|stop|stopwait|restart|status`

Licensed under `LICENSE.md`
