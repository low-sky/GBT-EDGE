# GBT-EDGE

This toolkit helps you reducing the GBT EDGE data.
Still very preliminary, expect updates, here
as well as in 3rd party code mentioned here.

Example of use: (pick a directory):

      cd /lma1/teuben/GBT-EDGE                                       # at UMD on lma
      cd /home/astro-util/projects/gbt-edge/GBT-EDGE-pipeline        # at GBO on e.g. fourier
      
      source edge.sh
      ./reduce.py NGC0001
      ./mmaps.py NGC0001
	  
each galaxy takes about 20 mins to reduce, where the observing time was about 60 mins.
The use of the **edge.sh** script is optional in your installation, as long as the needed packages are
installed in *your* python (see Installation below). However, at GBO it is required.

You can push your luck by trying the example maskmoment based **mmaps.py** script which tries a number
of methods to make moment maps.

There are some -h flags to the **reduce.py** script. The gals.pars script controls which sessions contain
which galaxy



# Installation

      git clone https://github.com/teuben/GBT-EDGE

There are short-cuts in the Makefile, but basically you need to 
install the following python packages in your python3 environment:

* **gbtpipe**: https://github.com/GBTSpectroscopy/gbtpipe
* **degas**:   https://github.com/GBTSpectroscopy/degas

Probably better to use the source based "install -e", so you can "git pull" while code updates are being made:

      make git
      (cd gbtpipe; pip install -e .)
      (cd degas;   pip install -e .)
      pip install pyspeckit
	  
It was noted that python > 3.7 was needed, where GBO runs 3.6.8. I've use the lmtoy method to
install a container with anaconda3's python. Also the installation of gbtpipe might need the
bz2 library. On my ubuntu system I needed to install **libbz2-dev** for this to pass the cfitsio
installation that was needed for **gbtpipe**

The Makefile contains a few other targets that may guide you in getting a clean install.

On U22 cfitsio library is now causing a build failure with **gbtpipe**

# Sample Data

