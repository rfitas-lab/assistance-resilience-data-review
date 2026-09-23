"""Independent numerical checks for the corrected scientific estimator."""
import sys
from pathlib import Path
import unittest
import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from meta_analysis import reml_hk, DATA

class REMLChecks(unittest.TestCase):
    def test_equal_sampling_variances(self):
        # Exact REML solution: sample variance minus known sampling variance.
        y=np.array([-1.,0.,1.,2.]); se=np.full(4,.2)
        result=reml_hk(y,se)
        self.assertAlmostEqual(result['tau2'],np.var(y,ddof=1)-.04,places=10)
        self.assertAlmostEqual(result['mean'],.5,places=10)

    def test_zero_heterogeneity_boundary(self):
        result=reml_hk([.1,.1,.1],[.2,.3,.4])
        self.assertEqual(result['tau2'],0.)
        self.assertEqual(result['I2'],0.)

    def test_restricted_likelihood_and_historical_delayed_result(self):
        delayed=pd.read_csv(DATA/'delayed_retention_effects.csv')
        architecture=pd.read_csv(DATA/'architecture_effects.csv')
        groups=[delayed]+[g for _,g in architecture.groupby('architecture')]
        groups += [delayed.loc[~delayed.study.str.contains(name)] for name in ['Barcaui','Kreijkes']]
        for frame in groups:
            y=frame.effect.to_numpy(); v=frame.se.to_numpy()**2
            def negative_restricted_loglik(tau):
                w=1/(v+tau); mu=np.average(y,weights=w)
                return .5*(np.log(v+tau).sum()+np.log(w.sum())+(w*(y-mu)**2).sum())
            opt=minimize_scalar(negative_restricted_loglik,bounds=(0,5),method='bounded',options={'xatol':1e-13})
            result=reml_hk(y,np.sqrt(v))
            self.assertAlmostEqual(result['tau2'],opt.x,places=6)
        result=reml_hk(delayed.effect,delayed.se)
        self.assertAlmostEqual(result['mean'],.0304382,places=6)
        self.assertAlmostEqual(result['Q'],46.0480137,places=6)
        self.assertEqual(list(delayed.study),['Contractor & Reyes (2026)','Barcaui (2025)','Kazemitabaar et al. (2023)','Kalam et al. (2025)','Kreijkes et al. (2026)'])

if __name__=='__main__':unittest.main()
