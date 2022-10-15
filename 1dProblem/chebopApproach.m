%% Looping
clear; clc;
critPoints = zeros(500, 2); i=1;
epsilon = 1e-5;
ReUp = 5730; ReLow = 5700;
rCount = ReUp - ReLow;
aCount = 10;
maxRealEigval = zeros(1, rCount * aCount); eCount = 1;
for Re = ReLow:ReUp
    rIndex = Re - ReLow;
    for alpha = linspace(0,2,10)
        aIndex = (alpha - 0) / (2/10);
        tic; e = getEigvals(Re, alpha);
        maxRealEigval(eCount) = max(real(e)); eCount = eCount + 1;
        str = sprintf("%d out of %d, %d out of %d finished", rIndex, rCount, aIndex, aCount)
        if abs(max(real(e))) < epsilon
           critPoints(i,1) = Re;
           critPoints(i,2) = alpha;
           i = i+1;
           sprintf("Instability found at (%3f, %3f)!", Re, alpha);
        end
        toc;
    end
end

%% TESTING

Re = 5772.22; alph = 1.02;
tic; e1 = getEigvals(Re, alph);toc;
A = chebop(-1,1);
A.op = @(x,u) (diff(u,4)-2*alph^2*diff(u,2)+alph^4*u)/Re - ...
    2i*alph*u - 1i*alph*(1-x^2)*(diff(u,2)-alph^2*u);
B = chebop(-1,1);
B.op = @(x,u) diff(u,2) - alph^2*u;
A.lbc = [0; 0];
A.rbc = [0; 0];
tic; e2 = eigs(A,B,50,'LR'); toc;

function e = getEigvals(Re, alph)
    A = chebop(-1,1);
    A.op = @(x,u) (diff(u,4)-2*alph^2*diff(u,2)+alph^4*u)/Re - ...
        2i*alph*u - 1i*alph*(1-x^2)*(diff(u,2)-alph^2*u);
    B = chebop(-1,1);
    B.op = @(x,u) diff(u,2) - alph^2*u;
    A.lbc = [0; 0];
    A.rbc = [0; 0];
    e = eigs(A,B,50,'LR');
end