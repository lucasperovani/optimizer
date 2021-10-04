from scipy.special import lambertw
from scipy.optimize import fsolve
from scipy import exp
import numpy as np
from scipy.integrate import quad

# ================================Equations=====================================

# Calculates and returns vs
# input = vs
# aux = [vd, k, ICo, IB, IBo, T, n, alpha_u]
def vs_Equation (input, aux):
    # Variables assign

    vd      = aux[0]
    k       = aux[1]
    ICo     = aux[2]
    IB      = aux[3]
    IBo     = aux[4]
    T       = aux[5]
    n       = aux[6]
    alpha_u = aux[7]

    # Some specific calculations

    To      = 300
    phiTo   = 0.026


    Tx      = T + 273

    phiT    = phiTo * (Tx / To)


    IC      = (IB / IBo) * ICo * ((Tx / To) ** (-2 - alpha_u))

    # vs equation dependent on temperature
    out = -IB*((1-k)*lambertw(2*exp((2*input+vd)/(2*n*phiT)))**2+(-2*k+2)*lambertw(2*exp((2*input+vd)/(2*n*phiT)))+(lambertw(2*exp(-(-2*input+vd)/(2*n*phiT)))**2)*k+2*(lambertw(2*exp(-(-2*input+vd)/(2*n*phiT))))*k-4*IC)/(4*IC)
    return out[0]


# Calculates and returns gm
# input = gm
# aux = [vs, vd, k, ICo, IB, IBo, T, n, alpha_u]
def gm_Equation (input, aux):
    # Variables assign

    vs      = aux[0]
    vd      = aux[1]
    k       = aux[2]
    ICo     = aux[3]
    IB      = aux[4]
    IBo     = aux[5]
    T       = aux[6]
    n       = aux[7]
    alpha_u = aux[8]

    # Some specific calculations

    To      = 300
    phiTo   = 0.026


    Tx      = T + 273

    phiT    = phiTo * (Tx / To)


    IC      = (IB / IBo) * ICo * ((Tx / To) ** (-2 - alpha_u))


    # gm equation dependent on temperature
    out = -(IB*lambertw(2*exp(-(-2*vs+vd)/(2*n*phiT)))*k*lambertw(2*exp((2*vs+vd)/(2*n*phiT)))*(-1+k))/(2*n*phiT*IC*((1-k)*lambertw(2*exp((2*vs+vd)/(2*n*phiT)))+lambertw(2*exp(-(-2*vs+vd)/(2*n*phiT)))*k)) - input
    return out[0]


# Calculates and returns i0
# input = i0
# aux = [vs, vd, k, ICo, IB, IBo, T, n, alpha_u]
def io_Equation (input, aux):
    # Variables assign

    vs      = aux[0]
    vd      = aux[1]
    k       = aux[2]
    ICo     = aux[3]
    IB      = aux[4]
    IBo     = aux[5]
    T       = aux[6]
    n       = aux[7]
    alpha_u = aux[8]

    # Some specific calculations

    To      = 300
    phiTo   = 0.026


    Tx      = T + 273

    phiT    = phiTo * (Tx / To)


    IC      = (IB / IBo) * ICo * ((Tx / To) ** (-2 - alpha_u))


    # io equation dependent on temperature
    out = (-IB*lambertw(2*exp(-(-2*vs+vd)/(2*n*phiT)))**2*k-2*IB*lambertw(2*exp(-(-2*vs+vd)/(2*n*phiT)))*k+4*IC*(IB*k-input))/(4*IC)
    return out[0]


# Returns vs based on vd
def vs_point (vd, k, ICo, IB, IBo, T, n, alpha_u):
    vs = fsolve (vs_Equation, 0, [vd, k, ICo, IB, IBo, T, n, alpha_u])
    return vs


# Returns gm based on vd
def gm_point(vd, k, ICo, IB, IBo, T, n, alpha_u):
    To=300
    phi_T=0.026*((T+273)/To)
    IC=ICo*IB/IBo*((T+273)/To)**(-2-alpha_u)
    erro=1e-10
    kmin=1e-6
    k=np.clip(k,kmin,1-kmin)
    Iop=1-k
    Ion=-k
    IC=ICo
    Imax=Iop
    Imin=Ion
    if abs(vd) <= erro:
        Io=0        
    if abs(vd) > erro:
        custo=erro        
        while abs(custo) >= erro:
            Io=(Imax+Imin)/2
            if (abs(Io-Imin) <= erro) or (abs(Io-Imax) <= erro):
                custo=0
            else:
                custo = (np.sqrt(1+4*IC*(1+Io/k))-np.sqrt(1+4*IC*(1-Io/(1-k)))+np.log((np.sqrt(1+4*IC*(1+Io/k))-1)/(np.sqrt(1+4*IC*(1-Io/(1-k)))-1))-vd/n/phi_T)
                if (custo > 0):
                    Imax=Io
                elif (custo < 0):
                    Imin=Io
    Gm=-k*(np.sqrt(((4*Io+4*k)*IC+k)/k)-1)*(-1+k)*(np.sqrt(((4*Io+4*k-4)*IC-1+k)/(-1+k))-1)/(2*n*phi_T*((1-k)*np.sqrt(((4*Io+4*k-4)*IC-1+k)/(-1+k))+k*np.sqrt(((4*Io+4*k)*IC+k)/k)-1)*IC)
    return Gm*IB


