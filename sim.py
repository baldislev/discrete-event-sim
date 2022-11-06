
import numpy as np
import sys


class Packet:
    def __init__(self, arrival,  service_start=0.0):
        self.arrival = arrival
        self.service_start = service_start
        self.service_fin = 0.0

    def wait_time(self):
        return self.service_start - self.arrival

    def service_time(self):
        return self.service_fin - self.service_start

    def print(self):
        print(f'arrival time: {self.arrival} \n'
              f'service start: {self.service_start} \n'
              f'service finish: {self.service_fin} \n')


class Simulator:
    def __init__(self, arrive_scale,  service_scale, T, probs):
        self.arrive_scale = arrive_scale
        self.service_scale = service_scale
        self.T = T
        self.probs = probs
        self.successfuly_entered_packets: list[Packet] = []
        self.failed_to_enter_packets_count = 0
        self.served_packets: list[Packet] = []
        self.T_i = [0]*(len(probs))
        self.prev_change_time = 0  # for updating T_i
        self.next_arrived = np.random.exponential(scale=arrive_scale)
        self.next_served = 0
        self.T_W = 0

    def new_packet_arrived(self):
        curr_num_of_packets_in_buffer = len(self.successfuly_entered_packets)
        success_to_enter = np.random.binomial(
            1,
            self.probs[curr_num_of_packets_in_buffer],
            1
        )[0]
        if success_to_enter:
            self.successfuly_entered_packets.append(Packet(self.next_arrived))
            self.T_i[curr_num_of_packets_in_buffer] += self.next_arrived - \
                                            self.prev_change_time
            self.prev_change_time = self.next_arrived
        else:
            self.failed_to_enter_packets_count += 1

        self.next_arrived = self.next_arrived + np.random.exponential(scale=self.arrive_scale)

    def a_packet_was_printed(self):
        if len(self.successfuly_entered_packets) > 0:
            self.successfuly_entered_packets[0].service_start = self.next_served
            service_fin = self.next_served + np.random.exponential(scale=self.service_scale)
            self.successfuly_entered_packets[0].service_fin = service_fin

            while self.next_arrived < min(service_fin, self.T):
                self.new_packet_arrived()

            current_packet_num = len(self.successfuly_entered_packets)
            served_packet = self.successfuly_entered_packets.pop(0)
            self.T_i[current_packet_num] += served_packet.service_fin - \
                self.prev_change_time
            self.prev_change_time = served_packet.service_fin

            self.T_W += served_packet.service_start - served_packet.arrival

            self.served_packets.append(served_packet)
            self.next_served = served_packet.service_fin

    def start(self):
        while self.next_arrived <= self.T:
            if len(self.successfuly_entered_packets) == 0:
                self.next_served = self.next_arrived
                self.new_packet_arrived()
            elif self.next_arrived <= self.next_served:
                self.new_packet_arrived()
            else:
                self.a_packet_was_printed()

        # self.next_arrived = np.inf

        while len(self.successfuly_entered_packets) > 0:
            self.a_packet_was_printed()

        total_entered_to_buffer = len(self.served_packets) + \
            len(self.successfuly_entered_packets)

        Y = len(self.served_packets)

        X = self.failed_to_enter_packets_count + \
            len(self.successfuly_entered_packets)

        T_prime = self.served_packets[Y-1].service_fin

        Z_i = map(lambda x: (x/T_prime), self.T_i)

        T_S = sum(map(
            lambda x: (x.service_fin-x.service_start),
            self.served_packets
        )) / total_entered_to_buffer

        lambda_A = total_entered_to_buffer / self.T

        print(
            Y,
            X,
            T_prime,
            ' '.join([str(t) for t in self.T_i]),
            ' '.join([str(t) for t in Z_i]),
            self.T_W / total_entered_to_buffer,
            T_S,
            lambda_A
        )


if __name__ == '__main__':
    probs = []
    T = float(sys.argv[1])
    arrival_rate = float(sys.argv[2])  # lambda
    service_rate = float(sys.argv[3])  # mu
    service_scale = 1 / (service_rate + 0.0)  # 1/mu
    arrival_scale = 1 / (arrival_rate + 0.0)  # 1/lambda

    for i in range(4, len(sys.argv)):
        probs.append(float(sys.argv[i]))

    ########################## Start##########################

    s = Simulator(arrival_scale, service_scale, T, probs)
    s.start()