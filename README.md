# SIS parser

Parse `.html` files from site sis.eti.pg.edu.pl into a
compatible format for your class schedule app.

Apps supported right now:

- Nice plan (iOS)

## Usage

Clone the repository:

```cmd
git clone https://github.com/olaaaf/sis-parser.git
```

Download the `.html` site file (single HTML file) into the project directory.
Name it `sis.html`

```cmd
cd sis-parser
pip install -r requirements.txt
python3 parse.py
```

Move the desired ouput file to your phone.
