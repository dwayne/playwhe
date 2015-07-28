**What is this?**

A Python API and script for the retrieval and storage of Play Whe results from the [National Lotteries Control Board](http://www.nlcb.co.tt/) (NLCB) website.

**Why was this written?**

*Short answer:*

> Because it can be written.

*Slightly longer answer:*

> Because I was looking for a small Python project to work on for practice.

**Which version do I have?**

Version 0.6.

After installing the package you can also check the version number by issuing
the following command at a shell prompt.

    $ playwhe.py --version

**What has changed from version 0.5 to 0.6?**

On July 6th, 2015 the [NLCB](http://www.nlcb.co.tt/) started drawing Play Whe
4 times per day. The script was changed to correctly scrape the 4:00 PM draw.

Also, previously the `period` stored with the results was changed from a
numeric format `(1, 2, 3)` to a string format `('EM', 'AM', 'AN', 'PM')`.

**What has changed from version 0.4 to 0.5?**

Around February 21st, 2015 the [NLCB](http://www.nlcb.co.tt/) took down their
website to redesign and rebuild it. They changed the service URL along with the
format of the HTML results. This required an update to the parser to ensure that
the results could still be retrieved in the future.

**What has changed from version 0.3 to 0.4?**

On November 21st, 2011 the [NLCB](http://www.nlcb.co.tt/) started drawing
Play Whe 3 times per day. Due to this change the display format of the results
retrieved via their website was changed. Since this program simply scrapes the
HTML off their results page, I needed to update the script to work with the new
format.

Hence, the logic for retrieving and storing the Play Whe results have changed.
However, the interface to perform these operations have not.

**How do I install it?**

    $ tar xvzf playwhe-0.6.tar.gz
    $ cd playwhe-0.6
    $ sudo python setup.py install

**What are some of the things it can do?**

You can get Play Whe results directly from [NLCB](http://www.nlcb.co.tt/) using
the playwhe module.

    import playwhe
    p = playwhe.PlayWhe()

    # retrieve and display all the results for the month of April in the year 2011
    print "\n\n".join(map(lambda r: r.prettyprint(), p.results_for_month(2011, 4)))

    # retrieve and display the results for April 2nd, 2011
    print "\n\n".join(map(lambda r: r.prettyprint(), p.results_for_day(2011, 4, 2)))

    # retrieve and display the three most recent results
    print "\n\n".join(map(lambda r: r.prettyprint(), p.results()))

You can get Play Whe results directly from [NLCB](http://www.nlcb.co.tt/) using
the playwhe.py script.

    $ echo Retrieve and display the results for the month of April in the year 2011
    $ playwhe.py --pretty-print --date=2011-04
    $ playwhe.py -p -d 2011-04

    $ echo Retrieve and display the results for April 2nd, 2011
    $ playwhe.py --pretty-print --date=2011-04-02
    $ playwhe.py -p -d 2011-04-02

    $ echo Retrieve and display the three most recent results
    $ playwhe.py --pretty-print
    $ playwhe.py -p

You can keep a local copy of previous Play Whe results in an SQLite database.

    $ echo Create and initialize a Play Whe database
    $ playwhe.py --createdb="/home/<username>/playwhe.db"
    $ playwhe.py -c "/home/<username>/playwhe.db"

    $ echo Update the Play Whe database
    $ playwhe.py --updatedb="/home/<username>/playwhe.db"
    $ playwhe.py -u "/home/<username>/playwhe.db"

    $ echo Update the Play Whe database and keep a log
    $ playwhe.py -u "/home/<username>/playwhe.db" 2>> "/home/<username>/playwhe.log"

**Where can I get the latest development version of this project?**

This project is hosted on GitHub at https://github.com/dwayne/playwhe.

    $ git clone git://github.com/dwayne/playwhe.git

**What liscense does this project use?**

This project is in the public domain. Do with it whatever you want.

**Where can I get help?**

    > import playwhe
    > help(playwhe)

    $ playwhe.py --help

You can also get help, report bugs, make suggestions or ask thoughtful
questions by contacting [Dwayne R. Crooks](mailto:me@dwaynecrooks.com).
