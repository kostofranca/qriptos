## The most basic implementation for generation of Random Numbers using IBM's Quantum Computers

#This code uses the Hadamard Gate's superposition principle to create random numbers

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 14:41:44 2021

@author: Ahmet Kasım Erbay
"""

# The most basic method for creating truely (as true as IBM Quantum Computers exist! :)) random numbers using IBM Quantum Computers. This method depends on Hadamard Gate's Superposition effect.

from qiskit import *
from qiskit import QuantumCircuit, transpile
from qiskit.providers.ibmq import least_busy

def Connection(account_key):
    
    IBMQ.save_account(account_key) # Takes your key for authentication
    provider = IBMQ.load_account() # Loads the account

    provider = IBMQ.get_provider("ibm-q")
    
    # Finds the most available device to work on
    device = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= 5 and 
                                           not x.configuration().simulator and x.status().operational==True))
    print("The device we wil be working on: ", device)

    return device

def Qriptos(account_key,qubits):

    device = Connection(account_key) # Connects the account info when called

    circuit = QuantumCircuit(qubits) # Create Quantum Circuit has # of "qubits"

    # Apply Hadamard Gate to all qubits
    for i in range(qubits):
        circuit.h(i)

    circuit.measure_all() # Measure all qubit states and erite on classical bits

    compiled_circuit = transpile(circuit, device)#simulator) # Compile the circuit
    
    #circuit.draw('mpl')

    last = []

    for i in range(1):

        # Run the Circuit on real computer experiment
        
        job  = execute(compiled_circuit,device,shots = 1)#simulator.run(compiled_circuit, shots=1)
        #print(tools.job_monitor(job)) #
        result = job.result()
        counts = dict(result.get_counts(circuit))

        last.append(*counts)

    return "".join(last)

account_key = "Your_IBM_Account_Token"

print(Qriptos(account_key,5))

