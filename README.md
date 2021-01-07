# malshared
hacky way to compare lists of >2 people at a time that i made in a day

# usage
enter myanimelist client id and client secret in config.py.

if udk what that is, the api page is [here](https://myanimelist.net/apiconfig).

if you don't have a token, delete the token line from config.py and run main.py, there is a helper to retrieve the bearer token easily. alternatively, you could just read the code, but retrieving the bearer code is just a little annoying,

after you're sure your credentials are set up right, populate the list on line 136 with users you want to compare. also, you should change limit on line 134 to 1000, i don't know of any rate limiting from their services as of yet cus smaller datasets were easier to manage when debugging.

# to-do (not really in any order)
- rewrite in javascript to make userscript/extension
- add more metrics (community score, avg deviation, avg deviation from community score)
- filter helper function
  - filter items based on instances in list (ex: remove rows with <3 ratings) (quick hack: for filtering animes with no ratings, remove all rows with no avg score before formatting)
  - filter based on genre(s)
- sort helper function based on any category (currently being sorted alphabetically in order of list1, ilst2-list1, list3-list2-list1... if you add a bunch of people with decently sized lists, you'll notice it)
  - title (alphabetically)
  - users (by rating)
  - metrics (numerically)
- dynamic table columns
- organize code
- make some tests (this is bound to break at some point, ive ran current commit like 2 times on the same data...)

# notes
- first time really seeing a need for classes when using python, didnt really care to follow class styling guides, might fix later
- considering between passing variables to each gen function or just having them pull straight from within the class. (latter is cleaner but former is more functional)
- considering auto-gen of lists and table (is that what i want? ... probably)
- filter helper function IS there (kinda), but it doesnt even work
