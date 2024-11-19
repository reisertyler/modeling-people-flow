
import numpy as np
import pandas as pd


####################################################################################
#
#   Class: SparsityCalculator
#
####################################################################################

class SparsityCalculator:
    
    def calculate_sparsity( self, data:pd.DataFrame  )  ->  pd.DataFrame:
        """Calculates the sparsity of the data."""
        
        total_elements  = data.size
        zero_elements   = total_elements - np.count_nonzero(data)
        sparsity        = zero_elements  / float(total_elements)
        
        sparsity_info = pd.DataFrame({'total_elements'   : [    total_elements  ],
                                      'zero_elements'    : [    zero_elements   ],
                                      'sparsity'         : [    sparsity        ]
                                      })
        
        return sparsity_info