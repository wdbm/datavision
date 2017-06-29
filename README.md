# datavision

Python data visualisation

# setup

```Bash
sudo pip install datavision
```

# qunti and zus lists

Qunti (群体, groups) are lists that act

- as dictionaries that can contain duplicate keys and
- as sets for the purposes of enabling set-like operations for qunti objects, such as symmetric difference, intersection and update operations.

Qunti are composed of multiple zu (组, group) objects.

## qunti operations

In an update operation, one qunti is used to update another. Any zus in the updating qunti that are not in the updated qunti are appended to the updated qunti. Any zus that are in the updating qunti and the updated qunti replace the corresponding zus in the updated qunti.

The following example illustrates a qunti update operation in which an `alpha` zus is replaced and a `delta` zus is appended:

```Python
# example qunti update:
a = [['alpha', '10'], ['beta', '20'], ['gamma', '30'], ['gamma', '15']]
b = [['delta', '40'], ['alpha', '50']]
# update of a with b:
a = [['beta', '20'], ['gamma', '30'], ['gamma', '15'], ['delta', '40'], ['alpha', '50']]
```

The following example illustrates qunti symmetric difference, intersection and update operations. In the update operation, two old `gamma` zus are replaced by a single new `gamma` zu:

```Python
# example qunti symmetric difference, intersection and update:
a = [['alpha', '10'], ['beta', '20'], ['gamma', '30'], ['gamma', '15']]
b = [['delta', '40'], ['alpha', '50'], ['gamma', '25']]
# symmetric difference of a and b:
[['beta', '20'], ['delta', '40']]
# intersection of a and b:
[['alpha', '10'], ['gamma', '30'], ['gamma', '15'], ['alpha', '50'], ['gamma', '25']]
# update of a with b:
a = [['beta', '20'], ['delta', '40'], ['alpha', '50'], ['gamma', '25']]
```

# data visualisation

Datavision provides utilities for data visualisation.

## matrices as colormaps

![](https://raw.githubusercontent.com/wdbm/datavision/master/media/image_1.png)
![](https://raw.githubusercontent.com/wdbm/datavision/master/media/image_2.png)
![](https://raw.githubusercontent.com/wdbm/datavision/master/media/image_3.png)

## histograms

![](https://raw.githubusercontent.com/wdbm/datavision/master/media/histogram_comparison_1.png)

## terminal graphs and histograms

```
   │                                                                            
   ┼+79.548                                                                 ○   
   │                                                                            
   │                                                                ○           
   │                                                                            
   │                                                        ○                   
   │                                                                            
   │                                                ○                           
   ◽       ◽       ◽                       ○                                    
   │                       ◽       ○                                            
   │                       ○       ◽                                            
───○┼──────○───────○───────────────────────◽────────────────────────────────┼───
   │ +0.046                                         ◽               +8.97638    
   │                                                                            
   │                                                        ◽                   
   │                                                                            
   │                                                                ◽           
   ┼-48.228                                                                     
   │                                                                        ◽   
   │                                                                            
```

```
                         │                        
                         ┼+75503.2                
                       ∘∘|∘                       
                      ∘||||∘                      
                      ||||||∘                     
                     ∘|||||||                     
                     ||||||||∘                    
                    ∘|||||||||                    
                    ||||||||||∘                   
                   ∘|||||||||||                   
                   |||||||||||∘                   
                  ∘||||||||||||                   
                  |||||||||||||∘                  
                  ||||||||||||||∘                 
                 ∘|||||||||||||||∘                
                ∘|||||||||||||||||∘               
               ∘|||||||||||||||||||∘              
            ∘∘∘||||||||||┼+1603.2|||∘∘∘           
──┼--------------------------------------------┼──
   -4.69099              │              +4.6147   
```

```Bash
echo "0,  1,  4,  9, 16, 25, 36, 49, 64, 81" | datavision_TTY_plot.py
```

## combinations of variables

![](https://raw.githubusercontent.com/wdbm/datavision/master/media/variable_correlations_1.png)

## parallel coordinates

![](https://raw.githubusercontent.com/wdbm/datavision/master/media/parallel_coordinates_1.png)

## FFT

![](https://raw.githubusercontent.com/wdbm/datavision/master/media/FFT.png)

## time graphs

![](https://raw.githubusercontent.com/wdbm/datavision/master/media/time_1.png)

## Bollinger bands

![](https://raw.githubusercontent.com/wdbm/datavision/master/media/Bollinger_bands_1.png)

![](https://raw.githubusercontent.com/wdbm/datavision/master/media/Bollinger_bands_2.png)

## graphs

![](https://raw.githubusercontent.com/wdbm/datavision/master/media/graph.png)
![](https://raw.githubusercontent.com/wdbm/datavision/master/media/multigraph.png)
![](https://raw.githubusercontent.com/wdbm/datavision/master/media/multigraph_2D.png)
![](https://raw.githubusercontent.com/wdbm/datavision/master/media/multigraph_2D_date.png)
![](https://raw.githubusercontent.com/wdbm/datavision/master/media/multigraph_2D_time.png)

# databases

Datavision features some scripts for interacting with databases:

- `change_field_name_database_SQLite.py`
- `duplicates_database_SQLite.py`
- `view_database_SQLite.py`
