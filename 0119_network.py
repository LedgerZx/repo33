import psutil
import socket
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import ipaddress
from datetime import datetime
import threading

class NetworkAnalyzer:
    def __init__(self, max_points=100):
        self.max_points = max_points
        self.timestamps = deque(maxlen=max_points)
        self.bytes_sent = deque(maxlen=max_points)
        self.bytes_recv = deque(maxlen=max_points)
        self.connections = []
        self.processes = {}
        self.remote_ips = {}
        self.start_time = time.time()
        
    def get_network_stats(self):
        """Get current network statistics"""
        net_io = psutil.net_io_counters()
        current_time = time.time()
        
        self.timestamps.append(current_time)
        self.bytes_sent.append(net_io.bytes_sent)
        self.bytes_recv.append(net_io.bytes_recv)
        
        return net_io
    
    def get_connections(self):
        """Get active network connections"""
        self.connections = []
        connections = psutil.net_connections(kind='inet')
        
        for conn in connections:
            if conn.status == 'ESTABLISHED':
                try:
                    local_addr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                    remote_addr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                    
                    # Get process info
                    pid = conn.pid
                    process_name = "Unknown"
                    if pid:
                        try:
                            process = psutil.Process(pid)
                            process_name = process.name()
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pass
                    
                    self.connections.append({
                        'local_addr': local_addr,
                        'remote_addr': remote_addr,
                        'status': conn.status,
                        'pid': pid,
                        'process': process_name,
                        'type': 'TCP' if conn.type == socket.SOCK_STREAM else 'UDP'
                    })
                    
                    # Track remote IP statistics
                    if conn.raddr:
                        ip = conn.raddr.ip
                        if ip not in self.remote_ips:
                            self.remote_ips[ip] = {'count': 0, 'first_seen': current_time}
                        self.remote_ips[ip]['count'] += 1
                        
                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    pass
        
        return self.connections
    
    def get_top_processes(self):
        """Get processes with highest network usage"""
        self.processes = {}
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                pid = proc.info['pid']
                name = proc.info['name']
                
                # Get IO counters for this process
                io_counters = proc.io_counters()
                if io_counters:
                    self.processes[pid] = {
                        'name': name,
                        'read_bytes': io_counters.read_bytes,
                        'write_bytes': io_counters.write_bytes
                    }
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.NoSuchProcess):
                pass
        
        # Sort by total bytes (read + write)
        sorted_processes = sorted(
            self.processes.items(), 
            key=lambda x: x[1]['read_bytes'] + x[1]['write_bytes'], 
            reverse=True
        )
        
        return sorted_processes[:10]  # Return top 10
    
    def get_geolocation_info(self, ip):
        """Get basic geolocation info for an IP address"""
        try:
            ip_obj = ipaddress.ip_address(ip)
            
            # Check if it's a private IP
            if ip_obj.is_private:
                return "Private Network"
            
            # Check if it's a loopback IP
            if ip_obj.is_loopback:
                return "Loopback"
            
            # Check if it's a multicast IP
            if ip_obj.is_multicast:
                return "Multicast"
            
            # For public IPs, we would normally use a geolocation service
            # But since we're not making external API calls, we'll just identify the type
            if ip_obj.version == 4:
                if ip.startswith('8.8.') or ip.startswith('1.1.1.'):
                    return "DNS Server"
                elif ip.startswith('192.30.25') or ip.startswith('140.82.112'):
                    return "GitHub"
                elif ip.startswith('151.101.') or ip.startswith('104.16.'):
                    return "CDN"
                else:
                    return "Public IP"
            else:
                return "IPv6 Public"
        except ValueError:
            return "Invalid IP"

