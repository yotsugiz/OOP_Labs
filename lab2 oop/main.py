import asyncio
import random
import time
import networkx as nx
import matplotlib.pyplot as plt


# --- 1. Класи вузлів та маршрутизаторів ---
class Node:
    def __init__(self, name):
        self.name = name
        self.connections = []

    def connect(self, node):
        if node not in self.connections:
            self.connections.append(node)
            node.connections.append(self)

    async def send(self, packet, network):
        # Імітація затримки мережі
        await asyncio.sleep(random.uniform(0.01, 0.05))

        # Симуляція втрати пакетів (10-15%)
        if random.random() < network.loss_rate:
            network.packets_lost += 1
            return

        await self.forward(packet, network)

    async def forward(self, packet, network):
        if self == packet.dest:
            return  # Пакет успішно доставлено

        if self in packet.visited:
            return  # Запобігання зацикленню

        packet.visited.append(self)
        for node in self.connections:
            if node not in packet.visited:
                await node.send(packet, network)


class Router(Node):
    pass


# --- 2. Пакет та Протоколи ---
class Packet:
    def __init__(self, src, dest, size, protocol):
        self.src = src
        self.dest = dest
        self.size = size
        self.protocol = protocol
        self.visited = []


class TCPProtocol:
    name = "TCP"

    @staticmethod
    async def transmit(src, dest, network):
        packet = Packet(src, dest, random.randint(200, 500), "TCP")
        await src.send(packet, network)


class UDPProtocol:
    name = "UDP"

    @staticmethod
    async def transmit(src, dest, network):
        packet = Packet(src, dest, random.randint(50, 200), "UDP")
        await src.send(packet, network)


# --- 3. Модель Мережі ---
class Network:
    def __init__(self, name):
        self.name = name
        self.nodes = []
        self.loss_rate = random.uniform(0.10, 0.15)
        self.packets_sent = 0
        self.packets_lost = 0
        self.total_time = 0

    async def simulate(self, protocol, packets=10):
        for _ in range(packets):
            src, dest = random.sample(self.nodes, 2)
            start = time.time()
            self.packets_sent += 1
            await protocol.transmit(src, dest, self)
            self.total_time += time.time() - start

    def analyze(self):
        avg_time = self.total_time / self.packets_sent if self.packets_sent else 0
        loss = (self.packets_lost / self.packets_sent) * 100 if self.packets_sent else 0
        bandwidth = (self.packets_sent - self.packets_lost) / self.total_time if self.total_time else 0

        print(f"\n--- Аналіз продуктивності: {self.name} топологія ---")
        print(f"Середній час передачі: {avg_time:.4f} с")
        print(f"Втрати пакетів: {loss:.2f}%")
        print(f"Пропускна здатність: {bandwidth:.2f} пак/с")

    def visualize(self):
        G = nx.Graph()
        for node in self.nodes:
            for conn in node.connections:
                G.add_edge(node.name, conn.name)

        plt.figure(figsize=(5, 4))
        nx.draw(G, with_labels=True, node_color="skyblue" if self.name == "Star" else "orange",
                node_size=2000, font_size=10, font_weight="bold")
        plt.title(f"Топологія: {self.name}")
        plt.show()


# --- 4. Запуск симуляції ---
async def main():
    # 1. Зіркова топологія (Star)
    star_net = Network("Star")
    router = Router("Router")
    pcs_star = [Node(f"PC{i}") for i in range(1, 5)]
    star_net.nodes = [router] + pcs_star
    for pc in pcs_star:
        router.connect(pc)

    await star_net.simulate(TCPProtocol, packets=20)
    star_net.analyze()
    star_net.visualize()

    # 2. Кільцева топологія (Ring)
    ring_net = Network("Ring")
    pcs_ring = [Node(f"Node{i}") for i in range(1, 6)]
    ring_net.nodes = pcs_ring
    for i in range(len(pcs_ring)):
        pcs_ring[i].connect(pcs_ring[(i + 1) % len(pcs_ring)])

    await ring_net.simulate(UDPProtocol, packets=20)
    ring_net.analyze()
    ring_net.visualize()

# Для запуску скрипта у звичайному середовищі:
# asyncio.run(main())