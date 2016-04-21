
__author__      = "Shivam Choudhary"
__uni__         = "sc3973"

"COMS 4180 Network Security Programming Assignment 3"
=====================================================

* Files
        a) ngrams.py The code to generate the ngrams from the input files.
        
        b) 2a.py This file will generate the PING packet and send it. The result
        is summarized in '2b_output.txt' file in the same folder. The file 
        icmp_server.png shows the input that was recieved at the server end.
        I sent a packet TEST as raw payload so its evident that it was recieved 
        at the server end.
        
        c)2b.py This file creates the HTTP GET request.Output is summarized in 
        in.txt. Input is read from inpartb.txt(its a config file).

        d)2c.py This file sends random packets to the source and destination
        defined by command line.
        
* Default Files:
        template.txt: This file is used for generating the reports for the TOP
        20 ngrams as per the given n and slide.

*How to Run?

Method 1:- 
        Type make ngrams. It will run all the given slides as per the question.

Method 2:-
        ngrams(Question 1): python ngrams.py <n> <s> <fname> <outfile>
        where:-
        <n>             : integer n that is length of the ngrams.
        <s>             : integer n that is length of the slide.
        <fname>         : name of the file to analyze.
        <outfile>       : name of the output file.
        
        Eg:
        ngrams          : python ngrams.py 3 3 prog1 prog1_3_1.txt
        


*Time taken on largest size file. 
 Below is the statistics I got when I ran it on prog2 which was 59k.
 python ngrams.py 2 1 prog2 prog2_2_1.txt  0.12s user 0.02s system 91% cpu 0.152 total
