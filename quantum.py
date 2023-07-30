import numpy as np
import scipy.constants as const
import matplotlib.pyplot as plt

a0 = const.value('Bohr radius')

def V(r):
    """
    H 原子的势能函数
    """
    return -const.elementary_charge ** 2 / (4 * np.pi * const.epsilon_0 * r)

def solve_radial_Schrodinger_eqn(r, l, E):
    """
    Solve the radial Schrodinger equation for hydrogen atom.

    Args:
    r: numpy 1D array, the radial grid
    l: int, the orbital angular momentum quantum number
    E: float, the energy eigenvalue

    Returns:
    R: numpy 1D array, the radial wave function
    """
    m_e = const.electron_mass
    hbar = const.hbar

    dr = r[1] - r[0]
    N = len(r)

    # Define the matrix A
    A = np.zeros((N, N))
    A[0, 0] = 1
    A[-1, -1] = 1
    for i in range(1, N - 1):
        A[i, i - 1] = -1 / (dr ** 2) - l * (l + 1) / (2 * m_e * r[i] ** 2) + 2 * m_e * (V(r[i]) - E) / (hbar ** 2)
        A[i, i] = 2 / (dr ** 2) + l * (l + 1) / (2 * m_e * r[i] ** 2) - 2 * m_e * (V(r[i]) - E) / (hbar ** 2)
        A[i, i + 1] = -1 / (dr ** 2)

    # Find the eigenvalues and eigenvectors of A
    eigenvalues, eigenvectors = np.linalg.eig(A)

    # Sort the eigenvalues and eigenvectors in ascending order
    idx = eigenvalues.argsort()
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # Extract the ground state radial wave function
    R = eigenvectors[:, 0]
    R /= np.sqrt(np.trapz(R ** 2 * r ** 2, r))

    return R

def solve_angular_Schrodinger_eqn(theta, l, ml):
    """
    Solve the angular Schrodinger equation for hydrogen atom.

    Args:
    theta: numpy 1D array, the angular grid
    l: int, the orbital angular momentum quantum number
    ml: int, the magnetic quantum number

    Returns:
    Y: numpy 1D array, the angular wave function
    """
    dtheta = theta[1] - theta[0]
    N = len(theta)

    # Define the matrix A
    A = np.zeros((N, N))
    A[0, 0] = 1
    A[-1, -1] = 1
    for i in range(1, N - 1):
        A[i, i - 1] = 1 / (dtheta ** 2) - np.cos(theta[i]) / (2 * dtheta * np.sin(theta[i]))
        A[i, i] = -2 / (dtheta ** 2) + l * (l + 1) / (np.sin(theta[i]) ** 2)
        A[i, i + 1] = 1 / (dtheta ** 2) + np.cos(theta[i]) / (2 * dtheta * np.sin(theta[i]))

    # Find the eigenvalues and eigenvectors of A
    eigenvalues, eigenvectors = np.linalg.eig(A)

    # Sort the eigenvalues and eigenvectors in ascending order
    idx = eigenvalues.argsort()
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # Extract the angular wave function
    Y = eigenvectors[:, ml + l]

    return Y

def solve_H_atom_wavefunction(n, l, m):
    """
    Solve the Schrodinger equation for hydrogen atom.

    Args:
    n: int, the principal quantum number
    l: int, the orbital angular momentum quantum number
    m: int, the magnetic quantum number

    Returns:
    r: numpy 1D array, the radial grid
    theta: numpy 1D array, the angular grid
    phi: numpy 1D array, the azimuthal grid
    R: numpy 1D array, the radial wave function
    Y: numpy 1D array, the angular wave function
    psi: numpy 3D array, the wave function
    """
    # Set up the grid
    r_max = 100 * a0
    dr = a0 / 20
    r = np.arange(0, r_max + dr, dr)

    theta_max = np.pi
    dtheta = np.pi / 20
    theta = np.arange(0, theta_max + dtheta, dtheta)

    phi_max = 2 * np.pi
    dphi = np.pi / 20
    phi = np.arange(0, phi_max + dphi, dphi)

    # Solve the radial Schrodinger equation
    E = -const.Rydberg * (1 / n ** 2)
    R = solve_radial_Schrodinger_eqn(r, l, E)

    # Solve the angular Schrodinger equation
    Y = solve_angular_Schrodinger_eqn(theta, l, m)

    # Combine the radial and angular wave functions
    psi = np.zeros((len(r), len(theta), len(phi)))
    for i in range(len(r)):
        for j in range(len(theta)):
            for k in range(len(phi)):
                psi[i, j, k] = R[i] * Y[j] * np.exp(1j * m * phi[k])

    return r, theta, phi, R, Y, psi

# Example usage
n = 1
l = 0
m = 0
r, theta, phi, R, Y, psi = solve_H_atom_wavefunction(n, l, m)

# Plot the wave function
r_mesh, theta_mesh, phi_mesh = np.meshgrid(r, theta, phi, indexing='ij')
x = r_mesh * np.sin(theta_mesh) * np.cos(phi_mesh)
y = r_mesh * np.sin(theta_mesh) * np.sin(phi_mesh)
z = r_mesh * np.cos(theta_mesh)
prob_density = np.real(psi * np.conj(psi))

# Plot the wave function in polar coordinates
fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_rlim(0, r[-1])
ax.set_rticks([0.25, 0.5, 0.75, 1])
ax.set_rlabel_position(135)
levels = np.linspace(0, np.max(prob_density[:, :, 10]), 50)
ax.contourf(theta_mesh[:, :, 0], r_mesh[:, :, 0], prob_density[:, :, 10], levels=levels, cmap='plasma')
plt.show()