Running the calibration off-line is not impossible, but involved, since it needs on-line weather
information. However, using
one of our datasets for [NGC0001](https://www.astro.umd.edu/~teuben/edge/data/NGC0001.tar) can be
used to play with the gridding step, viz.

     make NGC0001
      ./reduce.py -s NGC0001

and skipping the calibration.

# Masking

For baseline fitting it is useful to know where the signal is expected. Using the -M flag you can
place a mask file in **masks/mask_GAL.fits**, which should contain 0's and 1's where we expect signal.
A mask can also be made using the **mk_mask.sh** script (you will need NEMO for this),
documentation is embedded, but here is an
example of use

      ./mk_mask.sh refmap=NGC0776/NGC0776_12CO_rebase3_smooth2_hanning2.fits  \
	               mask=masks/mask_NGC0776.fits  \
	               inc=46 pa=315 vsys=4830 v1=90
      ./reduce.py -M NGC0776
      ./mmaps.py NGC0776

or if you have placed a specific mask file, e.g. masks/mask_NGC0001_Havfield_v1.fits, this would be

      ./reduce.py -m mask_NGC0001_Havfield_v1.fits NGC0776

# Bad Feeds

If there is some indication that some feeds add negatively to the maps, they can be removed at the gridding 
stage, viz.

      ./reduce.py -f 8,11 -M NGC0776

where feeds 8 and 11 (with feed 0 being the first feed) would be removed from gridding. They are still added to
the calibration stage, so one can continue experimenting with pure gridding:

      ./reduce.py -f 11 -s NGC0776
	  
to see what the effect on the final outcome is with just feed 11 removed.

Note we are currently looking into if/why/when feeds 8 and 11 (in the 0-based system), but be aware some users
may use a 1-based system in their language. Internally in the SDFITS files the feeds are numbered 0..15


# Observing

During observing you can edit the **gals.pars** file and add a new galaxy and scan numbers, then
reduce their data and view the resulting fits cube using **ds9** or **carta** for example.

An addition thing which is nice to do is preserving the *tsys* run of the night, as well as
the *astridlogs*.  For example for session 26 this would be:

1. **tsys**:

        ./tsys.py AGBT21B_024_26
        cp pro/AGBT21B_024_26.tsys tsyslogs
        git add tsyslogs/AGBT21B_024_26.tsys
        git commit -m new tsyslogs/AGBT21B_024_26.tsys
        git push

this **tsys.py** script will run IDL scripts,and take a while.

2. **astridlogs**:

        cd astridlogs
        getastridlog AGBT21B_024_26
        git add AGBT21B_024_26_log.txt
        git commit -m new AGBT21B_024_26_log.txt
        git push


      

# Working with selected sessions

GBT data is organized in sessions, usually starting with 1. In case you have many sessions and want to
revisit one particular session, use the -g flag. But remove the galaxy directory, in case other sessions
had calibrated scans lying around (or rename the directory):

      rm -rf  NGC0776
      ./reduce -g 26,27 NGC0776



# Working Offline

To fully work offline, you will need to create symlinks from
**rawdata** and **weather** to copies of the GBT (sdfits) rawdata and
weather information. The
[degas instructions](https://github.com/GBTSpectroscopy/degas/blob/master/README.md#local-installation-of-the-degas-pipeline)
go in more detail, our **Makefile** has some useful targets to aid in
the setup.

## Example

      wget https://www.astro.umd.edu/~teuben/edge/data/AGBT21B_024_01.tar
      wget https://www.astro.umd.edu/~teuben/edge/data/GBTWeather.tar.gz
      mkdir rawdata
      tar -C rawdata -xvf AGBT21B_024_01.tar
      tar zxf GBTWeather.tar.gz
      export GBTWEATHER=`pwd`/GBTWeather
      ./reduce.py NGC0001

the mask file is not here yet.  

## Nod_Galaxy

Example how to look at Tsys and Nod_Galaxy on NGC5908

      offline,'AGBT21B_024_14'
      vanecal,327
      # shows Tsys in range 150-248 (previous RAmap)
      # The NOD has scans 329-334
      vanecal,329
      # shows Tsys in range 184-242 (NOD)
      # fdnum=0..15     4 and 7 are the ones used by us
      argus_onoff,331,332,329,fdnum=4
      argus_onoff,332,331,329,fdnum=4
      argus_onoff,333,334,329,fdnum=4
      argus_onoff,334,333,329,fdnum=4
      # -> tsys=200
      argus_onoff,331,332,329,fdnum=7
      argus_onoff,332,331,329,fdnum=7
      argus_onoff,333,334,329,fdnum=7
      argus_onoff,334,333,329,fdnum=7
      # -> tsys=203

# Caveats/Issues

Some of these issues will be worked on in  the code, and will disappear. See also https://github.com/teuben/GBT-EDGE/issues
Otherwise just be aware of the listed ones here:

1. Although the **-s** can be handy, re-running the **reduce.py** script can be dangerous, as any 
   corrupt files that are in the galaxy working directory, will we wildcarded and taking into the gridding
   step.   In case of doubt, remove the directory before starting a fresh new run.   This also implies you 
   cannot make a differ RA and DEC map without removing all files and perhaps renaming. If you want to make
   separate RA and DEC maps, the gals.pars file will need to have commented out the other map, and the
   
	     edit gals.pars
		 rm -rf NGC0001
         ./reduce.py NGC0001 ;  mv NGC0001 NGC0001_RA
	     edit gals.pars
         ./reduce.py NGC0001 ;  mv NGC0001 NGC0001_DEC
		 
2. Because of the randomized sampler in the PCA methods (i.e., the svd_solver option
   here https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html) the results are not reproducable
   on a few mK level.  The solver is high efficiency but can lead to different outcomes.
   
   np.random.seed(123)  doesn't seem to work.

3. A few notes on CPU times: the **-s** flags makes the code run about 2x faster, but always inspect if the galaxy directory
   has the feed files that you expect! Using the weather information make the code
   run maybe 5% slower, not a huge effect. On fourier NGC0001 took about 10 mins, on my i5-1135G7 laptop 4 mins.
   On LMA bruteforce3 took 6:39

4. nProc (see code) doesn't seem to work for me.   Setting OMP_NUM_THREADS=1 actually seems to make the code run a bit faster.

5. For NGC0001 here are some RMS values:

         (2,2)   nomask: 12.6      mask:  8.9mK  ratio 1.4
         (1.3,1) nomask: 33.5      mask: 27.4mK  ratio 1.2
	 
   Going from (1.3,1) -> (2,2) S/N improved by about 3.

6. (in code) it would be useful if buildmasks() could return the mask filename, that we carry it all through

7. The percentage of flagged scans is very low when using a mask, and
   this can be expected as flagging occurs when (1) RMS being too
   high, (2) there being evidence of a large scale ripple in the
   spectrum or (3) there being a big spike in the data.  The mask
   causes the analysis to not check those conditions in the region
   associated with the galaxy.
   
8. The use of the maskfile in griddata() and postprocess.cleansplit() seems not used. This makes the -s useful
   to experiment with the -f flag to remove feeds from the gridding stage.

9. A script "rerun_parallel" has been prepared to allow simple reruns, in particular if you can run them
   in parallel on a bigger machine:

        OMP_NUM_THREADS=1 /usr/bin/time parallel --jobs 16 < rerun_parallel

   this took XX minutes on the "lma" machine for 49 galaxies. Note this assumes the calibration has been run once.=
   so the "-s" flag can be optimally used.
   TBD:    bad beams cannot be edited out without removing the offending feed fits file!
   

10. The first 25 sessions were taken with 1.5 x 1.5 arcmin maps and ~33sec integration time per scan.

    Then came session 26, where we experimented with a 1.5x bigger map (in the scan direction only), and
    ~89s integration, which is really too long.

    In session 27 we then changed to 51s (???, or is that the plan)

# Important Files and Directories

       GBTEDGE.cat   - this should also be in  /home/astro-util/projects/gbt-edge/GBTEDGE.cat 
       night1.py     - a bruteforce example script for Night 1 (Nov 5/6, 2021)
       reduce.py     - reduce one (or more) galaxies, based on parameters in gals.pars
       gals.pars     - galaxy parameter file for reduce.py containing the seq/scans 
       masks/        - here you need to place the mask_GAL.fits file (or symlink) for the -M flag
       rawdata/      - (symlink to) where the rawdata are stored
       weather/      - (symlink to) where the GBT Weather data are stored (with Coeff*.txt files)
       astridlogs/   - keeps the astrid logs created with "getastridlog"
       tsyslogs/     - keeps the tsys logs created with ./tsys.py

and specific to being at GBT:

       /home/sdfits/AGBT21B_024_01/ - night1 VEGAS raw data directory @ GBO  (1.3GB)
                                      this should be rawdata/AGBT21B_024_01 for a local install
