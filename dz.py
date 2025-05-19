from copy import deepcopy

class Printable:
    def print_me(self, prefix='', is_last=True):
        raise NotImplementedError

    def clone(self):
        return deepcopy(self)

class Component(Printable):
    def __init__(self, name):
        self.name = name

class CPU(Component):
    def __init__(self, cores, mhz):
        super().__init__('cpu')
        self.cores = cores
        self.mhz = mhz

    def print_me(self, prefix='', is_last=True):
        connector = '└─' if is_last else '├─'
        return f"{prefix}{connector}cpu, {self.cores} cores @ {self.mhz}mhz\n"

class Memory(Component):
    def __init__(self, size_mib):
        super().__init__('memory')
        self.size_mib = size_mib

    def print_me(self, prefix='', is_last=True):
        connector = '└─' if is_last else '├─'
        return f"{prefix}{connector}memory, {self.size_mib} mib\n"

class Partition(Printable):
    def __init__(self, index, size_gib, label):
        self.index = index
        self.size_gib = size_gib
        self.label = label

    def print_me(self, prefix='', is_last=True):
        connector = '└─' if is_last else '├─'
        return f"{prefix}{connector}[{self.index}]: {self.size_gib} gib, {self.label}\n"

class Disk(Component):
    def __init__(self, size_gib):
        super().__init__('HDD')
        self.size_gib = size_gib
        self.partitions = []

    def add_partition(self, partition):
        self.partitions.append(partition)

    def print_me(self, prefix='', is_last=True):
        connector = '└─' if is_last else '├─'
        output = f"{prefix}{connector}HDD, {self.size_gib} gib\n"
        new_prefix = prefix + ('   ' if is_last else '│  ')
        for i, part in enumerate(self.partitions):
            output += part.print_me(new_prefix, i == len(self.partitions) - 1)
        return output

class Host(Printable):
    def __init__(self, name):
        self.name = name
        self.ip_addresses = []
        self.components = []

    def add_ip(self, ip):
        self.ip_addresses.append(ip)

    def add_component(self, comp):
        self.components.append(comp)

    def print_me(self, prefix='', is_last=True):
        connector = '└─' if is_last else '├─'
        output = f"{prefix}{connector}Host: {self.name}\n"
        new_prefix = prefix + ('   ' if is_last else '│  ')
        for i, ip in enumerate(self.ip_addresses):
            last_ip = i == len(self.ip_addresses) - 1 and not self.components
            output += f"{new_prefix}{'└─' if last_ip else '├─'}{ip}\n"
        for i, comp in enumerate(self.components):
            output += comp.print_me(new_prefix, i == len(self.components) - 1)
        return output

class Network(Printable):
    def __init__(self, name):
        self.name = name
        self.hosts = []

    def add_host(self, host):
        self.hosts.append(host)

    def find_host(self, name):
        for host in self.hosts:
            if host.name == name:
                return host
        return None

    def print_me(self, prefix='', is_last=True):
        output = f"Network: {self.name}\n"
        for i, host in enumerate(self.hosts):
            output += host.print_me('', i == len(self.hosts) - 1)
        return output

# Пример использования
if __name__ == '__main__':
    net = Network("MISIS network")

    h1 = Host("server1.misis.ru")
    h1.add_ip("192.168.1.1")
    h1.add_component(CPU(4, 2500))
    h1.add_component(Memory(16000))

    h2 = Host("server2.misis.ru")
    h2.add_ip("10.0.0.1")
    h2.add_component(CPU(8, 3200))
    disk = Disk(2000)
    disk.add_partition(Partition(0, 500, "system"))
    disk.add_partition(Partition(1, 1500, "data"))
    h2.add_component(disk)

    net.add_host(h1)
    net.add_host(h2)

    print(net.print_me())