# Returns i0 based on vd
def io_point(vd, k, ICo, IB, IBo, T, n, alpha_u):
    To=300
    phi_T=0.026*((T+273)/To)
    IC=ICo*IB/IBo*((T+273)/To)**(-2-alpha_u)
    erro=1e-11
    kmin=1e-6
    k=np.clip(k,kmin,1-kmin)
    Iop=1-k
    Ion=-k
    IC=ICo
    Imax=Iop
    Imin=Ion
    if abs(vd) <= erro:
        Io=0        
    if abs(vd) > erro:
        custo=erro        
        while abs(custo) >= erro:
            Io=(Imax+Imin)/2
            if (abs(Io-Imin) <= erro) or (abs(Io-Imax) <= erro):
                custo=0
            else:
                custo = (np.sqrt(1+4*IC*(1+Io/k))-np.sqrt(1+4*IC*(1-Io/(1-k)))+np.log((np.sqrt(1+4*IC*(1+Io/k))-1)/(np.sqrt(1+4*IC*(1-Io/(1-k)))-1))-vd/n/phi_T)
                if (custo > 0):
                    Imax=Io
                elif (custo < 0):
                    Imin=Io
    return Io*IB


# Returns the total vsd
def vsd (vd, k, ICo, IB, IBo, T, n, alpha_u, eta):
    vsa = vs_point (vd, k, ICo, IB, IBo, T, n, alpha_u)
    vsb = vs_point (vd, 0.5, ICo, IB, IBo, T, n, alpha_u)
    vsc = vs_point (vd, (1-k), ICo, IB, IBo, T, n, alpha_u)
    return vsa + eta*vsb + vsc


# Returns the total gmd
def gmd (vd, k, ICo, IB, IBo, T, n, alpha_u, eta):
    gma = gm_point (vd, k, ICo, IB, IBo, T, n, alpha_u)
    gmb = gm_point (vd, 0.5, ICo, IB, IBo, T, n, alpha_u)
    gmc = gm_point (vd, (1-k), ICo, IB, IBo, T, n, alpha_u)
    return gma + eta*gmb + gmc


# Returns the total iod
def iod (vd, k, ICo, IB, IBo, T, n, alpha_u, eta):
    ioa = io_point (vd, k, ICo, IB, IBo, T, n, alpha_u)
    iob = io_point (vd, 0.5, ICo, IB, IBo, T, n, alpha_u)
    ioc = io_point (vd, (1-k), ICo, IB, IBo, T, n, alpha_u)
    return ioa + eta*iob + ioc


# Returns a list with all vs for plotting
def vs_plot (vd, k, ICo, IB, IBo, T, n, alpha_u, eta):
    vs = np.array([])
    for x in vd:
        vs = np.append (vs, vsd (x, k, ICo, IB, IBo, T, n, alpha_u, eta))
    return vs


# Returns a list with all gm for plotting
def gm_plot (vd, k, ICo, IB, IBo, T, n, alpha_u, eta):
    gm = np.array([])
    for x in vd:
        gm = np.append (gm, gmd(x, k, ICo, IB, IBo, T, n, alpha_u, eta))
    return gm


# Returns a list with all i0 for plotting
def io_plot (vd, k, ICo, IB, IBo, T, n, alpha_u, eta):
    io = np.array([])
    for x in vd:
        io = np.append (io, iod(x, k, ICo, IB, IBo, T, n, alpha_u, eta))
    return io

# Returns the THD in %
def thd (Vmax, k, ICo, IB, IBo, T, n, alpha_u, eta):

    def io (t):
        vd = Vmax * np.cos(2 * np.pi * t)
        return iod (vd, k, ICo, IB, IBo, T, n, alpha_u, eta) * np.cos(2 * np.pi * t)

    def pio (t):
        vd = Vmax * np.cos(2 * np.pi * t)
        return iod (vd, k, ICo, IB, IBo, T, n, alpha_u, eta) ** 2

    aux      = quad (io, -0.5, 0.5)
    I1       = 2 * aux[0]
    Ptotal  = quad (pio, -0.5, 0.5)

    return np.sqrt ((2 * Ptotal[0])/(I1 ** 2) - 1) * 100


# Returns a list with all thd for plotting
def thd_plot (Vdinterval, k, ICo, IB, IBo, T, n, alpha_u, eta):

    points = np.array([])

    # Calculates the THD from Vmin to Vmax using 100 points
    for x in Vdinterval:
        points = np.append (points, thd (x, k, ICo, IB, IBo, T, n, alpha_u, eta))

    return points
