# ServerMonitor
Run on the server
Catch the system info

1.overall introduction
With the continuous development of informatization construction in various industries, individual servers can no longer meet the needs of enterprises. The scale of networks and applications is expanding day by day, and server network clusters are widely used in medium and small enterprises. Server performance monitoring and routine maintenance become complicated. Server administrators urgently need a practical monitoring system to help them understand the running status of the server in real time, detect server failures, and keep the maintenance server running.

Server performance monitoring is a pointer to the running status of the server system and monitoring of various indicators. Monitoring indicators include: CPU usage, CPU load, memory usage, disk I/O, disk space, network traffic, and more. And in real-time, the server performance parameters obtained by the monitoring are transmitted back to the client and uploaded to the database on the central server for later query and analysis.


This paper focuses on the research and implementation of server application performance monitoring system, the network service technology, server performance parameter acquisition and the use of coal char component dynamic display server running state name. The use of web service simplifies the client system, server performance parameters The acquisition process is encapsulated in a Windows process, and the system is very scalable. The implementation goal of the system is remote monitoring of server performance, one-to-many monitoring, and the server administrator can view the running status of the server for a period of time.

2.System Development Environment
The development environment of the system includes the software environment and the hardware environment. It is an environment necessary for development systems.

  Software environment
  
    1. The client operating system is Microsoft Windows 7 and above.
    
    2. The operating system on the server and the central server is Windows Server 2000 and above. The Windows system is used because     the system calls the Sigar tool to get the performance data of the server.
    
    3. The database operating system is MySQL5.1.
    
    4. System development language: JAVA programming language.
    
    5. System development tools: MyEclipse8.5 and MySQL-Front tools.
    
    6. System operating environment: JDK1.6.
    
  Hardware environment
  
    1. Client configuration: It is recommended to use Intel processor (1.5GHz) or above, memory 2GB, hard disk 100GB or more.
    
    2. Central server configuration: It is recommended to use Intel dual-core processor (2.0GHz), memory 2GB, hard disk 150GB or more.
    
    3. Server configuration: It is recommended to use Intel processor (1.5GHz) or above, memory 2GB, hard disk 100GB or more.
    
    
    
3.Front End Design
The client program is a website that is mainly implemented using JSP. Provide the administrator with an operation interface and display the running status of the server in the browser. First, design the website interface. The website page is mainly written in HTML and CSS.

![image](https://user-images.githubusercontent.com/44720386/64757844-161cd400-d4e8-11e9-8f14-b9e543eee04b.png)

