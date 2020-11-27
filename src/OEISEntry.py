import urllib.request
import pprint

# Based on the internal format at https://oeis.org/eishelp1.html
letters_to_fields = {   'I' : 'identification',
                        'S' : 'sequence:1',
                        'T' : 'sequence:2',
                        'U' : 'sequence:3',
                        'N' : 'name' ,
                        'D' : 'detail',
                        'H' : 'links',
                        'F' : 'formula',
                        'Y' : 'cross-references',
                        'A' : 'author',
                        'O' : 'offset',
                        'p' : 'code:maple',
                        't' : 'code:mathematica',
                        'o' : 'code:other',
                        'E' : 'extensions',
                        'e' : 'examples',
                        'K' : 'keywords',
                        'C' : 'comments'
                    }

class OEISEntry:
    """An Online Encyclopedia of Integer Sequences Entry"""

    def __init__(self, number):
        self.fields = { }
        self.number = number

        self.retrieve(number)

        #pprint.PrettyPrinter().pprint(self.fields)

    def retrieve(self, number):
        url = ("https://oeis.org/search?fmt=text&q=id:%s" % number)
        response = urllib.request.urlopen(url)
        self.parse(response)

    def parse(self, response):

        for line in response:
            elements = str(line, encoding="utf-8").strip().split(" ", 2)

            if len(elements) < 2:
                continue

            if len(elements[0]) < 2:
                continue

            if elements[0][0] != '%':
                continue

            if elements[0][1] not in letters_to_fields:
                continue

            field_name = letters_to_fields[ elements[0][1] ]

            if field_name == 'identification':
                number = elements[1]
                continue

            if elements[1] != number:
                continue

            if field_name in self.fields:
                self.fields[field_name] += " " + elements[2]
            else:
                self.fields[field_name] = elements[2]

    def tweetify(self):
        CHARACTER_LIMIT = 280

        tweet = self.fields["name"] + " "

        if self.fields["sequence:1"]:
            tweet += self.fields["sequence:1"]

        if self.fields["sequence:2"]:
            tweet += self.fields["sequence:2"]

        if self.fields["sequence:3"]:
            tweet += self.fields["sequence:3"]

        url = (" https://oeis.org/%s" % self.number)

        if (len(tweet) > CHARACTER_LIMIT - len(url)):
            tweet = tweet[0:CHARACTER_LIMIT - len(url) - 3] + "..."

        tweet += url

        return tweet
