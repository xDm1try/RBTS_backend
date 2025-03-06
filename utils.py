import netifaces


def get_addreses():
    found_interfaces = netifaces.interfaces()
    wifi_interfaces = [interface for interface in found_interfaces if "w" == interface[0]]
    # print(netifaces.ifaddresses(wifi_interfaces[0]))
    return [netifaces.ifaddresses(wifi_interface)[netifaces.AF_INET] for wifi_interface in wifi_interfaces]


def get_broadcast_address() -> str:
    addreses = get_addreses()
    return addreses[0][0]["broadcast"]


def get_server_ip() -> str:
    addreses = get_addreses()
    return addreses[0][0]["addr"]