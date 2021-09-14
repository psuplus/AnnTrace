# Reproduce Evaluation Results

This project requires python>=3.7. 

The examples collected by AnnTrace benchmark are under `\examples` folder. Except for the
`__init__.py`, each file contains the examples collected from an
exsiting paper. `general_examples.py` contains the new examples created by us. 

The corresponding examples reported in Table II:
```
A(i)  ....... Declassification[0] (general_examples.py)
A(ii) ....... Declassification[1] (general_examples.py)
B(i)  ....... Erasure[0] (general_examples.py)
B(ii) ....... Erasure[1] (general_examples.py)
C(i)  ....... Revocation[0] (general_examples.py)
C(ii) ....... Revocation[1] (general_examples.py)
(A)   ....... Tricky[1] or Tricky[2] (general_examples.py)
(B)   ....... GradualRelease[1] (gradual_release.py)
```
1. Evaluation result for an example in Table II.
    
    For example, the Figure.A result for Gradual Release, run: 
    ```
    ./main.py -prog Declassification -pol GradualRelease
    ```
    The output looks like:
    ```
    ------------------------------------------------------------------------------------------------------------------------
                      Program              |             Policy     |   PASS  |  Truth  |  Result  |  Failed Traces 
    ------------------------------------------------------------------------------------------------------------------------
                   Declassification [ 0 ]  |        GradualRelease  |    -    |      T  |       T  |  [] 
                   Declassification [ 1 ]  |        GradualRelease  |    -    |      F  |       F  |  [0, 1] 
                   Declassification [ 2 ]  |        GradualRelease  |    -    |      F  |       F  |  [0, 1] 
                   Declassification [ 3 ]  |        GradualRelease  |    -    |      F  |       F  |  [0] 
                   Declassification [ 4 ]  |        GradualRelease  |    -    |      F  |       F  |  [2, 3]    
    ```
    According to the mapping, A(i) is `Declassification [ 0 ]` and  A(ii) is
    `Declassification [ 1 ] `. The result is reported in the `PASS` column,
    where '-' means passed, 'X' for failed and 'N/A' for not applicable.
    

2. Statistics results in Table II
   - For the Existing part:
    
        Temporarily remove `general_examples.py` from the `\example` folder
        since it contains all the new examples, and run the `main.py`:
        ```
        cd $project_home
        mkdir -p not_in_use
        mv examples/general_examples.py not_in_use/
        ./main.py > result_exist.out
        ```
        This takes about a minutes to finish. It runs all programs under `\examples` on all
        policies. The output should look similar to our output file
        `result_exist_demo.out`.
        
        Then run the statistics scripts `stat.sh` on the output file:
        ```
        ./stat.sh result_exist.out
        ```
        
        Remember to move all the examples back:
        
        ```
        mv not_in_use/*.py examples/
        ```
   - For the New part:
  
        Temporarily remove all other examples except `general_examples.py` and `__init__.py`from
        the `\example` folder, and run the main.py:
        ```
        cd $project_home
        mkdir -p not_in_use
        mv examples/*.py not_in_use/
        mv not_in_use/general_examples.py examples/
        mv not_in_use/__init__.py examples/
        ./main.py > result_new.out
        ```
        This takes a few seconds to finish. The output should look similar to our output file
        `result_new_demo.out`.
        
        Then run the statistics scripts `stat.sh` on the output file:
        ```
        ./stat.sh result_new.out
        ```
        Remember to move all the examples back 
        ```
        mv not_in_use/*.py examples/
        ```
