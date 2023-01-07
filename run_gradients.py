import socket
import numpy as np
import matplotlib.pyplot as plt
import pdb
st = pdb.set_trace

import external # imports external.py
import local_config
import experiment as ex
from local_config import ip_address, port, fpga_clk_freq_MHz, grad_board

def run_gradients(prev_socket=None):
    exp = ex.Experiment(lo_freq=0.5, init_gpa=True, prev_socket=prev_socket, flush_old_rx=True, grad_max_update_rate=0.05)

    grad_vals = (np.array([50, 100, 150]), np.array([0, 0.1, 0]))
    event_dict = {'tx0': (np.array([50, 130, 200, 360]), np.array([1, 0, 1, 0])),
                  'tx1': (np.array([500, 700]), np.array([0.2, 0])),
                  'grad_vx': grad_vals,
                  'rx0_en': (np.array([400, 800]), np.array([1, 0])),
                  'rx1_en': (np.array([400, 800]), np.array([1, 0])) }
    exp.add_flodict(event_dict)
    if False:
        exp.plot_sequence()
        plt.show()

    rxd, msgs = exp.run()
    exp.close_server(only_if_sim=True)

    if False:
        plt.figure()
        plt.plot(np.abs(rxd['rx1']))
        plt.show()

    exp.__del__()

if __name__ == "__main__":
    if True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect( (local_config.ip_address, local_config.port) )
    else:
        sock = None

    for k in range(10000):
        print(k)
        run_gradients(prev_socket=sock)

    sock.close()
