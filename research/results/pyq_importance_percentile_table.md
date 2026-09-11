# Percentile-Based PYQ Topic Importance

## Score Cutoffs by Subject
### Operating Systems
- **High Threshold**: final_score >= 0.040300 (Top 15%, actual assigned: 8 topics)
- **Medium Threshold**: 0.040300 > final_score >= 0.019200 (Next 25%, actual assigned: 11 topics)
- **Low Threshold**: final_score < 0.019200 (Remaining 60% and all 0.0 scores, actual assigned: 28 topics)

### Computer Networks
- **High Threshold**: final_score >= 0.029200 (Top 15%, actual assigned: 11 topics)
- **Medium Threshold**: 0.029200 > final_score >= 0.010400 (Next 25%, actual assigned: 18 topics)
- **Low Threshold**: final_score < 0.010400 (Remaining 60% and all 0.0 scores, actual assigned: 43 topics)

### DBMS
- **High Threshold**: final_score >= 0.030700 (Top 15%, actual assigned: 12 topics)
- **Medium Threshold**: 0.030700 > final_score >= 0.015700 (Next 25%, actual assigned: 18 topics)
- **Low Threshold**: final_score < 0.015700 (Remaining 60% and all 0.0 scores, actual assigned: 44 topics)

## Operating Systems

