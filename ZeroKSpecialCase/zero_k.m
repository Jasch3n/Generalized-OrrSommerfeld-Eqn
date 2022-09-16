% assume Psi = -1/(2*pi) * cos(pi * y)
nees = 6;
tau = 1;
gammaDot = 350;
tBar = gammaDot * tau;
l = 0.1;
W = 1; 
lambda = 1;
aBar = 1;

a1 = (lambda * tBar^2) / (1 + tBar^2);
a2 = (lambda * tBar^3) / (1 + tBar^2);
% B = chebop(-1/2, 1/2);
% B.op = @(y, Psi, Qxx, Qxy)[0 * Psi; Qxx; Qxy];
% 
% A = chebop(-1/2, 1/2);
% A.op = @(y, Qxx, Qxy) [
%     Qxx/tau - (l/W)^2*diff(Qxx,2)/tau - (tBar/tau)*Qxy...
%     - (lambda*tBar^2)/(tau*(1+tBar^2)) * (pi/(2*tau))*cos(pi*y);
% 
%     Qxy/tau  - (l/W)^2*diff(Qxy,2)/tau - (tBar/tau)*Qxx...
%     - (lambda*tBar^3)/(tau*(1+tBar^2))*(pi/(2*tau))*cos(pi*y)];
%    
% A.lbc = @(Qxx, Qxy) [diff(Qxx); diff(Qxy)];
% A.rbc = @(Qxx, Qxy) [diff(Qxx); diff(Qxy)];

L = chebop(-1/2, 1/2);

L.op = @(y, Psi, Qxx, Qxy) [
    diff(Psi,4) - aBar*diff(Qxy,2);
    Qxx/tau - tBar*Qxy/tau - a1*diff(Psi,2)/tau;
    Qxy/tau + a2*diff(Psi,2)/tau - lambda*tBar*diff(Psi,2)/tau + tBar*Qxx/tau;
];

L.lbc = @(Psi, Qxx, Qxy) [Qxx-1; Psi; diff(Psi)+1/2; Qxy+1];
L.rbc = @(Psi, Qxx, Qxy) [Qxx-1; Psi; diff(Psi)-1/2; Qxy+1];

tic; [eigfcns, D] = eigs(L, 6); toc;
