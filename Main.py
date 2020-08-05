# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 13:32:33 2020

@author: Dillon Morse
"""



import pandas as pd
import numpy as np
import feature_processing_functions as fp
import labeling_city_functions as lf
import format_data as form
import make_map as mm


# =============================================================================
# Settings
# =============================================================================

min_venues = 15             # Minimum number of features required to keep a
                            #   region in the analysis. Default: 4

primary_city = 'triangle'   # String, 'triangle' or 'denver'. The city used to
                            #   generate the labels and to be compared against.
                            
second_city = 'denver'      # String, 'triangle' or 'denver'. The city for which
                            #   comparisons will be made to the primary city.
                        
num_clusters = 5            # The number of distinct region-types to segment
                            #   the cities in to. Default: 5

num_pca_vars = 135          # Number of features to keep when applying PCA,


# =============================================================================
# Load Data keeping only those regions which are populated with at least 
#   'min_features' number of features.
# =============================================================================

city1_data = fp.fetch_data(primary_city, min_venues)
city2_data = fp.fetch_data( second_city, min_venues)

# =============================================================================
# Combine cities before one-hot-encode to make sure they both reflect all 
# possible venue categories.
# =============================================================================
all_data = ( pd.concat( [city1_data, city2_data] )
               .reset_index(drop = True)
               )

# =============================================================================
# Print some descriptions of the data set
# =============================================================================

fp.describe(all_data, primary_city, second_city)


# =============================================================================
# One-hot-encode
# =============================================================================

city1_encoded, city2_encoded = fp.encode(all_data)


# =============================================================================
# Reduce the number of feeatures using PCA, keeping > 90% of variance
# =============================================================================

city1_reduced = form.apply_pca(city1_encoded, 'The Triangle', num_pca_vars)
city2_reduced = form.apply_pca(city2_encoded, 'Denver',       num_pca_vars)


# =============================================================================
# Normalize the data 
# =============================================================================

city1_scaled, city2_scaled  = form.apply_scaling(city1_reduced, city2_reduced)

# =============================================================================
# Cluster the primary city
# =============================================================================

city1_labeled = lf.cluster(city1_reduced, city2_reduced, num_clusters )
city2_labeled, acc = lf.label_city2(city1_labeled, city2_reduced )

print('\nAccuracy for predictions of primary city labels is {:.3f}.'
      .format(acc)
      )

#print('\nThe best estimator values are: ', esti)

print('\nThe number of regions per label is given by:\n' )
print(lf.count_labels(city1_labeled, city2_labeled, primary_city, second_city))


# =============================================================================
# Make maps
# =============================================================================



city1_map = mm.make_map(city1_labeled, primary_city, num_clusters)
city2_map = mm.make_map(city2_labeled, second_city, num_clusters)