| Unit | Topic | Q Count | Freq Score | Recency Score | Final Score | Label |
|---|---|---|---|---|---|---|
| 1: Introduction to Operating Systems | Operating System Introduction | 20 | 0.099500 | 0.088900 | 0.096300 | **High** |
| 1: Introduction to Operating Systems | Parallel Systems | 13 | 0.064700 | 0.062000 | 0.063900 | **High** |
| 1: Introduction to Operating Systems | System Components | 12 | 0.059700 | 0.066200 | 0.061600 | **High** |
| 2: CPU Scheduling and Deadlocks | Scheduling Criteria | 11 | 0.054700 | 0.060000 | 0.056300 | **High** |
| 1: Introduction to Operating Systems | Threads | 10 | 0.049800 | 0.043400 | 0.047900 | **High** |
| 5: File Systems and Disk Management | File Allocation Methods | 9 | 0.044800 | 0.042400 | 0.044100 | **High** |
| 4: Memory Management | Logical Versus Physical Address Space | 8 | 0.039800 | 0.052700 | 0.043700 | **High** |
| 3: Process Synchronization and IPC | Semaphores | 8 | 0.039800 | 0.041400 | 0.040300 | **High** |
| 4: Memory Management | Memory Management Unit (MMU) | 7 | 0.034800 | 0.042400 | 0.037100 | **Medium** |
| 5: File Systems and Disk Management | File Protection | 7 | 0.034800 | 0.031000 | 0.033700 | **Medium** |
| 5: File Systems and Disk Management | Disk Scheduling Algorithms FCFS SSTF SCAN C-SCAN | 7 | 0.034800 | 0.027900 | 0.032800 | **Medium** |
| 1: Introduction to Operating Systems | Time-shared Systems | 6 | 0.029900 | 0.037200 | 0.032100 | **Medium** |
| 1: Introduction to Operating Systems | Operations on Processes | 7 | 0.034800 | 0.025900 | 0.032100 | **Medium** |
| 1: Introduction to Operating Systems | Simple Batch Systems | 6 | 0.029900 | 0.033100 | 0.030800 | **Medium** |
| 5: File Systems and Disk Management | File System Interface and Access Methods | 6 | 0.029900 | 0.023800 | 0.028000 | **Medium** |
| 2: CPU Scheduling and Deadlocks | Deadlock Characterization | 5 | 0.024900 | 0.017600 | 0.022700 | **Medium** |
| 5: File Systems and Disk Management | System Calls for File I/O Operations | 4 | 0.019900 | 0.021700 | 0.020400 | **Medium** |
| 1: Introduction to Operating Systems | Real-Time Systems | 4 | 0.019900 | 0.020700 | 0.020100 | **Medium** |
| 5: File Systems and Disk Management | Directory Structure | 4 | 0.019900 | 0.017600 | 0.019200 | **Medium** |
| 2: CPU Scheduling and Deadlocks | Deadlock Prevention | 4 | 0.019900 | 0.016500 | 0.018900 | **Low** |
| 1: Introduction to Operating Systems | Process Concepts and Scheduling | 3 | 0.014900 | 0.022800 | 0.017300 | **Low** |
| 1: Introduction to Operating Systems | Personal Computer Systems | 3 | 0.014900 | 0.016500 | 0.015400 | **Low** |
| 5: File Systems and Disk Management | File System Structure | 3 | 0.014900 | 0.015500 | 0.015100 | **Low** |
| 1: Introduction to Operating Systems | Distributed Systems | 3 | 0.014900 | 0.014500 | 0.014800 | **Low** |
| 2: CPU Scheduling and Deadlocks | Deadlocks System Model | 3 | 0.014900 | 0.014500 | 0.014800 | **Low** |
| 4: Memory Management | Virtual Address Space | 3 | 0.014900 | 0.013400 | 0.014500 | **Low** |
| 4: Memory Management | Relocation Register | 3 | 0.014900 | 0.013400 | 0.014500 | **Low** |
| 3: Process Synchronization and IPC | Critical Section Problem | 3 | 0.014900 | 0.006200 | 0.012300 | **Low** |
| 1: Introduction to Operating Systems | Operating System Services | 2 | 0.010000 | 0.017600 | 0.012200 | **Low** |
| 2: CPU Scheduling and Deadlocks | Methods for Handling Deadlocks | 3 | 0.014900 | 0.005200 | 0.012000 | **Low** |
| 3: Process Synchronization and IPC | IPC Between Processes on a Single System | 2 | 0.010000 | 0.015500 | 0.011600 | **Low** |
| 3: Process Synchronization and IPC | Monitors | 2 | 0.010000 | 0.014500 | 0.011300 | **Low** |
| 2: CPU Scheduling and Deadlocks | Scheduling Algorithms | 2 | 0.010000 | 0.006200 | 0.008800 | **Low** |
| 2: CPU Scheduling and Deadlocks | Deadlock Detection and Recovery | 1 | 0.005000 | 0.009300 | 0.006300 | **Low** |
| 3: Process Synchronization and IPC | Shared Memory | 1 | 0.005000 | 0.009300 | 0.006300 | **Low** |
| 1: Introduction to Operating Systems | Cooperating Processes | 1 | 0.005000 | 0.008300 | 0.006000 | **Low** |
| 2: CPU Scheduling and Deadlocks | Multiple-Processor Scheduling | 1 | 0.005000 | 0.007200 | 0.005700 | **Low** |
| 3: Process Synchronization and IPC | Message Queues | 1 | 0.005000 | 0.007200 | 0.005700 | **Low** |
| 1: Introduction to Operating Systems | Multi-programmed Systems | 1 | 0.005000 | 0.005200 | 0.005000 | **Low** |
| 3: Process Synchronization and IPC | Classical Problems of Synchronization | 1 | 0.005000 | 0.005200 | 0.005000 | **Low** |
| 3: Process Synchronization and IPC | Critical Regions | 1 | 0.005000 | 0.000000 | 0.003500 | **Low** |
| 2: CPU Scheduling and Deadlocks | Deadlock Avoidance | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 3: Process Synchronization and IPC | Synchronization Hardware | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 3: Process Synchronization and IPC | IPC Between Processes on Different Systems | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 3: Process Synchronization and IPC | Pipes and FIFOs | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 4: Memory Management | Address Binding at Compile Time and Load Time | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 5: File Systems and Disk Management | Kernel Support for Files | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |

## Computer Networks

