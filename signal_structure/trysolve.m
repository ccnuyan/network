syms emnp1_minus_mn p01 p10 p0 un pd
factor(solve('emnp1_minus_mn=(1-p10)*un*p0/(p01+(1-p01-p10)*un)+p10*un*(1-p0)/(1-p01-(1-p01-p10)*un)-un','emnp1_minus_mn'))

% [ un, un - 1, p01 + p10 - 1, p0 - p01 - un + p01*un + p10*un, -1/(p01*un - un - p01 + p10*un + 1), -1/(p01 + un - p01*un - p10*un)]