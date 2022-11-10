# discrete-event-sim
> M/M/1 queue simulation for packet Poisson arrival and processing in perspective of a Queue Theory.

## Input:
> Input arguments in the following order: time of simulation (T), arrival rate $\lambda$, service rate $\mu$, list of probabilities <br>
> to enter the buffer. During a period of time T new packets will arrive as a Poisson process with rate= $\lambda$. <br>
> When buffer is not empty, a packet is processed with rate = $\mu$. <br>
>
> Buffer is limited according to the list of probabilities. The $i_{th}$ probability describes the chance of a packet entering <br>
> a buffer when there are i packets in the buffer.

## Output:
>* Number of processed packets.
>* Number of packets that haven't been processed.
>* Time of the last processed packet.
>* $T_i$ - total time during which buffer had i packets.
>* $Z_i$ - empirical probability for i packets in the buffer.
>* Average time of waiting for a packet in a buffer to be processed.
>* Average processing time.
>* Average arrival rate to the buffer.
