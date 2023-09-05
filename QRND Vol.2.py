# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


from qiskit import *
from qiskit.providers.ibmq import least_busy

print("Kütüphaneler Yüklendi...")

def Connection(account_key):
    IBMQ.save_account(account_key)
    provider = IBMQ.load_account()

    provider = IBMQ.get_provider("ibm-q")
    device = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= 5 and 
                                           not x.configuration().simulator and x.status().operational==True))
    print("En az sıra olan cihaz ile çalışacağız: ", device)
    print("IBM Hesabınıza erişim tamamlandı.")
    IBMQ.disable_account()
    return device

def real_map(deger, sol_asinir, sol_usinir, alt_sinir, ust_sinir):

    sol_Span = sol_usinir - sol_asinir
    sag_Span = ust_sinir - alt_sinir
#print("LeftSpan: ",sol_Span,"\nRightSpan: ", sag_Span)

    deger_Scaled = float(deger - sol_asinir) / float(sol_Span)
#print("ValueScaled",deger_Scaled)

    return round(alt_sinir + (deger_Scaled * sag_Span),3)

def Qriptos(account_key,qubits,alt_sinir,ust_sinir):

    # Devrenin kurulumu ve gözlem yapılması
    circuit = QuantumCircuit(qubits)

    for i in range(qubits):
        circuit.h(i)

    circuit.measure_all()

    # IBM Bilgisayarına bağlanıp devrenin bilgisayarda çalıştırılması
    device = Connection(account_key)
    
    compiled_circuit = transpile(circuit, device)

    last = []

    for i in range(1):
        job  = execute(compiled_circuit,device,shots = 1)
        print(tools.job_monitor(job))
        result = job.result()
        counts = dict(result.get_counts(circuit))

        last.append(*counts)

    #Sonuç olarak gelen bit-sting değerin sayıya dönüştürülmesi
    binary = "".join(last)
    # Binary değerin decimal haline dönüştürülmesi
    binaryQ = int("".join(last),2)
    
    qubits = len(binary)
    
    #print(binaryQ,-qubits, (qubits**2)-1+qubits, 0, 100)
    
    return real_map(binaryQ,-qubits, (qubits**2)-1+qubits, alt_sinir, ust_sinir)

print("Fonksyonlar Yüklendi..")

# Hesap anahtarının girilmesi
account_key = "ACCOUNT_KEY"
# Sayıyı almak istediğimiz aralığı belirliyoruz
alt_sinir = 0
ust_sinir = 100
# Kullanılacak Qubit sayısını gönderiyoruz.
number_of_qubits = 5

print(Qriptos(account_key,number_of_qubits,alt_sinir,ust_sinir))