| Unit | Topic | Q Count | Freq Score | Recency Score | Final Score | Label |
|---|---|---|---|---|---|---|
| 4: Internetworking and Transport Layer | Elements of Transport Protocol | 14 | 0.074900 | 0.095600 | 0.081100 | **High** |
| 1: Overview of Internet, Physical Layer and Data Link Layer | Physical Layer Guided Transmission Media | 11 | 0.058800 | 0.062700 | 0.060000 | **High** |
| 3: Network Layer and Routing | Congestion Control Algorithms | 10 | 0.053500 | 0.051000 | 0.052700 | **High** |
| 5: Internet Transport Protocols and Application Layer | DNS | 8 | 0.042800 | 0.043600 | 0.043000 | **High** |
| 4: Internetworking and Transport Layer | Transport Layer Services to Upper Layers | 7 | 0.037400 | 0.043600 | 0.039300 | **High** |
| 1: Overview of Internet, Physical Layer and Data Link Layer | Data Link Layer Design Issues | 7 | 0.037400 | 0.037200 | 0.037400 | **High** |
| 1: Overview of Internet, Physical Layer and Data Link Layer | Comparison of OSI and TCP/IP Reference Model | 7 | 0.037400 | 0.034000 | 0.036400 | **High** |
| 5: Internet Transport Protocols and Application Layer | Electronic Mail | 6 | 0.032100 | 0.042500 | 0.035200 | **High** |
| 5: Internet Transport Protocols and Application Layer | Introduction to TCP | 6 | 0.032100 | 0.039300 | 0.034300 | **High** |
| 1: Overview of Internet, Physical Layer and Data Link Layer | Physical Layer Wireless Transmission Media | 5 | 0.026700 | 0.035100 | 0.029200 | **High** |
| 1: Overview of Internet, Physical Layer and Data Link Layer | Sliding Window Protocol | 5 | 0.026700 | 0.035100 | 0.029200 | **High** |
| 3: Network Layer and Routing | Distance Vector Routing | 5 | 0.026700 | 0.027600 | 0.027000 | **Medium** |
| 1: Overview of Internet, Physical Layer and Data Link Layer | CRC Codes | 5 | 0.026700 | 0.025500 | 0.026400 | **Medium** |
| 3: Network Layer and Routing | Network Layer Design Issues | 5 | 0.026700 | 0.023400 | 0.025700 | **Medium** |
| 2: Multiple Access Protocols and Data Link Layer Switching | CSMA | 5 | 0.026700 | 0.020200 | 0.024800 | **Medium** |
| 4: Internetworking and Transport Layer | ICMP | 4 | 0.021400 | 0.028700 | 0.023600 | **Medium** |
| 2: Multiple Access Protocols and Data Link Layer Switching | ALOHA | 4 | 0.021400 | 0.026600 | 0.022900 | **Medium** |
| 5: Internet Transport Protocols and Application Layer | HTTP | 4 | 0.021400 | 0.025500 | 0.022600 | **Medium** |
| 5: Internet Transport Protocols and Application Layer | UDP and RPC | 4 | 0.021400 | 0.024400 | 0.022300 | **Medium** |
| 3: Network Layer and Routing | Routing Algorithms | 4 | 0.021400 | 0.017000 | 0.020100 | **Medium** |
| 3: Network Layer and Routing | Hierarchical Routing | 4 | 0.021400 | 0.012800 | 0.018800 | **Medium** |
| 3: Network Layer and Routing | Shortest Path Routing | 3 | 0.016000 | 0.017000 | 0.016300 | **Medium** |
| 1: Overview of Internet, Physical Layer and Data Link Layer | Overview of the Internet | 3 | 0.016000 | 0.014900 | 0.015700 | **Medium** |
| 2: Multiple Access Protocols and Data Link Layer Switching | Data Link Layer Switching | 2 | 0.010700 | 0.017000 | 0.012600 | **Medium** |
| 5: Internet Transport Protocols and Application Layer | Application Layer Introduction | 2 | 0.010700 | 0.015900 | 0.012300 | **Medium** |
| 4: Internetworking and Transport Layer | ARP | 2 | 0.010700 | 0.014900 | 0.011900 | **Medium** |
| 2: Multiple Access Protocols and Data Link Layer Switching | Repeaters, Hubs, Bridges, Switches, Routers and Gateways | 2 | 0.010700 | 0.011700 | 0.011000 | **Medium** |
| 5: Internet Transport Protocols and Application Layer | TCP Connection Establishment | 2 | 0.010700 | 0.010600 | 0.010700 | **Medium** |
| 4: Internetworking and Transport Layer | Connection Establishment | 2 | 0.010700 | 0.009600 | 0.010400 | **Medium** |
| 3: Network Layer and Routing | Flooding | 2 | 0.010700 | 0.008500 | 0.010000 | **Low** |
| 4: Internetworking and Transport Layer | IPv4 Protocol | 2 | 0.010700 | 0.008500 | 0.010000 | **Low** |
| 5: Internet Transport Protocols and Application Layer | TCP Sliding Window | 2 | 0.010700 | 0.008500 | 0.010000 | **Low** |
| 3: Network Layer and Routing | Connectionless and Connection Oriented Networks | 2 | 0.010700 | 0.007400 | 0.009700 | **Low** |
| 5: Internet Transport Protocols and Application Layer | TCP Connection Release | 2 | 0.010700 | 0.007400 | 0.009700 | **Low** |
| 3: Network Layer and Routing | Optimality Principle | 2 | 0.010700 | 0.006400 | 0.009400 | **Low** |
| 2: Multiple Access Protocols and Data Link Layer Switching | Collision Free Protocols | 2 | 0.010700 | 0.005300 | 0.009100 | **Low** |
| 2: Multiple Access Protocols and Data Link Layer Switching | Ethernet Physical Layer | 2 | 0.010700 | 0.005300 | 0.009100 | **Low** |
| 5: Internet Transport Protocols and Application Layer | TCP Segment Header | 2 | 0.010700 | 0.005300 | 0.009100 | **Low** |
| 1: Overview of Internet, Physical Layer and Data Link Layer | Internet History, Standards and Administration | 2 | 0.010700 | 0.003200 | 0.008400 | **Low** |
| 5: Internet Transport Protocols and Application Layer | FTP | 1 | 0.005300 | 0.007400 | 0.006000 | **Low** |
| 4: Internetworking and Transport Layer | Packet Fragmentation | 1 | 0.005300 | 0.006400 | 0.005700 | **Low** |
| 5: Internet Transport Protocols and Application Layer | Real Time Transport Protocols | 1 | 0.005300 | 0.006400 | 0.005700 | **Low** |
| 5: Internet Transport Protocols and Application Layer | TCP Service Model | 1 | 0.005300 | 0.006400 | 0.005700 | **Low** |
| 2: Multiple Access Protocols and Data Link Layer Switching | Multi Access Protocols | 1 | 0.005300 | 0.004300 | 0.005000 | **Low** |
| 3: Network Layer and Routing | Count to Infinity Problem | 1 | 0.005300 | 0.004300 | 0.005000 | **Low** |
| 4: Internetworking and Transport Layer | Tunneling | 1 | 0.005300 | 0.004300 | 0.005000 | **Low** |
| 4: Internetworking and Transport Layer | IP Addresses | 1 | 0.005300 | 0.004300 | 0.005000 | **Low** |
| 4: Internetworking and Transport Layer | CIDR | 1 | 0.005300 | 0.004300 | 0.005000 | **Low** |
| 2: Multiple Access Protocols and Data Link Layer Switching | Ethernet MAC Sublayer | 1 | 0.005300 | 0.003200 | 0.004700 | **Low** |
| 4: Internetworking and Transport Layer | Internetwork Routing | 1 | 0.005300 | 0.003200 | 0.004700 | **Low** |
| 4: Internetworking and Transport Layer | IPv6 Protocol | 1 | 0.005300 | 0.003200 | 0.004700 | **Low** |
| 5: Internet Transport Protocols and Application Layer | Application Layer Paradigms | 1 | 0.005300 | 0.003200 | 0.004700 | **Low** |
| 5: Internet Transport Protocols and Application Layer | Client Server Model | 1 | 0.005300 | 0.003200 | 0.004700 | **Low** |
| 5: Internet Transport Protocols and Application Layer | TELNET | 1 | 0.005300 | 0.003200 | 0.004700 | **Low** |
| 2: Multiple Access Protocols and Data Link Layer Switching | Use of Bridges | 1 | 0.005300 | 0.002100 | 0.004400 | **Low** |
| 1: Overview of Internet, Physical Layer and Data Link Layer | Elementary Data Link Layer Protocols | 1 | 0.005300 | 0.001100 | 0.004100 | **Low** |
| 4: Internetworking and Transport Layer | Addressing | 1 | 0.005300 | 0.001100 | 0.004100 | **Low** |
| 4: Internetworking and Transport Layer | Connection Release | 1 | 0.005300 | 0.000000 | 0.003700 | **Low** |
| 1: Overview of Internet, Physical Layer and Data Link Layer | Protocol Layering Scenario | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 1: Overview of Internet, Physical Layer and Data Link Layer | TCP/IP Protocol Suite | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 1: Overview of Internet, Physical Layer and Data Link Layer | The OSI Model | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 2: Multiple Access Protocols and Data Link Layer Switching | Learning Bridges | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 2: Multiple Access Protocols and Data Link Layer Switching | Spanning Tree Bridges | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 3: Network Layer and Routing | Store and Forward Packet Switching | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 3: Network Layer and Routing | Admission Control | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 4: Internetworking and Transport Layer | RARP | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 4: Internetworking and Transport Layer | DHCP | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 4: Internetworking and Transport Layer | Crash Recovery | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 5: Internet Transport Protocols and Application Layer | TCP Connection Management Modeling | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 5: Internet Transport Protocols and Application Layer | TCP Congestion Control | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 5: Internet Transport Protocols and Application Layer | Future of TCP | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 5: Internet Transport Protocols and Application Layer | SSH | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |

