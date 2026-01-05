#!/usr/bin/env python3
"""
Real-time Network Traffic Visualizer
Captures network packets and visualizes connections as an interactive graph
"""

import scapy.all as scapy
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import time
from collections import defaultdict, deque
import socket
import argparse
from datetime import datetime

class NetworkVisualizer:
    def __init__(self, interface=None, max_nodes=50, history_size=100):
        self.interface = interface or scapy.conf.iface
        self.max_nodes = max_nodes
        self.history_size = history_size
        
        # Network graph
        self.G = nx.Graph()
        self.pos = nx.spring_layout(self.G)
        
        # Traffic statistics
        self.traffic_data = defaultdict(lambda: {'bytes': 0, 'packets': 0})
        self.connection_history = deque(maxlen=history_size)
        self.node_sizes = defaultdict(int)
        
        # Colors for different protocols
        self.protocol_colors = {
            'TCP': '#FF6B6B',
            'UDP': '#4ECDC4',
            'ICMP': '#45B7D1',
            'HTTP': '#96CEB4',
            'HTTPS': '#FFEAA7',
            'DNS': '#DDA0DD',
            'default': '#95A5A6'
        }
        
        # Visualization setup
        self.fig, (self.ax_graph, self.ax_stats) = plt.subplots(1, 2, figsize=(16, 8))
        self.fig.suptitle(f'Network Traffic Monitor - Interface: {self.interface}', fontsize=16)
        
        # Stop flag
        self.running = False
        
    def resolve_hostname(self, ip):
        """Resolve IP to hostname with caching"""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname.split('.')[0] if '.' in hostname else hostname
        except:
            return ip
    
    def process_packet(self, packet):
        """Process captured packet and update graph"""
        if packet.haslayer(scapy.IP):
            src_ip = packet[scapy.IP].src
            dst_ip = packet[scapy.IP].dst
            protocol = packet[scapy.IP].proto
            
            # Get protocol name
            if packet.haslayer(scapy.TCP):
                proto_name = 'TCP'
                if packet.haslayer(scapy.Raw) and packet[scapy.TCP].dport in [80, 8080]:
                    proto_name = 'HTTP'
                elif packet[scapy.TCP].dport == 443:
                    proto_name = 'HTTPS'
            elif packet.haslayer(scapy.UDP):
                proto_name = 'UDP'
                if packet.haslayer(scapy.DNS):
                    proto_name = 'DNS'
            elif packet.haslayer(scapy.ICMP):
                proto_name = 'ICMP'
            else:
                proto_name = f'IP-{protocol}'
            
            # Update node information
            src_name = self.resolve_hostname(src_ip)
            dst_name = self.resolve_hostname(dst_ip)
            
            # Add nodes if not exists
            if src_name not in self.G:
                self.G.add_node(src_name, ip=src_ip)
            if dst_name not in self.G:
                self.G.add_node(dst_name, ip=dst_ip)
            
            # Update edge with protocol info
            if self.G.has_edge(src_name, dst_name):
                self.G[src_name][dst_name]['weight'] += 1
                if proto_name not in self.G[src_name][dst_name]['protocols']:
                    self.G[src_name][dst_name]['protocols'].append(proto_name)
            else:
                self.G.add_edge(src_name, dst_name, weight=1, protocols=[proto_name])
            
            # Update traffic statistics
            packet_size = len(packet)
            self.traffic_data[f"{src_name}-{dst_name}"]['bytes'] += packet_size
            self.traffic_data[f"{src_name}-{dst_name}"]['packets'] += 1
            
            # Update node sizes
            self.node_sizes[src_name] += packet_size
            self.node_sizes[dst_name] += packet_size
            
            # Add to history
            self.connection_history.append({
                'timestamp': datetime.now(),
                'src': src_name,
                'dst': dst_name,
                'protocol': proto_name,
                'size': packet_size
            })
            
            # Limit graph size
            if len(self.G.nodes) > self.max_nodes:
                self._prune_graph()
    
    def _prune_graph(self):
        """Remove least active nodes to maintain size limit"""
        # Sort nodes by activity (total bytes)
        sorted_nodes = sorted(self.node_sizes.items(), key=lambda x: x[1], reverse=True)
        nodes_to_remove = [node for node, _ in sorted_nodes[self.max_nodes:]]
        
        for node in nodes_to_remove:
            if node in self.G:
                self.G.remove_node(node)
                del self.node_sizes[node]
    
    def update_visualization(self, frame):
        """Update the visualization"""
        if not self.G.nodes:
            return
        
        # Clear axes
        self.ax_graph.clear()
        self.ax_stats.clear()
        
        # Update layout
        self.pos = nx.spring_layout(self.G, pos=self.pos, iterations=5)
        
        # Prepare node sizes and colors
        node_sizes = [max(300, self.node_sizes.get(node, 0) / 100) for node in self.G.nodes()]
        node_colors = []
        
        for node in self.G.nodes():
            # Color based on activity
            activity = self.node_sizes.get(node, 0)
            if activity > 10000:
                node_colors.append('#FF6B6B')  # High activity - red
            elif activity > 5000:
                node_colors.append('#FFA500')  # Medium activity - orange
            else:
                node_colors.append('#4ECDC4')  # Low activity - cyan
        
        # Draw graph
        nx.draw_networkx_nodes(self.G, self.pos, node_size=node_sizes, 
                              node_color=node_colors, alpha=0.8, ax=self.ax_graph)
        
        # Draw edges with protocol colors
        for edge in self.G.edges(data=True):
            src, dst, data = edge
            protocols = data.get('protocols', ['default'])
            color = self.protocol_colors.get(protocols[0], self.protocol_colors['default'])
            weight = min(data.get('weight', 1), 5)  # Cap edge width
            
            nx.draw_networkx_edges(self.G, self.pos, [(src, dst)], 
                                  width=weight, alpha=0.6, edge_color=color, ax=self.ax_graph)
        
        # Draw labels (only for active nodes)
        labels = {node: node for node in self.G.nodes() if self.node_sizes.get(node, 0) > 1000}
        nx.draw_networkx_labels(self.G, self.pos, labels, font_size=8, ax=self.ax_graph)
        
        # Update statistics
        self._update_stats()
        
        # Set titles
        self.ax_graph.set_title(f'Network Connections ({len(self.G.nodes)} nodes, {len(self.G.edges)} edges)')
        self.ax_graph.axis('off')
        
        plt.tight_layout()
    
    def _update_stats(self):
        """Update statistics panel"""
        if not self.connection_history:
            return
        
        # Recent connections
        recent = list(self.connection_history)[-10:]
        stats_text = "Recent Connections:\n" + "="*30 + "\n"
        
        for conn in recent:
            stats_text += f"{conn['timestamp'].strftime('%H:%M:%S')} - "
            stats_text += f"{conn['src']} → {conn['dst']}\n"
            stats_text += f"  Protocol: {conn['protocol']}, Size: {conn['size']} bytes\n\n"
        
        # Top talkers
        if self.node_sizes:
            stats_text += "\nTop Talkers:\n" + "="*30 + "\n"
            top_talkers = sorted(self.node_sizes.items(), key=lambda x: x[1], reverse=True)[:5]
            for node, size in top_talkers:
                stats_text += f"{node}: {size/1024:.1f} KB\n"
        
        self.ax_stats.text(0.05, 0.95, stats_text, transform=self.ax_stats.transAxes,
                          fontsize=9, verticalalignment='top', fontfamily='monospace')
        self.ax_stats.axis('off')
    
    def start_capture(self):
        """Start packet capture in separate thread"""
        self.running = True
        
        def capture_thread():
            scapy.sniff(iface=self.interface, prn=self.process_packet, 
                       store=False, stop_filter=lambda x: not self.running)
        
        self.capture_thread = threading.Thread(target=capture_thread, daemon=True)
        self.capture_thread.start()
    
    def stop(self):
        """Stop packet capture"""
        self.running = False
    
    def run(self):
        """Run the visualizer"""
        print(f"Starting network capture on interface: {self.interface}")
        print("Press Ctrl+C to stop...")
        
        self.start_capture()
        
        # Create animation
        self.ani = FuncAnimation(self.fig, self.update_visualization, interval=1000, blit=False)
        
        try:
            plt.show()
        except KeyboardInterrupt:
            print("\nStopping capture...")
            self.stop()

def main():
    parser = argparse.ArgumentParser(description='Real-time Network Traffic Visualizer')
    parser.add_argument('-i', '--interface', help='Network interface to monitor')
    parser.add_argument('-n', '--nodes', type=int, default=50, help='Maximum number of nodes to display')
    parser.add_argument('-l', '--list', action='store_true', help='List available interfaces')
    
    args = parser.parse_args()
    
    if args.list:
        print("Available network interfaces:")
        for iface in scapy.get_if_list():
            print(f"  - {iface}")
        return
    
    # Check for root privileges (required for packet capture)
    if os.geteuid() != 0:
        print("Warning: This script requires root privileges for packet capture.")
        print("Try running with 'sudo' if you encounter permission errors.")
    
    visualizer = NetworkVisualizer(interface=args.interface, max_nodes=args.nodes)
    visualizer.run()

if __name__ == "__main__":
    import os
    main()
