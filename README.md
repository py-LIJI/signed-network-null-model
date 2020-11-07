# **Sign Null Model**
&ensp; This project contains null model construction of sign networks and its statistic features. The null model construction of sign networks involve directed & undirected sign networks parts, at the same time, its statistic features include matching coefficient、excess average degree、clustering coefficient、embeddedness and FMF. The whole project is divided three parts, as follow:
***
## Part1: null model construction of undirected sign networks
**sign_null_model_undirected**
* undirected_positive_swap.py  
* undirected_negative_swap.py  
* undirected_separate_swap.py  
* undirected_full_swap.py  
* undirected_sign_swap.py  
* N46edge.txt  
  
**function discription**  
&ensp; This part is null model construction of undirected sign networks. It has five programs and one data file, these programs stand for five different methods of null model construction of undirected sign networks; First: positive-edge randomized null model, Second: negative-edge randomized null model, Third: the positive-edge and negative-edge randomized null model, Forth: full-edge randomized null model, Fifth: sign randomized null model. Special instruction, the last text file is a demo data, you can use it to understand programs. Of course, you also can use your own data to get the result you want.  
  
## Part2: null model construction of directed sign networks  
**sign_null_model_directed**
* directed_positive_swap.py    
* directed_negative_swap.py    
* directed_separate_swap.py    
* directed_full_swap.py    
* directed_sign_swap.py    
* N46edge.txt  

**function discription**    
&ensp; This part is null model construction of directed sign networks. It also has five programs and one data file, these programs stand for five different methods of null model construction of directed sign networks just like the undirected part; First: positive-edge randomized null model, Second: negative-edge randomized null model, Third: the positive-edge and negative-edge randomized null model, Forth: full-edge randomized null model, Fifth: sign randomized null model. Special instruction, the last text file is a demo data, you can use it to understand programs. Of course, you also can use your own data to get the result you want.  

## Part3: statistic features of sign networks  
**statistic_features**  
* matching_coefficient.py  
* excess_average_degree.py  
* clustering_coefficient.py  
* embeddedness.py  
* FMF.py  
* N46edge.txt  

**function discription**  
&ensp; This part is statistic features of sign model, you can use this part describe the difference between the null model and the real networks, and discover the extraordinary characteristics of real networks. These statistic features are matching coefficient、excess average degree、clustering coefficient、embeddedness and FMF. Special instruction, the last text file is a demo data, you can use it to understand programs. Of course, you also can use your own data to get the result you want.  

***
## environment  
**install software**
* Spyder(or Python 3.8)  

**python package**
* networkx  
* random  
* copy  
* numpy  
* pandas  
* matplotlib