## DBMS

| Unit | Topic | Q Count | Freq Score | Recency Score | Final Score | Label |
|---|---|---|---|---|---|---|
| 3: SQL, Constraints, and Triggers | SQL Queries | 7 | 0.056500 | 0.079500 | 0.063400 | **High** |
| 1: Introduction to Database Systems | Structure of a DBMS | 6 | 0.048400 | 0.060700 | 0.052100 | **High** |
| 2: Relational Model and Algebra | Relational algebra | 6 | 0.048400 | 0.058600 | 0.051400 | **High** |
| 4: Schema Refinement and Normalization | Fourth normal form | 5 | 0.040300 | 0.043900 | 0.041400 | **High** |
| 5: Transaction Management and Recovery | Locking systems with several lock modes | 5 | 0.040300 | 0.043900 | 0.041400 | **High** |
| 1: Introduction to Database Systems | Database System Applications | 5 | 0.040300 | 0.035600 | 0.038900 | **High** |
| 1: Introduction to Database Systems | Data Models | 4 | 0.032300 | 0.046000 | 0.036400 | **High** |
| 1: Introduction to Database Systems | File Systems versus a DBMS | 4 | 0.032300 | 0.039700 | 0.034500 | **High** |
| 1: Introduction to Database Systems | Additional features of the ER model | 4 | 0.032300 | 0.031400 | 0.032000 | **High** |
| 2: Relational Model and Algebra | Tuple relational calculus | 4 | 0.032300 | 0.031400 | 0.032000 | **High** |
| 3: SQL, Constraints, and Triggers | Nested queries | 4 | 0.032300 | 0.031400 | 0.032000 | **High** |
| 3: SQL, Constraints, and Triggers | Aggregation operators | 4 | 0.032300 | 0.027200 | 0.030700 | **High** |
| 4: Schema Refinement and Normalization | Schema refinement | 4 | 0.032300 | 0.027200 | 0.030700 | **Medium** |
| 1: Introduction to Database Systems | Database design and ER diagrams | 4 | 0.032300 | 0.023000 | 0.029500 | **Medium** |
| 5: Transaction Management and Recovery | Transaction concept | 3 | 0.024200 | 0.025100 | 0.024500 | **Medium** |
| 5: Transaction Management and Recovery | B+ Trees | 3 | 0.024200 | 0.023000 | 0.023800 | **Medium** |
| 5: Transaction Management and Recovery | Concurrency control by timestamps | 3 | 0.024200 | 0.018800 | 0.022600 | **Medium** |
| 5: Transaction Management and Recovery | Buffer management | 3 | 0.024200 | 0.018800 | 0.022600 | **Medium** |
| 2: Relational Model and Algebra | Domain relational calculus | 3 | 0.024200 | 0.016700 | 0.022000 | **Medium** |
| 5: Transaction Management and Recovery | Serializability | 2 | 0.016100 | 0.031400 | 0.020700 | **Medium** |
| 5: Transaction Management and Recovery | Extendible Hashing | 3 | 0.024200 | 0.010500 | 0.020100 | **Medium** |
| 5: Transaction Management and Recovery | Primary Index | 3 | 0.024200 | 0.008400 | 0.019400 | **Medium** |
| 1: Introduction to Database Systems | Levels of abstraction in a DBMS | 2 | 0.016100 | 0.025100 | 0.018800 | **Medium** |
| 2: Relational Model and Algebra | Introduction to the Relational Model | 2 | 0.016100 | 0.023000 | 0.018200 | **Medium** |
| 3: SQL, Constraints, and Triggers | Complex integrity constraints in SQL | 2 | 0.016100 | 0.023000 | 0.018200 | **Medium** |
| 5: Transaction Management and Recovery | Validation | 2 | 0.016100 | 0.020900 | 0.017600 | **Medium** |
| 4: Schema Refinement and Normalization | Closure of a set of functional dependencies | 2 | 0.016100 | 0.018800 | 0.016900 | **Medium** |
| 5: Transaction Management and Recovery | System log | 2 | 0.016100 | 0.018800 | 0.016900 | **Medium** |
| 5: Transaction Management and Recovery | Secondary Index | 2 | 0.016100 | 0.018800 | 0.016900 | **Medium** |
| 4: Schema Refinement and Normalization | Multivalued dependencies | 2 | 0.016100 | 0.014600 | 0.015700 | **Medium** |
| 4: Schema Refinement and Normalization | Problems caused by redundancy | 2 | 0.016100 | 0.010500 | 0.014400 | **Low** |
| 2: Relational Model and Algebra | Destroying/altering tables and views | 2 | 0.016100 | 0.006300 | 0.013200 | **Low** |
| 5: Transaction Management and Recovery | Failure with loss of non-volatile storage | 2 | 0.016100 | 0.004200 | 0.012500 | **Low** |
| 5: Transaction Management and Recovery | Linear Hashing | 2 | 0.016100 | 0.004200 | 0.012500 | **Low** |
| 4: Schema Refinement and Normalization | Second normal form | 2 | 0.016100 | 0.000000 | 0.011300 | **Low** |
| 5: Transaction Management and Recovery | Static Hashing | 1 | 0.008100 | 0.016700 | 0.010700 | **Low** |
| 4: Schema Refinement and Normalization | First normal form | 1 | 0.008100 | 0.012600 | 0.009400 | **Low** |
| 4: Schema Refinement and Normalization | Lossless join decomposition | 1 | 0.008100 | 0.012600 | 0.009400 | **Low** |
| 5: Transaction Management and Recovery | Recovery with concurrent transactions | 1 | 0.008100 | 0.012600 | 0.009400 | **Low** |
| 3: SQL, Constraints, and Triggers | Triggers and active databases | 1 | 0.008100 | 0.010500 | 0.008800 | **Low** |
| 4: Schema Refinement and Normalization | Third normal form | 1 | 0.008100 | 0.006300 | 0.007500 | **Low** |
| 2: Relational Model and Algebra | Enforcing integrity constraints | 1 | 0.008100 | 0.004200 | 0.006900 | **Low** |
| 3: SQL, Constraints, and Triggers | UNION, INTERSECT, and EXCEPT | 1 | 0.008100 | 0.004200 | 0.006900 | **Low** |
| 1: Introduction to Database Systems | Relationships and Relationship sets | 1 | 0.008100 | 0.000000 | 0.005600 | **Low** |
| 1: Introduction to Database Systems | Data independence | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 1: Introduction to Database Systems | Entities, Attributes, and Entity sets | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 1: Introduction to Database Systems | Conceptual design with the ER model | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 2: Relational Model and Algebra | Integrity constraints over relations | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 2: Relational Model and Algebra | Database design | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 2: Relational Model and Algebra | Logical database design | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 2: Relational Model and Algebra | Introduction to views | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 3: SQL, Constraints, and Triggers | Form of basic SQL query | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 3: SQL, Constraints, and Triggers | NULL values | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 4: Schema Refinement and Normalization | Decompositions and associated problems | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 4: Schema Refinement and Normalization | Reasoning about functional dependencies | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 4: Schema Refinement and Normalization | Armstrong's axioms | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 4: Schema Refinement and Normalization | Minimal covers | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 4: Schema Refinement and Normalization | BCNF | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 5: Transaction Management and Recovery | Transaction state | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 5: Transaction Management and Recovery | Commit point | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 5: Transaction Management and Recovery | Desirable properties | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 5: Transaction Management and Recovery | Concurrent executions | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 5: Transaction Management and Recovery | Recoverability | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 5: Transaction Management and Recovery | Implementation of isolation | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 5: Transaction Management and Recovery | Testing for serializability | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 5: Transaction Management and Recovery | Serializability by locks | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 5: Transaction Management and Recovery | Log-based recovery | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 5: Transaction Management and Recovery | Checkpoints | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 5: Transaction Management and Recovery | External Storage and Indexing | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 5: Transaction Management and Recovery | Heap Files | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 5: Transaction Management and Recovery | Sequential Files | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 5: Transaction Management and Recovery | Clustered Files | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 5: Transaction Management and Recovery | Cluster Index | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |
| 5: Transaction Management and Recovery | ISAM | 0 | 0.000000 | 0.000000 | 0.000000 | **Low** |