class NetworkVisualizer:
    def __init__(self):
        self.analyzer = NetworkAnalyzer()
        self.fig, self.axes = plt.subplots(2, 2, figsize=(15, 10))
        self.fig.suptitle('Network Traffic Analyzer', fontsize=16)
        
        # Network traffic plot
        self.ax_traffic = self.axes[0, 0]
        self.ax_traffic.set_title('Network Traffic (Bytes/sec)')
        self.ax_traffic.set_xlabel('Time')
        self.ax_traffic.set_ylabel('Bytes/sec')
        
        # Top processes plot
        self.ax_processes = self.axes[0, 1]
        self.ax_processes.set_title('Top Processes by Network Usage')
        self.ax_processes.set_xlabel('Process')
        self.ax_processes.set_ylabel('Bytes')
        
        # Remote IPs plot
        self.ax_ips = self.axes[1, 0]
        self.ax_ips.set_title('Remote IP Connections')
        self.ax_ips.set_xlabel('IP Address')
        self.ax_ips.set_ylabel('Connection Count')
        
        # Connection status pie chart
        self.ax_status = self.axes[1, 1]
        self.ax_status.set_title('Connection Status')
        
        # Initialize plots
        self.line_sent, = self.ax_traffic.plot([], [], 'b-', label='Sent')
        self.line_recv, = self.ax_traffic.plot([], [], 'r-', label='Received')
        self.ax_traffic.legend()
        
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        
    def update(self, frame):
        """Update the visualization"""
        # Get network stats
        net_io = self.analyzer.get_network_stats()
        
        # Calculate bytes/sec
        if len(self.analyzer.timestamps) > 1:
            time_diff = self.analyzer.timestamps[-1] - self.analyzer.timestamps[-2]
            if time_diff > 0:
                sent_rate = (self.analyzer.bytes_sent[-1] - self.analyzer.bytes_sent[-2]) / time_diff
                recv_rate = (self.analyzer.bytes_recv[-1] - self.analyzer.bytes_recv[-2]) / time_diff
            else:
                sent_rate = 0
                recv_rate = 0
        else:
            sent_rate = 0
            recv_rate = 0
        
        # Update traffic plot
        if len(self.analyzer.timestamps) > 1:
            times = [(t - self.analyzer.start_time) for t in self.analyzer.timestamps]
            sent_values = []
            recv_values = []
            
            for i in range(1, len(self.analyzer.bytes_sent)):
                time_diff = self.analyzer.timestamps[i] - self.analyzer.timestamps[i-1]
                if time_diff > 0:
                    sent_values.append((self.analyzer.bytes_sent[i] - self.analyzer.bytes_sent[i-1]) / time_diff)
                    recv_values.append((self.analyzer.bytes_recv[i] - self.analyzer.bytes_recv[i-1]) / time_diff)
                else:
                    sent_values.append(0)
                    recv_values.append(0)
            
            self.line_sent.set_data(times[1:], sent_values)
            self.line_recv.set_data(times[1:], recv_values)
            
            # Adjust axes
            self.ax_traffic.relim()
            self.ax_traffic.autoscale_view()
        
        # Get and display connections
        connections = self.analyzer.get_connections()
        
        # Update connection status pie chart
        status_counts = {}
        for conn in connections:
            status = conn['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        self.ax_status.clear()
        if status_counts:
            self.ax_status.pie(status_counts.values(), labels=status_counts.keys(), autopct='%1.1f%%')
        self.ax_status.set_title('Connection Status')
        
        # Update top processes bar chart
        top_processes = self.analyzer.get_top_processes()
        
        self.ax_processes.clear()
        if top_processes:
            processes = [p[1]['name'] for p in top_processes]
            bytes_usage = [p[1]['read_bytes'] + p[1]['write_bytes'] for p in top_processes]
            
            self.ax_processes.barh(processes, bytes_usage)
            self.ax_processes.set_title('Top Processes by Network Usage')
            self.ax_processes.set_xlabel('Total Bytes')
        
        # Update remote IPs
        if self.analyzer.remote_ips:
            # Sort by connection count
            sorted_ips = sorted(self.analyzer.remote_ips.items(), key=lambda x: x[1]['count'], reverse=True)
            top_ips = sorted_ips[:10]  # Show top 10
            
            ip_addresses = [ip[0] for ip in top_ips]
            ip_counts = [ip[1]['count'] for ip in top_ips]
            
            # Get geolocation info for each IP
            ip_locations = [self.analyzer.get_geolocation_info(ip) for ip in ip_addresses]
            
            # Create labels with IP and location
            ip_labels = [f"{ip}\n({loc})" for ip, loc in zip(ip_addresses, ip_locations)]
            
            self.ax_ips.clear()
            bars = self.ax_ips.bar(range(len(ip_counts)), ip_counts)
            
            # Color bars based on location type
            for i, bar in enumerate(bars):
                location = ip_locations[i]
                if location == "Private Network":
                    bar.set_color('blue')
                elif location == "Public IP":
                    bar.set_color('green')
                elif "DNS" in location:
                    bar.set_color('orange')
                elif "GitHub" in location:
                    bar.set_color('purple')
                elif "CDN" in location:
                    bar.set_color('red')
                else:
                    bar.set_color('gray')
            
            self.ax_ips.set_xticks(range(len(ip_labels)))
            self.ax_ips.set_xticklabels(ip_labels, rotation=45, ha='right')
            self.ax_ips.set_title('Remote IP Connections')
            self.ax_ips.set_ylabel('Connection Count')
        
        # Update timestamp
        self.fig.suptitle(f'Network Traffic Analyzer - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', fontsize=16)
        
        return self.line_sent, self.line_recv
    
    def start(self):
        """Start the animation"""
        self.ani = FuncAnimation(self.fig, self.update, interval=1000, blit=False)
        plt.show()

def main():
    print("Starting Network Traffic Analyzer...")
    print("This will monitor your network connections and display statistics.")
    print("Note: This tool only monitors network activity and does not capture packet contents.")
    
    visualizer = NetworkVisualizer()
    visualizer.start()

if __name__ == "__main__":
    main()
