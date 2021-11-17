# Project Description

This Project contains a skill for Amazon Alexa, that can be used to query the menu of the university canteen of 
HS Mittweida (Mensa). 

# Capabilities

The skill is capable of answering questions regarding:
- the menu of a specific day within the next 14 days
- the dishes offered in a specific category within the next 14 days

It is currently working for requests in german only, but could easily be extended to support other languages as well.

# Examples

To get the menu (that means all dishes of all categories) of a specific day, say for example:
- Was finde ich Mittwoch in der Mensa?
- Sag mir, was es am Donnerstag gibt.
- Wie sieht das Angebot am Mittwoch aus?
- Freitag essen.
- Montag Gerichte.
- Was gibt es am Dienstag?

To get the dishes offered in a specific category on a specific day, say for example:
- Was gibt es bei Campusteller am Mittwoch?
- Was kann ich am Montag in der Kategorie Pfanne und Grill essen?
- Was gibt es Freitag bei MensaInternational?
- Montag Vegetarisch
- Vegetarisch Montag

# Project Structure

## Sources

- `base_builder.py` is the main entry point for the skill. This is where the request handlers are registered.
- `context.py` contains the `Context` class, which holds the language as well as the representation of the current 
menu for the next 14 days. 
- `custom_handler.py` contains `DayIntentHandler` and `DayAndCategoryIntentHandler`, to which the user requests are delegated 
- `speech_output.py` contains logic to build an answer to the request by concatenating the phrases from `template.py`. 
- `template.py` contains the phrases that are used to build the answers.
- `xml_parser.py` parses the menu, that is retrieved from the API, into a list of `dish` objects.
- `utterances` contains the exported utterances (the phrases used to invoke the handler) as csv. They can be imported
into alexa console to be build the communication model. 


## Utilities

On first setup, create a Python 3.9 virtual environment and install the dependencies from `requirements.txt`.
Also on first setup, execute the `setup_packaging.sh` script to create a directory that contains the sources of 
the dependencies, which the skill needs when deployd on AWS lambda.
AWS lambda expects the skill to be uploaded as a zip archive containing the source files and all dependencies.

Executing `make package` will create a `skill.zip`, that can be deployed on AWS lambda. It will include all current
project files in from the `handler` directory as well as the dependencies from the `dependencies` directory.