import numpy as np
from scipy.linalg import eig
import numpy as np
from cheb import cheb
import matplotlib.pyplot as plt

"""
	3D implementation with gammadot AND kz set to 0.
"""

##------------------------------------
def spectrum(kz,a,_ell_over_W_squared=0.01, M=50):
	"""Takes in a set of parameters and returns the spectrum that 
	corresponds to these parameter values. The spectrum is calculated at 
	zero shear in a three dimensional system, with y being the wall-normal
	coordinate

	Args:
		kx (float): perturbation wavenumber
		a (float): activity

	Returns:
		list[complx numbers]: a (cleaned of any infinities) list of eigenvalues
	"""
	# M is the resolution

	# parameters
	eta = 1.0
	tau = 1.0

	##------------------------------------

	II = np.identity(M,dtype='d')

	# Build Chebyshev differentiation matrix and the grid points on [-1, 1]
	D1, ygl = cheb(M)
	D2 = np.dot(D1,D1)
	D3 = np.dot(D2,D1)
	D4 = np.dot(D3,D1)
	SPEC_OP2 = (1 + _ell_over_W_squared*(kz**2))*II - _ell_over_W_squared*D2 

	# Variable layout
	# psi[0:M] Qxx[M:2*M] Qxy[2*M:3*M] 
	RVx  = slice(0*M,1*M)
	RVy = slice(1*M, 2*M)
	RVz = slice(2*M, 3*M)
	RQxx  = slice(3*M,4*M)
	RQxy  = slice(4*M,5*M)
	RQxz = slice(5*M, 6*M)
	RQyz = slice(6*M, 7*M)
	RQzz = slice(7*M, 8*M)

	LHS = np.zeros((8*M,8*M),dtype='D')

    # V1 equation
	LHS[RVx, RVy] = -1j*kz**3*eta*II - 1j*eta/kz*D4 + 2j*kz*eta*D2
	LHS[RVx, RQxx] = 1j*a*kz*tau*D1 
	LHS[RVx, RQyz] = a*tau*D2 + a*kz**2*tau*II
	LHS[RVx, RQzz] = 2j*a*kz*tau*D1 

	# V2 equation
	LHS[RVy, RVx] = 1j*kz**3*eta*II - 1j*kz*eta*D2
	LHS[RVy, RQxz] = a*(kz**2)*tau*II
	LHS[RVy, RQxy] = -1j*a*kz*tau*D1

	# V3 equation
	LHS[RVz,RVx] = -(kz**2)*eta*D1 + eta*D3
	LHS[RVz,RQxy] = -a*tau*D2
	LHS[RVz,RQxz] = -1j*a*kz*tau*D1

	## Qxx equation
	LHS[RQxx,RQxx] = SPEC_OP2

	## Qxy equation
	LHS[RQxy,RQxy] = SPEC_OP2
	LHS[RQxy,RVx] = -D1

	## Qxz equation
	LHS[RQxz, RQxz] = SPEC_OP2 
	LHS[RQxz, RVx] = -1j*kz*II 

	## Qyz equation
	LHS[RQyz, RQyz] = SPEC_OP2
	LHS[RQyz, RVy] = -1j*kz*II - 1j*D2/kz
	
	## Qzz equation. 
	LHS[RQzz, RQzz] = SPEC_OP2
	LHS[RQzz, RVy] = 2*D1
	

	RHS = np.zeros((8*M,8*M),dtype='D')
	RHS[RQxx,RQxx] = -tau*II
	RHS[RQxy,RQxy] = -tau*II
	RHS[RQxz,RQxz] = -tau*II
	RHS[RQyz,RQyz] = -tau*II
	RHS[RQzz,RQzz] = -tau*II 

	## Boundary conditions

    # Vx vanishes at boundary
	LHS[0,:]     = np.zeros(8*M,dtype='D')
	LHS[M-1,:]   = np.zeros(8*M,dtype='D')
	LHS[0,0]      = 1.0
	LHS[M-1,M-1]  = 1.0

	LHS[M,:]     = np.zeros(8*M,dtype='D') # Vy vanishes at boundary
	LHS[2*M-1,:] = np.zeros(8*M,dtype='D')
	LHS[M,M]     = 1.0
	LHS[2*M-1,2*M-1] = 1.0

	LHS[2*M,:]   = np.zeros(8*M,dtype='D') # Vz vanishes at the boundary
	LHS[3*M-1,:] = np.zeros(8*M,dtype='D')
	LHS[2*M,2*M] = 1.0
	LHS[3*M-1,3*M-1] = 1.0
	
	# LHS[3*M,:] = np.zeros(8*M,dtype='D') # dy(Qxx) vanishes 
	# LHS[4*M-1,:] = np.zeros(8*M,dtype='D')
	# LHS[3*M, RQxx] = D1[0]
	# LHS[4*M-1, RQxx] = D1[M-1]
	
	# LHS[4*M,:] = np.zeros(8*M, dtype='D') # dy(Qxy) vanishes at the boundary
	# LHS[5*M-1,:] = np.zeros(8*M, dtype='D')
	# LHS[4*M, RQxy] = D1[0]
	# LHS[5*M-1, RQxy] = D1[M-1]
    
	# LHS[5*M,:] = np.zeros(8*M, dtype='D') # dy(Qxz) vanishes at the boundary
	# LHS[6*M-1,:] = np.zeros(8*M,dtype='D')
	# LHS[5*M,RQxz] = D1[0]
	# LHS[6*M-1,RQxz] = D1[M-1]
	
	# LHS[6*M,:] = np.zeros(8*M,dtype='D') # dy(Qyz) vanishes
	# LHS[7*M-1,:] = np.zeros(8*M,dtype='D')
	# LHS[6*M,RQyz] = D1[0]
	# LHS[7*M-1,RQyz] = D1[M-1]
	
	LHS[7*M,:] = np.zeros(8*M, dtype='D') # dy(Qzz) vanishes 
	LHS[8*M-1,:] = np.zeros(8*M, dtype='D')
	LHS[7*M,RQzz] = D1[0]
	LHS[8*M-1,RQzz] = D1[M-1]

	RHS[0,:]     = np.zeros(8*M,dtype='D')
	RHS[M-1,:]   = np.zeros(8*M,dtype='D')
	RHS[M,:]     = np.zeros(8*M,dtype='D')
	RHS[2*M-1,:] = np.zeros(8*M,dtype='D')
	RHS[2*M,:]   = np.zeros(8*M,dtype='D')
	RHS[3*M-1,:] = np.zeros(8*M,dtype='D')
	RHS[3*M,:]   = np.zeros(8*M,dtype='D')
	RHS[4*M-1,:] = np.zeros(8*M,dtype='D')
	RHS[4*M,:]   = np.zeros(8*M,dtype='D')
	RHS[5*M-1,:] = np.zeros(8*M,dtype='D')
	RHS[5*M,:]   = np.zeros(8*M,dtype='D')
	RHS[6*M-1,:] = np.zeros(8*M,dtype='D')
	RHS[6*M,:]   = np.zeros(8*M,dtype='D')
	RHS[7*M-1,:] = np.zeros(8*M,dtype='D')
	RHS[7*M,:]   = np.zeros(8*M,dtype='D')
	RHS[8*M-1,:] = np.zeros(8*M,dtype='D')
	
	print("Spectral Operator Matrix Condition Num:", np.linalg.cond(LHS))
	_spec = eig(LHS,RHS,left=0,right=1)

	_eig_list = _spec[0]
	finite_idx = np.where(np.isfinite(_eig_list))[0]
	_modes_list = _spec[1]

	# clean the eigenvalue list of all infinities
	clean_eig_list = _eig_list[finite_idx]
	clean_modes_list = _modes_list[:,finite_idx]
	
	return (clean_eig_list, clean_modes_list)