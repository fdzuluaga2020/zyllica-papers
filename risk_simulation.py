import numpy as np
import pandas as pd

def monte_carlo_simulation(start_price, days, mu, sigma):
    """
    Simula la trayectoria de precios de un activo usando 
    Movimiento Browniano Geométrico.
    
    Parámetros:
    - start_price: Precio inicial
    - days: Días a proyectar
    - mu: Retorno esperado
    - sigma: Volatilidad diaria
    """
    price = np.zeros(days)
    price[0] = start_price
    
    shock = np.zeros(days)
    drift = np.zeros(days)
    
    for x in range(1, days):
        shock[x] = np.random.normal(loc=mu * dt, scale=sigma * np.sqrt(dt))
        drift[x] = mu * dt
        price[x] = price[x-1] + (price[x-1] * (drift[x] + shock[x]))
        
    return price

# Configuración Inicial para Zyllica Risk Model
start_price = 100
days = 365
mu = 0.0002
sigma = 0.01
dt = 1

# Ejecutar Simulación
simulated_path = monte_carlo_simulation(start_price, days, mu, sigma)

print(f"Precio proyectado al día {days}: {simulated_path[days-1]:.2f}")
