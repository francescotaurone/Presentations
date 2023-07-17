## How to build

To build the presentation, first create a virtual environment with 
<code>
python3 -m venv env
</code> 

or, for all the steps, follow [this guide](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/).

Once activated the environment with 
<code>
source env/bin/activate
</code>

install the required packages with
<code>
python3 -m pip install -r requirements.txt
</code>

Then, build the presentation using manim, with the command
<code>
manim -qh main.py FullPresentation
</code>

In order to get a sharable html file, I use the [manim-slides](https://github.com/jeertmans/manim-slides) package, with the command
<code>
manim-slides convert FullPresentation FullPresentation.html
</code>

To see the presentation, open "FullPresentation.html" in a browser. If you want to share it, remember to include the folder with all the assets. Cheers!
