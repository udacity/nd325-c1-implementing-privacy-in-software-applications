### Introduction

So in this demo, I'm going to be giving you the basics of composing regexes. After this, we're
actually going to do an example together, where we use what we learned to find regular expressions
in text.


### Setting the stage

Here we're actually on a website called regex101.com, where we can build and test our regexes. The first thing I'm going to do is:


##### Select Python as your programming language
Select Python as my programming language, because this is the language our exercises and project are in. If you're using a different language for work, what I'm about to show you should still transfer over just fine, except that, that language might have specific instructions for how to handle strings in general, and you might have to adjust for that.

##### Point to regex section
Now, this bar up here is where we can actually specify our test regex...


#### point to test section
... and this is where we can type in some inputs that we can compare it against


### "Fun" example
Let's start with a simpler example. Say we wanted to match the word `fun` with a regex, but we also wanted to account for additional `n`s at the end of the word; for example `funnnn`.
For this, we use the `+` symbol after the `n`. Let's see this **type in `fun+`**.

Now, that `+` is acting on the `n` that's right before it, so we will be matching anything that starts with an `f`, followed by a `u`, and ending with at least one `n`. If I, say, add more `u`'s (**add more `u`'s**'), then it'll no longer match, unless of course I add a `+` after the `u`


### "Fu" example
Now, say we wanted to match  `fu`, `fun`, and longer versions like `funnnn`, then we could use the `*` marker. This start indicates "*zero* or more" of the previous character. So here our regular expression would be `fun*`.


### Parentheses
In both these cases, we can also use parentheses for grouping, and making things more explicit. For example `fu(n+)` and `fu(n*)` would effectively be equivalent if we wanted to match the whole words.


### Limited "fun" example
Now, what if we wanted to match `fun`, `funn` and `funnn`, but nothing longer that? Then we can specify an upper bound like in this regex `fun{1,3}` The `{1,3}` indicates that there can be anywhere from `1` to `3` `n`s at the end here, but nothing more or less.

### Word boundary
Now in this example, you can see that this regex actually matches the beginning of the words that we don't want it to match. To get around this, we use something called a word boundary. Here's how that looks **do word boundary**. All this indicates is that there must be a word break, like a piece of punctuation, or whitespace. **Do `fun` `funn` `funnn` AND `funny`**


### Question mark
The `?` is another useful marker, which indicates "optional", or "one or none". For example, the regex `fun?\b`, with a word boundary t the end of it, would match `fu` and `fun`, but wouldn't match `funn` or anything else for that matter.


### Digit -- CLEAR SCREEN
Now, `\d` matches a single digit. So here `\d{3}` would match any 3 consecutive digits

*Put `482`, `283`, `23948028390480`, AND `asd`*

### Word boundaries on either end
Now, we could of course put word boundaries on either end, so that we can get this to match exactly 3 digits, and nothing more.


### Non-digit
`\D` matches a single non-digit. So for example, `\D{3}` would match any 3 consecutive non-digits.

### OR -- CLEAR SCREEN
*Put `fun`, `fan` and `fin`*
The `|` mean OR. So **put regex as `f(u|a)n`** would match `fun` and `fan`. You can string them together **put regex as `f(u|a|i)n`**, and it'll match `fin` as well.

### Space -- CLEAR SCREEN
*Put `   ` and `asd`*
Similarly, `\s` indicates whitespace (space or a tab), while `\S` matches anything that's *not* a whitespace.

### Dot
`.` matches any character (not just dots), and this includes spaces.
*Put `hi my name is bob and I'm 32 years old.` <--- with period at the end*

### Escaping
 To match *only* a dot, you can escape the dot like so `\.`. You can also escape other special characters, like `\(`, which will only match parenthesis, or `\+`, which will only match a `+`.

### Not
The `[^]` marker is a negative. This is best explained with an example - say we have the regex `f[^aoi]n`. This will match `fun`, `f-n`, `f3n`, `fbn`, `f.n`. But it will *not* match `fan`, `fin` or `fon`, but will match any other single character between `f` and `n` (like `fun`, `f3n` or `f-n`).


### Lookaheads and lookbehinds
Finally, we have look-aheads and look-behinds, which are more advanced features of a regexes, but are quite useful.

Suppose we wanted to match the string `123`, but didn't want to match something like `0123`. However, say we're ok with `car123`; we want to match the `123` there.

**Put `123`, `car123` and `0123`, and the regex `123`**

Now, to do this, we have to look _behind_ the `123` to see what came before. So in this case we want to make sure that whatever came before was _not_ a digit. So we're going use something called a negative lookbehind. Here's how that looks.

**Put `(?<!\d))` into regex**

What this basically says is, that, along as the character immediately before is _not_ a digit, we want to match.

##### Why not negate?

You might ask, why don't we just do `[^\d]123` as our regex? Well you can see this actually matches more than just the `123`; it matches the character before as well, so if we were doing a find and replace for `123`, it would replace extra stuff. This is why we need lookaheads and lookbehinds; they help narrow down the match, but are not included in the match.

##### Positive Lookahead

Now, we could've also done this with a positive lookahead. So if we go back to what we had before, we are insisting that there is no digit before `123`. What if we wanted to the opposite -- look behind for the digit instead? We want to Here's how that'd look **put `(?<=\d)123`**.

##### Lookbehinds -- CLEAR SCREEN

**Put `123` regex, `123`, `123thing`, `123124123123`**

The same deal works in the other direction. We have positive lookaheads **put (?=\d) on the regex**, which would mean that there must be a digit after the `123`, and negative lookaheads **change to (?!\d)**, which would mean that there must _not_ be a digit after the `123`.

### Quick Reference
You can actually find all these characters and more here in the quick reference tab **point there, search for "look"**. You can click on these and tell you an explanation of that it is.
