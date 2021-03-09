# AUML

AUML is a simple regex-like syntax for turning a few sentences into 100s or 1000s of Amazon Alexa skill utterances via a Python parser. It also allows you to keep, store and maintain all your intents and utterances outside of the Alexa GUI. Finally, it allows you to work around the fact that an utterance can accept only a single slot.

## Installation

1. Clone/download the repo.
2. Make sure you have pyperclip, `pip install pyperclip`
3. Copy data.py.example to a new file called data.py: `cp data.py.example data.py`
4. Make sure that parse.py is executable: `chmod u+x parse.py`
5. Adjust the `intents` and (if needed) `variables` dictionaries within data.py to suit your skill.
6. Run the parsing script to generate utterances: `./parse.py`
7. If you'd like the output to be quoted or appended with commas, use `-q` and/or `-c` options respectively.
8. (If you're on OSX, the all the utterances will be automatically inserted into your clipboard.)
9. Insert utterances into your skill (via Developer Console bulk edit tool, ASK-SDK, etc.)

## Usage

Each intent element can be a string or a list of strings, representing a single intent. Each string represents a base utterance that then can be parsed into multiple utterances.

Each element can be a string or a list of strings, representing a single intent. Each string represents a base utterance that can be parsed into multiple utterances.

The syntax (AUML) can include the following:

* simple, literal words
* optional words, followed by a ?
* a list of OR'ed words, offset by () and separated by a |
* Alexa literal slots, offset of course by {}
* variables, begins with $ (see below)

For example, a ‘stream’ intent, which allows a listener to access an FM livestream, could look like this within data.py:

```
intents = {
	'stream': [
		"{stream}"
		"listen live?",
		"$play the? {stream}"
	]
}
```

In that last string, `$play` maps to a variable, like

```
variables = {
	'play': "(play|play me|I want to listen to)"
}
```

which means that string

`$play the? {stream}`

will first become

`(play|play me|I want to listen to) the? {stream}`

This, in turn, will yield the following utterances when parsed.

```
play {stream}
play me {stream}
I want to listen to {stream}
play the {stream}
play me the {stream}
I want to listen to the {stream}
```

Variables, in other words, are a way to reuse phrases across multiple intents and base utterances. It also allows one to sidestep the Alexa rule of only one slot per utterance.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
MIT
