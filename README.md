# EnsightPostProcess #

Simple repository to post-process Ensight files using VTK and Python. This repository can be used to write similar ones for other statistics.

## Summary of set up ##

The different statistics are defined in `statistics.py`. The input parameters are provided in `input.py`. The main file used for running is `process.py`. One can run the program using 
```
python process.py input.py
```

## Examples ##

The program currently computes domain-averaged and periodic-direction(s)-averaged statistics. As an example, the output for the periodic-directions-averaged mass fraction in the channel is shown below.

![Example-Figure](https://image.ibb.co/cq2ipJ/Yf.png)

## Who do I talk to? ##

* Repo owner or admin : [Pavan Bharadwaj](https://github.com/gpavanb)
* Other community or team contact : The code was developed at Stanford University as part of the Center for Turbulence Research Summer Program 2018. Please direct any queries to [Pavan Bharadwaj](mailto:gpavanb@gmail.com)
